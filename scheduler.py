import os
import pandas as pd
import random

from ml_engine import predict
from utils import generate_store_sku, normalize_sku
from alerts import send_alert
from data_source import fetch_all_products


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "current.csv")


STORE_MAP = {
    "1280": "Home Depot - Farmingdale, NY",
    "6170": "Home Depot - Patchogue, NY",
    "2201": "Home Depot - Commack, NY"
}


def generate_data():

    products = fetch_all_products()

    if not products:
        send_alert("❌ No products found from search pipeline")
        return pd.DataFrame()

    rows = []

    for p in products:

        store_id = random.choice(list(STORE_MAP.keys()))

        original_price = random.randint(80, 400)
        drop_pct = random.randint(20, 90)
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

            "hd_url": p["url"],
            "hd_title": p["name"],
            "hd_confidence": 1.0
        })

    return pd.DataFrame(rows)


df = generate_data()

if df.empty:
    print("No data")
    exit()

df = predict(df)

df.to_csv(DATA_PATH, index=False)

deals = df[df["drop_pct"] >= 20].sort_values("drop_pct", ascending=False)


message = "🔥 DEAL ENGINE OUTPUT\n\n"

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


send_alert(message)

print("DONE")
