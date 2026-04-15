import pandas as pd
import numpy as np


# =========================
# TRAIN MODEL (placeholder for future upgrade)
# =========================
def train_model(df):
    """
    Placeholder for future ML training system.
    Not used yet in current pipeline.
    """
    return None


# =========================
# PREDICTION ENGINE
# =========================
def predict(df):

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
    df["drop_pct"] = pd.to_numeric(df.get("drop_pct", 0), errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df.get("velocity", 0), errors="coerce").fillna(0)

    # Ensure original price exists
    if "original_price" not in df.columns:
        df["original_price"] = df["price"]

    df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce").fillna(df["price"])

    # =========================
    # FEATURE ENGINEERING
    # =========================

    # Normalize signals (0–1 range)
    discount_signal = np.clip(df["drop_pct"] / 100, 0, 1)
    velocity_signal = np.clip(df["velocity"] / 10, 0, 1)

    # Price attractiveness (lower price vs original is better)
    price_ratio = df["price"] / (df["original_price"] + 1)
    price_signal = 1 - np.clip(price_ratio, 0, 1)

    # =========================
    # FINAL ML SCORE
    # =========================
    df["ml_score"] = (
        discount_signal * 50 +
        velocity_signal * 30 +
        price_signal * 20
    ) * 10

    # =========================
    # SAFETY CLEANUP
    # =========================
    df["ml_score"] = df["ml_score"].fillna(0)
    df["ml_score"] = df["ml_score"].round(2)

    return df
