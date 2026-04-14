import pandas as pd
from engine import process
from ml_engine import predict
from alerts import send_alert

df = pd.read_csv("data.csv")

df = process(df)
df = predict(df)

# SAVE BACK TO CSV (this is now your database)
df.to_csv("data.csv", index=False)

# TELEGRAM ALERTS
for _, row in df.iterrows():
    if row["ml_score"] > 80:
        send_alert(f"🚨 ALERT SKU {row['sku']} Score {row['ml_score']}")

print("Updated system")
