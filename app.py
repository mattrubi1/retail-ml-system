import streamlit as st
import pandas as pd

st.title("Retail ML System")

# LOAD DATA FROM GITHUB RAW FILE
url = "https://raw.githubusercontent.com/YOUR_USERNAME/retail-ml-system/main/data.csv"

df = pd.read_csv(url)

st.dataframe(df)

st.subheader("Top Items")
st.dataframe(df.sort_values("ml_score", ascending=False))

