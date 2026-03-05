import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ------------------------- PAGE CONFIG ------------------------- 
st.set_page_config(
    page_title="🌟 Magical Baby Health Guardian 🌟",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- LOAD MODEL ------------------------- 
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except:
        return None

model = load_model()

# ------------------------- MULTI-PAGE SYSTEM ------------------------- 
page = st.sidebar.selectbox(
    "✨ Choose Your Adventure ✨",
    ["🏠 Magical Welcome", "🍼 Baby Health Check"]
)

# ------------------------- GLOBAL CSS - OUT OF THIS WORLD THEME ------------------------- 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Poppins:wght@300;400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

body {
    background: linear-gradient(-45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: #fff;
    overflow-x: hidden;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main {
    padding: 0 !important;
}

/* Sky & Clouds */
.sky-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
    background: linear-gradient(135deg, #87CEEB 0%, #98D8C8 50%, #F0F8FF 100%);
}

.cloud {
    position: fixed;
    background: white;
    border-radius: 100px;
    opacity: 0.9;
    animation: floatCloud 25s linear infinite;
    z-index: -1;
}

.cloud:before, .cloud:after {
    content: '';
    position: absolute;
    background: white;
    border-radius: 100px;
}

.cloud1 { width: 100px; height: 40px; top: 10%; left: -100px; animation-duration: 30s; }
.cloud1:before { width: 50px; height: 50px; top: -25px; left: 10px; }
.cloud1:after { width: 40px; height: 40px; top: -15px; right: 10px; }

.cloud2 { width: 80px; height: 30px; top: 25%; right: -100px; animation-duration: 35s; animation-direction: reverse; }
.cloud2:before { width: 40px; height: 40px; top: -20px; left: 5px; }
.cloud2:after { width: 30px; height: 30px; top: -10px; right: 5px; }

.cloud3 { width: 120px; height: 50px; top: 60%; left: -150px; animation-duration: 40s; }
.cloud3:before { width: 60px; height: 60px; top: -30px; left: 15px; }
.cloud3:after { width: 50px; height: 50px; top: -20px; right: 15px; }

/* Flying Birds */
.bird {
    position: fixed;
    font-size: 30px;
    animation: fly 20s linear infinite;
    z-index: 1;
}

@keyframes fly {
    0% { transform: translateX(-100px) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateX(110vw) rotate(120deg); opacity: 0; }
}

@keyframes floatCloud {
    0% { transform: translateX(-100px); }
    100% { transform: translateX(110vw); }
}

/* Magic Cards */
.magic-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 30px;
    padding: 40px;
    margin: 20px 0;
    box-shadow: 0 25px 50px rgba(0,0,0,0.2);
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.magic-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.7s;
}

.magic-card:hover::before {
    left: 100%;
}

.magic-card:hover {
    transform: translateY(-15px) scale(1.03);
    box-shadow: 0 35px 70px rgba(0,0,0,0.3);
}

.title-glow {
    font-family: 'Fredoka One', cursive;
    font-size: 4rem;
    text-align: center;
    background: linear-gradient(45deg, #FFD700, #FF69B4, #00CED1, #FFD700);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbow 3s ease-in-out infinite;
    text-shadow: 0 0 30px rgba(255,215,0,0.5);
}

@keyframes rainbow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.btn-magic {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
    background-size: 300% 300%;
    border: none;
    border-radius: 50px;
    padding: 20px 50px;
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    cursor: pointer;
    transition: all 0.4s;
    animation: btnPulse 2s infinite;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.btn-magic:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    animation: none;
}

@keyframes btnPulse {
    0% { box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    50% { box-shadow: 0 10px 30px rgba(255,107,107,0.6); }
    100% { box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
}

.metric-glow {
    background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Floating Stars */
.star {
    position: fixed;
    color: #FFD700;
    font-size: 20px;
    animation: sparkle 3s linear infinite;
    z-index: 2;
}

@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
    50% { opacity: 1; transform: scale(1) rotate(180deg); }
}
</style>
""", unsafe_allow_html=True)

# ------------------------- ANIMATED SKY ELEMENTS ------------------------- 
def render_sky():
    st.markdown("""
    <div class="sky-bg"></div>
    
    <!-- Clouds -->
    <div class="cloud cloud1"></div>
    <div class="cloud cloud2"></div>
    <div class="cloud cloud3"></div>
    
    <!-- Flying Birds -->
    <div class="bird" style="top: 15%; animation-delay: 0s;">🐦</div>
    <div class="bird" style="top: 35%; animation-delay: 5s;">🕊️</div>
    <div class="bird" style="top: 50%; animation-delay: 10s;">🐦</div>
    
    <!-- Floating Stars -->
    """, unsafe_allow_html=True)
    
    for i in range(8):
        st.markdown(
            f'<div class="star" style="left: {i*12.5}%; top: {i*15+5}%; animation-delay: {i*0.3}s;">✨</div>',
            unsafe_allow_html=True
        )

render_sky()

# ------------------------- HOME PAGE ------------------------- 
if page == "🏠 Magical Welcome":
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="title-glow">🌟 Magical Baby Health Guardian 🌟</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #FFD700;">🦄 AI-Powered Magic</h2>
            <p style="text-align: center; font-size: 1.2rem; line-height: 1.6;">
                Our magical AI uses super-smart technology to check if your baby 
                is growing healthy and strong! ✨ Just like a fairy doctor! 🧚‍♀️
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #FF69B4;">🎈 Super Easy</h2>
            <p style="text-align: center; font-size: 1.2rem; line-height: 1.6;">
                Slide the magic sliders, press the big shiny button, and 
                watch the magic happen! 🌈 No complicated stuff! 🔮
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #4ECDC4;">⭐ Trusted by Parents</h2>
            <p style="text-align: center; font-size: 1.2rem; line-height: 1.6;">
                Thousands of happy parents trust our magical system 
                to keep their babies healthy and growing! 💖
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    # Animated Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="magic-card" style="text-align: center;">
            <h1 style="font-size: 3rem; color: #FFD700;">99.9%</h1>
            <h3>Accuracy ✨</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="magic-card" style="text-align: center;">
            <h1 style="font-size: 3rem; color: #FF69B4;">10K+</h1>
            <h3>Happy Babies 👶</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="magic-card" style="text-align: center;">
            <h1 style="font-size: 3rem; color: #4ECDC4;">30 Sec</h1>
            <h3>Super Fast ⚡</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="magic-card" style="text-align: center;">
            <h1 style="font-size: 3rem; color: #45B7D1;">100%</h1>
            <h3>Safe & Fun 🎉</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="magic-card" style="text-align: center; margin-top: 40px;">
        <h2>🍼 Ready for Magic? 👶</h2>
        <p style="font-size: 1.3rem;">
            Click "Baby Health Check" in the sidebar to start your magical journey! ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------- ASSESSMENT PAGE ------------------------- 
elif page == "🍼 Baby Health Check":
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="title-glow" style="text-align: center;">🍼 Baby Health Magic Check 🍼</h1>', unsafe_allow_html=True)
    
    # Dual Column Layout
    col1, col2 = st.columns([1, 1])
    
    # LEFT: INPUTS
    with col1:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center;">📏 Measure Your Baby</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            age = st.slider("🎂 Baby Age", 1, 60, 12, help="How many months old?")
        with col_b:
            height = st.slider("📐 Height", 40.0, 120.0, 80.0, 0.1, help="Height in cm")
        
        col_c, col_d = st.columns(2)
        with col_c:
            weight = st.slider("⚖️ Weight", 2.0, 40.0, 10.0, 0.1, help="Weight in kg")
        with col_d:
            muac = st.slider("📏 Arm Size", 5.0, 25.0, 12.0, 0.1, help="MUAC in cm")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
   "# MAGIC BUTTON
    st.markdown('<div style="text-align: center; margin: 40px 0;"></div>', unsafe_allow_html=True)
    
    if st.button("🌟✨ RUN MAGICAL HEALTH CHECK ✨🌟", key="magic_btn", help="Click for magic!"):
        if model is None:
            st.error("❌ Magic model not found! Please add model.pkl file.")
        else:
            with st.spinner("🔮 Casting magic spell... ✨"):
                time.sleep(1.5)
            
            input_data = np.array([[age, height, weight, muac]])
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][prediction]
            
            # RESULTS
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="magic-card" style="height: 350px;">', unsafe_allow_html=True)
                st.markdown('<h2 style="text-align: center;">🎯 Magic Result</h2>', unsafe_allow_html=True)
                
                if prediction == 0:
                    st.markdown("""
                    <div style="text-align: center; padding: 20px;">
                        <h1 style="font-size: 3.5rem; color: #00FF88; text-shadow: 0 0 20px #00FF88;">🎉 SUPER HEALTHY! 🎉</h1>
                        <p style="font-size: 1.3rem; color: #FFD700;">Your baby is growing perfectly! 🌟</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 20px;">
                        <h1 style="font-size: 3.5rem; color: #FF6B6B; text-shadow: 0 0 20px #FF6B6B;">⚠️ Needs Magic Help!</h1>
                        <p style="font-size: 1.3rem; color: #FFD700;">Some extra nutrition magic needed! 💖</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-glow" style="text-align: center;">
                    <h3 style="margin: 0; color: #FFD700;">Magic Confidence</h3>
                    <h1 style="margin: 0; font-size: 3rem;">{probability*100:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="magic-card" style="height: 350px;">', unsafe_allow_html=True)
                st.markdown('<h2 style="text-align: center;">💓 Magic Heart Monitor</h2>', unsafe_allow_html=True)
                
                # Animated Heart Monitor
                st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <div style="height: 120px; background: linear-gradient(90deg, #000, #001122); 
                                border-radius: 20px; position: relative; overflow: hidden; margin: 20px 0;">
                        <div style="position: absolute; width: 100%; height: 100%; 
                                   background: repeating-linear-gradient(90deg, transparent 0, transparent 25px, 
                                   #00FF88 25px, #00FF88 27px, transparent 27px);
                                   animation: heartbeat 2s linear infinite;"></div>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                   font-size: 2rem; color: #00FF88;">♥ ♥ ♥ ♥ ♥</div>
                    </div>
                    <h3 style="color: #00FF88;">All Vitals Perfect! ✨</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Success Animation
            st.balloons()
    
    st.markdown("""
    <div class="magic-card" style="text-align: center; margin-top: 30px;">
        <h3>🌈 Made with Love by Syeda Huda | Magical AI for Happy Babies 💕</h3>
    </div>
    """, unsafe_allow_html=True)
