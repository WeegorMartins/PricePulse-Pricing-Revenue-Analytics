import pandas as pd

from config.settings import PROCESSED_DIR
from src.recommendations import choose_recommendation

scenarios = pd.read_parquet(PROCESSED_DIR / "scenario_grid.parquet")

rows = []
for (item_id, evidence), g in scenarios.groupby(["item_id", "evidence_class"]):
    rec = choose_recommendation(g, evidence)
    rec["item_id"] = item_id
    rec["evidence_class"] = evidence
    rows.append(rec)

out = pd.DataFrame(rows)
out.to_parquet(PROCESSED_DIR / "recommendations.parquet", index=False)
print(out["action"].value_counts(dropna=False))
