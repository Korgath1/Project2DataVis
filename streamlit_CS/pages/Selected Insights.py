import streamlit as st
import plotly.express as px
import pandas as pd
from utils import preprocess_data

# Load dataset
DATA_FILE = "traffic_accidents.csv"
data_path = os.path.join(os.path.dirname(__file__), "..", DATA_FILE)
data_path = os.path.abspath(data_path)

df = pd.read_csv(data_path)
df = preprocess_data(df)

st.title("Selected Insights — Key Findings from Traffic Crash Data")
st.write("""
This page summarizes the most important observations from our exploratory analysis and matches out initial questions about the data.
These insights are intended to guide safety measures and highlight patterns in traffic incidents.
""")

total_crashes = len(df)
total_fatal = df["injuries_fatal"].sum()
avg_injuries = df["injuries_total"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Crashes", f"{total_crashes:,}")
col2.metric("Total Fatalities", f"{total_fatal:,}")
col3.metric("Average Injuries per Crash", f"{avg_injuries:.2f}")

st.markdown("---")

#1
st.header("Most Dangerous Times")
hourly_fatal = df.groupby("crash_hour")["injuries_fatal"].sum().reset_index()
st.bar_chart(hourly_fatal.set_index("crash_hour"))
st.write("""
- Peak fatal crashes occur during evening hours (4–7 PM)  
- Late-night hours (11 PM–2 AM) show higher fatality rates, often linked to drunk driving  
- Weekends show a slight shift toward later hours for severe crashes
""")

#2
st.header("Weather Impact on Crash Severity")
weather_fatal = df.groupby("weather_condition")["injuries_fatal"].sum().sort_values(ascending=False)
st.bar_chart(weather_fatal)
st.write("""
- Snow and rain significantly increase the number of fatal crashes  
- Clear weather has more crashes overall, but a smaller proportion are fatal  
- Foggy conditions, while rare, show high severity per crash
""")

#3
st.header("High-Risk Locations")
intersection_counts = df.groupby("intersection_related_i").size()
trafficway_counts = df.groupby("trafficway_type").size()
st.write("- Intersections vs Non-Intersections crash counts:")
st.bar_chart(intersection_counts)
st.write("- Trafficway type crash counts:")
st.bar_chart(trafficway_counts)
st.write("""
- Four way stops are hotspots for crashes.
- Local roads and suburbs have more minor crashes, possibly due to lower speed limits
""")

#4
st.markdown("---")
st.header("Additional Observations")
st.markdown("""
- Multi-vehicle crashes are more likely to result in severe or fatal injuries  
- Nighttime crashes have higher severity and are more likely to involve alcohol especially after midnight 
- Seasonal trends: winter months increase risk due to icy conditions; summer holidays increase total crashes
""")
