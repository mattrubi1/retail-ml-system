import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Retail Intelligence System", layout="wide")
st.title("🧠 Retail Intelligence Dashboard")

# =========================
# PATH FIX (CRITICAL)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "current.csv")

# =========================
# LOAD DATA
# =========================
def load_data():

    if not os.path.exists(DATA_PATH):
        st.error("No data found")
        return pd.DataFrame()

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

    if df.empty:
        st.warning("Dataset is empty")
        return df

    return df


df = load_data()

if df.empty:
    st.stop()

# =========================
# CLEAN DATA
# =========================
df["ml_score"] = pd.to_numeric(df.get("ml_score", 0), errors="coerce").fillna(0)
df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
df["original_price"] = pd.to_numeric(df.get("original_price", 0), errors="coerce").fillna(0)
df["drop_pct"] = pd.to_numeric(df.get("drop_pct", 0), errors="coerce").fillna(0)
df["stock_qty"] = pd.to_numeric(df.get("stock_qty", 0), errors="coerce").fillna(0)

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum ML Score", 0, 100, 0)

df = df[df["ml_score"] >= min_score]

# =========================
# TOP DEALS
# =========================
st.subheader("🔥 Top Opportunities")

top = df.sort_values("ml_score", ascending=False).head(20)

for _, row in top.iterrows():
    st.markdown(f"""
### 📦 {row.get('item_name', 'Unknown')}
- 🏷 SKU: {row.get('sku', 'N/A')}
- 🏬 {row.get('store_name', 'Unknown Store')}
- 💰 ${row.get('price', 0)} (Was ${row.get('original_price', 0)})
- 📉 {row.get('drop_pct', 0)}%
- 📦 Stock: {row.get('stock_qty', 0)}
- 🧠 Score: {row.get('ml_score', 0)}
""")
    st.divider()

# =========================
# FULL DATA TABLE (FIXED)
# =========================
st.subheader("📊 Full Dataset")

st.dataframe(df, width="stretch")

# =========================
# ANALYTICS
# =========================
st.subheader("📈 ML Score Distribution")

st.bar_chart(df["ml_score"])

# =========================
# STORE BREAKDOWN
# =========================
if "store_name" in df.columns:
    st.subheader("🏬 Store Activity")
    st.bar_chart(df["store_name"].value_counts())

# =========================
# STATUS
# =========================
st.success("✅ Live data running")
