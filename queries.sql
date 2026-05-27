-- ================================================================
-- E-Commerce Analytics — SQL Queries
-- Database: ecommerce.db (SQLite)
-- Author: [Your Name]
-- ================================================================

-- ── 1. Revenue & Profit by Category ─────────────────────────────
SELECT
    category,
    COUNT(order_id)                         AS total_orders,
    SUM(quantity)                           AS units_sold,
    ROUND(SUM(revenue), 2)                  AS total_revenue,
    ROUND(SUM(profit), 2)                   AS total_profit,
    ROUND(AVG(profit_margin), 2)            AS avg_margin_pct,
    ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS net_margin_pct
FROM orders
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY total_revenue DESC;

-- ── 2. Monthly Revenue Trend (2023 & 2024) ───────────────────────
SELECT
    year,
    month,
    month_name,
    COUNT(order_id)            AS orders,
    ROUND(SUM(revenue), 2)     AS monthly_revenue,
    ROUND(SUM(profit), 2)      AS monthly_profit
FROM orders
WHERE order_status = 'Delivered'
GROUP BY year, month
ORDER BY year, month;

-- ── 3. Top 10 Products by Revenue ────────────────────────────────
SELECT
    product_name,
    category,
    COUNT(order_id)            AS order_count,
    SUM(quantity)              AS units_sold,
    ROUND(SUM(revenue), 2)     AS total_revenue,
    ROUND(AVG(profit_margin),2) AS avg_margin
FROM orders
WHERE order_status = 'Delivered'
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 10;

-- ── 4. Return Rate by Category ───────────────────────────────────
SELECT
    category,
    COUNT(order_id)                                         AS total_orders,
    SUM(CASE WHEN order_status='Returned' THEN 1 ELSE 0 END) AS returns,
    ROUND(
        SUM(CASE WHEN order_status='Returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 2
    )                                                       AS return_rate_pct
FROM orders
GROUP BY category
ORDER BY return_rate_pct DESC;

-- ── 5. Payment Method Distribution ───────────────────────────────
SELECT
    payment_method,
    COUNT(order_id)            AS total_orders,
    ROUND(SUM(revenue), 2)     AS total_revenue,
    ROUND(AVG(revenue), 2)     AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY payment_method
ORDER BY total_orders DESC;

-- ── 6. Top 10 States by Revenue ──────────────────────────────────
SELECT
    state,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(order_id)             AS orders,
    ROUND(SUM(revenue), 2)      AS revenue,
    ROUND(AVG(revenue), 2)      AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY state
ORDER BY revenue DESC
LIMIT 10;

-- ── 7. High-Value Customer Segments (RFM) ────────────────────────
SELECT
    customer_id,
    recency,
    frequency,
    ROUND(monetary, 2) AS lifetime_value,
    CASE
        WHEN recency <= 30  AND frequency >= 5 AND monetary >= 10000 THEN 'Champion'
        WHEN recency <= 60  AND frequency >= 3 AND monetary >= 5000  THEN 'Loyal'
        WHEN recency <= 90  AND frequency >= 2                        THEN 'Potential Loyalist'
        WHEN recency > 180  AND frequency = 1                         THEN 'At Risk'
        ELSE 'Needs Attention'
    END AS segment
FROM rfm
ORDER BY lifetime_value DESC;

-- ── 8. Day-of-Week Sales Pattern ─────────────────────────────────
SELECT
    day_name,
    COUNT(order_id)        AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY day_name
ORDER BY revenue DESC;

-- ── 9. Delivery Performance ──────────────────────────────────────
SELECT
    CASE
        WHEN delivery_days <= 3 THEN '1-3 days (Fast)'
        WHEN delivery_days <= 6 THEN '4-6 days (Standard)'
        ELSE '7+ days (Slow)'
    END AS delivery_bucket,
    COUNT(order_id)        AS orders,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    ROUND(AVG(profit_margin), 2) AS avg_margin
FROM orders
WHERE order_status = 'Delivered' AND delivery_days IS NOT NULL
GROUP BY delivery_bucket
ORDER BY orders DESC;

-- ── 10. Quarter-over-Quarter Growth ──────────────────────────────
SELECT
    year,
    quarter,
    ROUND(SUM(revenue), 2)                                          AS quarterly_revenue,
    ROUND(
        (SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY year, quarter))
        * 100.0 / LAG(SUM(revenue)) OVER (ORDER BY year, quarter), 2
    )                                                               AS qoq_growth_pct
FROM orders
WHERE order_status = 'Delivered'
GROUP BY year, quarter
ORDER BY year, quarter;
