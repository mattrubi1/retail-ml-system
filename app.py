import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Retail Intelligence System", layout="wide")
st.title("🧠 Retail Intelligence Dashboard")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "current.csv")


def load_data():

    if not os.path.exists(DATA_PATH):
        st.error("No data found")
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        st.warning("Empty dataset")
        return df

    return df


df = load_data()

if df.empty:
    st.stop()

df["ml_score"] = pd.to_numeric(df["ml_score"], errors="coerce").fillna(0)

st.sidebar.header("Filters")
min_score = st.sidebar.slider("Minimum ML Score", 0, 100, 0)

df = df[df["ml_score"] >= min_score]

st.subheader("🔥 Top Opportunities")

top = df.sort_values("ml_score", ascending=False).head(20)

for _, row in top.iterrows():
    st.markdown(f"""
### 📦 {row['item_name']}
- 🏷 SKU: {row['sku']}
- 🏬 {row['store_name']}
- 💰 ${row['price']} (Was ${row['original_price']})
- 📉 {row['drop_pct']}%
- 📦 Stock: {row['stock_qty']}
- 🧠 Score: {row['ml_score']}
""")
    st.divider()

st.dataframe(df, use_container_width=True)
st.bar_chart(df["ml_score"])

st.success("✅ Live data running")
