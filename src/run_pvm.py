import duckdb
import pandas as pd

from config.settings import DB_PATH, PROCESSED_DIR
from src.pvm import compute_pvm

con = duckdb.connect(str(DB_PATH))

df = con.sql("""
SELECT
    item_id,
    store_id,
    week_start,
    units,
    sell_price,
    revenue
FROM mart_pricing_weekly_enriched
WHERE sell_price IS NOT NULL
""").df()

df["week_start"] = pd.to_datetime(df["week_start"])

max_date = df["week_start"].max()
comp_end = max_date
comp_start = comp_end - pd.Timedelta(weeks=12)
base_end = comp_start - pd.Timedelta(weeks=1)
base_start = base_end - pd.Timedelta(weeks=12)

result = compute_pvm(df, base_start, base_end, comp_start, comp_end)

if abs(result["reconciliation_error"]) > 0.01:
    raise AssertionError(f"PVM does not reconcile: {result['reconciliation_error']}")

pd.DataFrame([result]).to_parquet(
    PROCESSED_DIR / "pvm_summary.parquet",
    index=False
)

print(pd.DataFrame([result]))
con.close()
