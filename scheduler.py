import os
import pandas as pd
from engine import process
from ml_engine import train_model, predict
from alerts import send_alert

DATA_DIR = "data"
CURRENT_FILE = f"{DATA_DIR}/current.csv"
HISTORY_FILE = f"{DATA_DIR}/history.csv"
ALERT_LOG = f"{DATA_DIR}/alerts_sent.csv"


# =========================
# SAFE FILE INIT
# =========================
def ensure_files():

    os.makedirs(DATA_DIR, exist_ok=True)

    for file in [CURRENT_FILE, HISTORY_FILE, ALERT_LOG]:
        if not os.path.exists(file):
            pd.DataFrame(columns=[
                "sku","item_name","price","ml_score"
            ]).to_csv(file, index=False)


def load(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()


ensure_files()

current = load(CURRENT_FILE)
history = load(HISTORY_FILE)
alerts_log = load(ALERT_LOG)


# =========================
# REMOVE TEST DATA PROBLEM
# =========================
# Only process if dataset has more than bootstrap size
if len(current) <= 1:
    print("⚠️ Waiting for real data... skipping alerts")
    exit()


# =========================
# ENGINE + ML
# =========================
current = process(current)
train_model(current)
current = predict(current)


# =========================
# ALERT DEDUPLICATION LOGIC
# =========================
sent_skus = set(alerts_log["sku"].astype(str)) if not alerts_log.empty else set()

new_alerts = []

for _, row in current.iterrows():

    sku = str(row.get("sku"))
    score = row.get("ml_score", 0)

    # 🔥 ONLY HIGH VALUE + NOT PREVIOUSLY SENT
    if score > 80 and sku not in sent_skus:

        message = f"""🚨 HOME DEPOT INTELLIGENCE ALERT

📦 Item: {row.get('item_name')}
🏷 SKU: {sku}
🏬 Store: {row.get('last_store_location')}
💰 Price: ${row.get('price')}
🧠 Score: {round(score,2)}
"""

        send_alert(message)

        new_alerts.append({
            "sku": sku,
            "item_name": row.get("item_name"),
            "ml_score": score
        })


# =========================
# SAVE ALERT HISTORY
# =========================
if new_alerts:
    alerts_log = pd.concat([alerts_log, pd.DataFrame(new_alerts)], ignore_index=True)
    alerts_log.to_csv(ALERT_LOG, index=False)


# =========================
# UPDATE DATA
# =========================
current.to_csv(CURRENT_FILE, index=False)
history = pd.concat([history, current], ignore_index=True)
history.to_csv(HISTORY_FILE, index=False)

print("✅ Alerts fixed — no more test spam")
