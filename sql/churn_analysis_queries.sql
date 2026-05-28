-- Churn distribution
SELECT churn, COUNT(*) AS customers
FROM customer_churn
GROUP BY churn;

-- Churn rate by contract type
SELECT
    contract,
    COUNT(*) AS customers,
    AVG(CASE WHEN churn = 1 THEN 1.0 ELSE 0.0 END) AS churn_rate
FROM customer_churn
GROUP BY contract
ORDER BY churn_rate DESC;

-- Revenue at risk from high-risk customers
SELECT
    SUM(monthly_charges) AS monthly_revenue_at_risk,
    SUM(monthly_charges) * 12 AS annual_revenue_at_risk
FROM customer_churn_predictions
WHERE churn_probability >= 0.70;

