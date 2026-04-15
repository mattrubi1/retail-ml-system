import os
import pandas as pd

from engine import process
from ml_engine import train_model, predict
from alerts import send_alert

DATA_DIR = "data"
CURRENT_FILE = f"{DATA_DIR}/current.csv"
HISTORY_FILE = f"{DATA_DIR}/history.csv"


def ensure_files():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(CURRENT_FILE):
        pd.DataFrame(columns=[
            "sku","item_name","description","price",
            "drop_pct","velocity","last_store_location",
            "ml_score","status"
        ]).to_csv(CURRENT_FILE, index=False)

    if not os.path.exists(HISTORY_FILE):
        pd.DataFrame(columns=[
            "sku","item_name","description","price",
            "drop_pct","velocity","last_store_location",
            "ml_score","status"
        ]).to_csv(HISTORY_FILE, index=False)


def load(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()


ensure_files()

current = load(CURRENT_FILE)
history = load(HISTORY_FILE)

# bootstrap if empty
if current.empty:
    current = pd.DataFrame([{
        "sku": 1004,
        "item_name": "Bootstrap Item",
        "description": "Starter data",
        "price": 10,
        "drop_pct": 20,
        "velocity": 1,
        "last_store_location": "1280",
        "ml_score": 50,
        "status": "existing"
    }])

# feature engineering
current = process(current)

# train ML model
train_model(current)

# predict
current = predict(current)

# update history
history = pd.concat([history, current], ignore_index=True)

current.to_csv(CURRENT_FILE, index=False)
history.to_csv(HISTORY_FILE, index=False)

# alerts
for _, row in current.iterrows():

    if row.get("ml_score", 0) > 80:

        send_alert(f"""🚨 HOME DEPOT INTELLIGENCE ALERT

📦 {row.get('item_name')}
🏷 SKU: {row.get('sku')}
🏬 Store: {row.get('last_store_location')}
💰 Price: ${row.get('price')}
🧠 Score: {round(row.get('ml_score',0),2)}

⚡ ML DETECTED HIGH VALUE ITEM
""")

print("ML pipeline complete")
