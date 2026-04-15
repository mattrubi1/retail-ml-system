import os
import pandas as pd
import random

from ml_engine import predict
from alerts import send_alert
from utils import generate_sku, normalize_sku


DATA_PATH = "data/current.csv"

os.makedirs("data", exist_ok=True)


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
    ("Makita Grinder", 160)
]


def generate():

    data = []

    for _ in range(120):

        name, base_price = random.choice(ITEMS)
        store_id = random.choice(list(STORE_MAP.keys()))

        original = base_price + random.randint(10, 80)
        drop = random.randint(5, 60)
        price = round(original * (1 - drop / 100), 2)

        data.append({
            "sku": generate_sku(),
            "item_name": name,
            "price": price,
            "original_price": original,
            "drop_pct": drop,
            "velocity": random.randint(1, 10),
            "store_name": STORE_MAP[store_id],
            "last_store_location": store_id
        })

    return pd.DataFrame(data)


# =========================
# GENERATE + SCORE
# =========================
df = generate()
df = predict(df)

# =========================
# SAVE
# =========================
df.to_csv(DATA_PATH, index=False)

print("✅ current.csv updated")


# =========================
# TELEGRAM (TOP 100)
# =========================
top = df.sort_values("ml_score", ascending=False).head(100)

message = "🚨 RETAIL INTELLIGENCE ALERT\n\n"

for _, row in top.iterrows():

    message += f"""
📦 {row['item_name']}
🏷 SKU: {normalize_sku(row['sku'])}
🏬 {row['store_name']}
💰 ${row['price']} (Was ${row['original_price']})
📉 {row['drop_pct']}%
🧠 Score: {row['ml_score']}

----------------------
"""

send_alert(message)

print("✅ Telegram sent")
