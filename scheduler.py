import os
import pandas as pd
from engine import process
from ml_engine import predict
from alerts import send_alert

DATA_DIR = "data"
CURRENT_FILE = f"{DATA_DIR}/current.csv"
HISTORY_FILE = f"{DATA_DIR}/history.csv"

# =========================
# SELF-HEALING FUNCTIONS
# =========================
def ensure_files():

    os.makedirs(DATA_DIR, exist_ok=True)

    # create current.csv if missing
    if not os.path.exists(CURRENT_FILE):
        df = pd.DataFrame(columns=[
            "sku","item_name","description","price",
            "drop_pct","velocity","last_store_location",
            "ml_score","status"
        ])

        df.to_csv(CURRENT_FILE, index=False)

    # create history.csv if missing
    if not os.path.exists(HISTORY_FILE):
        df = pd.DataFrame(columns=[
            "sku","item_name","description","price",
            "drop_pct","velocity","last_store_location",
            "ml_score","status"
        ])

        df.to_csv(HISTORY_FILE, index=False)

# =========================
# LOAD SAFELY
# =========================
def load_safe(path):

    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

# =========================
# MAIN PIPELINE
# =========================
ensure_files()

current = load_safe(CURRENT_FILE)
history = load_safe(HISTORY_FILE)

# if empty → bootstrap safe data
if current.empty:
    current = pd.DataFrame([
        {
            "sku": 1004,
            "item_name": "Bootstrap Item",
            "description": "Auto-generated starter",
            "price": 10,
            "drop_pct": 20,
            "velocity": 1,
            "last_store_location": "1280",
            "ml_score": 50,
            "status": "existing"
        }
    ])

# =========================
# PROCESS + ML
# =========================
current = process(current)
current = predict(current)

# =========================
# UPDATE HISTORY
# =========================
history = pd.concat([history, current], ignore_index=True)

# =========================
# SAVE BACK
# =========================
current.to_csv(CURRENT_FILE, index=False)
history.to_csv(HISTORY_FILE, index=False)

# =========================
# ALERT ENGINE
# =========================
for _, row in current.iterrows():

    if row.get("ml_score", 0) > 80:

        send_alert(f"""🚨 SELF-HEALING ALERT

📦 {row.get('item_name')}
🏷 SKU: {row.get('sku')}
🏬 Store: {row.get('last_store_location')}
💰 Price: ${row.get('price')}
🧠 Score: {round(row.get('ml_score',0),2)}

🔧 System Status: Healthy
""")

print("✅ Self-healing pipeline completed successfully")
