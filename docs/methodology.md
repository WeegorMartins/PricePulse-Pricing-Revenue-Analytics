# Methodology

## 1. Data Grain

Daily fact:
`SKU × Store × Day`

Price fact:
`SKU × Store × Week`

Elasticity analytical grain:
primarily `SKU × Store × Week`, estimated by SKU using store/time variation.

## 2. Eligibility

An item must have enough time history and price variation before modeling.

Default operational thresholds:

- at least 52 calendar weeks
- at least 4 distinct observed prices
- price CV >= 1%
- price change in at least 3 stores

These are guardrails, not universal econometric laws.

## 3. Models

### Baseline controlled log-log

`log(Q) ~ log(P) + store FE + seasonality + trend + events + SNAP`

### Two-way fixed effects

`log(Q_st) = beta log(P_st) + store FE + week FE + e_st`

### PPML sensitivity model

Used because zeros make log-demand models selective.

## 4. Evidence

Magnitude and evidence are separate dimensions.

A highly elastic coefficient with a wide confidence interval is not a strong result.

## 5. PVM

Matched-assortment exact decomposition:

`Revenue Change = Price + Volume + Mix + Assortment`

The implementation must reconcile numerically.

## 6. Scenario Engine

Uses constant elasticity locally:

`Q1 = Q0 * (P1 / P0)^elasticity`

Scenario grid defaults to -10% to +10%, but candidate actions must remain inside historical support unless explicitly flagged.

## 7. Recommendations

Recommendations are hypotheses, not automated decisions.

Possible actions:

- TEST PRICE INCREASE
- TEST PRICE REDUCTION
- MAINTAIN
- INVESTIGATE
- INSUFFICIENT EVIDENCE
