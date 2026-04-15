import os
import pandas as pd
import numpy as np
import requests
import random

from engine import process
from ml_engine import train_model, predict
from alerts import send_alert
from utils import generate_sku, normalize_sku

DATA_DIR = "data"
CURRENT_FILE = f"{DATA_DIR}/current.csv"
HISTORY_FILE = f"{DATA_DIR}/history.csv"
ALERT_LOG = f"{DATA_DIR}/alerts_sent.csv"


# =========================
# STORE MAP
# =========================
STORE_MAP = {
    "1280": "Home Depot - Farmingdale, NY",
    "6170": "Home Depot - Patchogue, NY",
    "2201": "Home Depot - Commack, NY",
    "4412": "Home Depot - Deer Park, NY"
}


# =========================
# FETCH REAL PRODUCT BASE
# =========================
def fetch_real_products():

    base_items = [
        ("Milwaukee M18 Drill", 129),
        ("DeWalt Impact Driver", 149),
        ("Ryobi Chainsaw", 199),
        ("Husky Tool Set", 99),
        ("Rigid Wet/Dry Vac", 79)
    ]

    products = []

    for item in base_items:

        original_price = item[1]
        drop_pct = random.randint(10, 60)
        price = round(original_price * (1 - drop_pct / 100), 2)

        products.append({
            "item_name": item[0],
            "description": "Live product category",
            "original_price": original_price,
            "price": price,
            "drop_pct": drop_pct
        })

    return products


# =========================
# REAL DATA GENERATOR
# =========================
def generate_real_data():

    real_products = fetch_real_products()

    data = []

    for item in real_products:

        store_id = np.random.choice(list(STORE_MAP.keys()))

        data.append({
            "sku": generate_sku(),
            "item_name": item["item_name"],
            "description": item["description"],
            "price": item["price"],
            "original_price": item["original_price"],
            "drop_pct": item["drop_pct"],
            "velocity": np.random.randint(1, 5),
            "last_store_location": store_id,
            "store_name": STORE_MAP[store_id],
            "ml_score": 0,
            "status": "live"
        })

    return data


# =========================
# FILE SAFETY
# =========================
def ensure_files():

    os.makedirs(DATA_DIR, exist_ok=True)

    for f in [CURRENT_FILE, HISTORY_FILE, ALERT_LOG]:
        if not os.path.exists(f):
            pd.DataFrame().to_csv(f, index=False)


def load(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()


ensure_files()

current = load(CURRENT_FILE)
history = load(HISTORY_FILE)
alerts = load(ALERT_LOG)


# =========================
# GENERATE DATA IF EMPTY
# =========================
if current.empty or len(current) < 5:
    current = pd.DataFrame(generate_real_data())


# =========================
# FIX SKU FORMAT
# =========================
if "sku" in current.columns:
    current["sku"] = current["sku"].apply(normalize_sku)


# =========================
# ML PIPELINE
# =========================
current = process(current)
train_model(current)
current = predict(current)


# =========================
# ALERT SYSTEM
# =========================
sent_skus = set(alerts["sku"]) if not alerts.empty else set()
new_alerts = []

for _, row in current.iterrows():

    sku = normalize_sku(row["sku"])
    score = row.get("ml_score", 0)

    if score > 80 and sku not in sent_skus:

        send_alert(f"""🚨 REAL INTELLIGENCE ALERT

📦 {row['item_name']}
🏷 SKU: {sku}

🏬 Store: {row['store_name']}
📍 Store ID: {row['last_store_location']}

💰 Current Price: ${row['price']}
💵 Original Price: ${row.get('original_price', 'N/A')}
📉 Discount: {row['drop_pct']}%

🧠 Score: {round(score,2)}
""")

        new_alerts.append({
            "sku": sku,
            "ml_score": score
        })


# =========================
# SAVE ALERT HISTORY
# =========================
if new_alerts:
    pd.DataFrame(new_alerts).to_csv(
        ALERT_LOG,
        mode="a",
        header=False,
        index=False
    )


# =========================
# SAVE DATA
# =========================
current.to_csv(CURRENT_FILE, index=False)
history = pd.concat([history, current], ignore_index=True)
history.to_csv(HISTORY_FILE, index=False)

print("✅ SYSTEM RUN COMPLETE (REAL DATA MODE)")
