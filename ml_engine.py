import pandas as pd


# =========================
# "TRAIN MODEL" (NO-OP SAFE)
# =========================
def train_model(df):
    # No training needed (lightweight system)
    return None


# =========================
# LIGHTWEIGHT ML PREDICTION
# =========================
def predict(df):

    df = df.copy()

    # ensure numeric
    df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
    df["drop_pct"] = pd.to_numeric(df.get("drop_pct", 0), errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df.get("velocity", 0), errors="coerce").fillna(0)

    # =========================
    # SIMPLE ML SCORING MODEL
    # =========================
    df["ml_score"] = (
        df["drop_pct"] * 1.5 +     # bigger drop = higher score
        (100 - df["price"]) * 0.3 + # cheaper = better
        df["velocity"] * 10        # faster movement = better
    )

    # normalize (0–100 range)
    df["ml_score"] = df["ml_score"].clip(lower=0)

    return df
