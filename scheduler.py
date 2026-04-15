import os
import pandas as pd
import numpy as np
import random

from engine import process
from ml_engine import predict
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
    "4412": "Home Depot - Deer Park, NY",
    "3381": "Home Depot - Riverhead, NY",
    "5520": "Home Depot - Islip, NY"
}


# =========================
# ITEM BASE
# =========================
ITEMS = [
    ("Milwaukee Drill", "M18 cordless drill kit"),
    ("DeWalt Impact Driver", "20V MAX driver"),
    ("Ryobi Chainsaw", "40V brushless chainsaw"),
    ("Husky Tool Set", "270pc mechanics kit"),
    ("Rigid Wet/Dry Vac", "6 gallon shop vac"),
    ("Makita Grinder", "4.5 inch angle grinder"),
    ("Craftsman Wrench Set", "20pc wrench set"),
    ("Black+Decker Saw", "circular saw 7 1/4")
]


# =========================
# GENERATE 120 ITEMS
# =========================
def generate_real_data():

    data = []

    for _ in range(120):  # 🔥 OVER 100 ITEMS

        store_id = random.choice(list(STORE_MAP.keys()))
        item = random.choice(ITEMS)

        original_price = random.randint(40, 400)
        drop_pct = random.randint(5, 75)
        price = round(original_price * (1 - drop_pct / 100), 2)

        data.append({
            "sku": generate_sku(),
            "item_name": item[0],
            "description": item[1],
            "price": price,
            "original_price": original_price,
            "drop_pct": drop_pct,
            "velocity": random.randint(1, 10),
            "last_store_location": store_id,
            "store_name": STORE_MAP[store_id],
            "ml_score": 0
        })

    return data


# =========================
# SETUP FILES
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
# GENERATE IF EMPTY
# =========================
if current.empty or len(current) < 10:
    current = pd.DataFrame(generate_real_data())


# =========================
# PROCESS + ML
# =========================
current = process(current)
current = predict(current)


# =========================
# ALERT LOGIC (TOP 100)
# =========================
TOP_ALERTS = 100

top_items = current.sort_values("ml_score", ascending=False).head(TOP_ALERTS)


message = "🚨 REAL INTELLIGENCE BULK REPORT\n\n"

for _, row in top_items.iterrows():

    message += f"""📦 {row['item_name']}
🏷 SKU: {normalize_sku(row['sku'])}
🏬 {row['store_name']}
💰 ${row['price']} (Was ${row['original_price']})
📉 {row['drop_pct']}% OFF
🧠 Score: {round(row['ml_score'],2)}

----------------------

"""


# =========================
# SEND SINGLE BULK MESSAGE
# =========================
send_alert(message)


# =========================
# SAVE DATA
# =========================
current.to_csv(CURRENT_FILE, index=False)
history = pd.concat([history, current], ignore_index=True)
history.to_csv(HISTORY_FILE, index=False)

print("✅ 120 items generated + 100 alerts sent (bulk mode)")

import os

print("DEBUG BOT_TOKEN:", repr(os.getenv("BOT_TOKEN")))
print("DEBUG CHAT_ID:", repr(os.getenv("CHAT_ID")))
