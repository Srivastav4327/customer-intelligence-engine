-- Retention Analysis

WITH cohort_size AS (
    SELECT cohort_month,
           COUNT(DISTINCT customer_id) AS total_users
    FROM (
        SELECT customer_id,
               DATE_TRUNC('month', MIN(invoicedate)) AS cohort_month
        FROM transactions
        GROUP BY customer_id
    ) t
    GROUP BY cohort_month
),
retention AS (
    SELECT f.cohort_month,
           DATE_TRUNC('month', t.invoicedate) AS activity_month,
           COUNT(DISTINCT t.customer_id) AS retained_users
    FROM transactions t
    JOIN (
        SELECT customer_id,
               DATE_TRUNC('month', MIN(invoicedate)) AS cohort_month
        FROM transactions
        GROUP BY customer_id
    ) f
    ON t.customer_id = f.customer_id
    GROUP BY f.cohort_month, activity_month
)
SELECT r.cohort_month,
       r.activity_month,
       r.retained_users,
       c.total_users,
       ROUND(r.retained_users * 100.0 / c.total_users, 2) AS retention_rate
FROM retention r
JOIN cohort_size c
ON r.cohort_month = c.cohort_month
ORDER BY r.cohort_month, r.activity_month;
