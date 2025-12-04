import streamlit as st
from datetime import datetime, timedelta, time

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Fasting Insight Tracker",
    page_icon="⏳",
    layout="centered"
)

# -------------------------
# Helper Functions
# -------------------------
def calculate_fasting_hours(last_meal, break_fast):
    if break_fast < last_meal:
        break_fast += timedelta(days=1)
    return (break_fast - last_meal).total_seconds() / 3600

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

def timeline_bar(hours):
    st.markdown("### 🕘 Fasting Timeline")
    pct = min(hours / 24, 1.0)
    st.progress(pct)
    st.caption(f"Approximate fasting progress: {pct*100:.1f}% of a 24-hour window")

# -------------------------
# UI
# -------------------------
st.title("⏳ Fasting Insight Tracker")
st.write("Track your fasting window and learn about the metabolic state you are likely in.")

st.divider()

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Last Meal Time (Previous Day)")
    last_meal_time = st.time_input("Select time", time(20, 0))

with col2:
    st.subheader("Break-Fast Time (Today)")
    break_fast_time = st.time_input("Select time ", time(10, 0))

# Convert to datetime for calculation
today = datetime.today()
last_meal_dt = datetime.combine(today - timedelta(days=1), last_meal_time)
break_fast_dt = datetime.combine(today, break_fast_time)

# Compute fasting hours
hours_fasted = calculate_fasting_hours(last_meal_dt, break_fast_dt)

st.divider()

# Result box
st.subheader("⏱️ Fasting Duration")
st.metric("Hours Fasted", f"{hours_fasted:.2f}")

# Metabolic state explanation
st.markdown("### 🔬 Likely Metabolic State")
st.info(metabolic_state(hours_fasted))

# Visual timeline
timeline_bar(hours_fasted)

st.divider()

st.caption("You can log your fasting duration in Notion or sync this tool later using an API.")
