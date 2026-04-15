import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL = None


def train_model(df):

    global MODEL

    df = df.copy()

    if len(df) < 5:
        MODEL = None
        return

    # synthetic label (initial learning signal)
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


def predict(df):

    global MODEL

    df = df.copy()

    features = ["price", "drop_pct", "velocity", "feature_score"]

    for col in features:
        if col not in df.columns:
            df[col] = 0

    X = df[features]

    if MODEL is None:
        df["ml_score"] = df["feature_score"]
        return df

    df["ml_score"] = MODEL.predict_proba(X)[:, 1] * 100

    return df
