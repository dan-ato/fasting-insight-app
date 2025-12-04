import streamlit as st
from datetime import datetime, timedelta, time

# -------------------------
# Helper Functions
# -------------------------
def calculate_fasting_hours(last_meal, break_fast):
    # If last meal is in the evening and break-fast is the next morning
    if break_fast < last_meal:
        break_fast += timedelta(days=1)
    hours = (break_fast - last_meal).total_seconds() / 3600
    return hours

def metabolic_state(hours):
    if hours < 4:
        return "Active digestion. Rising blood glucose and insulin."
    elif hours < 8:
        return "Insulin lowering. Beginning to shift into fat utilization."
    elif hours < 12:
        return "Glycogen stores gradually decreasing. More fat oxidation."
    elif hours < 16:
        return "Glycogen low. Ketone production starting."
    elif hours < 20:
        return "Mild ketosis. Increased fat burning. Autophagy beginning."
    elif hours < 24:
        return "Deeper ketosis. Autophagy and AMPK activation rising."
    else:
        return "Prolonged fasting state. High ketone production and cellular cleanup."

def timeline_chart(hours):
    # A simple horizontal chart
    st.write("### Fasting Timeline")
    st.progress(min(hours / 24, 1.0))
    st.caption(f"{hours:.2f} hours out of a 24-hour reference window")

# -------------------------
# Streamlit UI
# -------------------------
st.title("⏳ Fasting Tracker + Metabolic Insight")

st.write("Enter your last meal time and the time you broke your fast. This tool will calculate fasting duration and explain the state your body is likely in.")

st.subheader("🕒 Input")

# Time inputs
last_meal_time = st.time_input("Last meal time (previous day)", time(20, 0))  # default 8pm
break_fast_time = st.time_input("Break-fast time (today)", time(10, 0))       # default 10am

# Convert to datetime for calculations
today = datetime.today()
last_meal_dt = datetime.combine(today - timedelta(days=1), last_meal_time)
break_fast_dt = datetime.combine(today, break_fast_time)

# Calculation
hours_fasted = calculate_fasting_hours(last_meal_dt, break_fast_dt)

st.subheader("⏱️ Result")
st.metric("Hours Fasted", f"{hours_fasted:.2f} hours")

# State description
state = metabolic_state(hours_fasted)
st.write("### 🔬 Likely Metabolic State")
st.info(state)

# Visual timeline
timeline_chart(hours_fasted)

st.write("---")
st.write("You can paste your fasting duration into Notion for tracking and journaling.")
