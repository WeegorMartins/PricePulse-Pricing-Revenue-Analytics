import duckdb
from config.settings import DB_PATH

con = duckdb.connect(str(DB_PATH))


def scalar(query):
    return con.execute(query).fetchone()[0]


def test_products():
    assert scalar("SELECT COUNT(*) FROM dim_product") == 3049


def test_stores():
    assert scalar("SELECT COUNT(*) FROM dim_store") == 10


def test_daily_sales_count():
    assert scalar("SELECT COUNT(*) FROM fact_sales") == 59181090


def test_no_negative_units():
    assert scalar("SELECT COUNT(*) FROM fact_sales WHERE units < 0") == 0


def test_no_nonpositive_prices():
    assert scalar("SELECT COUNT(*) FROM fact_prices WHERE sell_price <= 0") == 0


def test_price_key_unique():
    duplicates = scalar("""
        SELECT COUNT(*)
        FROM (
            SELECT item_id, store_id, wm_yr_wk, COUNT(*) AS n
            FROM fact_prices
            GROUP BY 1,2,3
            HAVING COUNT(*) > 1
        )
    """)
    assert duplicates == 0
