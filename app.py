import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Child Health AI",
    page_icon="🍼",
    layout="wide"
)

# -------------------------
# THEME TOGGLE
# -------------------------
theme = st.sidebar.toggle("🌙 Dark Mode")

if theme:
    bg_color = "#0f172a"
    text_color = "white"
    card_bg = "rgba(30,41,59,0.7)"
else:
    bg_color = "#fdf2f8"
    text_color = "#111"
    card_bg = "rgba(255,255,255,0.7)"

# -------------------------
# GLOBAL CSS + ANIMATIONS
# -------------------------
st.markdown(f"""
<style>
body {{
    background: {bg_color};
    color: {text_color};
}}

.main {{
    background: {bg_color};
}}

/* Floating bubbles */
.bubble {{
    position: fixed;
    bottom: -100px;
    width: 40px;
    height: 40px;
    background: rgba(255, 182, 193, 0.4);
    border-radius: 50%;
    animation: rise 20s infinite ease-in;
}}

@keyframes rise {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(-1200px); }}
}}

/* Glass 3D Card */
.card {{
    background: {card_bg};
    backdrop-filter: blur(20px);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    transform: perspective(1000px) rotateX(2deg);
    margin-bottom: 30px;
}}

/* Title */
.title {{
    font-size:55px;
    font-weight:900;
    text-align:center;
}}

/* Particle background */
#particles-js {{
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: -1;
}}
</style>

<div id="particles-js"></div>

<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
<script>
particlesJS("particles-js", {{
  "particles": {{
    "number": {{"value": 60}},
    "size": {{"value": 3}},
    "move": {{"speed": 1}},
    "line_linked": {{"enable": true}}
  }}
}});
</script>

""", unsafe_allow_html=True)

# Floating bubbles
for i in range(8):
    st.markdown(f'<div class="bubble" style="left:{i*12}%"></div>', unsafe_allow_html=True)

# -------------------------
# LOAD MODEL
# -------------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------------
# NAVIGATION
# -------------------------
page = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Child Portal"])

# =========================
# HOME PAGE
# =========================
if page == "🏠 Home":

    st.markdown('<div class="title">🍼 Child Malnutrition AI</div>', unsafe_allow_html=True)

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4333/4333609.png",
        width=250
    )

    st.markdown("""
    ### 🌟 AI-Powered Pediatric Health Screening
    Advanced Machine Learning system designed for early malnutrition detection.
    Navigate to the portal to begin analysis.
    """)

# =========================
# CHILD PORTAL
# =========================
if page == "📊 Child Portal":

    st.markdown('<div class="title">👶 Child Health Portal</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age (Months)", 1, 60, 12)
        height = st.slider("Height (cm)", 40, 120, 80)

    with col2:
        weight = st.slider("Weight (kg)", 2, 40, 10)
        muac = st.slider("MUAC (cm)", 5, 25, 12)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Analyze"):

        input_data = np.array([[age, height, weight, muac]])
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][prediction]

        # Sound effect
        st.markdown("""
        <audio autoplay>
          <source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)

        if prediction == 0:
            st.success("✅ Healthy Child")
        else:
            st.error("⚠️ Malnourished Child")

        # 3D Confidence Chart
        fig = go.Figure(data=[go.Bar(
            x=[probability],
            y=["Confidence"],
            orientation='h'
        )])

        fig.update_layout(
            title="AI Confidence Level",
            xaxis=dict(range=[0,1]),
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

        # Height vs Weight
        scatter = go.Figure()
        scatter.add_trace(go.Scatter(
            x=[height],
            y=[weight],
            mode='markers',
            marker=dict(size=25)
        ))

        scatter.update_layout(
            title="Height vs Weight",
            xaxis_title="Height",
            yaxis_title="Weight"
        )

        st.plotly_chart(scatter, use_container_width=True)

    st.markdown("---")
    st.markdown("Built with ❤️ by Syeda Huda | AI for Social Impact")
