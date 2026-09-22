from pathlib import Path
import shutil
import duckdb

from config.settings import RAW_DIR, INTERIM_DIR, PROCESSED_DIR, DB_PATH

INTERIM_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

required = [
    RAW_DIR / "calendar.csv",
    RAW_DIR / "sell_prices.csv",
    RAW_DIR / "sales_train_evaluation.csv",
]

missing = [str(p) for p in required if not p.exists()]
if missing:
    raise FileNotFoundError(
        "Missing M5 raw files:\n- " + "\n- ".join(missing)
    )

fact_sales_path = INTERIM_DIR / "fact_sales"
if fact_sales_path.exists():
    shutil.rmtree(fact_sales_path)

con = duckdb.connect(str(DB_PATH))
con.execute("PRAGMA threads=8;")

calendar_file = (RAW_DIR / "calendar.csv").as_posix()
prices_file = (RAW_DIR / "sell_prices.csv").as_posix()
sales_file = (RAW_DIR / "sales_train_evaluation.csv").as_posix()

print("1/7 Loading calendar...")
con.execute(f"""
CREATE OR REPLACE TABLE raw_calendar AS
SELECT
    d,
    CAST(date AS DATE) AS date,
    CAST(wm_yr_wk AS INTEGER) AS wm_yr_wk,
    weekday,
    wday,
    month,
    year,
    event_name_1,
    event_type_1,
    event_name_2,
    event_type_2,
    snap_CA,
    snap_TX,
    snap_WI
FROM read_csv_auto('{calendar_file}', HEADER = TRUE);
""")

print("2/7 Loading prices...")
con.execute(f"""
CREATE OR REPLACE TABLE fact_prices AS
SELECT
    CAST(store_id AS VARCHAR) AS store_id,
    CAST(item_id AS VARCHAR) AS item_id,
    CAST(wm_yr_wk AS INTEGER) AS wm_yr_wk,
    CAST(sell_price AS DOUBLE) AS sell_price
FROM read_csv_auto('{prices_file}', HEADER = TRUE);
""")

print("3/7 Loading sales wide table...")
con.execute(f"""
CREATE OR REPLACE TABLE raw_sales_wide AS
SELECT *
FROM read_csv_auto('{sales_file}', HEADER = TRUE);
""")

print("4/7 Creating dimensions...")
con.execute("""
CREATE OR REPLACE TABLE dim_product AS
SELECT DISTINCT
    CAST(item_id AS VARCHAR) AS item_id,
    CAST(dept_id AS VARCHAR) AS department_id,
    CAST(cat_id AS VARCHAR) AS category_id
FROM raw_sales_wide;
""")

con.execute("""
CREATE OR REPLACE TABLE dim_store AS
SELECT DISTINCT
    CAST(store_id AS VARCHAR) AS store_id,
    CAST(state_id AS VARCHAR) AS state_id
FROM raw_sales_wide;
""")

con.execute("""
CREATE OR REPLACE TABLE dim_calendar AS
SELECT *
FROM raw_calendar
WHERE CAST(SUBSTRING(d, 3) AS INTEGER) <= 1941;
""")

print("5/7 Unpivoting sales to partitioned Parquet...")
target = fact_sales_path.as_posix()

con.execute(f"""
COPY (
    WITH long_sales AS (
        UNPIVOT raw_sales_wide
        ON COLUMNS(
            * EXCLUDE (
                id,
                item_id,
                dept_id,
                cat_id,
                store_id,
                state_id
            )
        )
        INTO NAME d VALUE units
    )
    SELECT
        CAST(s.item_id AS VARCHAR) AS item_id,
        CAST(s.store_id AS VARCHAR) AS store_id,
        CAST(s.state_id AS VARCHAR) AS state_id,
        c.date,
        c.d,
        c.wm_yr_wk,
        c.year,
        c.month,
        CAST(s.units AS INTEGER) AS units
    FROM long_sales s
    INNER JOIN raw_calendar c ON s.d = c.d
    WHERE CAST(SUBSTRING(s.d, 3) AS INTEGER) <= 1941
)
TO '{target}'
(
    FORMAT PARQUET,
    PARTITION_BY (state_id, year),
    COMPRESSION ZSTD
);
""")

con.execute(f"""
CREATE OR REPLACE VIEW fact_sales AS
SELECT *
FROM read_parquet(
    '{target}/**/*.parquet',
    hive_partitioning = true
);
""")

print("6/7 Creating weekly pricing mart...")
con.execute("""
CREATE OR REPLACE TABLE mart_pricing_weekly AS
WITH weekly_sales AS (
    SELECT
        s.item_id,
        s.store_id,
        s.state_id,
        s.wm_yr_wk,
        MIN(s.date) AS week_start,
        MAX(s.date) AS week_end,
        SUM(s.units) AS units,
        SUM(
            CASE
                WHEN c.event_name_1 IS NOT NULL
                  OR c.event_name_2 IS NOT NULL
                THEN 1 ELSE 0
            END
        ) AS event_days,
        SUM(
            CASE
                WHEN s.state_id = 'CA' THEN c.snap_CA
                WHEN s.state_id = 'TX' THEN c.snap_TX
                WHEN s.state_id = 'WI' THEN c.snap_WI
                ELSE 0
            END
        ) AS snap_days
    FROM fact_sales s
    INNER JOIN raw_calendar c ON s.d = c.d
    GROUP BY 1,2,3,4
),
joined AS (
    SELECT
        ws.*,
        p.sell_price,
        CASE
            WHEN p.sell_price IS NOT NULL
            THEN ws.units * p.sell_price
        END AS revenue
    FROM weekly_sales ws
    LEFT JOIN fact_prices p
      ON ws.item_id = p.item_id
     AND ws.store_id = p.store_id
     AND ws.wm_yr_wk = p.wm_yr_wk
),
price_history AS (
    SELECT
        *,
        LAG(sell_price) OVER (
            PARTITION BY item_id, store_id
            ORDER BY week_start
        ) AS previous_price,
        LAG(week_start) OVER (
            PARTITION BY item_id, store_id
            ORDER BY week_start
        ) AS previous_price_week
    FROM joined
    WHERE sell_price IS NOT NULL
)
SELECT
    *,
    DATE_DIFF('week', previous_price_week, week_start) AS weeks_since_previous_price,
    CASE
        WHEN previous_price IS NOT NULL AND previous_price > 0
        THEN sell_price / previous_price - 1
    END AS price_change_pct,
    CASE
        WHEN previous_price IS NOT NULL AND sell_price != previous_price
        THEN 1 ELSE 0
    END AS price_changed
FROM price_history;
""")

print("7/7 Creating enriched pricing mart...")
con.execute("""
CREATE OR REPLACE TABLE mart_pricing_weekly_enriched AS
WITH benchmark AS (
    SELECT
        item_id,
        wm_yr_wk,
        MEDIAN(sell_price) AS item_week_median_price
    FROM mart_pricing_weekly
    WHERE sell_price IS NOT NULL
    GROUP BY 1,2
)
SELECT
    m.*,
    p.department_id,
    p.category_id,
    b.item_week_median_price,
    100.0 * m.sell_price / NULLIF(b.item_week_median_price, 0) AS price_index
FROM mart_pricing_weekly m
LEFT JOIN dim_product p USING (item_id)
LEFT JOIN benchmark b
  ON m.item_id = b.item_id
 AND m.wm_yr_wk = b.wm_yr_wk;
""")

print("Done.")
con.close()
