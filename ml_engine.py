import joblib
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = "model.pkl"

def train_model(df):
    df["target"] = df["drop_pct"] * 0.6 + df["velocity"] * 20
    X = df[["drop_pct", "velocity"]]
    y = df["target"]

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except:
        return None

def predict(df):
    model = load_model()
    if model is None:
        model = train_model(df)

    df["ml_score"] = model.predict(df[["drop_pct", "velocity"]])
    return df
