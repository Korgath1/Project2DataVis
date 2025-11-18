import streamlit as st
import plotly.express as px
import pandas as pd
import os
from utils import preprocess_data, compute_kpis

# Load dataset
DATA_FILE = "traffic_accidents.csv"
data_path = os.path.join(os.path.dirname(__file__), "..", DATA_FILE)
data_path = os.path.abspath(data_path)

df = pd.read_csv(data_path)
df = preprocess_data(df)

st.title("Crash Dashboard — Interactive Insights")

# Sidebar filters
st.sidebar.header("Filters")
min_date = df["crash_date"].min()
max_date = df["crash_date"].max()
date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)
severity_opts = df["most_severe_injury"].unique().tolist()
selected_sev = st.sidebar.multiselect("Severity", severity_opts, default=severity_opts)
weather_opts = df["weather_condition"].value_counts().index.tolist()
selected_weather = st.sidebar.multiselect("Weather", weather_opts, default=weather_opts[:5])
hour_window = st.sidebar.slider("Hour window", 0, 23, (0,23))

mask = (
    (df["crash_date"] >= pd.to_datetime(date_range[0])) &
    (df["crash_date"] <= pd.to_datetime(date_range[1])) &
    (df["most_severe_injury"].isin(selected_sev)) &
    (df["weather_condition"].isin(selected_weather)) &
    (df["crash_hour"] >= hour_window[0]) & (df["crash_hour"] <= hour_window[1])
)
dff = df[mask]

# KPIs
kpis = compute_kpis(dff)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Filtered Records", f"{kpis['total']:,}")
col2.metric("Fatal %", f"{kpis['fatal_pct']:.2f}%")
col3.metric("Avg Injuries", f"{kpis['avg_injuries']:.2f}")
col4.metric("Top Weather", kpis["top_weather"])

st.markdown("---")
# Charts
sev_by_weather = dff.groupby(["weather_condition","most_severe_injury"]).size().reset_index(name="count")
fig1 = px.bar(sev_by_weather, x="weather_condition", y="count", color="most_severe_injury", barmode="stack")
st.plotly_chart(fig1, use_container_width=True)

heat = dff.groupby(["weekday","crash_hour"]).size().reset_index(name="count")
heat["weekday"] = pd.Categorical(heat["weekday"], categories=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], ordered=True)
fig2 = px.density_heatmap(heat, x="crash_hour", y="weekday", z="count", nbinsx=24)
st.plotly_chart(fig2, use_container_width=True)
