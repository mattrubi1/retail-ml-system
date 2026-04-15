import pandas as pd

def process(df):

    df = df.copy()

    # ensure numeric
    for col in ["price", "drop_pct", "velocity"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    # ensure original price exists
    if "original_price" not in df.columns:
        df["original_price"] = df["price"] * 1.2

    # simple feature score
    df["feature_score"] = (
        df["drop_pct"] * 0.5 +
        (100 - df["price"]) * 0.2 +
        df["velocity"] * 10
    )

    return df
