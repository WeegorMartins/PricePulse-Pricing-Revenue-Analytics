import numpy as np
import pandas as pd


def aggregate_period(df):
    result = (
        df.groupby(["item_id", "store_id"], as_index=False)
        .agg(
            units=("units", "sum"),
            revenue=("revenue", "sum"),
            avg_list_price=("sell_price", "mean"),
        )
    )
    result["price"] = np.where(
        result["units"] > 0,
        result["revenue"] / result["units"],
        result["avg_list_price"],
    )
    return result


def compute_pvm(df, base_start, base_end, comp_start, comp_end):
    data = df.copy()
    data["week_start"] = pd.to_datetime(data["week_start"])

    base = aggregate_period(data[data["week_start"].between(base_start, base_end)])
    comp = aggregate_period(data[data["week_start"].between(comp_start, comp_end)])

    base = base.rename(columns={"units": "q0", "revenue": "r0", "price": "p0"})
    comp = comp.rename(columns={"units": "q1", "revenue": "r1", "price": "p1"})

    merged = base.merge(comp, on=["item_id", "store_id"], how="outer", indicator=True)

    total_r0 = merged["r0"].fillna(0).sum()
    total_r1 = merged["r1"].fillna(0).sum()
    total_delta = total_r1 - total_r0

    matched = merged[merged["_merge"] == "both"].copy()
    Q0 = matched["q0"].sum()
    Q1 = matched["q1"].sum()

    matched["s0"] = matched["q0"] / Q0 if Q0 else 0
    matched["s1"] = matched["q1"] / Q1 if Q1 else 0

    base_avg_price = (matched["s0"] * matched["p0"]).sum()
    volume_effect = (Q1 - Q0) * base_avg_price
    mix_effect = Q1 * (((matched["s1"] - matched["s0"]) * matched["p0"]).sum())
    price_effect = Q1 * ((matched["s1"] * (matched["p1"] - matched["p0"])).sum())

    matched_delta = matched["r1"].sum() - matched["r0"].sum()
    assortment_effect = total_delta - matched_delta

    reconciliation = price_effect + volume_effect + mix_effect + assortment_effect

    return {
        "base_revenue": total_r0,
        "comparison_revenue": total_r1,
        "revenue_change": total_delta,
        "price_effect": price_effect,
        "volume_effect": volume_effect,
        "mix_effect": mix_effect,
        "assortment_effect": assortment_effect,
        "reconciliation": reconciliation,
        "reconciliation_error": total_delta - reconciliation,
    }
