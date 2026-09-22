import numpy as np
import pandas as pd


def scenario_grid(
    current_price,
    baseline_volume,
    elasticity,
    elasticity_low,
    elasticity_high,
    historical_p10,
    historical_p90,
    cost_ratio=0.70,
    min_change=-0.10,
    max_change=0.10,
    step=0.01,
):
    changes = np.arange(min_change, max_change + step / 2, step)
    rows = []

    simulated_unit_cost = current_price * cost_ratio
    current_revenue = current_price * baseline_volume
    current_margin = (current_price - simulated_unit_cost) * baseline_volume

    for change in changes:
        proposed_price = current_price * (1 + change)
        price_ratio = proposed_price / current_price

        expected_volume = baseline_volume * price_ratio ** elasticity
        volume_a = baseline_volume * price_ratio ** elasticity_low
        volume_b = baseline_volume * price_ratio ** elasticity_high
        expected_volume_low = min(volume_a, volume_b)
        expected_volume_high = max(volume_a, volume_b)

        expected_revenue = proposed_price * expected_volume
        revenue_low = proposed_price * expected_volume_low
        revenue_high = proposed_price * expected_volume_high

        expected_margin = (proposed_price - simulated_unit_cost) * expected_volume
        margin_low = (proposed_price - simulated_unit_cost) * expected_volume_low
        margin_high = (proposed_price - simulated_unit_cost) * expected_volume_high

        rows.append({
            "price_change_pct": change,
            "current_price": current_price,
            "proposed_price": proposed_price,
            "baseline_volume": baseline_volume,
            "expected_volume": expected_volume,
            "expected_volume_low": expected_volume_low,
            "expected_volume_high": expected_volume_high,
            "current_revenue": current_revenue,
            "expected_revenue": expected_revenue,
            "revenue_low": min(revenue_low, revenue_high),
            "revenue_high": max(revenue_low, revenue_high),
            "incremental_revenue": expected_revenue - current_revenue,
            "simulated_unit_cost": simulated_unit_cost,
            "current_margin_sim": current_margin,
            "expected_margin_sim": expected_margin,
            "margin_low_sim": min(margin_low, margin_high),
            "margin_high_sim": max(margin_low, margin_high),
            "incremental_margin_sim": expected_margin - current_margin,
            "extrapolation_risk": not (historical_p10 <= proposed_price <= historical_p90),
        })

    return pd.DataFrame(rows)
