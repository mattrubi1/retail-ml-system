import pandas as pd
import numpy as np

# =========================
# SAFE PROCESSING ENGINE
# =========================
def process(df):

    if df is None:
        return pd.DataFrame()

    df = df.copy()

    # =========================
    # REQUIRED COLUMNS (AUTO FIX)
    # =========================
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

    # =========================
    # TYPE SAFETY
    # =========================
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["drop_pct"] = pd.to_numeric(df["drop_pct"], errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce").fillna(0)

    # =========================
    # FEATURE ENGINEERING
    # =========================

    # value score (higher drop + lower price = better deal)
    df["value_score"] = (df["drop_pct"] * 2) + (100 - df["price"])

    # velocity boost (items moving faster are more important)
    df["velocity_score"] = df["velocity"] * 10

    # scarcity factor (simulated - can be replaced later with real inventory)
    df["scarcity_score"] = np.where(df["price"] < 20, 20, 5)

    # =========================
    # FINAL FEATURE SET
    # =========================
    df["feature_score"] = (
        df["value_score"] +
        df["velocity_score"] +
        df["scarcity_score"]
    )

    return df


# =========================
# OPTIONAL LEGACY SUPPORT
# =========================
def build_features(df):
    return process(df)
