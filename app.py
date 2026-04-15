import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Retail Intelligence System", layout="wide")
st.title("🧠 Retail Intelligence Dashboard")


# =========================
# ABSOLUTE PATH (CRITICAL FIX)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "current.csv")


# =========================
# LOAD DATA
# =========================
def load_data():

    if not os.path.exists(DATA_PATH):
        st.error("❌ No data file found. Scheduler has not run.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

    if df.empty:
        st.warning("⚠️ Data file is empty")
        return df

    return df


df = load_data()

if df.empty:
    st.stop()


# =========================
# CLEAN DATA
# =========================
df["ml_score"] = pd.to_numeric(df["ml_score"], errors="coerce").fillna(0)


# =========================
# FILTER
# =========================
st.sidebar.header("Filters")
min_score = st.sidebar.slider("Minimum ML Score", 0, 100, 0)

df = df[df["ml_score"] >= min_score]


# =========================
# TOP ITEMS
# =========================
st.subheader("🔥 Top Opportunities")

top = df.sort_values("ml_score", ascending=False).head(20)

for _, row in top.iterrows():
    st.markdown(f"""
### 📦 {row['item_name']}
- 🏷 SKU: {row['sku']}
- 🏬 Store: {row['store_name']}
- 📍 ID: {row['last_store_location']}
- 💰 ${row['price']} (Was ${row['original_price']})
- 📉 {row['drop_pct']}%
- 📦 Stock: {row['stock_qty']}
- 🧠 Score: {row['ml_score']}
""")
    st.divider()


# =========================
# TABLE
# =========================
st.subheader("📊 Full Dataset")
st.dataframe(df, use_container_width=True)


# =========================
# CHART
# =========================
st.subheader("📈 ML Score Distribution")
st.bar_chart(df["ml_score"])


st.success("✅ Live data loaded")
