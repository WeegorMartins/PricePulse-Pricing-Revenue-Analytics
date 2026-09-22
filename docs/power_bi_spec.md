# Power BI Specification

## Page 1 — Executive Overview

Question:
Where are the largest pricing opportunities and risks?

KPIs:
- Revenue
- Units
- ASP
- Price Index
- Eligible SKUs
- Estimated Incremental Revenue
- Estimated Incremental Margin (Simulated Cost)

Charts:
- Revenue trend
- Revenue by category
- Elasticity vs revenue bubble chart
- Recommendation distribution

## Page 2 — Price Architecture

Question:
How is price structured across categories, products and stores?

Charts:
- Price index by store
- Price distribution
- Price ladder
- Price change frequency
- Price change magnitude
- Store × category price-index heatmap

## Page 3 — Elasticity

Question:
Where do we have evidence that demand responds to price?

Charts:
- Elasticity vs historical revenue
- Confidence interval visual
- Model comparison
- Price and units history
- Evidence table

## Page 4 — Revenue Drivers / PVM

Question:
What drove the change in revenue?

Charts:
- Waterfall: Base Revenue → Price → Volume → Mix → Assortment → Comparison Revenue
- Top positive price effects
- Top negative volume effects

## Page 5 — Scenario Simulator

Question:
What is the estimated outcome of alternative prices?

Inputs:
- SKU
- Store / region
- Price change

Outputs:
- Current price
- Proposed price
- Expected volume
- Expected revenue
- Expected margin using simulated cost
- Lower / expected / upper estimates
- Extrapolation warning

## Page 6 — Recommendation Center

Question:
Which pricing hypotheses should be evaluated first?

Columns:
- SKU
- Elasticity
- Evidence
- Candidate action
- Delta price
- Incremental revenue
- Incremental margin
- Risk
- Historical support
