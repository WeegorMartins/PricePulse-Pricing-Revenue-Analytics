# Suggested DAX Measures

```DAX
Revenue =
SUM ( fact_pricing_weekly[revenue] )
```

```DAX
Units =
SUM ( fact_pricing_weekly[units] )
```

```DAX
ASP =
DIVIDE ( [Revenue], [Units] )
```

```DAX
Price Index =
DIVIDE (
    SUMX (
        fact_pricing_weekly,
        fact_pricing_weekly[price_index] * fact_pricing_weekly[units]
    ),
    [Units]
)
```

```DAX
Median Eligible Elasticity =
MEDIANX (
    FILTER (
        elasticity_models,
        elasticity_models[evidence_class] <> "Insufficient"
    ),
    elasticity_models[elasticity_final]
)
```

```DAX
Estimated Incremental Revenue =
SUM ( recommendations[incremental_revenue] )
```

```DAX
Estimated Incremental Margin Simulated =
SUM ( recommendations[incremental_margin_sim] )
```
