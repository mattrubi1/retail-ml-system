import os
import pandas as pd
import random

from ml_engine import predict
from utils import generate_store_sku, normalize_sku
from alerts import send_alert
from product_matcher import match_product


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "current.csv")

os.makedirs(DATA_DIR, exist_ok=True)


STORE_MAP = {
    "1280": "Home Depot - Farmingdale, NY",
    "6170": "Home Depot - Patchogue, NY",
    "2201": "Home Depot - Commack, NY"
}


ITEMS = [
    ("Milwaukee Drill", 120),
    ("DeWalt Impact Driver", 180),
    ("Ryobi Chainsaw", 150),
    ("Husky Tool Set", 90),
    ("Rigid Wet/Dry Vac", 110),
    ("Makita Grinder", 160),
    ("Ryobi Blower", 85),
    ("DeWalt Saw", 210)
]


def generate_data():

    rows = []

    for _ in range(120):

        name, base_price = random.choice(ITEMS)
        store_id = random.choice(list(STORE_MAP.keys()))

        original_price = base_price + random.randint(10, 80)
        drop_pct = random.randint(20, 100)

        price = round(original_price * (1 - drop_pct / 100), 2)

        match = match_product(name)

        rows.append({
            "sku": generate_store_sku(name, store_id),

            "item_name": name,
            "price": price,
            "original_price": original_price,
            "drop_pct": drop_pct,
            "velocity": random.randint(1, 10),
            "stock_qty": random.randint(0, 30),
            "store_name": STORE_MAP[store_id],

            "hd_title": match["title"],
            "hd_url": match["url"],
            "hd_confidence": match["confidence"]
        })

    return pd.DataFrame(rows)


df = generate_data()
df = predict(df)

df.to_csv(DATA_PATH, index=False)

print("DEBUG: rows =", len(df))


deals = df[df["drop_pct"] >= 20].sort_values("drop_pct", ascending=False)


def chunk(text, limit=3500):
    chunks, current = [], ""

    for line in text.split("\n"):
        if len(current) + len(line) > limit:
            chunks.append(current)
            current = ""
        current += line + "\n"

    if current:
        chunks.append(current)

    return chunks


message = "🚀 RETAIL INTELLIGENCE ENGINE\n\n"

for _, row in deals.iterrows():

    message += f"""
📦 {row['item_name']}
🏷 SKU: {normalize_sku(row['sku'])}
🏬 {row['store_name']}

💰 ${row['price']} (Was ${row['original_price']})
📉 {row['drop_pct']}% OFF
📦 Stock: {row['stock_qty']}

🧠 ML Score: {row['ml_score']}

🔎 HD MATCH: {row['hd_title'] if row['hd_title'] else 'None'}
🌐 {row['hd_url'] if row['hd_url'] else 'None'}
🎯 Confidence: {row['hd_confidence']}

----------------------
"""


sent = False

if not sent:
    for part in chunk(message):
        send_alert(part)

    sent = True

print("✅ Done")
