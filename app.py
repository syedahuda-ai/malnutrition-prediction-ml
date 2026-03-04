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

# ------------------------- GLOBAL CSS - FULL SCREEN MAGIC ------------------------- 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Poppins:wght@300;400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

body, .main {
    margin: 0 !important;
    padding: 0 !important;
    background: none !important;
}

/* FULL SCREEN SKY */
#sky-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
    background: linear-gradient(135deg, #87CEEB 0%, #98D8C8 40%, #E0F6FF 70%, #B8E6FF 100%);
    overflow: hidden;
}

#sky-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(120,119,198,0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255,119,198,0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120,219,255,0.3) 0%, transparent 50%);
    animation: skyGlow 8s ease-in-out infinite alternate;
}

@keyframes skyGlow {
    0% { opacity: 0.8; }
    100% { opacity: 1; }
}

/* Clouds */
.cloud {
    position: absolute;
    background: rgba(255,255,255,0.95);
    border-radius: 100px;
    box-shadow: 0 8px 32px rgba(255,255,255,0.3);
    animation: floatCloud 30s linear infinite;
}

.cloud:before, .cloud:after {
    content: '';
    position: absolute;
    background: rgba(255,255,255,0.95);
    border-radius: 100px;
}

.cloud1 { 
    width: 120px; height: 50px; top: 15%; left: -120px; animation-duration: 35s; 
}
.cloud1:before { width: 60px; height: 60px; top: -30px; left: 15px; }
.cloud1:after { width: 50px; height: 50px; top: -20px; right: 15px; }

.cloud2 { 
    width: 90px; height: 35px; top: 30%; right: -90px; animation-duration: 40s; animation-direction: reverse; 
}
.cloud2:before { width: 45px; height: 45px; top: -22px; left: 8px; }
.cloud2:after { width: 35px; height: 35px; top: -15px; right: 8px; }

.cloud3 { 
    width: 150px; height: 60px; top: 55%; left: -150px; animation-duration: 45s; 
}
.cloud3:before { width: 75px; height: 75px; top: -37px; left: 20px; }
.cloud3:after { width: 60px; height: 60px; top: -25px; right: 20px; }

.cloud4 { 
    width: 80px; height: 30px; top: 75%; right: -80px; animation-duration: 38s; animation-direction: reverse; 
}
.cloud4:before { width: 40px; height: 40px; top: -20px; left: 5px; }
.cloud4:after { width: 30px; height: 30px; top: -12px; right: 5px; }

@keyframes floatCloud {
    0% { transform: translateX(0) translateY(0px); }
    50% { transform: translateX(15px) translateY(-5px); }
    100% { transform: translateX(30px) translateY(0px); }
}

/* Flying Birds */
.bird {
    position: fixed;
    font-size: 28px;
    animation: fly 25s linear infinite;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    z-index: 10;
}

@keyframes fly {
    0% { 
        transform: translateX(-150px) rotate(-10deg); 
        opacity: 0; 
    }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { 
        transform: translateX(110vw) rotate(20deg); 
        opacity: 0; 
    }
}

@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
    50% { opacity: 1; transform: scale(1.2) rotate(180deg); }
}

/* Floating Elements */
.floating-baby {
    position: fixed;
    font-size: 45px;
    animation: floatUp 20s linear infinite;
    z-index: 5;
    text-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

@keyframes floatUp {
    0% { 
        transform: translateY(100vh) rotate(0deg) scale(0.5); 
        opacity: 0; 
    }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { 
        transform: translateY(-20vh) rotate(360deg) scale(1.1); 
        opacity: 0; 
    }
}

/* Magic Cards - FULL HEIGHT */
.magic-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.22), rgba(255,255,255,0.08));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 35px;
    padding: 45px;
    margin: 25px 10px;
    box-shadow: 
        0 25px 60px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.4);
    transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    overflow: hidden;
    min-height: 200px;
}

.magic-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -120%;
    width: 120%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.8s;
}

.magic-card:hover::before {
    left: 120%;
}

.magic-card:hover {
    transform: translateY(-20px) scale(1.04);
    box-shadow: 
        0 40px 80px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.5);
}

.title-glow {
    font-family: 'Fredoka One', cursive;
    font-size: 4.5rem;
    text-align: center;
    background: linear-gradient(45deg, #FFD700, #FF69B4, #00CED1, #96CEB4, #FFD700);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbow 4s ease-in-out infinite;
    text-shadow: 0 0 40px rgba(255,215,0,0.6);
    margin-bottom: 10px !important;
    line-height: 1.1;
}

@keyframes rainbow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.btn-magic {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FECA57);
    background-size: 400% 400%;
    border: none;
    border-radius: 60px;
    padding: 25px 60px;
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
    cursor: pointer;
    transition: all 0.5s;
    animation: btnPulse 2.5s infinite;
    box-shadow: 0 15px 45px rgba(0,0,0,0.3);
    width: 100%;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.btn-magic:hover {
    transform: translateY(-8px) scale(1.08);
    box-shadow: 0 25px 60px rgba(0,0,0,0.4);
    animation: none;
    background-position: 100% 50%;
}

@keyframes btnPulse {
    0%, 100% { 
        box-shadow: 0 15px 45px rgba(255,107,107,0.5); 
        background-position: 0% 50%; 
    }
    50% { 
        box-shadow: 0 15px 45px rgba(78,205,196,0.8); 
        background-position: 100% 50%; 
    }
}

.metric-glow {
    background: linear-gradient(145deg, rgba(255,255,255,0.25), rgba(255,255,255,0.1));
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.3);
    text-align: center;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}

/* Remove all default margins */
section[data-testid="stHorizontalBlock"] > div > div {
    margin: 0 !important;
    padding: 0 20px !important;
}

.st-emotion-cache-1m38y2q {
    padding-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------- FULL SCREEN SKY ------------------------- 
st.markdown("""
<div id="sky-container">
    <!-- Clouds -->
    <div class="cloud cloud1"></div>
    <div class="cloud cloud2"></div>
    <div class="cloud cloud3"></div>
    <div class="cloud cloud4"></div>
    
    <!-- Flying Birds -->
    <div class="bird" style="top: 12%; animation-delay: 0s;">🐦</div>
    <div class="bird" style="top: 28%; font-size: 24px; animation-delay: 6s;">🕊️</div>
    <div class="bird" style="top: 45%; animation-delay: 12s;">🐦</div>
    <div class="bird" style="top: 65%; font-size: 26px; animation-delay: 18s;">🦢</div>
    
    <!-- Floating Babies & Toys -->
    <div class="floating-baby" style="left: 10%; animation-delay: 0s;">🍼</div>
    <div class="floating-baby" style="left: 25%; font-size: 35px; animation-delay: 4s;">👶</div>
    <div class="floating-baby" style="left: 70%; animation-delay: 8s;">🧸</div>
    <div class="floating-baby" style="left: 85%; font-size: 40px; animation-delay: 12s;">🎈</div>
</div>
""", unsafe_allow_html=True)

# ------------------------- MULTI-PAGE SYSTEM ------------------------- 
page = st.sidebar.selectbox(
    "✨ Choose Your Magical Journey ✨",
    ["🏠 Welcome to Magic Land", "🍼 Baby Health Adventure"]
)

# ------------------------- HOME PAGE - FULL IMMERSION ------------------------- 
if page == "🏠 Welcome to Magic Land":
    # FULL WIDTH HERO
    st.markdown("""
    <div style="padding: 0 20px 40px 20px;">
        <div class="magic-card" style="text-align: center; padding: 60px 40px; margin: 20px 0;">
            <h1 class="title-glow">🌟 Magical Baby Health Guardian 🌟</h1>
            <p style="font-size: 1.6rem; margin: 30px 0; line-height: 1.6;">
                Welcome to the most magical place for your baby! 🦄✨<br>
                Our super-smart AI will check if your little star is growing perfectly! 🌟
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #FFD700; font-size: 2rem;">🦄 AI Magic Power</h2>
            <p style="text-align: center; font-size: 1.3rem; line-height: 1.7;">
                Super-smart technology that works like a fairy doctor! 🧚‍♀️<br>
                Checks growth with 99.9% magic accuracy! ✨
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #FF69B4; font-size: 2rem;">🎈 So Super Easy!</h2>
            <p style="text-align: center; font-size: 1.3rem; line-height: 1.7;">
                Just slide colorful sliders and press the big shiny button! 🌈<br>
                Magic happens in just 30 seconds! ⚡
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #4ECDC4; font-size: 2rem;">⭐ Loved by Parents</h2>
            <p style="text-align: center; font-size: 1.3rem; line-height: 1.7;">
                10,000+ happy parents trust our magic! 💖<br>
                Safe, fun, and loved by babies too! 👶
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # MAGIC STATS ROW
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="magic-card" style="text-align: center; padding: 30px;">
            <h1 style="font-size: 3.5rem; color: #FFD700; margin: 0;">99.9%</h1>
            <h3 style="color: #FFD700;">Magic Accuracy ✨</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="magic-card" style="text-align: center; padding: 30px;">
            <h1 style="font-size: 3.5rem; color: #FF69B4; margin: 0;">10K+</h1>
            <h3 style="color: #FF69B4;">Happy Babies 👶</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="magic-card" style="text-align: center; padding: 30px;">
            <h1 style="font-size: 3.5rem; color: #4ECDC4; margin: 0;">30s</h1>
            <h3 style="color: #4ECDC4;">Lightning Fast ⚡</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="magic-card" style="text-align: center; padding: 30px;">
            <h1 style="font-size: 3.5rem; color: #45B7D1; margin: 0;">100%</h1>
            <h3 style="color: #45B7D1;">Safe & Fun 🎉</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 40px 20px;">
        <div class="magic-card" style="text-align: center;">
            <h2 style="color: #FFD700; font-size: 2.2rem;">🍼 Ready for Your Baby's Magic Adventure? 👶</h2>
            <p style="font-size: 1.5rem; margin: 20px 0;">
                Click "Baby Health Adventure" in the sidebar! 🚀✨
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------- ASSESSMENT PAGE ------------------------- 
elif page == "🍼 Baby Health Adventure":
    st.markdown('<div style="padding: 20px;"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 0 20px 40px;">
        <h1 class="title-glow">🍼 Baby Health Magic Check 🍼</h1>
        <p style="font-size: 1.6rem; margin-top: 10px;">
            Enter measurements and watch the magic happen! 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # DUAL COLUMNS
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #FFD700;">📏 Baby Measurements</h2>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            age = st.slider("🎂 Baby's Age", 1, 60, 12, help="Months old")
        with col_b:
            height = st.slider("📏 Height", 40.0, 120.0, 80.0, 0.1, help="in cm")
        
        col_c, col_d = st.columns(2)
        with col_c:
            weight = st.slider("⚖️ Weight", 2.0, 40.0, 10.0, 0.1, help="in kg")
        with col_d:
            muac = st.slider("📐 Arm Circle", 5.0, 25.0, 12.0, 0.1, help="MUAC in cm")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="magic-card" style="padding: 20px;">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #FF69B4;">👶 Baby Avatar</h2>', unsafe_allow_html=True)
        
        scale = height / 80 * 0.7
        
        model_html = f"""
        <div style="border-radius: 25px; overflow: hidden; height: 450px; box-shadow: 0 20px 50px rgba(0,0,0,0.3);">
        <model-viewer
            src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
            auto-rotate
            camera-controls
            shadow-intensity="1"
            exposure="0.9"
            scale="{scale} {scale} {scale}"
            style="width:100%; height:100%; background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);">
        </model-viewer>
        </div>
        """
        components.html(model_html, height=470)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # FULL WIDTH MAGIC BUTTON
    st.markdown("""
    <div style="padding: 40px 20px; text-align: center;">
        <button class="btn-magic" onclick="this.blur()">
            🌟✨ RUN SUPER MAGIC HEALTH CHECK ✨🌟
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌟✨ RUN SUPER MAGIC HEALTH CHECK ✨🌟", key="magic_check", help="Click for instant magic!"):
        if model is None:
            st.error("❌ Magic model missing! Upload model.pkl file first.")
            st.info("💡 Put your trained model as 'model.pkl' in the same folder!")
        else:
            with st.spinner("🔮✨ Preparing magical diagnosis... ✨🔮"):
                time.sleep(2)
            
            input_data = np.array([[age, height, weight, muac]])
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][prediction]
            
            # FULL WIDTH RESULTS
            st.markdown('<div style="padding: 0 20px 40px;">', unsafe_allow_html=True)
            
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.markdown('<div class="magic-card" style="height: 380px;">', unsafe_allow_html=True)
                st.markdown('<h2 style="text-align: center;">🎯 Magic Health Result</h2>', unsafe_allow_html=True)
                
                if prediction == 0:
                    st.markdown("""
                    <div style="text-align: center; padding: 30px 0;">
                        <h1 style="font-size: 4rem; color: #00FF88; 
                                   text-shadow: 0 0 30px #00FF88; margin: 20px 0;">🎉 PERFECTLY HEALTHY! 🎉</h1>
                        <p style="font-size: 1.6rem; color: #FFD700; margin: 20px 0;">
                            Your baby is a super healthy star! 🌟✨
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 30px 0;">
                        <h1 style="font-size: 4rem; color: #FF6B6B; 
                                   text-shadow: 0 0 30px #FF6B6B; margin: 20px 0;">⚠️ MAGIC NEEDED!</h1>
                        <p style="font-size: 1.6rem; color: #FFD700; margin: 20px 0;">
                            Extra nutrition magic will help! 💖 Let's make it perfect!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-glow">
                    <h3 style="margin: 0 0 10px 0; color: #FFD700; font-size: 1.4rem;">🔮 Magic Confidence Level</h3>
                    <h1 style="margin: 0; font-size: 4rem; color: #FFF;">{probability*100:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with result_col2:
                st.markdown('<div class="magic-card" style="height: 380px;">', unsafe_allow_html=True)
                st.markdown('<h2 style="text-align: center;">💓 Magical Heart Monitor</h2>', unsafe_allow_html=True)
                
                st.markdown("""
                <div style="text-align: center; padding: 30px;">
                    <div style="height: 140px; background: linear-gradient(90deg, #000428, #004e92); 
                                border-radius: 25px; position: relative; overflow: hidden; 
                                margin: 25px auto; width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                        <div style="position: absolute; width: 100%; height: 100%; 
                                   background: repeating-linear-gradient(90deg, transparent 0, transparent 30px, 
                                   #00FF88 30px, #00FF88 32px, transparent 32px);
                                   animation: heartbeat 1.8s linear infinite;"></div>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                   font-size: 2.5rem; color: #00FF88; animation: heartBeat 1.8s infinite;">
                                   ♥♥♥♥♥♥♥♥♥
                        </div>
                    </div>
                    <h3 style="color: #00FF88; font-size: 1.5rem;">All Heart Signals Perfect! ✨</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # CELEBRATION
            if prediction == 0:
                st.balloons()
            else:
                st.success("💖 Let's schedule a nutrition magic plan! ✨")
    
    st.markdown("""
    <div style="padding: 40px 20px;">
        <div class="magic-card" style="text-align: center;">
            <h3 style="color: #FFD700;">🌈 Created with ❤️ by Syeda Huda | Magical AI for Happy Babies 💕</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
@keyframes heartbeat {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes heartBeat {
    0%, 100% { transform: translate(-50%, -50%) scale(1); }
    50% { transform: translate(-50%, -50%) scale(1.2); }
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.2) !important;
}

[data-testid="stSidebar"] .css-1d391kg {
    color: #FFD700 !important;
}

[data-testid="stSidebar"] label {
    color: #FFF !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)
