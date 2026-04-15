import pandas as pd


def predict(df):

    df = df.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["drop_pct"] = pd.to_numeric(df["drop_pct"], errors="coerce").fillna(0)
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce").fillna(0)
    df["stock_qty"] = pd.to_numeric(df["stock_qty"], errors="coerce").fillna(0)

    df["ml_score"] = (
        df["drop_pct"] * 2.2 +
        df["velocity"] * 7 +
        (25 - df["stock_qty"]) * 1.3 +
        (100 - df["price"]) * 0.15
    )

    return df
