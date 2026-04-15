import pandas as pd
import numpy as np

def process(df):

    if df is None:
        return pd.DataFrame()

    df = df.copy()

    required_columns = [
        "sku",
        "item_name",
        "description",
        "price",
        "drop_pct",
        "velocity",
        "last_store_location"
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = 0

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["drop_pct"] = pd.to_numeric(df["drop_pct"], errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce").fillna(0)

    df["value_score"] = (df["drop_pct"] * 2) + (100 - df["price"])
    df["velocity_score"] = df["velocity"] * 10
    df["scarcity_score"] = np.where(df["price"] < 20, 20, 5)

    df["feature_score"] = (
        df["value_score"] +
        df["velocity_score"] +
        df["scarcity_score"]
    )

    return df
