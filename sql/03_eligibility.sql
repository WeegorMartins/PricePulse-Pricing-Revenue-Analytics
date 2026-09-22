CREATE OR REPLACE TABLE elasticity_eligibility AS

WITH base AS (
    SELECT
        item_id,
        COUNT(*) AS n_observations,
        COUNT(DISTINCT wm_yr_wk) AS n_calendar_weeks,
        COUNT(DISTINCT store_id) AS n_stores,
        COUNT(DISTINCT sell_price) AS n_price_points,
        STDDEV_SAMP(sell_price) / NULLIF(AVG(sell_price), 0) AS price_cv,
        AVG(CASE WHEN units = 0 THEN 1.0 ELSE 0.0 END) AS zero_share,
        SUM(revenue) AS historical_revenue
    FROM mart_pricing_weekly_enriched
    WHERE sell_price > 0
    GROUP BY item_id
),

store_variation AS (
    SELECT
        item_id,
        SUM(CASE WHEN distinct_prices > 1 THEN 1 ELSE 0 END) AS stores_with_price_change
    FROM (
        SELECT
            item_id,
            store_id,
            COUNT(DISTINCT sell_price) AS distinct_prices
        FROM mart_pricing_weekly_enriched
        WHERE sell_price > 0
        GROUP BY 1,2
    )
    GROUP BY item_id
)

SELECT
    b.*,
    s.stores_with_price_change,
    CASE
        WHEN n_calendar_weeks < 52 THEN 'INSUFFICIENT_HISTORY'
        WHEN n_price_points < 4 THEN 'LOW_PRICE_VARIATION'
        WHEN price_cv < 0.01 THEN 'LOW_PRICE_VARIATION'
        WHEN stores_with_price_change < 3 THEN 'LOW_WITHIN_STORE_VARIATION'
        ELSE 'ELIGIBLE'
    END AS eligibility_status
FROM base b
LEFT JOIN store_variation s USING (item_id);
