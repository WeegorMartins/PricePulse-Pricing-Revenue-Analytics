import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS


def elasticity_class(beta):
    if pd.isna(beta):
        return "Unknown"
    if beta < -2:
        return "Highly elastic"
    if beta < -1:
        return "Elastic"
    if beta < 0:
        return "Inelastic"
    return "Unexpected / investigate"


def baseline_ols(df):
    data = df[(df["units"] > 0) & (df["sell_price"] > 0)].copy()
    data["log_units"] = np.log(data["units"])
    data["log_price"] = np.log(data["sell_price"])
    data["trend"] = (data["week_start"] - data["week_start"].min()).dt.days / 7
    data["month"] = data["week_start"].dt.month

    result = smf.ols(
        "log_units ~ log_price + C(store_id) + C(month) + trend + snap_days + event_days",
        data=data,
    ).fit(cov_type="HC3")

    ci = result.conf_int().loc["log_price"]
    return {
        "estimate": float(result.params["log_price"]),
        "std_error": float(result.bse["log_price"]),
        "p_value": float(result.pvalues["log_price"]),
        "ci_low": float(ci.iloc[0]),
        "ci_high": float(ci.iloc[1]),
        "n_obs": int(result.nobs),
        "r2": float(result.rsquared),
    }


def two_way_fixed_effects(df):
    data = df[(df["units"] > 0) & (df["sell_price"] > 0)].copy()
    data["log_units"] = np.log(data["units"])
    data["log_price"] = np.log(data["sell_price"])
    data = data.set_index(["store_id", "week_start"]).sort_index()

    model = PanelOLS.from_formula(
        "log_units ~ 1 + log_price + snap_days + EntityEffects + TimeEffects",
        data=data,
        drop_absorbed=True,
    )
    result = model.fit(cov_type="kernel", kernel="bartlett", bandwidth=4)
    ci = result.conf_int().loc["log_price"]

    return {
        "estimate": float(result.params["log_price"]),
        "std_error": float(result.std_errors["log_price"]),
        "p_value": float(result.pvalues["log_price"]),
        "ci_low": float(ci.iloc[0]),
        "ci_high": float(ci.iloc[1]),
        "n_obs": int(result.nobs),
        "r2_within": float(result.rsquared_within),
    }


def poisson_sensitivity(df):
    data = df[df["sell_price"] > 0].copy()
    data["log_price"] = np.log(data["sell_price"])
    data["trend"] = (data["week_start"] - data["week_start"].min()).dt.days / 7
    data["month"] = data["week_start"].dt.month

    result = smf.glm(
        "units ~ log_price + C(store_id) + C(month) + trend + snap_days + event_days",
        data=data,
        family=sm.families.Poisson(),
    ).fit(cov_type="HC0", maxiter=200)

    ci = result.conf_int().loc["log_price"]
    return {
        "estimate": float(result.params["log_price"]),
        "std_error": float(result.bse["log_price"]),
        "p_value": float(result.pvalues["log_price"]),
        "ci_low": float(ci.iloc[0]),
        "ci_high": float(ci.iloc[1]),
        "n_obs": int(result.nobs),
    }


def evidence_class(row):
    # Conservative rule set. Tune only after sensitivity analysis.
    if pd.isna(row.get("twfe_estimate")):
        return "Insufficient"

    if row.get("twfe_ci_high", 1) >= 0:
        return "Insufficient"

    if row.get("same_sign_twfe_ppml") is False:
        return "Insufficient"

    gap = row.get("model_gap", np.inf)
    if gap <= 0.35 and row.get("twfe_p_value", 1) < 0.05:
        return "High"

    if gap <= 0.75 and row.get("twfe_p_value", 1) < 0.10:
        return "Medium"

    return "Insufficient"
