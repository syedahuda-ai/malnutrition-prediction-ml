import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go
import streamlit.components.v1 as components

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Pediatric Smart AI System",
    page_icon="🍼",
    layout="wide"
)

# -------------------------
# THEME TOGGLE
# -------------------------
dark_mode = st.sidebar.toggle("🌙 Pediatric Dark Mode")

if dark_mode:
    bg = "linear-gradient(to right, #0f172a, #1e293b)"
    card_bg = "rgba(30,41,59,0.8)"
    text = "white"
else:
    bg = "linear-gradient(to right, #e0f2fe, #fdf2f8)"
    card_bg = "rgba(255,255,255,0.85)"
    text = "#0f172a"

# -------------------------
# GLOBAL CSS + FLOATING ITEMS
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
    font-size:45px;
    font-weight:900;
    text-align:center;
}}

.card {{
    background:{card_bg};
    backdrop-filter: blur(25px);
    padding:30px;
    border-radius:25px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    transition: transform 0.4s ease;
    margin-bottom:25px;
}}

.card:hover {{
    transform: translateY(-8px) scale(1.02);
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

/* Floating Baby Elements */
.floating {{
    position: fixed;
    font-size: 50px;
    animation: floatUp 18s linear infinite;
    opacity: 0.5;
    z-index: 0;
}}

@keyframes floatUp {{
    0% {{ transform: translateY(100vh) rotate(0deg); }}
    100% {{ transform: translateY(-10vh) rotate(360deg); }}
}}

</style>
""", unsafe_allow_html=True)

# Floating Pacifiers & Toys
items = ["🍼", "🧸", "👶", "🍼", "🧸"]
for i, item in enumerate(items):
    st.markdown(
        f'<div class="floating" style="left:{i*18+5}%; animation-duration:{12+i*2}s;">{item}</div>',
        unsafe_allow_html=True
    )

# -------------------------
# LOAD MODEL
# -------------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="hospital-title">🍼 Pediatric Smart AI Monitoring System</div>', unsafe_allow_html=True)
st.write("Advanced Malnutrition Risk Assessment Dashboard")
st.write("---")

# -------------------------
# LAYOUT
# -------------------------
col1, col2 = st.columns([1,1])

# =========================
# LEFT PANEL – INPUT
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
# RIGHT PANEL – 3D CHILD MODEL
# =========================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("3D Child Visualization")

    scale = height / 80

    model_html = f"""
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
    <model-viewer
      src="https://modelviewer.dev/shared-assets/models/RobotExpressive.glb"
      auto-rotate
      camera-controls
      shadow-intensity="1"
      exposure="1"
      scale="{scale} {scale} {scale}"
      style="width:100%; height:420px; background:transparent;">
    </model-viewer>
    """

    components.html(model_html, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ANALYSIS BUTTON
# =========================
if st.button("🔬 Run Pediatric Assessment"):

    input_data = np.array([[age, height, weight, muac]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][prediction]

    # Soft Pediatric Sound
    st.markdown("""
    <audio autoplay>
      <source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    st.write("---")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("AI Diagnosis")

        if prediction == 0:
            st.markdown(
                "<h2 style='color:green;'>🎉 Great News! Child is Healthy</h2>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<h2 style='color:red;'>⚠️ Nutritional Attention Required</h2>",
                unsafe_allow_html=True
            )

        st.metric("AI Confidence Level", f"{probability*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with result_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Vital Monitor Simulation")
        st.markdown('<div class="monitor"><div class="wave"></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Pediatric AI System | Developed by Syeda Huda | AI for Social Impact")
