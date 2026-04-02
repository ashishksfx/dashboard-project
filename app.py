import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("QC Mode - Dedicated Dashboard")

# Load Data
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8ze543EsXv5xgTm3jblkiE0PVsue0mQa1gUtiY8z6g4wypWjScgIyNr3QLdOZJQdrtkF2Cvcm_pFw/pub?gid=174468535&single=true&output=csv"

df = pd.read_csv(url)

# Clean Data
df["city_name"] = df["city_name"].astype(str).str.strip().str.title()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

df = df.dropna(subset=["city_name", "order_date"])

# -----------------------------
# LAST 7 DAYS DATA
# -----------------------------
last_7_days = df["order_date"].max() - pd.Timedelta(days=6)
df_7 = df[df["order_date"] >= last_7_days]

# -----------------------------
# 1. OVERALL TREND
# -----------------------------
st.subheader("Overall Orders Trend (Last 7 Days)")

overall_trend = df_7.groupby("order_date").size().reset_index(name="orders")
overall_trend["date"] = overall_trend["order_date"].dt.strftime("%d/%m")

fig1 = px.line(overall_trend, x="date", y="orders")
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# 2. CITY TREND
# -----------------------------
st.subheader("City-wise Trend (Last 7 Days)")

cities = sorted(df["city_name"].unique())
city = st.selectbox("Select City", cities)

city_df = df_7[df_7["city_name"] == city]

city_trend = city_df.groupby("order_date").size().reset_index(name="orders")
city_trend["date"] = city_trend["order_date"].dt.strftime("%d/%m")

fig2 = px.line(city_trend, x="date", y="orders")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 3. CITY PERFORMANCE
# -----------------------------
st.subheader("City Performance (Yesterday)")

yesterday = df["order_date"].max() - pd.Timedelta(days=1)
df_y = df[df["order_date"] == yesterday]

city_perf = df_y.groupby("city_name").agg(
    orders=("city_name", "count"),
    riders=("rider_id", "nunique")
).reset_index().sort_values(by="orders", ascending=False)

st.dataframe(city_perf)

# -----------------------------
# 4. TOP RIDERS
# -----------------------------
st.subheader("Top Riders (Yesterday)")

top_riders = df_y.groupby(["rider_id", "city_name"]).size().reset_index(name="orders")
top_riders = top_riders.sort_values(by="orders", ascending=False).head(10)

st.dataframe(top_riders)

# -----------------------------
# 5. DATE WISE DATA
# -----------------------------
st.subheader("Date-wise Summary (Last 7 Days)")

date_summary = df_7.groupby("order_date").agg(
    orders=("city_name", "count"),
    riders=("rider_id", "nunique")
).reset_index()

date_summary = date_summary.sort_values(by="order_date", ascending=False)
date_summary["date"] = date_summary["order_date"].dt.strftime("%d/%m")

st.dataframe(date_summary[["date", "orders", "riders"]])

# -----------------------------
# 6. RAW DATA TAB
# -----------------------------
st.subheader("Raw Data")
st.dataframe(df)
