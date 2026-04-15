import pandas as pd
import numpy as np


# =========================
# SAFE ENGINE PROCESSOR
# =========================
def process(df):

    df = df.copy()

    # -------------------------
    # REQUIRED COLUMN SAFETY
    # -------------------------
    required_columns = [
        "sku",
        "item_name",
        "description",
        "price",
        "drop_pct",
        "velocity",
        "last_store_location",
        "ml_score",
        "status"
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = 0

    # -------------------------
    # CLEAN NUMERIC FIELDS
    # -------------------------
    numeric_cols = ["price", "drop_pct", "velocity", "ml_score"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # -------------------------
    # FEATURE ENGINEERING
    # -------------------------
    df["feature_score"] = (
        df["drop_pct"] * 0.5 +
        (100 - df["price"]) * 0.2 +
        df["velocity"] * 10
    )

    # normalize feature_score
    df["feature_score"] = df["feature_score"].fillna(0)

    # -------------------------
    # SAFE SKU STRING FORMAT
    # (DO NOT FORMAT HERE — handled in utils.py)
    # -------------------------
    df["sku"] = df["sku"].astype(str)

    # -------------------------
    # CLEAN TEXT FIELDS
    # -------------------------
    df["item_name"] = df["item_name"].astype(str)
    df["description"] = df["description"].astype(str)

    # -------------------------
    # DEFAULT STATUS
    # -------------------------
    if "status" not in df.columns:
        df["status"] = "live"

    return df
