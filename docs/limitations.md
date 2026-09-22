# Limitations & Guardrails

1. Historical elasticity does not automatically identify causal price effects.
2. Price may be endogenous to expected demand.
3. SKU-level promotion is not fully observed in M5.
4. Stockouts are not directly observed.
5. Price is weekly while unit sales are daily.
6. Intermittent demand can make log-demand specifications selective.
7. Low price variation weakens identification.
8. Simulated cost is not an observed M5 variable.
9. Competitor price is deliberately not simulated because it would add false precision.
10. M5 is historical and should not be interpreted as a direct representation of 2026 consumers.
11. Scenario simulation assumes approximately constant local elasticity.
12. Extrapolation outside the historical support is flagged and should not be recommended automatically.
13. Confidence intervals represent model uncertainty, not all business risk.
14. Recommended actions should be validated through controlled experimentation whenever feasible.
15. Cross-product substitution/cannibalization is not fully modeled in the MVP.
16. Price availability may itself reflect product assortment/launch timing.
