import pandas as pd
import numpy as np


def train_model(df):
    return None


def predict(df):

    df = df.copy()

    # =========================
    # SAFE CLEANING
    # =========================
    df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
    df["original_price"] = pd.to_numeric(df.get("original_price", df["price"]), errors="coerce").fillna(df["price"])
    df["drop_pct"] = pd.to_numeric(df.get("drop_pct", 0), errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df.get("velocity", 0), errors="coerce").fillna(0)

    # =========================
    # NORMALIZATION (0–1)
    # =========================
    discount = np.clip(df["drop_pct"] / 100, 0, 1)
    velocity = np.clip(df["velocity"] / 10, 0, 1)

    price_efficiency = 1 - np.clip(
        df["price"] / (df["original_price"] + 1),
        0,
        1
    )

    # =========================
    # SCORE ENGINE (0–100 SCALE)
    # =========================
    raw_score = (
        discount * 0.5 +
        velocity * 0.3 +
        price_efficiency * 0.2
    )

    df["ml_score"] = (raw_score * 100).round(2)

    return df
