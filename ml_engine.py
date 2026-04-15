import pandas as pd
import numpy as np


def train_model(df):
    return None


def predict(df):

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
    df["original_price"] = pd.to_numeric(df.get("original_price", df["price"]), errors="coerce").fillna(df["price"])
    df["drop_pct"] = pd.to_numeric(df.get("drop_pct", 0), errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df.get("velocity", 0), errors="coerce").fillna(0)

    # NEW: stock field
    df["stock_qty"] = pd.to_numeric(df.get("stock_qty", 0), errors="coerce").fillna(0)

    # =========================
    # NORMALIZATION
    # =========================
    discount = np.clip(df["drop_pct"] / 100, 0, 1)
    velocity = np.clip(df["velocity"] / 10, 0, 1)

    price_efficiency = 1 - np.clip(
        df["price"] / (df["original_price"] + 1),
        0,
        1
    )

    # STOCK INTELLIGENCE (LOW STOCK = HIGHER SCORE)
    stock_signal = 1 - np.clip(df["stock_qty"] / 25, 0, 1)

    # =========================
    # FINAL SCORE (0–100)
    # =========================
    raw_score = (
        discount * 0.45 +
        velocity * 0.25 +
        price_efficiency * 0.20 +
        stock_signal * 0.10
    )

    df["ml_score"] = (raw_score * 100).round(2)

    return df
