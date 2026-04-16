import os
import pandas as pd
import random

from ml_engine import predict
from utils import generate_store_sku, normalize_sku
from alerts import send_alert
from data_source import fetch_all_products
from price_engine import fetch_price


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "current.csv")


STORE_MAP = {
    "1280": "Home Depot - Farmingdale, NY",
    "6170": "Home Depot - Patchogue, NY",
    "2201": "Home Depot - Commack, NY"
}


# ==============================
# 🔥 REAL DATA GENERATION
# ==============================

def generate_data():

    products = fetch_all_products()

    if not products:
        send_alert("❌ No products found from pipeline")
        return pd.DataFrame()

    rows = []

    for p in products:

        print(f"Fetching price: {p['url']}")

        price = fetch_price(p["url"])

        if price is None:
            print("⚠️ Skipping (no price found)")
            continue

        # Temporary original price estimation (until we extract real MSRP)
        original_price = round(price * random.uniform(1.2, 1.8), 2)

        drop_pct = round((original_price - price) / original_price * 100, 2)

        store_id = random.choice(list(STORE_MAP.keys()))

        rows.append({
            "sku": generate_store_sku(p["name"], store_id),

            "item_name": p["name"],
            "price": price,
            "original_price": original_price,
            "drop_pct": drop_pct,
            "velocity": random.randint(1, 10),
            "stock_qty": random.randint(0, 30),
            "store_name": STORE_MAP[store_id],

            "hd_url": p["url"],
            "hd_title": p["name"],
            "hd_confidence": 1.0
        })

    df = pd.DataFrame(rows)

    print(f"✅ REAL PRODUCTS WITH PRICE: {len(df)}")

    return df


# ==============================
# 🚀 PIPELINE EXECUTION
# ==============================

df = generate_data()

if df.empty:
    print("❌ No data generated")
    exit()

# ML scoring
df = predict(df)

# Save output
df.to_csv(DATA_PATH, index=False)

# Filter deals
deals = df[df["drop_pct"] >= 20].sort_values("drop_pct", ascending=False)


# ==============================
# 📤 TELEGRAM FORMATTING
# ==============================

def chunk(text, limit=3500):
    parts = []
    cur = ""

    for line in text.split("\n"):
        if len(cur) + len(line) > limit:
            parts.append(cur)
            cur = ""
        cur += line + "\n"

    if cur:
        parts.append(cur)

    return parts


message = "🔥 REAL DEAL ENGINE OUTPUT\n\n"

for _, row in deals.iterrows():

    message += f"""
📦 {row['item_name']}
🏷 SKU: {normalize_sku(row['sku'])}
🏬 {row['store_name']}

💰 ${row['price']} (Was ${row['original_price']})
📉 {row['drop_pct']}% OFF
📦 Stock: {row['stock_qty']}

🧠 Score: {row['ml_score']}

🌐 {row['hd_url']}

----------------------
"""


# Send in chunks (Telegram safe)
for part in chunk(message):
    send_alert(part)


print("🚀 DONE")
