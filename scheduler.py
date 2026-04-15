import os
import pandas as pd
import random

from ml_engine import predict
from utils import generate_store_sku, normalize_sku
from alerts import send_alert


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

        # FULL DISCOUNT RANGE (0–100%)
        drop_pct = random.randint(0, 100)

        price = round(original_price * (1 - drop_pct / 100), 2)
        price = max(price, 0)

        rows.append({
            "sku": generate_store_sku(name, store_id),
            "item_name": name,
            "price": price,
            "original_price": original_price,
            "drop_pct": drop_pct,
            "velocity": random.randint(1, 10),
            "stock_qty": random.randint(0, 30),
            "store_name": STORE_MAP[store_id],
            "store_id": store_id
        })

    return pd.DataFrame(rows)


# =========================
# PIPELINE
# =========================
df = generate_data()

df = predict(df)

df.to_csv(DATA_PATH, index=False, encoding="utf-8")

print("DEBUG: Generated rows =", len(df))


# =========================
# FILTER (20%+ DEALS ONLY)
# =========================
deals = df[df["drop_pct"] >= 20].sort_values("drop_pct", ascending=False)


# =========================
# TELEGRAM SAFE CHUNKING
# =========================
def chunk(text, limit=3500):
    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) > limit:
            chunks.append(current)
            current = ""
        current += line + "\n"

    if current:
        chunks.append(current)

    return chunks


message = "🚨 FULL RETAIL DEAL INTELLIGENCE (STABLE SKU SYSTEM)\n\n"

for _, row in deals.iterrows():

    message += f"""
📦 {row['item_name']}
🏷 SKU: {normalize_sku(row['sku'])}
🏬 {row['store_name']}

💰 ${row['price']} (Was ${row['original_price']})
📉 {row['drop_pct']}% OFF
📦 Stock: {row['stock_qty']}

🧠 ML Score: {row['ml_score']}

----------------------
"""


for part in chunk(message):
    send_alert(part)

print("✅ SKU System + Scheduler Updated Successfully")
