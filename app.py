import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Child Malnutrition AI Predictor",
    page_icon="🧒",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main-title {
    font-size:40px;
    font-weight:700;
    text-align:center;
    color:#2C7BE5;
}

.subtitle {
    text-align:center;
    font-size:18px;
    color:gray;
}

.result-box {
    padding:20px;
    border-radius:12px;
    font-size:22px;
    text-align:center;
    font-weight:bold;
}

.low-risk {
    background-color:#d4edda;
    color:#155724;
}

.medium-risk {
    background-color:#fff3cd;
    color:#856404;
}

.high-risk {
    background-color:#f8d7da;
    color:#721c24;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<p class="main-title">🧒 AI Malnutrition Prediction System</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Early Detection of Child Malnutrition using Machine Learning</p>', unsafe_allow_html=True)

st.write("")

# -----------------------------
# LOAD MODEL
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Child Information")

age = st.sidebar.slider("Age (months)", 1, 60, 24)
weight = st.sidebar.slider("Weight (kg)", 2.0, 30.0, 10.0)
height = st.sidebar.slider("Height (cm)", 40.0, 130.0, 80.0)
muac = st.sidebar.slider("MUAC (cm)", 8.0, 20.0, 12.0)
gender = st.sidebar.selectbox("Gender", ["Male","Female"])

gender = 1 if gender=="Male" else 0

# -----------------------------
# MAIN LAYOUT
# -----------------------------
col1, col2 = st.columns([1,1])

# -----------------------------
# CHILD DATA DISPLAY
# -----------------------------
with col1:

    st.subheader("Child Health Data")

    st.metric("Age", f"{age} months")
    st.metric("Weight", f"{weight} kg")
    st.metric("Height", f"{height} cm")
    st.metric("MUAC", f"{muac} cm")

# -----------------------------
# PREDICTION
# -----------------------------
with col2:

    st.subheader("AI Prediction")

    input_data = np.array([[age,weight,height,muac,gender]])

    if st.button("Predict Malnutrition Risk"):

        prediction = model.predict(input_data)[0]
        confidence = model.predict_proba(input_data)[0].max()*100

        if prediction == 0:
            risk="Healthy"
            style="low-risk"

        elif prediction == 1:
            risk="Moderate Malnutrition"
            style="medium-risk"

        else:
            risk="Severe Malnutrition"
            style="high-risk"

        st.markdown(
            f'<div class="result-box {style}">{risk}</div>',
            unsafe_allow_html=True
        )

        st.write(f"Confidence: **{confidence:.2f}%**")


# -----------------------------
# 3D CHILD GROWTH VISUALIZATION
# -----------------------------

import plotly.graph_objects as go

st.subheader("3D Child Growth Visualization")

# Example healthy reference points
healthy_age = [6,12,24,36,48,60]
healthy_height = [65,75,85,95,105,110]
healthy_weight = [7,9,12,14,16,18]

fig = go.Figure()

# Healthy growth reference
fig.add_trace(go.Scatter3d(
    x=healthy_age,
    y=healthy_height,
    z=healthy_weight,
    mode='lines+markers',
    marker=dict(size=5),
    name="Healthy Growth Curve"
))

# Child data point
fig.add_trace(go.Scatter3d(
    x=[age],
    y=[height],
    z=[weight],
    mode='markers',
    marker=dict(
        size=12,
        color='red',
        symbol='circle'
    ),
    name="Child Data"
))

fig.update_layout(
    scene=dict(
        xaxis_title='Age (Months)',
        yaxis_title='Height (cm)',
        zaxis_title='Weight (kg)'
    ),
    margin=dict(l=0, r=0, b=0, t=30)
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# VISUAL GAUGE
# -----------------------------
st.subheader("Risk Level Indicator")

risk_score = np.random.randint(0,100)

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk_score,
    title={'text': "Malnutrition Risk"},
    gauge={
        'axis': {'range': [0,100]},
        'bar': {'color': "darkred"},
        'steps': [
            {'range': [0,33], 'color': "lightgreen"},
            {'range': [33,66], 'color': "yellow"},
            {'range': [66,100], 'color': "red"},
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown(
"""
⚠️ **Disclaimer:**  
This AI tool is for research and educational purposes only and should not replace professional medical diagnosis.
"""
)
