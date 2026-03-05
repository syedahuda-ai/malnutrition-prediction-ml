import streamlit as st
import numpy as np
import pickle
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

# ------------------------- MULTI PAGE -------------------------
page = st.sidebar.selectbox(
    "✨ Choose Your Adventure ✨",
    ["🏠 Magical Welcome", "🍼 Baby Health Check"]
)

# ------------------------- GLOBAL CSS -------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Poppins:wght@300;400;600;700&display=swap');

*{
font-family:'Poppins',sans-serif;
}

body{
background:linear-gradient(-45deg,#667eea,#764ba2,#f093fb,#f5576c,#4facfe);
background-size:400% 400%;
animation:gradientShift 15s ease infinite;
color:white;
overflow-x:hidden;
}

@keyframes gradientShift{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

/* SKY BACKGROUND */

.sky-bg{
position:fixed;
top:0;
left:0;
width:100vw;
height:100vh;
z-index:-2;
background:linear-gradient(135deg,#87CEEB,#98D8C8,#F0F8FF);
}

/* CLOUDS */

.cloud{
position:fixed;
background:white;
border-radius:100px;
opacity:0.9;
animation:floatCloud 25s linear infinite;
z-index:-1;
}

.cloud1{width:100px;height:40px;top:10%;left:-100px;}
.cloud2{width:80px;height:30px;top:25%;right:-100px;animation-direction:reverse;}
.cloud3{width:120px;height:50px;top:60%;left:-150px;}

@keyframes floatCloud{
0%{transform:translateX(-100px);}
100%{transform:translateX(110vw);}
}

/* BIRDS */

.bird{
position:fixed;
font-size:18px;
animation:fly 15s linear infinite;
z-index:1;
}

@keyframes fly{
0%{transform:translateY(-100px);opacity:0;}
10%{opacity:1;}
90%{opacity:1;}
100%{transform:translateY(110vh);opacity:0;}
}

/* MAGIC CARD */

.magic-card{
background:linear-gradient(135deg,rgba(255,255,255,0.15),rgba(255,255,255,0.05));
backdrop-filter:blur(20px);
border-radius:30px;
padding:40px;
margin:20px 0;
box-shadow:0 25px 50px rgba(0,0,0,0.2);
transition:0.4s;
}

.magic-card:hover{
transform:translateY(-10px);
}

/* TITLE */

.title-glow{
font-family:'Fredoka One',cursive;
font-size:4rem;
text-align:center;
background:linear-gradient(45deg,#FFD700,#FF69B4,#00CED1);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

/* STARS */

.star{
position:fixed;
color:#FFD700;
font-size:18px;
animation:sparkle 3s linear infinite;
}

@keyframes sparkle{
0%,100%{opacity:0;transform:scale(0);}
50%{opacity:1;transform:scale(1);}
}

</style>
""", unsafe_allow_html=True)

# ------------------------- SKY ELEMENTS -------------------------
def render_sky():

    st.markdown("""
    <div class="sky-bg"></div>

    <div class="cloud cloud1"></div>
    <div class="cloud cloud2"></div>
    <div class="cloud cloud3"></div>

    <!-- Birds moving vertically -->
    <div class="bird" style="left:20%;animation-delay:0s;">🐦</div>
    <div class="bird" style="left:50%;animation-delay:4s;">🕊️</div>
    <div class="bird" style="left:80%;animation-delay:8s;">🐦</div>

    """, unsafe_allow_html=True)

    for i in range(8):
        st.markdown(
            f'<div class="star" style="left:{i*12.5}%;top:{i*15+5}%;animation-delay:{i*0.3}s;">✨</div>',
            unsafe_allow_html=True
        )

render_sky()

# ------------------------- HOME PAGE -------------------------
if page == "🏠 Magical Welcome":

    st.markdown('<h1 class="title-glow">🌟 Magical Baby Health Guardian 🌟</h1>', unsafe_allow_html=True)

    col1,col2,col3=st.columns(3)

    with col1:
        st.markdown("""
        <div class="magic-card">
        <h2 style="text-align:center;">🦄 AI Powered Magic</h2>
        <p style="text-align:center;">Our AI checks if your baby is growing healthy and strong!</p>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="magic-card">
        <h2 style="text-align:center;">🎈 Super Easy</h2>
        <p style="text-align:center;">Use the sliders and run the magic health check.</p>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="magic-card">
        <h2 style="text-align:center;">⭐ Trusted</h2>
        <p style="text-align:center;">Helping parents monitor baby growth.</p>
        </div>
        """,unsafe_allow_html=True)

# ------------------------- HEALTH CHECK PAGE -------------------------
elif page == "🍼 Baby Health Check":

    st.markdown('<h1 class="title-glow">🍼 Baby Health Magic Check</h1>', unsafe_allow_html=True)

    col1,col2=st.columns(2)

    # INPUTS
    with col1:

        st.markdown('<div class="magic-card">',unsafe_allow_html=True)

        age=st.slider("🎂 Age (Months)",1,60,12)
        height=st.slider("📐 Height (cm)",40.0,120.0,80.0)
        weight=st.slider("⚖️ Weight (kg)",2.0,40.0,10.0)
        muac=st.slider("📏 MUAC (cm)",5.0,25.0,12.0)

        st.markdown('</div>',unsafe_allow_html=True)

    # 3D AVATAR
    with col2:

        st.markdown("""
        <div class="magic-card">
        <h2 style="text-align:center;">👶 Your Baby Avatar</h2>
        </div>
        """,unsafe_allow_html=True)

        scale=height/80

        model_html=f"""

        <script type="module"
        src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

        <model-viewer
        src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        auto-rotate
        camera-controls
        shadow-intensity="1"
        exposure="0.8"
        scale="0.8 {scale*0.6} 0.8"
        style="width:100%;height:500px;">
        </model-viewer>

        """

        components.html(model_html,height=520)

    # PREDICTION BUTTON
    if st.button("🌟 RUN MAGICAL HEALTH CHECK 🌟"):

        if model is None:

            st.error("Model file not found")

        else:

            with st.spinner("Running AI prediction..."):
                time.sleep(1)

            input_data=np.array([[age,height,weight,muac]])

            prediction=model.predict(input_data)[0]
            probability=model.predict_proba(input_data)[0][prediction]

            st.markdown('<div class="magic-card">',unsafe_allow_html=True)

            if prediction==0:

                st.success("🎉 Baby is Healthy!")

            else:

                st.warning("⚠️ Baby may need nutritional attention.")

            st.metric("Confidence",f"{probability*100:.1f}%")

            st.markdown('</div>',unsafe_allow_html=True)

            st.balloons()

st.markdown("""
<div style="text-align:center;margin-top:40px;">
Made with ❤️ by Syeda Huda
</div>
""",unsafe_allow_html=True)
