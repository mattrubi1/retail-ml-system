import streamlit as st
import pandas as pd

st.title("🧠 Retail ML System")

url = "https://raw.githubusercontent.com/YOUR_USERNAME/retail-ml-system/main/data.csv"
df = pd.read_csv(url)

st.subheader("All Items")
st.dataframe(df)

st.subheader("Top Opportunities")

st.dataframe(
    df.sort_values("ml_score", ascending=False)[
        ["item_name", "description", "last_store_location", "price", "ml_score"]
    ]
)
