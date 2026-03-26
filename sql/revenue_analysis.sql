-- Monthly Revenue Trend

SELECT DATE_TRUNC('month', invoicedate) AS month,
       SUM(totalprice) AS revenue
FROM transactions
GROUP BY month
ORDER BY month;
