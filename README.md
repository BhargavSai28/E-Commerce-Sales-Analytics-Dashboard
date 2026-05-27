# 🛒 E-Commerce Sales Analytics Dashboard

> End-to-end data analytics project: Python · SQL · Power BI / Tableau

---

## 📌 Project Overview

This project performs a full analytics cycle on a simulated Indian e-commerce dataset (12,000 orders across 2023–2024). It covers data generation, cleaning, SQL analysis, exploratory data analysis (EDA), and a business dashboard — designed as a portfolio project for data analyst roles.

**Business Questions Answered:**
- Which product categories drive the most revenue and profit?
- How do sales trend seasonally, and when are peak periods?
- Which customer segments are most valuable (RFM analysis)?
- What is the return rate across categories, and what does it cost the business?
- Which states and cities generate the highest order values?

---

## 📂 Project Structure

```
ecommerce-analytics/
│
├── data/
│   ├── generate_data.py       # Synthetic dataset generator
│   ├── clean_data.py          # Cleaning, feature engineering, SQLite load
│   ├── raw_orders.csv         # Raw generated dataset (12,000 rows)
│   └── cleaned_orders.csv     # Cleaned dataset ready for analysis
│
├── notebooks/
│   └── eda_analysis.py        # Full EDA — 10 charts saved to /images
│
├── sql/
│   └── queries.sql            # 10 analytical SQL queries
│
├── dashboard/
│   └── DASHBOARD_GUIDE.md     # Power BI / Tableau setup instructions
│
├── images/                    # All exported chart PNGs
│
├── requirements.txt
└── README.md
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Data generation, cleaning, EDA |
| pandas | Data manipulation |
| matplotlib / seaborn | Visualisation |
| SQLite | Relational database for SQL queries |
| SQL | Aggregation, window functions, RFM segmentation |
| Power BI / Tableau | Interactive business dashboard |

---

## 📊 Key Insights

### 1. Revenue & Seasonality
- **November 2024** was the peak month — driven by Diwali and end-of-year festive sales
- Q4 consistently outperforms Q1 by ~2.8× in total revenue
- Weekend orders (Sat–Sun) contribute ~31% more revenue per day vs weekdays

### 2. Category Performance

| Category | Revenue Share | Avg Margin | Return Rate |
|----------|-------------|------------|-------------|
| Electronics | Highest | ~37% | 12% |
| Fashion | 2nd | ~35% | 18% (highest) |
| Home & Kitchen | 3rd | ~38% | 8% |
| Books | Lowest | ~40% | 4% (lowest) |
| Beauty | 4th | ~36% | 10% |
| Sports | 5th | ~37% | 7% |

### 3. Customer Segmentation (RFM)
- **Champions** (~8% of customers) drive ~28% of total revenue
- **At Risk** customers represent a revenue recovery opportunity of ₹15L+
- Average customer lifetime value: ₹2,700 (delivered orders only)

### 4. Payment Trends
- **UPI** is the most popular method (~32% of orders)
- **Credit Card** orders have the highest average order value
- **Cash on Delivery** has a slightly higher cancellation rate

---

## 📈 Charts Generated

| # | Chart | Insight |
|---|-------|---------|
| 1 | Monthly Revenue Trend | Seasonal peaks visible in Oct–Nov |
| 2 | Revenue by Category | Electronics leads, Books is stable |
| 3 | Top 10 Products | Smart Watch & Air Fryer are top earners |
| 4 | Return Rate by Category | Fashion has 18% return rate |
| 5 | Payment Method Analysis | UPI dominates; CC drives highest AOV |
| 6 | Profit Margin Distribution | Electronics has widest variance |
| 7 | Monthly Revenue Heatmap | Nov/Dec hotspot visible across all categories |
| 8 | RFM Customer Segments | Champion segment drives outsized revenue |
| 9 | Day-of-Week Pattern | Weekends peak in spend |
| 10 | Year-over-Year Comparison | 2024 outperforms 2023 in all months |

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ecommerce-analytics.git
cd ecommerce-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset
python3 data/generate_data.py

# 4. Clean data & create SQLite DB
python3 data/clean_data.py

# 5. Run EDA and generate charts
python3 notebooks/eda_analysis.py

# 6. Open SQL queries in any SQLite client
# DB file: data/ecommerce.db
```

---

## 🗄️ SQL Highlights

```sql
-- Top categories by net profit margin
SELECT category,
       ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS net_margin_pct
FROM orders
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY net_margin_pct DESC;

-- Quarter-over-Quarter growth with window function
SELECT year, quarter,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND((SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY year, quarter))
             * 100.0 / LAG(SUM(revenue)) OVER (ORDER BY year, quarter), 2) AS qoq_growth
FROM orders
WHERE order_status = 'Delivered'
GROUP BY year, quarter;
```

Full queries: [`sql/queries.sql`](sql/queries.sql)

---

## 📋 Dataset Description

| Column | Type | Description |
|--------|------|-------------|
| order_id | str | Unique order identifier |
| order_date | date | Date of order placement |
| customer_id | str | Anonymised customer ID |
| city / state | str | Delivery location |
| category | str | Product category (6 categories) |
| product_name | str | Product name |
| quantity | int | Units ordered |
| unit_price | float | Price per unit (₹) |
| discount_pct | int | Discount applied (%) |
| revenue | float | Net revenue after discount (₹) |
| cost | float | Cost of goods (₹) |
| profit | float | Gross profit (₹) |
| profit_margin | float | Profit as % of revenue |
| payment_method | str | Payment type used |
| order_status | str | Delivered / Returned / Cancelled / Pending |
| delivery_days | int | Days to deliver (Delivered orders only) |

---

## 🔮 Future Enhancements

- [ ] Add Streamlit interactive web app
- [ ] Implement ML-based demand forecasting (Prophet / ARIMA)
- [ ] Add customer churn prediction model
- [ ] Connect to live API data source

---

## 👤 Author

**[Your Name]**
- LinkedIn: [your-linkedin]
- Email: [your-email]

---

*Dataset is synthetically generated for portfolio purposes.*
