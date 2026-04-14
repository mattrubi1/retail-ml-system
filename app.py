import streamlit as st
from db import read_data

st.title("Retail ML System")

df = read_data()

st.dataframe(df)

st.subheader("Top Items")
st.dataframe(df.sort_values("ml_score", ascending=False))
