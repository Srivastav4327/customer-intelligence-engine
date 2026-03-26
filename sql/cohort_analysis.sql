-- Cohort Analysis

WITH first_purchase AS (
    SELECT customer_id,
           DATE_TRUNC('month', MIN(invoicedate)) AS cohort_month
    FROM transactions
    GROUP BY customer_id
),
activity AS (
    SELECT t.customer_id,
           DATE_TRUNC('month', t.invoicedate) AS activity_month,
           f.cohort_month
    FROM transactions t
    JOIN first_purchase f
    ON t.customer_id = f.customer_id
),
cohort_data AS (
    SELECT cohort_month,
           activity_month,
           COUNT(DISTINCT customer_id) AS users
    FROM activity
    GROUP BY cohort_month, activity_month
)
SELECT * FROM cohort_data
ORDER BY cohort_month, activity_month;
