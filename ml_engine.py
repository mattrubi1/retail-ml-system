import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL = None


# =========================
# TRAIN MODEL
# =========================
def train_model(df):

    global MODEL

    df = df.copy()

    if len(df) < 5:
        MODEL = None
        return

    # =========================
    # SYNTHETIC LABEL (BOOTSTRAP LEARNING)
    # =========================
    # High value deal definition (initial training signal)
    df["label"] = np.where(
        (df["drop_pct"] > 40) & (df["price"] < 50),
        1,
        0
    )

    features = ["price", "drop_pct", "velocity", "feature_score"]

    for col in features:
        if col not in df.columns:
            df[col] = 0

    X = df[features]
    y = df["label"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    MODEL = model


# =========================
# PREDICT (FIXED PROBABILITY SCORING)
# =========================
def predict(df):

    global MODEL

    df = df.copy()

    features = ["price", "drop_pct", "velocity", "feature_score"]

    for col in features:
        if col not in df.columns:
            df[col] = 0

    X = df[features]

    # =========================
    # FALLBACK MODE (NO MODEL)
    # =========================
    if MODEL is None:
        # safe bounded score (0–100)
        df["ml_score"] = (df["feature_score"] % 100).clip(0, 100)
        return df

    # =========================
    # REAL ML PROBABILITY OUTPUT
    # =========================
    probs = MODEL.predict_proba(X)[:, 1]

    # normalize to 0–100
    df["ml_score"] = (probs * 100).clip(0, 100)

    return df
