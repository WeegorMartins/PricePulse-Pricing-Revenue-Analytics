import duckdb
import pandas as pd

from config.settings import (
    DB_PATH,
    PROCESSED_DIR,
    BASELINE_WEEKS,
    SIMULATED_COST_RATIO,
    PRICE_CHANGE_MIN,
    PRICE_CHANGE_MAX,
    PRICE_CHANGE_STEP,
)
from src.scenarios import scenario_grid

con = duckdb.connect(str(DB_PATH))

elasticity = pd.read_parquet(PROCESSED_DIR / "elasticity_models.parquet")
elasticity = elasticity[elasticity["evidence_class"].isin(["High", "Medium"])].copy()

rows = []

for _, erow in elasticity.iterrows():
    item_id = erow["item_id"]

    df = con.execute("""
        SELECT
            item_id,
            store_id,
            week_start,
            units,
            sell_price,
            revenue
        FROM mart_pricing_weekly_enriched
        WHERE item_id = ?
          AND sell_price > 0
        ORDER BY week_start
    """, [item_id]).df()

    if df.empty:
        continue

    df["week_start"] = pd.to_datetime(df["week_start"])

    current_price = float(df.sort_values("week_start").iloc[-1]["sell_price"])
    max_week = df["week_start"].max()
    cutoff = max_week - pd.Timedelta(weeks=BASELINE_WEEKS - 1)
    baseline_volume = float(df[df["week_start"] >= cutoff]["units"].mean())

    hist_p10 = float(df["sell_price"].quantile(0.10))
    hist_p90 = float(df["sell_price"].quantile(0.90))

    grid = scenario_grid(
        current_price=current_price,
        baseline_volume=baseline_volume,
        elasticity=float(erow["elasticity_final"]),
        elasticity_low=float(erow["twfe_ci_low"]),
        elasticity_high=float(erow["twfe_ci_high"]),
        historical_p10=hist_p10,
        historical_p90=hist_p90,
        cost_ratio=SIMULATED_COST_RATIO,
        min_change=PRICE_CHANGE_MIN,
        max_change=PRICE_CHANGE_MAX,
        step=PRICE_CHANGE_STEP,
    )
    grid.insert(0, "item_id", item_id)
    grid["evidence_class"] = erow["evidence_class"]
    rows.append(grid)

out = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
out.to_parquet(PROCESSED_DIR / "scenario_grid.parquet", index=False)
print(f"Saved {len(out):,} scenario rows.")

con.close()
