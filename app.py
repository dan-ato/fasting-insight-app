import streamlit as st
from datetime import datetime, timedelta, time
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page & Theme Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fasting Insight Tracker",
    page_icon="⏳",
    layout="centered"
)

# Inject a gradient header using HTML/CSS
st.markdown(
    """
    <style>
    .gradient-header {
        background: linear-gradient(to right, #3A7CA5, #2E3440);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="gradient-header">
        <h1>⏳ Fasting Insight Tracker</h1>
        <p>Track your fast and understand your metabolic state.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def calculate_fasting_hours(last_meal, break_fast):
    if break_fast < last_meal:
        break_fast += timedelta(days=1)
    return (break_fast - last_meal).total_seconds() / 3600


def metabolic_state(hours):
    if hours < 4:
        return "Active digestion; rising blood glucose and insulin."
    elif hours < 8:
        return "Insulin lowering; beginning to shift into fat utilization."
    elif hours < 12:
        return "Glycogen stores decreasing; fat oxidation rising."
    elif hours < 16:
        return "Glycogen low; ketone production beginning."
    elif hours < 20:
        return "Mild ketosis; increased fat burning; autophagy beginning."
    elif hours < 24:
        return "Deeper ketosis; increased autophagy and AMPK activation."
    else:
        return "Prolonged fast; high ketone production and cellular cleanup."


# Subtle science explanation
def science_details(hours):
    if hours < 4:
        return """
### What’s happening in your body?

- Digestive process is active  
- Blood glucose and insulin levels rise  
- Body is using incoming food as energy  
"""
    elif hours < 8:
        return """
### What’s happening in your body?

- Insulin levels drop  
- Body begins shifting away from glucose  
- Early rise in fat mobilization  
"""
    elif hours < 12:
        return """
### What’s happening in your body?

- Glycogen stores slowly decline  
- Fat oxidation increases  
- Mild hormonal shifts toward fasting state  
"""
    elif hours < 16:
        return """
### What’s happening in your body?

- Liver glycogen significantly reduced  
- Ketones begin appearing in the blood  
- Metabolic flexibility improves  
"""
    elif hours < 20:
        return """
### What’s happening in your body?

- Mild ketosis  
- Autophagy likely initiating  
- Body relying more on stored fat  
"""
    elif hours < 24:
        return """
### What’s happening in your body?

- Ketone levels rising  
- Autophagy and cellular cleanup elevated  
- Reduced inflammation markers  
"""
    else:
        return """
### What’s happening in your body?

- Deep ketosis  
- High autophagy  
- Strong metabolic regeneration phase  
"""


def fasting_gauge(hours):
    """Returns a Plotly gauge figure representing fasting progress."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=hours,
            domain={"x": [0, 1], "y": [0, 1]},
            title={'text': "Hours Fasted", 'font': {'size': 22}},
            gauge={
                'axis': {'range': [0, 24], 'tickwidth': 1, 'tickcolor': "#2E3440"},
                'bar': {'color': "#3A7CA5"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#2E3440",
                'steps': [
                    {'range': [0, 8], 'color': '#E5EEF4'},
                    {'range': [8, 16], 'color': '#C7D9E6'},
                    {'range': [16, 24], 'color': '#89B4FA'},
                ],
            }
        )
    )
    fig.update_layout(height=300)
    return fig


# ---------------------------------------------------------
# UI Layout
# ---------------------------------------------------------
st.subheader("Input Your Fasting Window")

col1, col2 = st.columns(2)

with col1:
    last_meal_time = st.time_input("Last meal (previous day)", time(20, 0))

with col2:
    break_fast_time = st.time_input("Break-fast (today)", time(10, 0))

# Time conversion
today = datetime.today()
last_meal_dt = datetime.combine(today - timedelta(days=1), last_meal_time)
break_fast_dt = datetime.combine(today, break_fast_time)

hours_fasted = calculate_fasting_hours(last_meal_dt, break_fast_dt)

st.divider()

# ---------------------------------------------------------
# Summary Card
# ---------------------------------------------------------
st.markdown("### 🧾 Summary")
with st.container():
    st.markdown(
        f"""
        <div style="
            background-color:#E5EEF4;
            padding:15px;
            border-radius:10px;
            border: 1px solid #C7D9E6;
        ">
            <b>Last meal:</b> {last_meal_time.strftime('%I:%M %p')}<br>
            <b>Break-fast:</b> {break_fast_time.strftime('%I:%M %p')}<br>
            <b>Hours fasted:</b> {hours_fasted:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# Gauge Visualization
# ---------------------------------------------------------
st.markdown("### ⏱️ Fasting Progress Gauge")
st.plotly_chart(fasting_gauge(hours_fasted), use_container_width=True)

# ---------------------------------------------------------
# Target Window Comparison
# ---------------------------------------------------------
st.markdown("### 🎯 Suggested Target Window (14–16 hours)")

if 14 <= hours_fasted <= 16:
    st.success(f"Your fast of **{hours_fasted:.2f} hours** is within the optimal 14–16 hour range! ✔")
elif hours_fasted < 14:
    st.info(f"Your fast is **{hours_fasted:.2f} hours** — slightly below the target window.")
else:
    st.warning(f"Your fast is **{hours_fasted:.2f} hours** — above the typical 14–16 hour window.")

# ---------------------------------------------------------
# Metabolic State
# ---------------------------------------------------------
st.markdown("### 🔬 Likely Metabolic State")
st.info(metabolic_state(hours_fasted))

# ---------------------------------------------------------
# Science Section (Expandable)
# ---------------------------------------------------------
with st.expander("Learn more about your current physiological phase"):
    st.markdown(science_details(hours_fasted))

st.write("---")
st.caption("Designed for insight and reflection. Log your daily fasts in Notion and build consistency.")
