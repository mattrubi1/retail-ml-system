import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Retail Full Inventory View", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "current.csv")

df = pd.read_csv(DATA_PATH)

# numeric safety
df["ml_score"] = pd.to_numeric(df.get("ml_score", 0), errors="coerce").fillna(0)

st.title("🟢 Full Retail Intelligence System (20%+ All Items)")

# =========================
# FILTERS
# =========================
st.sidebar.header("Filters")

min_discount = st.sidebar.slider("Minimum Discount %", 20, 80, 20)

df = df[df["drop_pct"] >= min_discount]

# =========================
# FULL TABLE VIEW
# =========================
st.subheader("📦 All Discounted Items")

st.dataframe(df.sort_values("drop_pct", ascending=False), width="stretch")

# =========================
# DISCOUNT ANALYTICS
# =========================
st.subheader("📉 Discount Distribution")

st.bar_chart(df["drop_pct"])

# =========================
# STORE VIEW
# =========================
st.subheader("🏬 Store Breakdown")

st.bar_chart(df["store_name"].value_counts())

# =========================
# SCORE VIEW (optional but useful)
# =========================
if "gpt_score" in df.columns:
    st.subheader("🧠 GPT Score Distribution")
    st.bar_chart(df["gpt_score"])

st.success("Full Inventory Mode Active ✅")
