import pandas as pd


REQUIRED_COLUMNS = [
    "price",
    "drop_pct",
    "velocity",
    "stock_qty"
]


def ensure_columns(df):
    """
    Ensure all required columns exist.
    If missing, create with safe defaults.
    """

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    return df


def clean_numeric(df):
    """
    Convert all numeric columns safely
    """

    for col in REQUIRED_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def predict(df):

    df = df.copy()

    # 🔒 Ensure schema is safe
    df = ensure_columns(df)

    # 🔒 Clean numeric values
    df = clean_numeric(df)

    # 🔥 ML scoring formula (stable + tunable)
    df["ml_score"] = (
        df["drop_pct"] * 2.5 +        # discount importance
        df["velocity"] * 6.0 +        # demand
        (30 - df["stock_qty"]) * 1.2 +  # scarcity
        (150 - df["price"]) * 0.2     # cheaper = better
    )

    # 🔒 Prevent negatives / weird values
    df["ml_score"] = df["ml_score"].clip(lower=0)

    return df
