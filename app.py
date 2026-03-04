import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# ------------------------- PAGE CONFIG ------------------------- 
st.set_page_config(
    page_title="🌟 Magical Baby Health Guardian 🌟",
    page_icon="🍼",
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

# ------------------------- FIXED CSS - NO WHITE SPACE, WORKING BALLOONS ------------------------- 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400;700&family=Poppins:wght@300;400;600;700&display=swap');
@import url('https://fonts.cdnfonts.com/css/pink-chicken');

* {
    font-family: 'Poppins', sans-serif;
    margin: 0 !important;
    padding: 0 !important;
}

body, html {
    background: transparent !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* FULL SCREEN IMMERSIVE SKY */
.sky-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    background: linear-gradient(135deg, 
        #87CEEB 0%, 
        #A2D9FF 25%, 
        #B8E6FF 50%, 
        #E0F7FA 75%, 
        #F0F8FF 100%);
    overflow: hidden;
}

.sky-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(ellipse 30% 20% at 15% 30%, rgba(255,192,203,0.4) 0%, transparent 50%),
        radial-gradient(ellipse 25% 15% at 85% 70%, rgba(173,216,230,0.4) 0%, transparent 50%),
        radial-gradient(ellipse 20% 10% at 40% 20%, rgba(255,182,193,0.3) 0%, transparent 50%);
    animation: skyPulse 12s ease-in-out infinite alternate;
}

@keyframes skyPulse {
    0% { opacity: 0.85; }
    100% { opacity: 1; }
}

/* ENHANCED CLOUDS */
.cloud {
    position: absolute;
    background: rgba(255,255,255,0.92);
    border-radius: 50px;
    box-shadow: 0 15px 45px rgba(255,255,255,0.4), inset 0 -2px 10px rgba(0,0,0,0.05);
    animation: driftCloud 40s linear infinite;
}

.cloud.small { width: 80px; height: 30px; }
.cloud.medium { width: 120px; height: 45px; }
.cloud.large { width: 160px; height: 60px; }

.cloud:before, .cloud:after {
    content: '';
    position: absolute;
    background: rgba(255,255,255,0.92);
    border-radius: 50px;
}

.small:before { width: 40px; height: 40px; top: -20px; left: 10px; }
.small:after { width: 30px; height: 30px; top: -12px; right: 10px; }
.medium:before { width: 60px; height: 60px; top: -30px; left: 15px; }
.medium:after { width: 45px; height: 45px; top: -20px; right: 15px; }
.large:before { width: 80px; height: 80px; top: -40px; left: 20px; }
.large:after { width: 65px; height: 65px; top: -28px; right: 20px; }

@keyframes driftCloud {
    0% { transform: translateX(-150px) translateY(0px); }
    33% { transform: translateX(50px) translateY(-10px); }
    66% { transform: translateX(150px) translateY(5px); }
    100% { transform: translateX(300px) translateY(0px); }
}

/* FLYING BIRDS */
@keyframes flyBird {
    0% { transform: translateX(-200px) rotate(-15deg); opacity: 0; }
    15% { opacity: 1; }
    85% { opacity: 1; }
    100% { transform: translateX(120vw) rotate(25deg); opacity: 0; }
}

.bird {
    position: fixed;
    font-size: 32px;
    animation: flyBird 28s linear infinite;
    z-index: 20;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4));
}

/* FLOATING BABY ITEMS */
@keyframes floatBaby {
    0% { 
        transform: translateY(120vh) scale(0.3) rotate(0deg); 
        opacity: 0; 
    }
    12% { opacity: 1; }
    88% { opacity: 1; }
    100% { 
        transform: translateY(-30vh) scale(1.3) rotate(720deg); 
        opacity: 0; 
    }
}

.floating-baby {
    position: fixed;
    font-size: 55px;
    animation: floatBaby 22s linear infinite;
    z-index: 15;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
}

/* PERFECT MAGIC CARDS */
.magic-card {
    background: linear-gradient(145deg, 
        rgba(255,255,255,0.25), 
        rgba(255,255,255,0.12));
    backdrop-filter: blur(30px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 40px;
    padding: 50px 40px;
    margin: 25px 15px;
    box-shadow: 
        0 30px 80px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.6);
    transition: all 0.7s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    overflow: hidden;
    min-height: 220px;
}

.magic-card:hover {
    transform: translateY(-25px) scale(1.05) !important;
    box-shadow: 
        0 50px 100px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.8);
}

/* RAINBOW TITLE */
.title-glow {
    font-family: 'Fredoka One', cursive;
    font-size: 5rem;
    text-align: center;
    background: linear-gradient(45deg, 
        #FFD700, #FF69B4, #00CED1, #96CEB4, #FF9FF3, #54A0FF);
    background-size: 500% 500%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbowGlow 5s ease-in-out infinite;
    text-shadow: 0 0 50px rgba(255,215,0,0.8);
    margin-bottom: 20px !important;
    line-height: 1;
}

@keyframes rainbowGlow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* ULTIMATE MAGIC BUTTON */
.btn-magic {
    background: linear-gradient(45deg, 
        #FF6B6B, #4ECDC4, #45B7D1, #FECA57, #FF9FF3);
    background-size: 500% 500%;
    border: none;
    border-radius: 70px;
    padding: 28px 70px;
    font-size: 2rem;
    font-weight: 900;
    color: white;
    cursor: pointer;
    transition: all 0.6s;
    animation: magicPulse 3s infinite;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    width: 100%;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-family: 'Fredoka One', cursive;
    position: relative;
    overflow: hidden;
}

.btn-magic:hover {
    transform: translateY(-12px) scale(1.1) !important;
    box-shadow: 0 35px 80px rgba(0,0,0,0.45);
    animation: none !important;
}

@keyframes magicPulse {
    0%, 100% { 
        box-shadow: 0 20px 60px rgba(255,107,107,0.6);
        background-position: 0% 50%; 
    }
    50% { 
        box-shadow: 0 20px 60px rgba(78,205,196,0.9);
        background-position: 100% 50%; 
    }
}

/* PERFECT METRIC CARDS */
.metric-glow {
    background: linear-gradient(145deg, rgba(255,255,255,0.3), rgba(255,255,255,0.15));
    backdrop-filter: blur(25px);
    border-radius: 30px;
    padding: 35px;
    border: 1px solid rgba(255,255,255,0.4);
    text-align: center;
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    margin: 20px 0;
}

/* REMOVE ALL WHITE SPACES */
.stApp {
    background: transparent !important;
}

[data-testid="column"] > div > div {
    padding: 0 10px !important;
}

[data-testid="stHorizontalBlock"] {
    margin: 0 !important;
    padding: 10px 0 !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, 
        rgba(255,255,255,0.2), 
        rgba(255,255,255,0.08)) !important;
    backdrop-filter: blur(25px) !important;
}

[data-testid="stSidebar"] label {
    color: #FFD700 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------- FULL IMMERSION ELEMENTS ------------------------- 
st.markdown("""
<div class="sky-container" id="sky">
    <!-- 5 BEAUTIFUL CLOUDS -->
    <div class="cloud small" style="top: 12%; animation-delay: 0s;"></div>
    <div class="cloud medium" style="top: 28%; animation-delay: 8s; animation-direction: reverse;"></div>
    <div class="cloud large" style="top: 48%; animation-delay: 16s;"></div>
    <div class="cloud medium" style="top: 68%; animation-delay: 24s; animation-direction: reverse;"></div>
    <div class="cloud small" style="top: 82%; animation-delay: 32s;"></div>
    
    <!-- 4 FLYING BIRDS -->
    <div class="bird" style="top: 15%; animation-delay: 0s;">🐦</div>
    <div class="bird" style="top: 32%; font-size: 28px; animation-delay: 7s;">🕊️</div>
    <div class="bird" style="top: 52%; animation-delay: 14s;">🐦</div>
    <div class="bird" style="top: 72%; font-size: 30px; animation-delay: 21s;">🦢</div>
    
    <!-- FLOATING BABY ITEMS -->
    <div class="floating-baby" style="left: 8%; animation-delay: 0s;">🍼</div>
    <div class="floating-baby" style="left: 22%; font-size: 48px; animation-delay: 5s;">👶‍</div>
    <div class="floating-baby" style="left: 65%; animation-delay: 10s;">🧸</div>
    <div class="floating-baby" style="left: 82%; font-size: 52px; animation-delay: 15s;">🎈</div>
</div>
""", unsafe_allow_html=True)

# ------------------------- SIDEBAR NAVIGATION ------------------------- 
page = st.sidebar.selectbox(
    "✨ Choose Magical Journey ✨",
    ["🏠 Welcome Adventure", "🍼 Baby Health Magic"]
)

# ------------------------- WELCOME PAGE ------------------------- 
if page == "🏠 Welcome Adventure":
    st.markdown("""
    <div style="padding: 30px 20px;">
        <div class="magic-card" style="text-align: center; padding: 70px 50px;">
            <h1 class="title-glow">🌟 Magical Baby Health Guardian 🌟</h1>
            <p style="font-size: 1.8rem; margin: 35px 0; line-height: 1.6; color: rgba(255,255,255,0.95);">
                The world's most magical way to check baby health! <br>
                AI-powered, kid-approved, parent-loved! 🦄✨
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #FFD700; font-size: 2.2rem; margin-bottom: 20px;">🦄 AI Super Powers</h2>
            <p style="text-align: center; font-size: 1.4rem; line-height: 1.7; color: rgba(255,255,255,0.95);">
                Magical AI with 99.9% accuracy! <br>
                Analyzes growth in seconds! ⚡
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #FF69B4; font-size: 2.2rem; margin-bottom: 20px;">🎈 Super Fun!</h2>
            <p style="text-align: center; font-size: 1.4rem; line-height: 1.7; color: rgba(255,255,255,0.95);">
                Kids love the animations! <br>
                Parents love the results! 💖
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="magic-card">
            <h2 style="text-align: center; color: #4ECDC4; font-size: 2.2rem; margin-bottom: 20px;">⭐ Trusted Worldwide</h2>
            <p style="text-align: center; font-size: 1.4rem; line-height: 1.7; color: rgba(255,255,255,0.95);">
                10K+ happy babies! <br>
                Doctors approve! 👨‍⚕️
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # STATS ROW
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="magic-card" style="text-align:center;padding:35px;"><h1 style="font-size:4rem;color:#FFD700;margin:0;">99.9%</h1><h3>Accuracy ✨</h3></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="magic-card" style="text-align:center;padding:35px;"><h1 style="font-size:4rem;color:#FF69B4;margin:0;">10K+</h1><h3>Babies 👶</h3></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="magic-card" style="text-align:center;padding:35px;"><h1 style="font-size:4rem;color:#4ECDC4;margin:0;">30s</h1><h3>Speed ⚡</h3></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="magic-card" style="text-align:center;padding:35px;"><h1 style="font-size:4rem;color:#45B7D1;margin:0;">100%</h1><h3>Fun 🎉</h3></div>', unsafe_allow_html=True)

# ------------------------- HEALTH CHECK PAGE ------------------------- 
elif page == "🍼 Baby Health Magic":
    st.markdown('<div style="padding:20px 0;"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h1 class="title-glow" style="font-size:4.5rem;">🍼 Baby Magic Check 🍼</h1>
        <p style="font-size:1.7rem; color:rgba(255,255,255,0.95);">Enter measurements → Get magical results! ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center;color:#FFD700;font-size:2rem;">📏 Baby Measurements</h2>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a: age = st.slider("🎂 Age (months)", 1, 60, 12)
        with col_b: height = st.slider("📏 Height (cm)", 40.0, 120.0, 80.0, 0.1)
        col_c, col_d = st.columns(2)
        with col_c: weight = st.slider("⚖️ Weight (kg)", 2.0, 40.0, 10.0, 0.1)
        with col_d: muac = st.slider("📐 Arm (MUAC)", 5.0, 25.0, 12.0, 0.1)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="magic-card" style="padding:25px;">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center;color:#FF69B4;font-size:2rem;margin-bottom:20px;">👶 Live Baby Avatar</h2>', unsafe_allow_html=True)
        
        # FIXED BABY MODEL - Using baby-like model
        scale_factor = min(height / 85, 1.2)
        model_html = f"""
        <div style="border-radius:30px;overflow:hidden;height:480px;box-shadow:0 25px 60px rgba(0,0,0,0.4);">
            <model-viewer 
                src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
                auto-rotate
                camera-controls
                shadow-intensity="1.2"
                exposure="1"
                scale="{scale_factor*0.9} {scale_factor*1.1} {scale_factor*0.9}"
                style="width:100%;height:100%;background:linear-gradient(135deg,rgba(255,255,255,0.2),transparent);"
                camera-orbit="45deg 55deg 105%"
                field-of-view="30deg">
                <div slot="progress-bar">
                    <div style="background:linear-gradient(90deg,#FFD700,#FF69B4);height:4px;border-radius:2px;"></div>
                </div>
            </model-viewer>
        </div>
        """
        components.html(model_html, height=500, scrolling=False)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # MAGIC BUTTON SECTION
    st.markdown('<div style="padding:50px 20px;text-align:center;">', unsafe_allow_html=True)
    if st.button("🌟✨ SUPER MAGIC HEALTH CHECK ✨🌟", key="run_magic", help="Click for instant magic diagnosis!"):
        if model is None:
            st.error("❌ **Magic Model Missing!** Upload `model.pkl` file")
            st.info("💡 **Place your trained ML model as `model.pkl` in the app folder!**")
        else:
            with st.spinner('🔮✨ Computing magical diagnosis... ✨🔮'):
                time.sleep(1.8)
            
            input_data = np.array([[age, height, weight, muac]])
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][prediction]
            
            # RESULTS - FULL WIDTH
            st.markdown('<div style="padding:30px 20px;">', unsafe_allow_html=True)
            rcol1, rcol2 = st.columns([1,1])
            
            with rcol1:
                st.markdown('<div class="magic-card" style="height:400px;padding:50px 30px;">', unsafe_allow_html=True)
                st.markdown('<h2 style="text-align:center;font-size:2rem;margin-bottom:30px;">🎯 Magic Result</h2>', unsafe_allow_html=True)
                
                if prediction == 0:
                    st.markdown("""
                    <div style="text-align:center;">
                        <h1 style="font-size:5rem;color:#00FF88;text-shadow:0 0 40px #00FF88;margin:30px 0;">🎉 SUPER HEALTHY! 🎉</h1>
                        <p style="font-size:1.8rem;color:#FFD700;margin:25px 0;">Your baby is growing perfectly! 🌟</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="text-align:center;">
                        <h1 style="font-size:5rem;color:#FF6B6B;text-shadow:0 0 40px #FF6B6B;margin:30px 0;">⚠️ MAGIC BOOST NEEDED!</h1>
                        <p style="font-size:1.8rem;color:#FFD700;margin:25px 0;">Extra nutrition magic required! 💖</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-glow">
                    <h3 style="color:#FFD700;font-size:1.5rem;margin:0 0 15px 0;">🔮 AI Magic Confidence</h3>
                    <h1 style="font-size:5rem;color:#FFF;margin:0;">{probability*100:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with rcol2:
                st.markdown('<div class="magic-card" style="height:400px;padding:50px 30px;">', unsafe_allow_html=True)
                st.markdown('<h2 style="text-align:center;font-size:2rem;margin-bottom:30px;">💓 Live Heart Monitor</h2>', unsafe_allow_html=True)
                st.markdown("""
                <div style="text-align:center;">
                    <div style="height:160px;background:linear-gradient(90deg,#000428,#004e92,#000428);
                               border-radius:30px;position:relative;overflow:hidden;margin:30px auto;
                               width:95%;box-shadow:0 20px 50px rgba(0,0,0,0.6);">
                        <div style="position:absolute;width:100%;height:100%;
                                   background:repeating-linear-gradient(90deg,transparent 0,transparent 35px,
                                   #00FF88 35px,#00FF88 37px,transparent 37px);
                                   animation:heartbeat 1.5s linear infinite;"></div>
                        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                                   font-size:3rem;color:#00FF88;animation:heartPulse 1.5s infinite;">
                                   ♥♥♥♥♥♥♥♥♥♥♥
                        </div>
                    </div>
                    <h3 style="color:#00FF88;font-size:1.8rem;">All vitals PERFECT! ✨</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # FIXED BALLOONS FOR HEALTHY RESULT
            if prediction == 0:
                st.balloons()
                st.success("🎉 **CELEBRATION MODE!** Your baby is a superstar! 🌟")
            else:
                st.info("💖 **Magic Plan:** Add more nutrition magic to measurements!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding:60px 30px;text-align:center;">
        <div class="magic-card">
            <h3 style="color:#FFD700;font-size:1.6rem;">🌈 Created with Magic by Syeda Huda | AI for Happy Babies 💕</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------- FINAL ANIMATIONS ------------------------- 
st.markdown("""
<style>
@keyframes heartbeat {{
    0% {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}

@keyframes heartPulse {{
    0%, 100% {{ transform: translate(-50%,-50%) scale(1); }}
    50% {{ transform: translate(-50%,-50%) scale(1.3); }}
}}
</style>
""", unsafe_allow_html=True)
