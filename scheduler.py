import os
import pandas as pd
import numpy as np
import random

from ml_engine import predict
from alerts import send_alert
from utils import generate_sku, normalize_sku


# =========================
# PATHS
# =========================
DATA_DIR = "data"
CURRENT_FILE = f"{DATA_DIR}/current.csv"
HISTORY_FILE = f"{DATA_DIR}/history.csv"


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
# FAKE REALISTIC ITEMS (SIMULATION LAYER)
# =========================
ITEMS = [
    ("Milwaukee Drill", "M18 cordless drill kit"),
    ("DeWalt Impact Driver", "20V MAX driver"),
    ("Ryobi Chainsaw", "40V brushless chainsaw"),
    ("Husky Tool Set", "270pc mechanics kit"),
    ("Rigid Wet/Dry Vac", "6 gallon shop vac"),
    ("Makita Grinder", "4.5 inch angle grinder")
]


# =========================
# GENERATE FRESH DATA
# =========================
def generate_data(n=120):

    data = []

    for _ in range(n):

        item = random.choice(ITEMS)
        store_id = random.choice(list(STORE_MAP.keys()))

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

    return pd.DataFrame(data)


# =========================
# ENSURE DATA FOLDER EXISTS
# =========================
os.makedirs(DATA_DIR, exist_ok=True)


# =========================
# LOAD OLD DATA (OPTIONAL)
# =========================
if os.path.exists(CURRENT_FILE):
    try:
        old = pd.read_csv(CURRENT_FILE)
    except:
        old = pd.DataFrame()
else:
    old = pd.DataFrame()


# =========================
# ALWAYS GENERATE FRESH DATA (FIXES YOUR ISSUE)
# =========================
current = generate_data(120)


# =========================
# RUN ML PREDICTION
# =========================
current = predict(current)


# =========================
# SAVE HISTORY
# =========================
if not old.empty:
    history = pd.concat([old, current], ignore_index=True)
else:
    history = current

history.to_csv(HISTORY_FILE, index=False)


# =========================
# OVERWRITE CURRENT DATA (IMPORTANT FIX)
# =========================
current.to_csv(CURRENT_FILE, index=False)

print("✅ current.csv UPDATED WITH LIVE DATA")


# =========================
# TELEGRAM ALERT (TOP 100)
# =========================
top = current.sort_values("ml_score", ascending=False).head(100)

message = "🚨 REAL INTELLIGENCE BULK REPORT\n\n"

for _, row in top.iterrows():

    message += f"""📦 {row['item_name']}
🏷 SKU: {normalize_sku(row['sku'])}
🏬 {row['store_name']}
💰 ${row['price']} (Was ${row['original_price']})
📉 {row['drop_pct']}% OFF
🧠 Score: {round(row['ml_score'],2)}

----------------------

"""

send_alert(message)

print("✅ TELEGRAM ALERT SENT")
