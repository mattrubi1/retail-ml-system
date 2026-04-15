import pandas as pd

def train_model(df):
    return None


def predict(df):

    df = df.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["drop_pct"] = pd.to_numeric(df["drop_pct"], errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce").fillna(0)

    df["ml_score"] = (
        df["drop_pct"] * 1.5 +
        (100 - df["price"]) * 0.3 +
        df["velocity"] * 10
    )

    return df
