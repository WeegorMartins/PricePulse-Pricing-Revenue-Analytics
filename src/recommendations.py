def choose_recommendation(scenarios, evidence_class):
    if evidence_class == "Insufficient":
        return {"action": "INSUFFICIENT EVIDENCE", "risk": "HIGH"}

    valid = scenarios[~scenarios["extrapolation_risk"]].copy()
    if valid.empty:
        return {"action": "INVESTIGATE", "risk": "HIGH"}

    best = valid.loc[valid["expected_margin_sim"].idxmax()]
    change = best["price_change_pct"]

    if abs(change) < 0.01:
        action = "MAINTAIN"
    elif change > 0:
        action = "TEST PRICE INCREASE"
    else:
        action = "TEST PRICE REDUCTION"

    downside_positive = best["margin_low_sim"] > best["current_margin_sim"]

    if evidence_class == "High" and downside_positive:
        risk = "LOWER MODEL RISK"
    elif evidence_class in {"High", "Medium"}:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    result = best.to_dict()
    result.update({"action": action, "risk": risk})
    return result
