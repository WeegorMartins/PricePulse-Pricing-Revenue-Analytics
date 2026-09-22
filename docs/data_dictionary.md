# Data Dictionary

| Field | Type | Source | Evidence label | Definition |
|---|---|---|---|---|
| item_id | string | M5 | Observed | Product identifier |
| department_id | string | M5 | Observed | Department |
| category_id | string | M5 | Observed | Category |
| store_id | string | M5 | Observed | Store |
| state_id | string | M5 | Observed | State |
| date | date | M5 | Observed | Calendar date |
| wm_yr_wk | int | M5 | Observed | M5 retail week |
| units | int | M5 | Observed | Units sold |
| sell_price | numeric | M5 | Observed | Weekly selling price |
| revenue | numeric | Derived | Calculated | units × sell_price |
| price_change_pct | numeric | Derived | Calculated | Weekly price change |
| price_index | numeric | Derived | Calculated | Store-item price / same item-week median × 100 |
| elasticity_final | numeric | Model | Estimated | Selected price elasticity estimate |
| expected_volume | numeric | Model | Estimated | Scenario volume under constant elasticity |
| simulated_unit_cost | numeric | Assumption | Simulated | Analytical cost assumption |
| expected_margin_sim | numeric | Derived/model | Simulated + Estimated | Margin using simulated cost and estimated demand |
| action | string | Rule engine | Hypothesis | Candidate action for testing |
