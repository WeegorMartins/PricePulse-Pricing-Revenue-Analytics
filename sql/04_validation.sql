-- Reconciliation / sanity checks used before publishing any result.

SELECT
    COUNT(*) AS eligible_items
FROM elasticity_eligibility
WHERE eligibility_status = 'ELIGIBLE';

SELECT
    eligibility_status,
    COUNT(*) AS items,
    SUM(historical_revenue) AS historical_revenue
FROM elasticity_eligibility
GROUP BY 1
ORDER BY historical_revenue DESC;
