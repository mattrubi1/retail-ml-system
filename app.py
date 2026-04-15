import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Retail Intelligence System", layout="wide")

st.title("🧠 Retail Intelligence Dashboard")


# =========================
# DATA PATH (SINGLE SOURCE OF TRUTH)
# =========================
DATA_PATH = "data/current.csv"


# =========================
# SAFE DATA LOADER
# =========================
def load_data():

    # If file doesn't exist yet
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame([{
            "sku": "0000-000-000",
            "item_name": "No Data Yet",
            "description": "Scheduler has not generated data",
            "price": 0,
            "original_price": 0,
            "drop_pct": 0,
            "velocity": 0,
            "store_name": "N/A",
            "last_store_location": "N/A",
            "ml_score": 0
        }])

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

    if df.empty:
        return pd.DataFrame([{
            "sku": "0000-000-000",
            "item_name": "Empty Dataset",
            "description": "No records available",
            "price": 0,
            "original_price": 0,
            "drop_pct": 0,
            "velocity": 0,
            "store_name": "N/A",
            "last_store_location": "N/A",
            "ml_score": 0
        }])

    return df


df = load_data()


# =========================
# ENSURE REQUIRED COLUMNS EXIST
# =========================
required_columns = [
    "sku",
    "item_name",
    "description",
    "price",
    "original_price",
    "drop_pct",
    "velocity",
    "store_name",
    "last_store_location",
    "ml_score"
]

for col in required_columns:
    if col not in df.columns:
        df[col] = 0


# Convert numeric safely
df["ml_score"] = pd.to_numeric(df["ml_score"], errors="coerce").fillna(0)
df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
df["drop_pct"] = pd.to_numeric(df["drop_pct"], errors="coerce").fillna(0)


# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum ML Score", 0, 1000, 0)

df = df[df["ml_score"] >= min_score]


# =========================
# TOP OPPORTUNITIES
# =========================
st.subheader("🔥 Top Opportunities")

top = df.sort_values("ml_score", ascending=False).head(20)

if top.empty:
    st.warning("No data available")
else:
    for _, row in top.iterrows():

        st.markdown(f"""
### 📦 {row.get('item_name', 'Unknown')}
- 🏷 SKU: {row.get('sku', 'N/A')}
- 🏬 Store: {row.get('store_name', 'N/A')}
- 📍 Location ID: {row.get('last_store_location', 'N/A')}
- 💰 Price: ${row.get('price', 0)} (Was ${row.get('original_price', 0)})
- 📉 Drop: {row.get('drop_pct', 0)}%
- 🧠 ML Score: {round(float(row.get('ml_score', 0)), 2)}
""")

        st.divider()


# =========================
# FULL TABLE
# =========================
st.subheader("📊 Full Dataset")

st.dataframe(df, use_container_width=True)


# =========================
# ANALYTICS
# =========================
st.subheader("📈 ML Score Distribution")

st.bar_chart(df["ml_score"])


# =========================
# STORE VIEW
# =========================
if "store_name" in df.columns:
    st.subheader("🏬 Store Activity")
    st.bar_chart(df["store_name"].value_counts())


# =========================
# STATUS
# =========================
st.success("System running successfully ✅")
