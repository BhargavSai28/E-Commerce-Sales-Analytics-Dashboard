import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import sqlite3, warnings
warnings.filterwarnings("ignore")

# ── Style ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor":   "#FAFAFA",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.color":       "#E5E5E5",
    "grid.linewidth":   0.6,
    "font.family":      "DejaVu Sans",
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})

PALETTE = ["#4E6EF2","#F28B30","#2CB67D","#E8504A","#A855F7","#F59E0B"]
CAT_COLORS = {
    "Electronics":"#4E6EF2","Fashion":"#F28B30","Home & Kitchen":"#2CB67D",
    "Books":"#A855F7","Beauty":"#E8504A","Sports":"#F59E0B"
}

conn = sqlite3.connect("/home/claude/ecommerce-analytics/data/ecommerce.db")
df   = pd.read_sql("SELECT * FROM orders", conn)
rfm  = pd.read_sql("SELECT * FROM rfm", conn)
conn.close()

df["order_date"] = pd.to_datetime(df["order_date"])
delivered = df[df["order_status"] == "Delivered"].copy()
IMAGES = "/home/claude/ecommerce-analytics/images"

def save(name):
    path = f"{IMAGES}/{name}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {name}.png")

# ── Chart 1: Monthly Revenue Trend ────────────────────────────────
print("Chart 1: Monthly Revenue Trend")
monthly = (delivered.groupby(["year","month"])["revenue"].sum().reset_index())
monthly["period"] = pd.to_datetime(monthly[["year","month"]].assign(day=1))
monthly = monthly.sort_values("period")

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.fill_between(range(len(monthly)), monthly["revenue"]/1e5, alpha=0.15, color="#4E6EF2")
ax.plot(range(len(monthly)), monthly["revenue"]/1e5, color="#4E6EF2", lw=2.5, marker="o", ms=5)
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels([p.strftime("%b'%y") for p in monthly["period"]], rotation=45, ha="right", fontsize=9)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.0fL"))
ax.set_title("Monthly Revenue Trend (Jan 2023 – Dec 2024)")
ax.set_ylabel("Revenue (Lakhs)")
# Annotate peak
peak_idx = monthly["revenue"].idxmax()
peak_row = monthly.loc[peak_idx]
rel_idx = list(monthly.index).index(peak_idx)
ax.annotate(f"Peak\n₹{peak_row['revenue']/1e5:.1f}L", xy=(rel_idx, peak_row["revenue"]/1e5),
            xytext=(rel_idx-2, peak_row["revenue"]/1e5 + 10),
            arrowprops=dict(arrowstyle="->", color="#E8504A"), color="#E8504A", fontsize=9)
plt.tight_layout()
save("01_monthly_revenue_trend")

# ── Chart 2: Revenue by Category ──────────────────────────────────
print("Chart 2: Revenue by Category")
cat_rev = delivered.groupby("category")["revenue"].sum().sort_values(ascending=True)
colors  = [CAT_COLORS[c] for c in cat_rev.index]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(cat_rev.index, cat_rev.values/1e5, color=colors, height=0.6)
for bar, val in zip(bars, cat_rev.values):
    ax.text(val/1e5 + 0.5, bar.get_y() + bar.get_height()/2,
            f"₹{val/1e5:.1f}L", va="center", fontsize=10)
ax.set_xlabel("Revenue (Lakhs)")
ax.set_title("Total Revenue by Category (Delivered Orders)")
ax.grid(axis="y", alpha=0)
ax.set_xlim(0, cat_rev.max()/1e5 * 1.15)
plt.tight_layout()
save("02_revenue_by_category")

# ── Chart 3: Top 10 Products ───────────────────────────────────────
print("Chart 3: Top 10 Products")
top_prods = (delivered.groupby(["product_name","category"])["revenue"]
             .sum().reset_index().sort_values("revenue", ascending=False).head(10))

fig, ax = plt.subplots(figsize=(10, 5.5))
bar_colors = [CAT_COLORS[c] for c in top_prods["category"]]
bars = ax.barh(top_prods["product_name"], top_prods["revenue"]/1e5, color=bar_colors, height=0.6)
for bar, val in zip(bars, top_prods["revenue"]):
    ax.text(val/1e5 + 0.2, bar.get_y() + bar.get_height()/2,
            f"₹{val/1e5:.1f}L", va="center", fontsize=9)
ax.set_xlabel("Revenue (Lakhs)")
ax.set_title("Top 10 Products by Revenue")
ax.invert_yaxis()
# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=v, label=k) for k,v in CAT_COLORS.items()]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.7)
plt.tight_layout()
save("03_top10_products")

# ── Chart 4: Return Rate by Category ──────────────────────────────
print("Chart 4: Return Rate")
ret = df.groupby("category").apply(
    lambda x: pd.Series({
        "return_rate": (x["order_status"]=="Returned").mean()*100,
        "total_orders": len(x)
    })
).reset_index()

fig, ax = plt.subplots(figsize=(8, 4.5))
colors_ret = ["#E8504A" if r > 12 else "#4E6EF2" for r in ret["return_rate"]]
bars = ax.bar(ret["category"], ret["return_rate"], color=colors_ret, width=0.55)
for bar, val in zip(bars, ret["return_rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f"{val:.1f}%", ha="center", fontsize=10)
ax.set_ylabel("Return Rate (%)")
ax.set_title("Return Rate by Category")
ax.axhline(ret["return_rate"].mean(), color="#888", ls="--", lw=1.2, label=f"Avg: {ret['return_rate'].mean():.1f}%")
ax.legend(fontsize=9)
ax.set_ylim(0, ret["return_rate"].max() * 1.25)
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
save("04_return_rate_by_category")

# ── Chart 5: Payment Method Distribution ──────────────────────────
print("Chart 5: Payment Methods")
pay = delivered.groupby("payment_method")["order_id"].count().sort_values(ascending=False)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

wedges, texts, autotexts = ax1.pie(pay.values, labels=pay.index, autopct="%1.1f%%",
                                    startangle=140, colors=PALETTE,
                                    pctdistance=0.78, wedgeprops=dict(width=0.55))
for t in autotexts: t.set_fontsize(9)
ax1.set_title("Orders by Payment Method")

avg_val = delivered.groupby("payment_method")["revenue"].mean().reindex(pay.index)
bars = ax2.bar(avg_val.index, avg_val.values, color=PALETTE[:len(avg_val)], width=0.55)
for bar, val in zip(bars, avg_val):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f"₹{val:,.0f}", ha="center", fontsize=9)
ax2.set_ylabel("Avg Order Value (₹)")
ax2.set_title("Avg Order Value by Payment Method")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
save("05_payment_methods")

# ── Chart 6: Profit Margin Distribution ───────────────────────────
print("Chart 6: Profit Margin Distribution")
fig, ax = plt.subplots(figsize=(9, 4.5))
for cat, color in CAT_COLORS.items():
    data = delivered[delivered["category"]==cat]["profit_margin"]
    ax.hist(data, bins=25, alpha=0.55, color=color, label=cat, density=True)
ax.set_xlabel("Profit Margin (%)")
ax.set_ylabel("Density")
ax.set_title("Profit Margin Distribution by Category")
ax.legend(fontsize=9, loc="upper left")
plt.tight_layout()
save("06_profit_margin_distribution")

# ── Chart 7: Heatmap — Revenue by Month & Category ────────────────
print("Chart 7: Heatmap")
pivot = (delivered.groupby(["month","category"])["revenue"].sum()
         .unstack(fill_value=0) / 1e5)
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
pivot.index = month_labels[:len(pivot)]

fig, ax = plt.subplots(figsize=(11, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"label":"Revenue (Lakhs)"},
            annot_kws={"size":9})
ax.set_title("Monthly Revenue Heatmap by Category (₹ Lakhs)")
ax.set_xlabel("Category")
ax.set_ylabel("Month")
plt.tight_layout()
save("07_revenue_heatmap")

# ── Chart 8: RFM Customer Segments ────────────────────────────────
print("Chart 8: RFM Segments")
snapshot = delivered["order_date"].max()
rfm_data = delivered.groupby("customer_id").agg(
    recency   = ("order_date", lambda x: (snapshot - x.max()).days),
    frequency = ("order_id",   "count"),
    monetary  = ("revenue",    "sum")
).reset_index()

def segment(row):
    if row.recency <= 30 and row.frequency >= 5 and row.monetary >= 10000: return "Champion"
    if row.recency <= 60 and row.frequency >= 3 and row.monetary >= 5000:  return "Loyal"
    if row.recency <= 90 and row.frequency >= 2:                            return "Potential"
    if row.recency >  180 and row.frequency == 1:                          return "At Risk"
    return "Needs Attention"

rfm_data["segment"] = rfm_data.apply(segment, axis=1)
seg_counts = rfm_data["segment"].value_counts()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
seg_colors = {"Champion":"#2CB67D","Loyal":"#4E6EF2","Potential":"#F59E0B","At Risk":"#E8504A","Needs Attention":"#A855F7"}
colors_seg = [seg_colors.get(s,"#888") for s in seg_counts.index]

bars = ax1.bar(seg_counts.index, seg_counts.values, color=colors_seg, width=0.55)
for bar, val in zip(bars, seg_counts):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             str(val), ha="center", fontsize=10)
ax1.set_ylabel("Number of Customers")
ax1.set_title("RFM Customer Segments")
ax1.set_xticklabels(seg_counts.index, rotation=20, ha="right")

seg_rev = rfm_data.groupby("segment")["monetary"].sum().reindex(seg_counts.index) / 1e5
bars2 = ax2.bar(seg_rev.index, seg_rev.values, color=colors_seg, width=0.55)
for bar, val in zip(bars2, seg_rev):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"₹{val:.0f}L", ha="center", fontsize=9)
ax2.set_ylabel("Total Revenue (Lakhs)")
ax2.set_title("Revenue by Customer Segment")
ax2.set_xticklabels(seg_rev.index, rotation=20, ha="right")
plt.tight_layout()
save("08_rfm_segments")

# ── Chart 9: Day-of-Week Pattern ──────────────────────────────────
print("Chart 9: Day of Week")
dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow = (delivered.groupby("day_name")["revenue"].sum()
       .reindex(dow_order).fillna(0) / 1e5)

fig, ax = plt.subplots(figsize=(8, 4))
bar_c = ["#4E6EF2" if d in ["Saturday","Sunday"] else "#A8B8F0" for d in dow.index]
bars = ax.bar(dow.index, dow.values, color=bar_c, width=0.6)
for bar, val in zip(bars, dow.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"₹{val:.0f}L", ha="center", fontsize=9)
ax.set_ylabel("Revenue (Lakhs)")
ax.set_title("Revenue by Day of Week")
ax.set_xticklabels(dow.index, rotation=20, ha="right")
plt.tight_layout()
save("09_day_of_week")

# ── Chart 10: YoY Comparison ──────────────────────────────────────
print("Chart 10: YoY Comparison")
yoy = (delivered.groupby(["year","month"])["revenue"].sum()
       .reset_index().pivot(index="month", columns="year", values="revenue") / 1e5)
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

fig, ax = plt.subplots(figsize=(11, 4.5))
x = np.arange(12)
w = 0.38
if 2023 in yoy.columns:
    ax.bar(x - w/2, yoy[2023].fillna(0), w, color="#A8B8F0", label="2023")
if 2024 in yoy.columns:
    ax.bar(x + w/2, yoy[2024].fillna(0), w, color="#4E6EF2", label="2024")
ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_ylabel("Revenue (Lakhs)")
ax.set_title("Year-over-Year Monthly Revenue Comparison")
ax.legend(fontsize=10)
plt.tight_layout()
save("10_yoy_comparison")

print("\nAll 10 charts saved successfully!")
