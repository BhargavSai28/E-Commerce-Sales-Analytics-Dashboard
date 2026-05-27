import pandas as pd
import numpy as np
import sqlite3

# ── Load raw data ──────────────────────────────────────────────────
df = pd.read_csv("/home/claude/ecommerce-analytics/data/raw_orders.csv")
print(f"Raw shape: {df.shape}")

# ── Step 1: Parse dates ────────────────────────────────────────────
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"]       = df["order_date"].dt.year
df["month"]      = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")
df["quarter"]    = df["order_date"].dt.quarter
df["week"]       = df["order_date"].dt.isocalendar().week.astype(int)
df["day_name"]   = df["order_date"].dt.day_name()

# ── Step 2: Data types ─────────────────────────────────────────────
df["quantity"]        = df["quantity"].astype(int)
df["discount_pct"]    = df["discount_pct"].astype(int)
df["revenue"]         = df["revenue"].round(2)
df["profit"]          = df["profit"].round(2)
df["profit_margin"]   = ((df["profit"] / df["revenue"]) * 100).round(2)

# ── Step 3: Feature engineering ────────────────────────────────────
df["is_delivered"] = (df["order_status"] == "Delivered").astype(int)
df["is_returned"]  = (df["order_status"] == "Returned").astype(int)

# ── Step 4: Remove duplicates & nulls ─────────────────────────────
before = len(df)
df.drop_duplicates(subset="order_id", inplace=True)
df.dropna(subset=["revenue","category","customer_id"], inplace=True)
print(f"After cleaning: {len(df)} rows (removed {before - len(df)})")

# ── Step 5: Save cleaned CSV ───────────────────────────────────────
df.to_csv("/home/claude/ecommerce-analytics/data/cleaned_orders.csv", index=False)

# ── Step 6: Load into SQLite ───────────────────────────────────────
conn = sqlite3.connect("/home/claude/ecommerce-analytics/data/ecommerce.db")
df.to_sql("orders", conn, if_exists="replace", index=False)

# RFM table
rfm = df[df["order_status"]=="Delivered"].copy()
snapshot = rfm["order_date"].max()
rfm_summary = rfm.groupby("customer_id").agg(
    recency   = ("order_date", lambda x: (snapshot - x.max()).days),
    frequency = ("order_id",   "count"),
    monetary  = ("revenue",    "sum")
).reset_index()
rfm_summary["monetary"] = rfm_summary["monetary"].round(2)
rfm_summary.to_sql("rfm", conn, if_exists="replace", index=False)

conn.close()
print("SQLite DB created: ecommerce.db")
print(df[["revenue","profit","profit_margin"]].describe().round(2))
