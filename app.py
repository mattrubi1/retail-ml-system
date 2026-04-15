import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="GPT Deal Engine", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "current.csv")

df = pd.read_csv(DATA_PATH)

st.title("🤖 GPT-Level Retail Intelligence System")

if "gpt_score" not in df.columns:
    st.warning("Run scheduler first")
    st.stop()

df = df[df["gpt_score"] >= 80]

st.subheader("🔥 Elite GPT Deals")

st.dataframe(df, width="stretch")

st.subheader("🧠 Score Comparison")

st.bar_chart(df[["ml_score", "ai_score", "gpt_score"]])

st.subheader("🚀 Verdict Breakdown")

st.bar_chart(df["gpt_verdict"].value_counts())

st.success("GPT Intelligence Active 🤖")
