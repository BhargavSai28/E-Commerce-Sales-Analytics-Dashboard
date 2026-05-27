# Dashboard Setup Guide
## Connecting Power BI / Tableau to this Project

### Option A — Power BI Desktop
1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Load `data/cleaned_orders.csv`
3. In **Power Query Editor**, verify column types:
   - `order_date` → Date
   - `revenue`, `profit`, `unit_price` → Decimal Number
   - `quantity`, `discount_pct` → Whole Number
4. Click **Close & Apply**

### Recommended Visuals to Build

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI | Card | SUM(revenue) |
| Total Profit KPI | Card | SUM(profit) |
| Avg Order Value KPI | Card | AVERAGE(revenue) |
| Return Rate KPI | Card | DIVIDE(COUNTIF(Returned), COUNT(order_id)) |
| Monthly Revenue Trend | Line Chart | order_date (Month), SUM(revenue) |
| Revenue by Category | Bar Chart | category, SUM(revenue) |
| Payment Method Split | Donut Chart | payment_method, COUNT(order_id) |
| State Revenue Map | Filled Map | state, SUM(revenue) |
| Top Products Table | Table | product_name, revenue, profit_margin |
| Order Status Breakdown | Pie Chart | order_status, COUNT(order_id) |

### Slicers to Add
- Date Range (order_date)
- Category (category)
- State (state)
- Order Status (order_status)

### DAX Measures (Power BI)
```
Total Revenue = SUM(orders[revenue])
Total Profit  = SUM(orders[profit])
Avg Order Value = AVERAGE(orders[revenue])
Return Rate % = DIVIDE(CALCULATE(COUNT(orders[order_id]), orders[order_status]="Returned"), COUNT(orders[order_id])) * 100
Profit Margin % = DIVIDE(SUM(orders[profit]), SUM(orders[revenue])) * 100
```

### Option B — Tableau Public (Free)
1. Open Tableau → **Connect → Text File** → select `cleaned_orders.csv`
2. Drag `order_date` to Columns, `revenue` to Rows for the trend line
3. Use **Show Me** panel for chart type suggestions
4. Publish to Tableau Public for a shareable link to add to your GitHub README

### Export
- Export Power BI dashboard as PDF: **File → Export → PDF**
- Save screenshots as PNG and place in `dashboard/` folder
