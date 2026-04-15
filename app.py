import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide")

st.title("🧠 Retail Intelligence Dashboard (Failsafe Mode)")

DATA_URL = "https://raw.githubusercontent.com/mattrubi1/retail-ml-system/main/data/current.csv"

# =========================
# SAFE DATA LOADER
# =========================
def load_data():

    try:
        df = pd.read_csv(DATA_URL)
    except:
        df = pd.DataFrame()

    # fallback bootstrap if empty or broken
    if df is None or df.empty:
        df = pd.DataFrame([{
            "sku": 1004,
            "item_name": "Fallback Item",
            "description": "Auto recovery mode active",
            "price": 10,
            "drop_pct": 20,
            "velocity": 1,
            "last_store_location": "1280",
            "ml_score": 50,
            "status": "RECOVERY",
            "image": ""
        }])

    return df


df = load_data()

# =========================
# SAFE CLEANING
# =========================
required_cols = [
    "sku","item_name","description","price",
    "drop_pct","velocity","last_store_location",
    "ml_score","status"
]

for col in required_cols:
    if col not in df.columns:
        df[col] = 0

df["ml_score"] = pd.to_numeric(df["ml_score"], errors="coerce").fillna(0)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

status_list = ["ALL"] + list(df["status"].dropna().unique())
status_filter = st.sidebar.selectbox("Status", status_list)

store_list = ["ALL"] + list(df["last_store_location"].dropna().unique())
store_filter = st.sidebar.selectbox("Store", store_list)

min_score = st.sidebar.slider("Min ML Score", 0, 200, 50)

# APPLY FILTERS
if status_filter != "ALL":
    df = df[df["status"] == status_filter]

if store_filter != "ALL":
    df = df[df["last_store_location"] == store_filter]

df = df[df["ml_score"] >= min_score]

# =========================
# TOP DEALS
# =========================
st.subheader("🔥 Top Deals")

top = df.sort_values("ml_score", ascending=False).head(10)

for _, row in top.iterrows():

    col1, col2 = st.columns([1, 3])

    with col1:
        if "image" in df.columns and row.get("image"):
            st.image(row["image"], use_container_width=True)
        else:
            st.write("📦 No Image")

    with col2:
        st.markdown(f"### {row.get('item_name','Unknown')}")
        st.write(f"📝 {row.get('description','N/A')}")
        st.write(f"🏬 Store: {row.get('last_store_location','N/A')}")
        st.write(f"🏷 SKU: {row.get('sku','N/A')}")
        st.write(f"💰 Price: ${row.get('price',0)}")
        st.write(f"📉 Discount: {row.get('drop_pct',0)}%")
        st.write(f"🧠 ML Score: {round(row.get('ml_score',0),2)}")

        if row.get("sku"):
            st.markdown(f"[🔗 View Product](https://www.homedepot.com/p/{row['sku']})")

    st.divider()

# =========================
# FULL DATA
# =========================
st.subheader("📦 Full Dataset")
st.dataframe(df, use_container_width=True)

# =========================
# ANALYTICS (SAFE)
# =========================
st.subheader("📊 Analytics")

st.bar_chart(df["ml_score"])

if "status" in df.columns:
    st.subheader("📌 Status Breakdown")
    st.bar_chart(df["status"].value_counts())

if "last_store_location" in df.columns:
    st.subheader("🏬 Store Activity")
    st.bar_chart(df["last_store_location"].value_counts())

# =========================
# FINAL HEALTH CHECK
# =========================
st.success("System running in failsafe mode ✔")
