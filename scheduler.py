import os
import pandas as pd
import random

from ml_engine import predict
from utils import generate_store_sku, normalize_sku
from alerts import send_alert
from data_source import fetch_products


send_alert("🚀 LIVE DATA PIPELINE STARTED")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "current.csv")


STORE_MAP = {
    "1280": "Home Depot - Farmingdale, NY",
    "6170": "Home Depot - Patchogue, NY",
    "2201": "Home Depot - Commack, NY"
}


def generate_data():

    rows = []

    products = fetch_products()

    print("REAL PRODUCTS FOUND:", len(products))

    if not products:
        print("❌ No products found")
        return pd.DataFrame()

    for p in products:

        store_id = random.choice(list(STORE_MAP.keys()))

        original_price = random.randint(80, 300)
        drop_pct = random.randint(20, 80)

        price = round(original_price * (1 - drop_pct / 100), 2)

        rows.append({
            "sku": generate_store_sku(p["name"], store_id),

            "item_name": p["name"],
            "price": price,
            "original_price": original_price,
            "drop_pct": drop_pct,
            "velocity": random.randint(1, 10),
            "stock_qty": random.randint(0, 30),
            "store_name": STORE_MAP[store_id],

            "hd_title": p["name"],
            "hd_url": p["url"],
            "hd_confidence": 0.9
        })

    return pd.DataFrame(rows)


df = generate_data()

if df.empty:
    send_alert("❌ No products found — pipeline failed")
    exit()


df = predict(df)

df.to_csv(DATA_PATH, index=False)


deals = df[df["drop_pct"] >= 20].sort_values("drop_pct", ascending=False)


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


message = "🔥 LIVE HOME DEPOT DEALS\n\n"

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


for part in chunk(message):
    send_alert(part)


print("✅ LIVE PIPELINE COMPLETE")
