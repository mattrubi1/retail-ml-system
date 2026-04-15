import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🧠 Home Depot Clearance Intelligence")

# 🔗 LOAD DATA FROM YOUR GITHUB REPO
url = "https://raw.githubusercontent.com/mattrubi1/retail-ml-system/main/data.csv"
df = pd.read_csv(url)

# 🛑 SAFETY CHECKS
if df.empty:
    st.warning("No data available yet.")
    st.stop()

# 🧾 SHOW FULL TABLE
st.subheader("📦 All Items")
st.dataframe(df)

# 🏆 TOP DEALS SECTION
st.subheader("🔥 Top Clearance Opportunities")

if "ml_score" in df.columns:

    top_df = df.sort_values("ml_score", ascending=False).head(10)

    for _, row in top_df.iterrows():

        col1, col2 = st.columns([1, 3])

        # 📸 IMAGE COLUMN
        with col1:
            if "image" in row and pd.notna(row["image"]) and row["image"] != "":
                st.image(row["image"], use_container_width=True)
            else:
                st.write("No Image")

        # 📊 INFO COLUMN
        with col2:
            st.markdown(f"### {row.get('item_name', 'Unknown Item')}")
            st.write(f"**Description:** {row.get('description', 'N/A')}")
            st.write(f"**Store:** {row.get('last_store_location', 'N/A')}")
            st.write(f"**SKU:** {row.get('sku', 'N/A')}")
            st.write(f"**Price:** ${row.get('price', 0)}")
            st.write(f"**Discount:** {row.get('drop_pct', 0)}%")
            st.write(f"**ML Score:** {round(row.get('ml_score', 0), 2)}")

            if "sku" in row:
                st.markdown(f"[🔗 View Product](https://www.homedepot.com/p/{row['sku']})")

        st.divider()

else:
    st.warning("ML model has not run yet — no scores available.")

# 📊 SCORE VISUALIZATION
if "ml_score" in df.columns:
    st.subheader("📊 ML Score Distribution")
    st.bar_chart(df["ml_score"])
