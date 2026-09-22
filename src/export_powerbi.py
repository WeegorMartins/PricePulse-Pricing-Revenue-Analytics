import duckdb
import pandas as pd

from config.settings import DB_PATH, PROCESSED_DIR, POWERBI_DIR

POWERBI_DIR.mkdir(parents=True, exist_ok=True)
con = duckdb.connect(str(DB_PATH))

exports = {
    "dim_product.parquet": "SELECT * FROM dim_product",
    "dim_store.parquet": "SELECT * FROM dim_store",
    "dim_calendar.parquet": "SELECT * FROM dim_calendar",
    "fact_pricing_weekly.parquet": "SELECT * FROM mart_pricing_weekly_enriched",
    "elasticity_eligibility.parquet": "SELECT * FROM elasticity_eligibility",
}

for filename, query in exports.items():
    df = con.sql(query).df()
    df.to_parquet(POWERBI_DIR / filename, index=False)

for filename in [
    "elasticity_models.parquet",
    "pvm_summary.parquet",
    "scenario_grid.parquet",
    "recommendations.parquet",
]:
    source = PROCESSED_DIR / filename
    if source.exists():
        pd.read_parquet(source).to_parquet(POWERBI_DIR / filename, index=False)

print(f"Power BI layer exported to {POWERBI_DIR}")
con.close()
