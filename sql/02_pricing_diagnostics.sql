CREATE OR REPLACE TABLE pricing_diagnostics AS
WITH base AS (
    SELECT
        item_id,
        store_id,
        state_id,
        COUNT(*) AS n_weeks,
        COUNT(DISTINCT sell_price) AS n_price_points,
        AVG(sell_price) AS mean_price,
        STDDEV_SAMP(sell_price) AS sd_price,
        STDDEV_SAMP(sell_price) / NULLIF(AVG(sell_price), 0) AS price_cv,
        SUM(CASE WHEN price_changed = 1 THEN 1 ELSE 0 END) AS n_price_changes,
        SUM(units) AS units,
        SUM(revenue) AS revenue
    FROM mart_pricing_weekly_enriched
    WHERE sell_price > 0
    GROUP BY 1,2,3
)
SELECT *
FROM base;
