from datetime import datetime

def process(df):
    df["timestamp"] = datetime.now().isoformat()
    return df
