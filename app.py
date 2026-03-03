import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Child Malnutrition Predictor",
    page_icon="🩺",
    layout="wide"
)

# ----------------------------
# CUSTOM CSS (MODERN UI)
# ----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #f5f7fa, #c3cfe2);
}
.big-title {
    font-size:40px !important;
    font-weight:800;
    text-align:center;
    color:#2C3E50;
}
.result-box {
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
}
.green-box {
    background-color:#d4edda;
    color:#155724;
}
.red-box {
    background-color:#f8d7da;
    color:#721c24;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD MODEL
# ----------------------------
model = pickle.load(open("model.pkl", "rb"))

# ----------------------------
# TITLE
# ----------------------------
st.markdown('<p class="big-title">🩺 Child Malnutrition Prediction System</p>', unsafe_allow_html=True)
st.markdown("### AI Powered Health Screening Dashboard")

st.write("---")

# ----------------------------
# INPUT SECTION
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age (Months)", 1, 60, 12)
    height = st.number_input("Height (cm)", min_value=30.0, max_value=150.0, value=80.0)
    
with col2:
    weight = st.number_input("Weight (kg)", min_value=2.0, max_value=40.0, value=10.0)
    muac = st.number_input("MUAC (Mid Upper Arm Circumference)", min_value=5.0, max_value=25.0, value=12.0)

# ----------------------------
# PREDICTION BUTTON
# ----------------------------
if st.button("🔍 Predict Health Status"):
    
    input_data = np.array([[age, height, weight, muac]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][prediction]

    st.write("---")

    # RESULT DISPLAY
    if prediction == 0:
        st.markdown('<div class="result-box green-box">✅ Healthy Child</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box red-box">⚠️ Malnourished Child</div>', unsafe_allow_html=True)

    # PROBABILITY BAR (Plotly)
    fig = go.Figure(go.Bar(
        x=[probability],
        y=["Prediction Confidence"],
        orientation='h',
        marker=dict(color='green' if prediction == 0 else 'red')
    ))

    fig.update_layout(
        title="Model Confidence Level",
        xaxis=dict(range=[0,1]),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

    # HEIGHT-WEIGHT VISUAL
    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(
        x=[height],
        y=[weight],
        mode='markers',
        marker=dict(
            size=20,
            color='green' if prediction == 0 else 'red'
        ),
        name="Child Data"
    ))

    scatter_fig.update_layout(
        title="Height vs Weight Visualization",
        xaxis_title="Height (cm)",
        yaxis_title="Weight (kg)"
    )

    st.plotly_chart(scatter_fig, use_container_width=True)

# ----------------------------
# FOOTER
# ----------------------------
st.write("---")
st.markdown("Built with ❤️ by Syeda Huda | AI for Social Impact")
