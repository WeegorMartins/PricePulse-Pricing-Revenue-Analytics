import duckdb
import numpy as np
import pandas as pd
from tqdm import tqdm

from config.settings import DB_PATH, PROCESSED_DIR
from src.elasticity import (
    baseline_ols,
    two_way_fixed_effects,
    poisson_sensitivity,
    elasticity_class,
    evidence_class,
)

con = duckdb.connect(str(DB_PATH))

eligible = con.sql("""
SELECT item_id
FROM elasticity_eligibility
WHERE eligibility_status = 'ELIGIBLE'
ORDER BY historical_revenue DESC
""").df()

results = []

for item_id in tqdm(eligible["item_id"]):
    df = con.execute("""
        SELECT
            item_id,
            store_id,
            week_start,
            wm_yr_wk,
            units,
            sell_price,
            revenue,
            event_days,
            snap_days
        FROM mart_pricing_weekly_enriched
        WHERE item_id = ?
          AND sell_price > 0
        ORDER BY store_id, week_start
    """, [item_id]).df()

    df["week_start"] = pd.to_datetime(df["week_start"])

    row = {"item_id": item_id}

    for name, func in [
        ("baseline", baseline_ols),
        ("twfe", two_way_fixed_effects),
        ("ppml", poisson_sensitivity),
    ]:
        try:
            out = func(df)
            for k, v in out.items():
                row[f"{name}_{k}"] = v
        except Exception as exc:
            row[f"{name}_error"] = str(exc)

    results.append(row)

res = pd.DataFrame(results)

if "twfe_estimate" in res and "ppml_estimate" in res:
    res["same_sign_twfe_ppml"] = (
        np.sign(res["twfe_estimate"]) == np.sign(res["ppml_estimate"])
    )
    res["model_gap"] = (res["twfe_estimate"] - res["ppml_estimate"]).abs()
else:
    res["same_sign_twfe_ppml"] = False
    res["model_gap"] = np.nan

res["elasticity_final"] = res.get("twfe_estimate")
res["elasticity_class"] = res["elasticity_final"].apply(elasticity_class)
res["evidence_class"] = res.apply(evidence_class, axis=1)

out = PROCESSED_DIR / "elasticity_models.parquet"
res.to_parquet(out, index=False)

print(f"Saved: {out}")
print(res["evidence_class"].value_counts(dropna=False))

con.close()
