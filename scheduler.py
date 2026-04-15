import pandas as pd
from engine import process
from ml_engine import predict
from alerts import send_alert
from hd_api import get_product_data

def format_sku(sku):
    sku = str(sku)
    return f"{sku[:4]}-{sku[4:7]}-{sku[7:]}" if len(sku) >= 10 else sku


df = pd.read_csv("data.csv")

# 🔥 FETCH REAL DATA
for i, row in df.iterrows():

    product = get_product_data(row["sku"])

    df.at[i, "item_name"] = product["item_name"]
    df.at[i, "price"] = product["price"]

    # Simulate discount logic
    df.at[i, "drop_pct"] = round((100 - product["price"]), 2)

# Process + ML
df = process(df)
df = predict(df)

df.to_csv("data.csv", index=False)

# ALERTS
for _, row in df.iterrows():

    if row["ml_score"] > 80:

        message = f"""🚨 HOME DEPOT LIVE ALERT

📦 {row['item_name']}
🏬 {row['last_store_location']}
🏷 SKU: {format_sku(row['sku'])}
💰 Price: ${row['price']}
📊 Score: {round(row['ml_score'], 2)}

🔗 https://www.homedepot.com/p/{row['sku']}
"""

        send_alert(message)

print("Live Home Depot data running")
