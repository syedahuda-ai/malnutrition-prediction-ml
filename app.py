import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.stats import zscore
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NutriScan AI — Child Malnutrition Detector",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  —  dark medical-tech aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT ── */
:root {
  --bg:        #f5f7ff;
  --surface:   #eef1fb;
  --card:      #ffffff;
  --border:    #d4daf5;
  --accent:    #5b8dee;
  --accent2:   #9b72e8;
  --danger:    #f5476a;
  --warn:      #f5a623;
  --safe:      #2ec27e;
  --text:      #2d3561;
  --muted:     #7a86c0;
  --font-head: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
}

/* ── BODY ── */
html, body, [class*="css"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font-body) !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── HERO BANNER ── */
.hero {
  background: linear-gradient(135deg, #e8eeff 0%, #f0eaff 40%, #e8f4ff 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3rem 3.5rem;
  margin-bottom: 2.5rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(91,141,238,0.12) 0%, transparent 70%);
  border-radius: 50%;
}
.hero::after {
  content: '';
  position: absolute;
  bottom: -40px; left: 30%;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(155,114,232,0.10) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-tag {
  display: inline-block;
  background: rgba(91,141,238,0.12);
  border: 1px solid rgba(91,141,238,0.3);
  color: var(--accent) !important;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.3rem 0.9rem;
  border-radius: 999px;
  margin-bottom: 1rem;
}
.hero h1 {
  font-family: var(--font-head) !important;
  font-size: clamp(2rem, 4vw, 3.2rem) !important;
  font-weight: 800 !important;
  color: var(--text) !important;
  line-height: 1.1 !important;
  margin: 0.4rem 0 1rem 0 !important;
}
.hero h1 span { color: var(--accent); }
.hero p {
  font-size: 1.05rem;
  color: var(--muted) !important;
  max-width: 620px;
  line-height: 1.7;
  margin: 0 !important;
}

/* ── METRIC CARD ── */
.metric-row { display: flex; gap: 1.2rem; margin-bottom: 2rem; flex-wrap: wrap; }
.metric-card {
  flex: 1; min-width: 150px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem 1.5rem;
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute; top: 0; left: 0;
  width: 3px; height: 100%;
  background: var(--accent);
}
.metric-card.danger::before { background: var(--danger); }
.metric-card.warn::before   { background: var(--warn); }
.metric-card.safe::before   { background: var(--safe); }
.metric-card.purple::before { background: var(--accent2); }
.metric-label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted) !important;
  margin-bottom: 0.4rem;
}
.metric-value {
  font-family: var(--font-head) !important;
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--text) !important;
.metric-sub { font-size: 0.78rem; color: var(--muted) !important; margin-top: 0.3rem; }

/* ── SECTION HEADER ── */
.section-head {
  font-family: var(--font-head) !important;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text) !important;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.7rem;
  margin-bottom: 1.5rem !important;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.section-head span { color: var(--accent); }

/* ── RESULT BADGE ── */
.result-box {
  border-radius: 16px;
  padding: 2rem 2.5rem;
  margin: 1.5rem 0;
  border: 1px solid;
  position: relative;
  overflow: hidden;
}
.result-box.healthy {
  background: rgba(0,230,118,0.06);
  border-color: rgba(0,230,118,0.3);
}
.result-box.moderate {
  background: rgba(255,179,71,0.06);
  border-color: rgba(255,179,71,0.3);
}
.result-box.severe {
  background: rgba(255,68,102,0.06);
  border-color: rgba(255,68,102,0.3);
}
.result-title {
  font-family: var(--font-head) !important;
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}
.result-title.healthy  { color: var(--safe) !important; }
.result-title.moderate { color: var(--warn) !important; }
.result-title.severe   { color: var(--danger) !important; }
.result-desc { color: var(--muted) !important; font-size: 0.95rem; line-height: 1.6; }

/* ── WHO TABLE ── */
.who-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.who-table th {
  background: var(--surface);
  color: var(--accent) !important;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.7rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.who-table td {
  padding: 0.65rem 1rem;
  border-bottom: 1px solid var(--border);
  color: var(--text) !important;
}
.who-table tr:hover td { background: rgba(0,212,255,0.04); }

/* ── INPUT OVERRIDES ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
.stSlider {
  background: var(--card) !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
}
label { color: var(--muted) !important; font-size: 0.85rem !important; font-weight: 500 !important; }

/* ── BUTTON ── */
.stButton > button {
  background: linear-gradient(135deg, #5b8dee, #4a7ddc) !important;
  color: #fff !important;
  font-family: var(--font-head) !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.65rem 2rem !important;
  width: 100% !important;
  letter-spacing: 0.05em;
  transition: all 0.2s ease;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #7aaaf5, #5b8dee) !important;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(91,141,238,0.3) !important;
}

/* ── UPLOAD ZONE ── */
[data-testid="stFileUploader"] {
  background: var(--card) !important;
  border: 2px dashed var(--border) !important;
  border-radius: 14px !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── TABS ── */
[data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px; }
[data-baseweb="tab"] { color: var(--muted) !important; }
[aria-selected="true"][data-baseweb="tab"] { color: var(--accent) !important; }

/* ── INFO BOX ── */
.info-pill {
  display: inline-block;
  background: rgba(91,141,238,0.08);
  border: 1px solid rgba(91,141,238,0.2);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.82rem;
  color: var(--accent) !important;
  margin: 0.3rem 0;
}

/* ── PLOTLY CHART CONTAINER ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── FOOTER ── */
.app-footer {
  text-align: center;
  padding: 2rem 0 1rem 0;
  color: var(--muted) !important;
  font-size: 0.78rem;
  border-top: 1px solid var(--border);
  margin-top: 3rem;
}
.app-footer a { color: var(--accent) !important; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS & MODEL
# ─────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(238,241,251,0.8)",
    font=dict(family="DM Sans", color="#7a86c0", size=12),
    xaxis=dict(gridcolor="#d4daf5", zerolinecolor="#d4daf5"),
    yaxis=dict(gridcolor="#d4daf5", zerolinecolor="#d4daf5"),
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(bgcolor="#ffffff", bordercolor="#d4daf5", font_color="#2d3561"),
)


def classify_muac(muac: float) -> str:
    if muac < 11.5:
        return "severe"
    elif muac < 12.5:
        return "moderate"
    else:
        return "healthy"


def classify_wfa(age_months: float, weight: float) -> str:
    """Rough WHO weight-for-age z-score approximation for children 0-60 months."""
    median = 3.3 + 0.19 * age_months - 0.0013 * age_months ** 2
    sd = 0.45 + 0.008 * age_months
    z = (weight - median) / sd
    if z < -3:
        return "severe"
    elif z < -2:
        return "moderate"
    else:
        return "healthy"


@st.cache_resource
def get_reference_model():
    """Build a GMM trained on WHO synthetic reference data (no external file needed)."""
    rng = np.random.default_rng(42)
    n = 800

    # Healthy children (0-60 months)
    ages_h = rng.uniform(0, 60, n)
    weights_h = 3.3 + 0.19 * ages_h - 0.0013 * ages_h**2 + rng.normal(0, 0.6, n)
    heights_h = 50 + 0.45 * ages_h + rng.normal(0, 1.5, n)
    muac_h = 13.5 + 0.02 * ages_h + rng.normal(0, 0.5, n)

    # Moderate malnutrition
    weights_m = (3.3 + 0.19 * ages_h - 0.0013 * ages_h**2) * 0.82 + rng.normal(0, 0.5, n)
    heights_m = (50 + 0.45 * ages_h) * 0.97 + rng.normal(0, 1.2, n)
    muac_m = 11.8 + 0.01 * ages_h + rng.normal(0, 0.3, n)

    # Severe malnutrition
    weights_s = (3.3 + 0.19 * ages_h - 0.0013 * ages_h**2) * 0.65 + rng.normal(0, 0.4, n)
    heights_s = (50 + 0.45 * ages_h) * 0.93 + rng.normal(0, 1.0, n)
    muac_s = 10.8 + 0.005 * ages_h + rng.normal(0, 0.3, n)

    df_ref = pd.DataFrame({
        "AGE":    np.concatenate([ages_h, ages_h, ages_h]),
        "WEIGHT": np.concatenate([weights_h, weights_m, weights_s]),
        "HEIGHT": np.concatenate([heights_h, heights_m, heights_s]),
        "MUAC":   np.concatenate([muac_h, muac_m, muac_s]),
    })
    df_ref = df_ref.clip(lower=0)

    scaler = StandardScaler()
    X = scaler.fit_transform(df_ref)
    gmm = GaussianMixture(n_components=3, random_state=42, n_init=5)
    gmm.fit(X)

    # Label clusters by MUAC mean (lowest = severe)
    df_ref["cluster"] = gmm.predict(X)
    muac_means = df_ref.groupby("cluster")["MUAC"].mean().sort_values()
    label_map = {
        muac_means.index[0]: "severe",
        muac_means.index[1]: "moderate",
        muac_means.index[2]: "healthy",
    }
    return gmm, scaler, label_map, df_ref


def predict_child(age, weight, height, muac):
    gmm, scaler, label_map, _ = get_reference_model()
    x = np.array([[age, weight, height, muac]])
    x_scaled = scaler.transform(x)
    cluster = gmm.predict(x_scaled)[0]
    proba = gmm.predict_proba(x_scaled)[0]
    status = label_map[cluster]
    return status, proba, cluster


def get_recommendations(status: str, age: float, muac: float, weight: float) -> dict:
    base = {
        "healthy": {
            "icon": "✅",
            "title": "Healthy — No Malnutrition Detected",
            "summary": "This child's measurements fall within WHO healthy reference ranges.",
            "actions": [
                "Continue balanced diet with fruits, vegetables, proteins & grains",
                "Schedule routine growth monitoring every 3 months",
                "Ensure adequate micronutrient intake (iron, zinc, vitamin A)",
                "Maintain breastfeeding if child is under 24 months",
            ],
            "urgency": "Routine check-up recommended",
        },
        "moderate": {
            "icon": "⚠️",
            "title": "Moderate Acute Malnutrition (MAM)",
            "summary": "MUAC and/or weight measurements indicate moderate malnutrition. Intervention is needed.",
            "actions": [
                "Enroll in Supplementary Feeding Programme (SFP)",
                "Provide Ready-to-Use Supplementary Food (RUSF) — 500 kcal/day",
                "Screen for infections (diarrhea, pneumonia, malaria)",
                "Monitor weight weekly and MUAC every 2 weeks",
                "Provide nutrition counselling to caregivers",
            ],
            "urgency": "Clinical review within 1 week",
        },
        "severe": {
            "icon": "🚨",
            "title": "Severe Acute Malnutrition (SAM)",
            "summary": "Critical malnutrition detected. Immediate medical intervention is required.",
            "actions": [
                "URGENT: Refer to inpatient Therapeutic Feeding Centre (TFC)",
                "Initiate Ready-to-Use Therapeutic Food (RUTF) — F-75 / F-100 protocol",
                "Screen for medical complications (hypoglycaemia, hypothermia, dehydration)",
                "Administer antibiotics per WHO SAM protocol",
                "Daily clinical monitoring until stabilisation",
                "Provide intensive caregiver counselling on home care",
            ],
            "urgency": "⚠️ IMMEDIATE REFERRAL REQUIRED",
        },
    }
    return base[status]


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.2rem 0 0.5rem 0;'>
        <div style='font-size:2.8rem;'>🩺</div>
        <div style='font-family:Syne,sans-serif; font-size:1.1rem; font-weight:800; color:#fff;'>NutriScan AI</div>
        <div style='font-size:0.75rem; color:#7a86c0; margin-top:0.2rem;'>Child Malnutrition Detector</div>
    </div>
    <hr style='border-color:#d4daf5; margin: 1rem 0;'>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "**Analysis Mode**",
        ["🔍 Single Child Assessment", "📊 Batch CSV Analysis"],
        label_visibility="visible"
    )

    st.markdown("<hr style='border-color:#d4daf5; margin: 1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.8rem; color:#7a86c0; line-height:1.7;'>
    <b style='color:#2d3561;'>Features</b><br>
    • WHO MUAC thresholds<br>
    • Gaussian Mixture Model<br>
    • 3-tier severity classification<br>
    • Clinical recommendations<br>
    • Batch CSV processing<br>
    • Interactive visualisations
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#d4daf5; margin: 1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#7a86c0; text-align:center;'>
    Based on <a href='https://www.who.int/tools/child-growth-standards' style='color:#5b8dee;'>WHO Child Growth Standards</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-tag'>🤖 AI-Powered · WHO Standards · GMM Clustering</div>
    <h1>Detect Child <span>Malnutrition</span><br>in Seconds</h1>
    <p>Enter a child's anthropometric measurements — age, weight, height, and MUAC — 
    and our Gaussian Mixture Model instantly classifies nutritional status according to 
    WHO guidelines with clinical-grade recommendations.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MODEL STATS ROW
# ─────────────────────────────────────────────
gmm_model, scaler_obj, label_map_obj, ref_df = get_reference_model()
X_all = scaler_obj.transform(ref_df[["AGE", "WEIGHT", "HEIGHT", "MUAC"]])
labels_all = gmm_model.predict(X_all)
sil = silhouette_score(X_all, labels_all)
db = davies_bouldin_score(X_all, labels_all)

st.markdown(f"""
<div class='metric-row'>
  <div class='metric-card safe'>
    <div class='metric-label'>Model</div>
    <div class='metric-value'>GMM</div>
    <div class='metric-sub'>Gaussian Mixture Model</div>
  </div>
  <div class='metric-card'>
    <div class='metric-label'>Silhouette Score</div>
    <div class='metric-value'>{sil:.3f}</div>
    <div class='metric-sub'>Cluster quality (higher = better)</div>
  </div>
  <div class='metric-card warn'>
    <div class='metric-label'>Davies-Bouldin</div>
    <div class='metric-value'>{db:.3f}</div>
    <div class='metric-sub'>Separation index (lower = better)</div>
  </div>
  <div class='metric-card purple'>
    <div class='metric-label'>WHO Tiers</div>
    <div class='metric-value'>3</div>
    <div class='metric-sub'>Healthy · MAM · SAM</div>
  </div>
  <div class='metric-card danger'>
    <div class='metric-label'>Features</div>
    <div class='metric-value'>4</div>
    <div class='metric-sub'>Age · Weight · Height · MUAC</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  MODE 1 : SINGLE CHILD
# ═══════════════════════════════════════════════
if "Single" in mode:

    st.markdown("<div class='section-head'>👶 Child <span>Measurements</span></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"], help="Child's biological sex")
        age_input = st.number_input("Age (months)", min_value=0.0, max_value=60.0, value=24.0, step=0.5,
                                    help="Child age in months (0–60 months / 0–5 years)")
        weight_input = st.number_input("Weight (kg)", min_value=1.0, max_value=30.0, value=10.5, step=0.1,
                                       help="Measured weight in kilograms")

    with col2:
        height_input = st.number_input("Height (cm)", min_value=40.0, max_value=130.0, value=82.0, step=0.5,
                                       help="Measured height/length in centimetres")
        muac_input = st.number_input("MUAC (cm)", min_value=5.0, max_value=20.0, value=13.2, step=0.1,
                                     help="Mid-Upper Arm Circumference in centimetres")
        st.markdown("""
        <div class='info-pill'>💡 MUAC: measure left upper arm midpoint between shoulder & elbow</div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔬 Run Malnutrition Assessment")

    if predict_btn:
        status, proba, cluster_id = predict_child(age_input, weight_input, height_input, muac_input)
        recs = get_recommendations(status, age_input, muac_input, weight_input)

        # ── Result badge
        css_class = status
        st.markdown(f"""
        <div class='result-box {css_class}'>
            <div class='result-title {css_class}'>{recs["icon"]} {recs["title"]}</div>
            <div class='result-desc'>{recs["summary"]}</div>
            <br>
            <div class='info-pill' style='background:rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.1); color:#2d3561;'>
                ⏱ Urgency: <b>{recs["urgency"]}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2-col: probabilities + recommendations
        r1, r2 = st.columns([1, 1], gap="large")

        with r1:
            st.markdown("<div class='section-head' style='font-size:1rem;'>📈 <span>Model Confidence</span></div>", unsafe_allow_html=True)

            status_labels = ["Healthy", "Moderate MAM", "Severe SAM"]
            # Reorder by label_map
            ordered_proba = {}
            for cid, lbl in label_map_obj.items():
                ordered_proba[lbl] = proba[cid]

            bar_labels = ["Healthy", "Moderate", "Severe"]
            bar_values = [ordered_proba.get("healthy", 0), ordered_proba.get("moderate", 0), ordered_proba.get("severe", 0)]
            bar_colors = ["#00e676", "#ffb347", "#ff4466"]

            fig_bar = go.Figure(go.Bar(
                x=bar_labels,
                y=[v * 100 for v in bar_values],
                marker_color=bar_colors,
                text=[f"{v*100:.1f}%" for v in bar_values],
                textposition="outside",
            ))
            fig_bar.update_layout(
                **PLOTLY_LAYOUT,
                yaxis_title="Probability (%)",
                yaxis_range=[0, 115],
                showlegend=False,
                height=280,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with r2:
            st.markdown("<div class='section-head' style='font-size:1rem;'>🏥 <span>Clinical Recommendations</span></div>", unsafe_allow_html=True)
            for i, action in enumerate(recs["actions"], 1):
                icon = "🔴" if status == "severe" else ("🟡" if status == "moderate" else "🟢")
                st.markdown(f"""
                <div style='display:flex; gap:0.6rem; align-items:flex-start; margin-bottom:0.6rem;'>
                  <span style='font-size:0.8rem; margin-top:0.1rem;'>{icon}</span>
                  <span style='font-size:0.88rem; color:#4a5580; line-height:1.5;'>{action}</span>
                </div>
                """, unsafe_allow_html=True)

        # ── WHO Gauge
        st.markdown("<br><div class='section-head' style='font-size:1rem;'>📏 <span>WHO Threshold Check</span></div>", unsafe_allow_html=True)

        g1, g2, g3 = st.columns(3)
        with g1:
            muac_status = classify_muac(muac_input)
            muac_color = {"healthy": "#00e676", "moderate": "#ffb347", "severe": "#ff4466"}[muac_status]
            st.markdown(f"""
            <div class='metric-card' style='border-left: 3px solid {muac_color};'>
              <div class='metric-label'>MUAC Check</div>
              <div class='metric-value' style='color:{muac_color}; font-size:1.5rem;'>{muac_input} cm</div>
              <div class='metric-sub'>{"✅ Normal (≥12.5)" if muac_status=="healthy" else ("⚠️ MAM (11.5–12.5)" if muac_status=="moderate" else "🚨 SAM (<11.5)")}</div>
            </div>
            """, unsafe_allow_html=True)
        with g2:
            bmi = weight_input / ((height_input / 100) ** 2)
            bmi_color = "#00e676" if bmi >= 15 else ("#ffb347" if bmi >= 13 else "#ff4466")
            st.markdown(f"""
            <div class='metric-card' style='border-left: 3px solid {bmi_color};'>
              <div class='metric-label'>BMI</div>
              <div class='metric-value' style='color:{bmi_color}; font-size:1.5rem;'>{bmi:.1f}</div>
              <div class='metric-sub'>Weight / Height²</div>
            </div>
            """, unsafe_allow_html=True)
        with g3:
            wfa_status = classify_wfa(age_input, weight_input)
            wfa_color = {"healthy": "#00e676", "moderate": "#ffb347", "severe": "#ff4466"}[wfa_status]
            st.markdown(f"""
            <div class='metric-card' style='border-left: 3px solid {wfa_color};'>
              <div class='metric-label'>Weight-for-Age</div>
              <div class='metric-value' style='color:{wfa_color}; font-size:1.5rem;'>{weight_input} kg</div>
              <div class='metric-sub'>{"✅ Normal" if wfa_status=="healthy" else ("⚠️ Moderate" if wfa_status=="moderate" else "🚨 Severe")}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Position on reference scatter
        st.markdown("<br><div class='section-head' style='font-size:1rem;'>🗺️ <span>Population Reference Chart</span></div>", unsafe_allow_html=True)

        ref_sample = ref_df.sample(600, random_state=1).copy()
        ref_sample["label"] = ref_sample["cluster"].map(label_map_obj).str.capitalize()
        color_map = {"Healthy": "#00e676", "Moderate": "#ffb347", "Severe": "#ff4466"}

        fig_scatter = px.scatter(
            ref_sample, x="HEIGHT", y="WEIGHT",
            color="label", color_discrete_map=color_map,
            opacity=0.35, size_max=6,
            labels={"HEIGHT": "Height (cm)", "WEIGHT": "Weight (kg)", "label": "Status"},
        )
        # Add the child's point
        child_color = {"healthy": "#00e676", "moderate": "#ffb347", "severe": "#ff4466"}[status]
        fig_scatter.add_trace(go.Scatter(
            x=[height_input], y=[weight_input],
            mode="markers",
            marker=dict(size=18, color=child_color, symbol="star",
                        line=dict(color="#fff", width=2)),
            name="This Child",
        ))
        fig_scatter.update_layout(**PLOTLY_LAYOUT, height=380, title="Child's position in WHO reference population")
        st.plotly_chart(fig_scatter, use_container_width=True)


# ═══════════════════════════════════════════════
#  MODE 2 : BATCH CSV
# ═══════════════════════════════════════════════
else:
    st.markdown("<div class='section-head'>📂 <span>Upload CSV File</span></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:var(--card); border:1px solid var(--border); box-shadow: 0 2px 8px rgba(91,141,238,0.08); border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1.2rem; font-size:0.88rem; color:#7a86c0;'>
    <b style='color:#2d3561;'>Required columns (case-insensitive):</b><br>
    <code style='color:#5b8dee;'>AGE</code> (months) &nbsp;·&nbsp;
    <code style='color:#5b8dee;'>WEIGHT</code> (kg) &nbsp;·&nbsp;
    <code style='color:#5b8dee;'>HEIGHT</code> (cm) &nbsp;·&nbsp;
    <code style='color:#5b8dee;'>MUAC</code> (cm)<br><br>
    Optional columns: <code>GENDER</code>, <code>NAME</code>, <code>ID</code>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop your CSV here", type=["csv"])

    if uploaded:
        df_upload = pd.read_csv(uploaded)
        df_upload.columns = df_upload.columns.str.upper().str.strip()

        required = {"AGE", "WEIGHT", "HEIGHT", "MUAC"}
        if not required.issubset(set(df_upload.columns)):
            st.error(f"Missing columns: {required - set(df_upload.columns)}")
            st.stop()

        for col in ["AGE", "WEIGHT", "HEIGHT", "MUAC"]:
            df_upload[col] = pd.to_numeric(df_upload[col], errors="coerce")
        df_upload.dropna(subset=["AGE", "WEIGHT", "HEIGHT", "MUAC"], inplace=True)

        gmm_b, scaler_b, lmap_b, _ = get_reference_model()
        X_b = scaler_b.transform(df_upload[["AGE", "WEIGHT", "HEIGHT", "MUAC"]])
        clusters_b = gmm_b.predict(X_b)
        df_upload["Status"] = [lmap_b[c].capitalize() for c in clusters_b]
        df_upload["MUAC_WHO"] = df_upload["MUAC"].apply(lambda x: classify_muac(x).capitalize())

        # ── Summary metrics
        counts = df_upload["Status"].value_counts()
        total = len(df_upload)
        h = counts.get("Healthy", 0)
        m = counts.get("Moderate", 0)
        s = counts.get("Severe", 0)

        st.markdown(f"""
        <div class='metric-row' style='margin-top:1.5rem;'>
          <div class='metric-card safe'>
            <div class='metric-label'>Total Children</div>
            <div class='metric-value'>{total}</div>
          </div>
          <div class='metric-card safe'>
            <div class='metric-label'>Healthy</div>
            <div class='metric-value'>{h}</div>
            <div class='metric-sub'>{h/total*100:.1f}% of total</div>
          </div>
          <div class='metric-card warn'>
            <div class='metric-label'>Moderate (MAM)</div>
            <div class='metric-value'>{m}</div>
            <div class='metric-sub'>{m/total*100:.1f}% of total</div>
          </div>
          <div class='metric-card danger'>
            <div class='metric-label'>Severe (SAM)</div>
            <div class='metric-value'>{s}</div>
            <div class='metric-sub'>{s/total*100:.1f}% of total</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Charts
        c1, c2 = st.columns(2, gap="large")

        with c1:
            fig_pie = go.Figure(go.Pie(
                labels=["Healthy", "Moderate (MAM)", "Severe (SAM)"],
                values=[h, m, s],
                hole=0.55,
                marker_colors=["#00e676", "#ffb347", "#ff4466"],
                textinfo="percent+label",
                hovertemplate="%{label}: %{value} children<extra></extra>",
            ))
            fig_pie.update_layout(
                **PLOTLY_LAYOUT, height=320,
                title="Nutritional Status Distribution",
                showlegend=False,
                annotations=[dict(text=f"<b>{total}</b><br>children", x=0.5, y=0.5,
                                  font_size=14, font_color="#2d3561", showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            fig_age = px.histogram(
                df_upload, x="AGE", color="Status",
                color_discrete_map={"Healthy": "#00e676", "Moderate": "#ffb347", "Severe": "#ff4466"},
                nbins=20, barmode="stack",
                labels={"AGE": "Age (months)", "count": "Children"},
            )
            fig_age.update_layout(**PLOTLY_LAYOUT, height=320, title="Age Distribution by Status", showlegend=True)
            st.plotly_chart(fig_age, use_container_width=True)

        # ── Scatter
        fig_sc = px.scatter(
            df_upload, x="HEIGHT", y="WEIGHT", color="Status",
            color_discrete_map={"Healthy": "#00e676", "Moderate": "#ffb347", "Severe": "#ff4466"},
            size="MUAC", hover_data=["AGE", "MUAC"],
            labels={"HEIGHT": "Height (cm)", "WEIGHT": "Weight (kg)"},
        )
        fig_sc.update_layout(**PLOTLY_LAYOUT, height=420, title="Height vs Weight — sized by MUAC")
        st.plotly_chart(fig_sc, use_container_width=True)

        # ── Results table
        st.markdown("<div class='section-head'>📋 <span>Full Results</span></div>", unsafe_allow_html=True)
        st.dataframe(
            df_upload,
            use_container_width=True,
            height=350,
        )

        # ── Download
        csv_out = df_upload.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Results CSV",
            data=csv_out,
            file_name="nutriscan_results.csv",
            mime="text/csv",
        )

    else:
        # ── Demo data generator
        st.markdown("<div class='section-head' style='font-size:1rem;'>🧪 <span>Or try a demo</span></div>", unsafe_allow_html=True)
        if st.button("⚡ Generate Demo Dataset (50 children)"):
            rng2 = np.random.default_rng(99)
            n_demo = 50
            ages_d = rng2.uniform(6, 59, n_demo)
            demo = pd.DataFrame({
                "NAME": [f"Child_{i:03d}" for i in range(1, n_demo+1)],
                "AGE": ages_d.round(1),
                "GENDER": rng2.choice(["Male", "Female"], n_demo),
                "WEIGHT": np.clip(3.3 + 0.18*ages_d + rng2.normal(0, 1.5, n_demo), 4, 22).round(2),
                "HEIGHT": np.clip(50 + 0.44*ages_d + rng2.normal(0, 3, n_demo), 55, 115).round(1),
                "MUAC": np.clip(rng2.normal(12.2, 1.2, n_demo), 9, 16).round(1),
            })
            csv_demo = demo.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download demo.csv", csv_demo, "demo_children.csv", "text/csv")


# ─────────────────────────────────────────────
#  ABOUT / WHO TABLE
# ─────────────────────────────────────────────
with st.expander("📖 About this tool & WHO Reference Standards"):
    st.markdown("""
    <div style='font-size:0.9rem; color:#7a86c0; line-height:1.8;'>
    <b style='color:#2d3561; font-family:Syne,sans-serif;'>NutriScan AI</b> uses a 
    <b style='color:#5b8dee;'>Gaussian Mixture Model (GMM)</b> trained on WHO synthetic reference 
    data to classify child nutritional status into three tiers:
    </div><br>
    <table class='who-table'>
      <tr><th>Indicator</th><th>Healthy (Normal)</th><th>Moderate (MAM)</th><th>Severe (SAM)</th></tr>
      <tr>
        <td>MUAC</td>
        <td style='color:#00e676;'>≥ 12.5 cm</td>
        <td style='color:#ffb347;'>11.5 – 12.4 cm</td>
        <td style='color:#ff4466;'>< 11.5 cm</td>
      </tr>
      <tr>
        <td>Weight-for-Height (WHZ)</td>
        <td style='color:#00e676;'>≥ -2 SD</td>
        <td style='color:#ffb347;'>-3 to -2 SD</td>
        <td style='color:#ff4466;'>< -3 SD</td>
      </tr>
      <tr>
        <td>Weight-for-Age (WAZ)</td>
        <td style='color:#00e676;'>≥ -2 SD</td>
        <td style='color:#ffb347;'>-3 to -2 SD</td>
        <td style='color:#ff4466;'>< -3 SD</td>
      </tr>
    </table><br>
    <div style='font-size:0.82rem; color:#7a86c0;'>
    ⚠️ <b style='color:#ffb347;'>Disclaimer:</b> This tool is for screening and educational purposes only. 
    All clinical decisions must be made by qualified healthcare professionals following local protocols.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='app-footer'>
    Built with ❤️ using <a href='https://streamlit.io'>Streamlit</a> · 
    Powered by <a href='https://scikit-learn.org'>scikit-learn GMM</a> · 
    Standards from <a href='https://www.who.int'>WHO</a>
</div>
""", unsafe_allow_html=True)
