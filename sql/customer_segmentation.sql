-- Customer Segmentation

SELECT customer_id,
       SUM(totalprice) AS total_spent,
       COUNT(DISTINCT invoice) AS orders,
       CASE
           WHEN SUM(totalprice) > 10000 THEN 'High Value'
           WHEN SUM(totalprice) BETWEEN 5000 AND 10000 THEN 'Medium Value'
           ELSE 'Low Value'
       END AS segment
FROM transactions
GROUP BY customer_id;
