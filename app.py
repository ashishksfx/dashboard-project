import streamlit as st
import pandas as pd
import plotly.express as px

st.title("QC Mode - Dedicated Dashboard")

# Google Sheet URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8ze543EsXv5xgTm3jblkiE0PVsue0mQa1gUtiY8z6g4wypWjScgIyNr3QLdOZJQdrtkF2Cvcm_pFw/pub?gid=174468535&single=true&output=csv"

# Load data safely
try:
    df = pd.read_csv(url)
    st.success("Data Loaded Successfully")
except Exception as e:
    st.error("Data loading failed")
    st.write(e)
    st.stop()

# Show columns
st.write("Columns:", df.columns)

# Clean data
df["city_name"] = df["city_name"].astype(str).str.strip().str.title()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

df = df.dropna(subset=["city_name", "order_date"])

# City dropdown
cities = sorted(df["city_name"].unique())
city = st.selectbox("Select City", cities)

# Filter data
filtered_df = df[df["city_name"] == city]

# Trend
orders_trend = filtered_df.groupby("order_date").size().reset_index(name="orders")

fig = px.line(orders_trend, x="order_date", y="orders", title=f"{city} Orders Trend")
st.plotly_chart(fig)

st.dataframe(filtered_df)
