import pandas as pd


REQUIRED_COLUMNS = [
    "price",
    "drop_pct",
    "velocity",
    "stock_qty"
]


def ensure_columns(df):
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    return df


def clean_numeric(df):
    for col in REQUIRED_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


def predict(df):

    df = df.copy()

    df = ensure_columns(df)
    df = clean_numeric(df)

    df["ml_score"] = (
        df["drop_pct"] * 5 +
        df["velocity"] * 10 +
        (40 - df["stock_qty"]) * 2 +
        (200 - df["price"]) * 0.3
    )

    df["ml_score"] = df["ml_score"].clip(lower=0)

    return df
