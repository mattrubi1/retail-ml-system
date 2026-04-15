import pandas as pd
from ml_engine import predict
from alerts import send_alert

# load datasets
current = pd.read_csv("data/current.csv")
history = pd.read_csv("data/history.csv")

# store snapshot history
current.to_csv("data/history.csv", mode="a", header=False, index=False)

# ML scoring
current = predict(current)

# detect removed items
removed = set(history["sku"]) - set(current["sku"])

# detect new items
new = set(current["sku"]) - set(history["sku"])

# update history tracking flags
current["status"] = "existing"
current.loc[current["sku"].isin(new), "status"] = "NEW"
current.loc[current["sku"].isin(removed), "status"] = "REMOVED"

# save
current.to_csv("data/current.csv", index=False)

# alerts
for _, row in current.iterrows():

    if row["ml_score"] > 80:

        send_alert(f"""🚨 STORE INTELLIGENCE ALERT

📦 {row['item_name']}
🏬 Store: {row['last_store_location']}
🏷 SKU: {row['sku']}
📊 Score: {round(row['ml_score'],2)}
📌 Status: {row['status']}
""")

print("Store intelligence system running")
