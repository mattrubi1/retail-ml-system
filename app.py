import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("🧠 Real Store Intelligence System")

# =========================
# LOAD DATA
# =========================
url = "https://raw.githubusercontent.com/mattrubi1/retail-ml-system/main/data/current.csv"
df = pd.read_csv(url)

if df.empty:
    st.warning("No data available yet.")
    st.stop()

# =========================
# CLEAN DATA
# =========================
df.columns = df.columns.str.strip()

if "ml_score" in df.columns:
    df["ml_score"] = pd.to_numeric(df["ml_score"], errors="coerce").fillna(0)
else:
    df["ml_score"] = 0

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

status_options = ["ALL"]
if "status" in df.columns:
    status_options += list(df["status"].dropna().unique())

status_filter = st.sidebar.selectbox("Item Status", status_options)

stores = []
if "last_store_location" in df.columns:
    stores = list(df["last_store_location"].dropna().unique())

store_filter = st.sidebar.selectbox("Store", ["ALL"] + stores)

min_score = st.sidebar.slider("Minimum ML Score", 0, 200, 50)

# APPLY FILTERS
if status_filter != "ALL" and "status" in df.columns:
    df = df[df["status"] == status_filter]

if store_filter != "ALL":
    df = df[df["last_store_location"] == store_filter]

df = df[df["ml_score"] >= min_score]

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🔥 Top Deals", "📦 Dataset", "📊 Analytics"])

# =========================
# TAB 1 - TOP DEALS
# =========================
with tab1:

    st.subheader("🔥 High Value Opportunities")

    top_df = df.sort_values("ml_score", ascending=False).head(10)

    for _, row in top_df.iterrows():

        col1, col2 = st.columns([1, 3])

        # IMAGE
        with col1:
            if "image" in df.columns and pd.notna(row.get("image")):
                st.image(row["image"], use_container_width=True)
            else:
                st.write("📦 No Image")

        # INFO
        with col2:
            st.markdown(f"### {row.get('item_name','Unknown Item')}")
            st.write(f"📝 {row.get('description','N/A')}")
            st.write(f"🏬 Store: {row.get('last_store_location','N/A')}")
            st.write(f"🏷 SKU: {row.get('sku','N/A')}")
            st.write(f"💰 Price: ${row.get('price',0)}")
            st.write(f"📉 Discount: {row.get('drop_pct',0)}%")
            st.write(f"🧠 ML Score: {round(row.get('ml_score',0),2)}")
            st.write(f"📌 Status: {row.get('status','UNKNOWN')}")

            if "sku" in row:
                st.markdown(f"[🔗 View Product](https://www.homedepot.com/p/{row['sku']})")

        st.divider()

# =========================
# TAB 2 - DATASET
# =========================
with tab2:

    st.subheader("📦 Full Intelligence Dataset")
    st.dataframe(df, use_container_width=True)

# =========================
# TAB 3 - ANALYTICS
# =========================
with tab3:

    st.subheader("📊 ML Score Distribution")
    st.bar_chart(df["ml_score"])

    if "last_store_location" in df.columns:
        st.subheader("🏬 Activity by Store")
        st.bar_chart(df["last_store_location"].value_counts())

    if "status" in df.columns:
        st.subheader("📌 Item Status Breakdown")
        st.bar_chart(df["status"].value_counts())

# =========================
# MAP VIEW (REAL + SAFE)
# =========================
st.subheader("🗺 Store Intelligence Map")

if "lat" in df.columns and "lon" in df.columns:

    map_df = df.dropna(subset=["lat", "lon"])[["lat", "lon"]].copy()
    map_df.columns = ["latitude", "longitude"]

    if not map_df.empty:
        st.map(map_df)
    else:
        st.warning("No valid coordinates available for map.")
else:
    st.info("Map unavailable: store coordinates not loaded yet.")

# =========================
# SYSTEM INSIGHTS
# =========================
st.subheader("🧠 System Insights")

if len(df) > 0:

    st.write("🔥 Top 5 Highest Value Items")
    st.dataframe(df.sort_values("ml_score", ascending=False).head(5))

    if "status" in df.columns:
        st.write("🆕 New Items Detected")
        st.dataframe(df[df["status"] == "NEW"].head(10))
