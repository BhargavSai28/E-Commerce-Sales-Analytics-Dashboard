import pandas as pd
import numpy as np
import random
import sqlite3
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# --- Config ---
N_ORDERS = 12000
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2024, 12, 31)

CATEGORIES = {
    "Electronics":    {"products": ["Wireless Earbuds","Smart Watch","Laptop Stand","USB-C Hub","Bluetooth Speaker","Gaming Mouse","Mechanical Keyboard","Webcam","External SSD","Phone Case"],
                       "price_range": (299, 4999), "return_rate": 0.12},
    "Fashion":        {"products": ["Men's T-Shirt","Women's Kurta","Denim Jeans","Sports Sneakers","Formal Shirt","Saree","Leggings","Jacket","Sunglasses","Wallet"],
                       "price_range": (199, 2499), "return_rate": 0.18},
    "Home & Kitchen": {"products": ["Pressure Cooker","Air Fryer","Non-stick Pan","Water Bottle","Knife Set","Mixer Grinder","Coffee Maker","Bedsheet Set","Pillow Pair","Storage Box"],
                       "price_range": (299, 3999), "return_rate": 0.08},
    "Books":          {"products": ["Data Science Handbook","Python Crash Course","Atomic Habits","Rich Dad Poor Dad","The Alchemist","Wings of Fire","Clean Code","Deep Work","Sapiens","Zero to One"],
                       "price_range": (149, 799),  "return_rate": 0.04},
    "Beauty":         {"products": ["Face Serum","Sunscreen SPF50","Hair Oil","Moisturizer","Lip Balm","Kajal","Foundation","Face Wash","Body Lotion","Perfume"],
                       "price_range": (199, 1999), "return_rate": 0.10},
    "Sports":         {"products": ["Yoga Mat","Resistance Bands","Dumbbells 5kg","Skipping Rope","Cricket Bat","Badminton Racket","Cycling Helmet","Running Shoes","Water Sipper","Gym Gloves"],
                       "price_range": (299, 3499), "return_rate": 0.07},
}

CITIES = ["Mumbai","Delhi","Bangalore","Hyderabad","Chennai","Kolkata","Pune","Ahmedabad","Jaipur","Lucknow",
          "Surat","Kochi","Chandigarh","Indore","Bhopal","Nagpur","Visakhapatnam","Patna","Vadodara","Coimbatore"]
STATES = {"Mumbai":"Maharashtra","Delhi":"Delhi","Bangalore":"Karnataka","Hyderabad":"Telangana",
          "Chennai":"Tamil Nadu","Kolkata":"West Bengal","Pune":"Maharashtra","Ahmedabad":"Gujarat",
          "Jaipur":"Rajasthan","Lucknow":"Uttar Pradesh","Surat":"Gujarat","Kochi":"Kerala",
          "Chandigarh":"Punjab","Indore":"Madhya Pradesh","Bhopal":"Madhya Pradesh","Nagpur":"Maharashtra",
          "Visakhapatnam":"Andhra Pradesh","Patna":"Bihar","Vadodara":"Gujarat","Coimbatore":"Tamil Nadu"}
PAYMENT = ["Credit Card","Debit Card","UPI","Net Banking","Cash on Delivery","EMI"]
STATUS  = ["Delivered","Returned","Cancelled","Pending"]

# Seasonal weights (higher sales in festive months)
def date_weight(d):
    m = d.month
    return {10:2.8,11:3.2,12:2.5,8:1.5,9:1.8}.get(m, 1.0)

# Generate dates with seasonal weighting
all_dates = [START_DATE + timedelta(days=i) for i in range((END_DATE - START_DATE).days + 1)]
date_weights = [date_weight(d) for d in all_dates]
date_weights = [w / sum(date_weights) for w in date_weights]
order_dates = np.random.choice(all_dates, size=N_ORDERS, p=date_weights)

rows = []
for i, order_date in enumerate(order_dates):
    cat   = random.choice(list(CATEGORIES.keys()))
    info  = CATEGORIES[cat]
    prod  = random.choice(info["products"])
    lo, hi = info["price_range"]
    price   = round(random.uniform(lo, hi), 2)
    qty     = random.choices([1,2,3,4,5], weights=[50,25,12,8,5])[0]
    discount_pct = random.choices([0,5,10,15,20,25,30], weights=[20,15,20,15,12,10,8])[0]
    discount = round(price * qty * discount_pct / 100, 2)
    revenue  = round(price * qty - discount, 2)
    cost     = round(price * qty * random.uniform(0.45, 0.65), 2)
    profit   = round(revenue - cost, 2)

    # Status: high return in fashion, low in books
    rr = info["return_rate"]
    status = random.choices(STATUS, weights=[1-rr-0.05-0.03, rr, 0.05, 0.03])[0]

    city  = random.choice(CITIES)
    state = STATES[city]
    cust_id = f"CUST{random.randint(1000, 4999):04d}"
    order_id = f"ORD{100000 + i}"
    delivery_days = None if status != "Delivered" else random.randint(1, 10)

    rows.append({
        "order_id": order_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer_id": cust_id,
        "city": city,
        "state": state,
        "category": cat,
        "product_name": prod,
        "quantity": qty,
        "unit_price": price,
        "discount_pct": discount_pct,
        "discount_amount": discount,
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "payment_method": random.choice(PAYMENT),
        "order_status": status,
        "delivery_days": delivery_days,
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/ecommerce-analytics/data/raw_orders.csv", index=False)
print(f"Generated {len(df)} orders | Revenue: ₹{df['revenue'].sum():,.0f}")
print(df["category"].value_counts())
print(df["order_status"].value_counts())
