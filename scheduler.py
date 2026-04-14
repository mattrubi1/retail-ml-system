import pandas as pd
from engine import process
from ml_engine import predict
from db import write_rows
from alerts import send_alert

df = pd.read_csv("data.csv")

df = process(df)
df = predict(df)

write_rows(df.to_dict(orient="records"))

for _, row in df.iterrows():
    if row["ml_score"] > 80:
        send_alert(f"🚨 ALERT SKU {row['sku']} Score {row['ml_score']}")
