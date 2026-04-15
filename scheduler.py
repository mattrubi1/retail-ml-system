import os
import pandas as pd

from engine import process
from ml_engine import train_model, predict
from alerts import send_alert
from utils import generate_sku, normalize_sku

DATA_DIR = "data"
CURRENT_FILE = f"{DATA_DIR}/current.csv"
HISTORY_FILE = f"{DATA_DIR}/history.csv"
ALERT_LOG = f"{DATA_DIR}/alerts_sent.csv"


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
# FIX SKU FORMAT SYSTEM-WIDE
# =========================
if not current.empty and "sku" in current.columns:
    current["sku"] = current["sku"].apply(normalize_sku)


# =========================
# BOOTSTRAP DATA IF EMPTY
# =========================
if current.empty:
    current = pd.DataFrame([{
        "sku": generate_sku(),
        "item_name": "Bootstrap Item",
        "description": "System initialized",
        "price": 10,
        "drop_pct": 20,
        "velocity": 1,
        "last_store_location": "1280",
        "ml_score": 50,
        "status": "live"
    }])


# =========================
# ML PIPELINE
# =========================
current = process(current)

train_model(current)
current = predict(current)


# =========================
# ALERT SYSTEM (DEDUPED)
# =========================
sent_skus = set(alerts["sku"]) if not alerts.empty else set()

new_alerts = []

for _, row in current.iterrows():

    sku = normalize_sku(row["sku"])
    score = row.get("ml_score", 0)

    if score > 80 and sku not in sent_skus:

        send_alert(f"""🚨 HOME DEPOT INTELLIGENCE ALERT

📦 {row['item_name']}
🏷 SKU: {sku}
🏬 Store: {row['last_store_location']}
💰 Price: ${row['price']}
📉 Drop: {row['drop_pct']}%
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

print("✅ SYSTEM RUN COMPLETE (SKU FIXED)")
