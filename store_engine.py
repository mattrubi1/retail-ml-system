import pandas as pd

def attach_store_data(df, stores_df):

    # simulate mapping (in real system this comes from API/scraper)
    df = df.copy()

    df = df.merge(
        stores_df,
        how="left",
        left_on="last_store_location",
        right_on="store_id"
    )

    return df
