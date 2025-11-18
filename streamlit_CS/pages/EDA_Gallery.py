import streamlit as st
import plotly.express as px
import pandas as pd
import os
from utils import preprocess_data

# Load dataset
DATA_FILE = "traffic_accidents.csv"
data_path = os.path.join(os.path.dirname(__file__), "..", DATA_FILE)
data_path = os.path.abspath(data_path)

df = pd.read_csv(data_path)
df = preprocess_data(df)

st.title("EDA Gallery — Exploratory Data Analysis")
st.write("Each chart includes a short 'How to read this chart' explainer and observations.")

# Chart 1: Hour vs Weekday Heatmap
heat = df.groupby(["weekday","crash_hour"]).size().reset_index(name="count")
weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
heat["weekday"] = pd.Categorical(heat["weekday"], categories=weekday_order, ordered=True)
heat = heat.sort_values(["weekday","crash_hour"])
fig1 = px.density_heatmap(heat, x="crash_hour", y="weekday", z="count", nbinsx=24,
                          title="Crashes by hour and weekday",
                          labels={"crash_hour":"Hour","weekday":"Weekday","count":"Crash count"})
st.plotly_chart(fig1, use_container_width=True)
st.markdown("**How to read:** Darker = more crashes. Peaks = high-risk hours/days.")
st.markdown("**Observation:** Commute hours have highest crashes; weekends show late-night spikes.")
st.markdown("---")

# Chart 2: Monthly Trend
monthly = df.groupby(df["crash_date"].dt.to_period("M")).size().reset_index(name="count")
monthly["crash_date"] = monthly["crash_date"].dt.to_timestamp()
fig2 = px.line(monthly, x="crash_date", y="count", title="Monthly crash count")
st.plotly_chart(fig2, use_container_width=True)
st.markdown("**How to read:** Each point = crashes per month. Seasonal trends visible.")
st.markdown("**Observation:** Winter/summer peaks; holidays may spike crashes.")
st.markdown("---")

# Chart 3: Severity by Weather
sev_weather = df.groupby(["weather_condition","most_severe_injury"]).size().reset_index(name="count")
top_weathers = df["weather_condition"].value_counts().nlargest(8).index
sev_weather = sev_weather[sev_weather["weather_condition"].isin(top_weathers)]
fig3 = px.bar(sev_weather, x="weather_condition", y="count", color="most_severe_injury", barmode="stack",
              title="Crash severity by weather")
st.plotly_chart(fig3, use_container_width=True)
st.markdown("**How to read:** Stacked bars = severity distribution per weather.")
st.markdown("**Observation:** Rain/Snow/Fog have higher severe/fatal crash share.")
st.markdown("---")

# Chart 4: Number of Vehicles vs Severity
if "num_units" in df.columns:
    fig4 = px.box(df, x="most_severe_injury", y="num_units", points="outliers",
                  title="Number of vehicles by severity")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("**How to read:** Boxes = vehicle count distribution per severity.")
    st.markdown("**Observation:** Severe crashes often involve multiple vehicles.")
