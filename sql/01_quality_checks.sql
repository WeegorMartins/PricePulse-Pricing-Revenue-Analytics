SELECT
    COUNT(*) AS observations,
    COUNT(DISTINCT item_id) AS items,
    COUNT(DISTINCT store_id) AS stores,
    COUNT(DISTINCT wm_yr_wk) AS weeks,
    SUM(units) AS total_units,
    SUM(revenue) AS total_revenue
FROM mart_pricing_weekly_enriched;

SELECT
    SUM(CASE WHEN sell_price IS NULL THEN 1 ELSE 0 END) AS missing_price,
    SUM(CASE WHEN units = 0 THEN 1 ELSE 0 END) AS zero_sales,
    SUM(CASE WHEN units > 0 AND sell_price IS NULL THEN 1 ELSE 0 END) AS sales_without_price
FROM mart_pricing_weekly_enriched;

SELECT
    item_id,
    store_id,
    wm_yr_wk,
    COUNT(*) AS n
FROM fact_prices
GROUP BY 1,2,3
HAVING COUNT(*) > 1;
