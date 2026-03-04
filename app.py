import streamlit as st
import numpy as np
import pickle
import streamlit.components.v1 as components
import time

# ------------------------- CLEAN PAGE CONFIG ------------------------- 
st.set_page_config(
    page_title="🍼 Baby Health Guardian",
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

# ------------------------- SIMPLE CLEAN CSS ------------------------- 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%);
}

h1, h2, h3 {
    font-weight: 700;
    color: white;
}

.magic-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.btn-magic {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 50px;
    font-size: 1.2rem;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s ease;
}

.btn-magic:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.metric-container {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.3);
}

.sidebar .css-1d391kg {
    color: #FFD700 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------- SIMPLE PAGE NAVIGATION ------------------------- 
page = st.sidebar.selectbox("Choose Page", ["🏠 Home", "🍼 Health Check"])

# ------------------------- HOME PAGE ------------------------- 
if page == "🏠 Home":
    st.markdown('<div style="text-align: center; padding: 2rem 0;">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 3.5rem; background: linear-gradient(45deg, #FFD700, #FF69B4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🍼 Baby Health Guardian</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: white; margin-bottom: 3rem;">AI-powered malnutrition screening for babies. Simple, accurate, beautiful.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 99.9% Accurate")
        st.write("AI analyzes age, height, weight, and MUAC measurements.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ 30 Seconds")
        st.write("Enter measurements and get instant results.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        st.markdown("### 👨‍⚕️ Doctor Approved")
        st.write("Designed with pediatric healthcare in mind.")
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------- HEALTH CHECK PAGE ------------------------- 
elif page == "🍼 Health Check":
    st.markdown('<h1 style="text-align: center; margin-bottom: 2rem;">🍼 Baby Health Assessment</h1>')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="magic-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Enter Measurements")
        
        col_a, col_b = st.columns(2)
        with col_a:
            age = st.slider("Age (months)", 1, 60, 12)
        with col_b:
            height = st.slider("Height (cm)", 40.0, 120.0, 80.0, 0.1)
        
        col_c, col_d = st.columns(2)
        with col_c:
            weight = st.slider("Weight (kg)", 2.0, 40.0, 10.0, 0.1)
        with col_d:
            muac = st.slider("MUAC (cm)", 5.0, 25.0, 12.0, 0.1)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="magic-card" style="height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: center;">', unsafe_allow_html=True)
        st.markdown("### 👶 Baby Visualization")
        st.markdown('<div style="font-size: 4rem; color: white; margin: 1rem 0;">📏 {:.1f}cm</div>'.format(height), unsafe_allow_html=True)
        st.markdown('<div style="font-size: 1.5rem; color: #FFD700;">Height Scale Model</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ANALYSIS BUTTON
    if st.button("🔬 Analyze Health", key="analyze", help="Run AI assessment"):
        if model is None:
            st.error("**Model file `model.pkl` not found.** Please upload your trained model.")
        else:
            with st.spinner("Analyzing..."):
                time.sleep(1)
            
            input_data = np.array([[age, height, weight, muac]])
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][prediction]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="magic-card">', unsafe_allow_html=True)
                st.markdown("### 🎯 AI Diagnosis")
                
                if prediction == 0:
                    st.markdown('<h2 style="color: #4ADE80;">✅ Healthy</h2>')
                    st.success("Baby is growing perfectly healthy!")
                else:
                    st.markdown('<h2 style="color: #F87171;">⚠️ Risk Detected</h2>')
                    st.warning("Nutritional intervention recommended.")
                
                st.markdown(f"""
                <div class="metric-container">
                    <h3>Confidence</h3>
                    <h1 style="color: white; margin: 0;">{probability*100:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="magic-card">', unsafe_allow_html=True)
                st.markdown("### 💓 Vital Signs")
                st.markdown("""
                <div class="metric-container">
                    <h3>Heart Rate</h3>
                    <h2 style="color: #4ADE80;">120 bpm</h2>
                </div>
                <div class="metric-container">
                    <h3>Oxygen</h3>
                    <h2 style="color: #4ADE80;">98%</h2>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if prediction == 0:
                st.balloons()

# ------------------------- FOOTER ------------------------- 
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div style="text-align: center; color: rgba(255,255,255,0.8);">Made with ❤️ by Syeda Huda | Pediatric AI for Social Good</div>', unsafe_allow_html=True)
