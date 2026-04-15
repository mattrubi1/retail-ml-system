import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Retail AI Intelligence", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "current.csv")

df = pd.read_csv(DATA_PATH)

df["ml_score"] = pd.to_numeric(df.get("ml_score", 0), errors="coerce").fillna(0)

if "ai_score" not in df.columns:
    df["ai_score"] = 0

st.title("🧠 Retail AI Deal Engine")

# =========================
# FILTERS
# =========================
st.sidebar.header("Filters")
min_score = st.sidebar.slider("Min ML Score", 0, 100, 80)

df = df[df["ml_score"] >= min_score]

# =========================
# TOP DEALS
# =========================
st.subheader("🔥 Elite Deals")

top = df.sort_values("ml_score", ascending=False).head(20)

st.dataframe(top, width="stretch")

# =========================
# ML + AI COMPARISON
# =========================
st.subheader("📊 Score Comparison")

st.bar_chart(top[["ml_score", "ai_score"]])

# =========================
# STORE VIEW
# =========================
st.subheader("🏬 Store Activity")

st.bar_chart(df["store_name"].value_counts())

st.success("AI Deal Engine Active 🤖")
