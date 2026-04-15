import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Retail Intelligence System", layout="wide")

st.title("🧠 Retail Intelligence Dashboard")


# =========================
# DATA PATH
# =========================
DATA_PATH = "data/current.csv"


# =========================
# SAFE DATA LOADER
# =========================
def load_data():

    if not os.path.exists(DATA_PATH):
        return pd.DataFrame([{
            "sku": "0000-000-000",
            "item_name": "No Data Yet",
            "description": "Waiting for pipeline to generate data",
            "price": 0,
            "drop_pct": 0,
            "velocity": 0,
            "last_store_location": "N/A",
            "ml_score": 0
        }])

    try:
        df = pd.read_csv(DATA_PATH)
    except:
        return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame([{
            "sku": "0000-000-000",
            "item_name": "Empty Dataset",
            "description": "No records available",
            "price": 0,
            "drop_pct": 0,
            "velocity": 0,
            "last_store_location": "N/A",
            "ml_score": 0
        }])

    return df


df = load_data()


# =========================
# SAFE COLUMN HANDLING
# =========================
required_columns = [
    "sku",
    "item_name",
    "description",
    "price",
    "drop_pct",
    "velocity",
    "last_store_location",
    "ml_score"
]

for col in required_columns:
    if col not in df.columns:
        df[col] = 0


df["ml_score"] = pd.to_numeric(df["ml_score"], errors="coerce").fillna(0)


# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum ML Score", 0, 100, 0)

df = df[df["ml_score"] >= min_score]


# =========================
# TOP OPPORTUNITIES
# =========================
st.subheader("🔥 Top Opportunities")

top = df.sort_values("ml_score", ascending=False).head(10)

for _, row in top.iterrows():

    col1, col2 = st.columns([1, 3])

    with col1:
        st.write("📦")

    with col2:
        st.markdown(f"### {row.get('item_name', 'Unknown')}")
        st.write(f"🏷 SKU: {row.get('sku', 'N/A')}")
        st.write(f"🏬 Store: {row.get('last_store_location', 'N/A')}")
        st.write(f"💰 Price: ${row.get('price', 0)}")
        st.write(f"📉 Drop: {row.get('drop_pct', 0)}%")
        st.write(f"🧠 ML Score: {round(float(row.get('ml_score', 0)), 2)}")

    st.divider()


# =========================
# FULL DATA TABLE
# =========================
st.subheader("📊 Full Dataset")

st.dataframe(df, use_container_width=True)


# =========================
# BASIC ANALYTICS
# =========================
st.subheader("📈 Analytics")

st.bar_chart(df["ml_score"])


if "last_store_location" in df.columns:
    st.subheader("🏬 Store Activity")
    st.bar_chart(df["last_store_location"].value_counts())


# =========================
# STATUS
# =========================
st.success("System running successfully ✅")
