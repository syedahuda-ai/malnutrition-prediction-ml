import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go
import streamlit.components.v1 as components

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Pediatric Clinical AI System",
    page_icon="🏥",
    layout="wide"
)

# -------------------------
# THEME TOGGLE
# -------------------------
dark_mode = st.sidebar.toggle("🌙 ICU Dark Mode")

if dark_mode:
    bg = "#0b1120"
    card_bg = "rgba(15,23,42,0.85)"
    text = "white"
else:
    bg = "#f4f8fb"
    card_bg = "rgba(255,255,255,0.9)"
    text = "#0f172a"

# -------------------------
# GLOBAL HOSPITAL CSS
# -------------------------
st.markdown(f"""
<style>
body {{
    background: {bg};
    color: {text};
}}

.main {{
    background: {bg};
}}

.hospital-title {{
    font-size:42px;
    font-weight:800;
    color:#1e3a8a;
}}

.card {{
    background:{card_bg};
    backdrop-filter: blur(25px);
    padding:25px;
    border-radius:20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    margin-bottom:20px;
}}

.monitor {{
    height:100px;
    background:black;
    border-radius:15px;
    position:relative;
    overflow:hidden;
}}

.wave {{
    position:absolute;
    width:200%;
    height:100%;
    background: repeating-linear-gradient(
        90deg,
        transparent,
        transparent 20px,
        #00ff88 20px,
        #00ff88 22px
    );
    animation: move 3s linear infinite;
}}

@keyframes move {{
    from {{ transform: translateX(0); }}
    to {{ transform: translateX(-50%); }}
}}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD MODEL
# -------------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="hospital-title">🏥 Pediatric Clinical AI Monitoring System</div>', unsafe_allow_html=True)
st.write("Advanced Malnutrition Risk Assessment Dashboard")

st.write("---")

# -------------------------
# LAYOUT
# -------------------------
col1, col2 = st.columns([1,1])

# =========================
# LEFT PANEL – PATIENT INPUT
# =========================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Patient Information")

    age = st.slider("Age (Months)", 1, 60, 12)
    height = st.slider("Height (cm)", 40, 120, 80)
    weight = st.slider("Weight (kg)", 2, 40, 10)
    muac = st.slider("MUAC (cm)", 5, 25, 12)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RIGHT PANEL – 3D PATIENT
# =========================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("3D Patient Model")

    scale = height / 80

    model_html = f"""
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
    <model-viewer
      src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
      auto-rotate
      camera-controls
      shadow-intensity="1"
      scale="{scale} {scale} {scale}"
      style="width:100%; height:400px;">
    </model-viewer>
    """

    components.html(model_html, height=420)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ANALYSIS BUTTON
# =========================
if st.button("🔬 Run Clinical Assessment"):

    input_data = np.array([[age, height, weight, muac]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][prediction]

    # Machine Beep Sound
    st.markdown("""
    <audio autoplay>
      <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    st.write("---")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Diagnosis Result")

        if prediction == 0:
            st.success("Patient Status: HEALTHY")
        else:
            st.error("Patient Status: MALNUTRITION RISK")

        st.metric("AI Confidence", f"{probability*100:.2f}%")

        st.markdown('</div>', unsafe_allow_html=True)

    with result_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Vital Monitor Simulation")
        st.markdown('<div class="monitor"><div class="wave"></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Clinical AI System | Developed by Syeda Huda | AI for Social Impact")
