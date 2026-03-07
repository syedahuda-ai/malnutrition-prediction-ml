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

st.set_page_config(
    page_title="NutriScan AI — Pediatric Health Guardian",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --ink:      #0a0f0d;
  --deep:     #0d1a14;
  --panel:    #111f18;
  --border:   rgba(52,211,121,0.18);
  --glow:     #34d379;
  --amber:    #f5a623;
  --crimson:  #ff3b5c;
  --ice:      #a8f5d0;
  --text:     #d6f5e6;
  --muted:    #5a8a70;
  --mono:     'JetBrains Mono', monospace;
  --head:     'Bebas Neue', sans-serif;
  --body:     'Space Grotesk', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
  background: var(--ink) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
}

body::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(52,211,121,0.012) 3px, rgba(52,211,121,0.012) 4px
  );
  pointer-events: none;
  z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 1.5rem 2.5rem !important;
  max-width: 1500px;
  position: relative;
  z-index: 1;
}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
  background: var(--deep) !important;
  border-right: 1px solid var(--border) !important;
  position: relative;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--glow), transparent);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.sb-logo {
  text-align: center;
  padding: 2rem 1rem 1.5rem;
}
.sb-logo-icon {
  font-size: 3.2rem;
  display: block;
  margin-bottom: 0.5rem;
  filter: drop-shadow(0 0 20px rgba(52,211,121,0.6));
  animation: pulse-icon 3s ease-in-out infinite;
}
@keyframes pulse-icon {
  0%, 100% { filter: drop-shadow(0 0 12px rgba(52,211,121,0.5)); transform: scale(1); }
  50% { filter: drop-shadow(0 0 28px rgba(52,211,121,0.9)); transform: scale(1.06); }
}
.sb-logo-name {
  font-family: var(--head) !important;
  font-size: 2rem !important;
  letter-spacing: 0.12em;
  color: var(--glow) !important;
  line-height: 1;
}
.sb-logo-sub {
  font-family: var(--mono) !important;
  font-size: 0.62rem;
  color: var(--muted) !important;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-top: 0.3rem;
}
.sb-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 1rem 0;
}
.sb-feature-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.45rem 0.8rem;
  border-radius: 6px;
  margin-bottom: 0.25rem;
  font-size: 0.78rem;
  color: var(--muted) !important;
}
.sb-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--glow);
  flex-shrink: 0;
  box-shadow: 0 0 5px var(--glow);
}

/* ═══ HERO ═══ */
.hero-grid {
  display: grid;
  grid-template-columns: 1fr 200px;
  align-items: center;
  gap: 2rem;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 0 20px 20px 0;
  border-left: 4px solid var(--glow);
  padding: 2.5rem 3rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.hero-grid::before {
  content: '';
  position: absolute;
  top: -100px; right: -100px;
  width: 350px; height: 350px;
  background: radial-gradient(circle, rgba(52,211,121,0.07) 0%, transparent 65%);
  border-radius: 50%;
  pointer-events: none;
}
.hero-eyebrow {
  font-family: var(--mono) !important;
  font-size: 0.68rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--glow) !important;
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.hero-eyebrow::before {
  content: '';
  display: inline-block;
  width: 20px; height: 1px;
  background: var(--glow);
}
.hero-title {
  font-family: var(--head) !important;
  font-size: clamp(2.8rem, 4.5vw, 4.8rem) !important;
  font-weight: 400 !important;
  color: #fff !important;
  line-height: 0.95 !important;
  letter-spacing: 0.04em;
  margin-bottom: 1rem !important;
}
.hero-title em {
  font-style: normal;
  color: var(--glow);
  text-shadow: 0 0 40px rgba(52,211,121,0.35);
}
.hero-desc {
  font-size: 0.88rem;
  color: var(--muted) !important;
  max-width: 500px;
  line-height: 1.7;
}
.hero-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}
.hbadge {
  font-family: var(--mono) !important;
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.25rem 0.7rem;
  border-radius: 3px;
  border: 1px solid rgba(52,211,121,0.28);
  color: var(--glow) !important;
  background: rgba(52,211,121,0.06);
}
.hero-stats-col {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}
.h-stat {
  text-align: right;
  padding: 0.7rem 1rem;
  background: rgba(52,211,121,0.05);
  border-radius: 10px;
  border: 1px solid var(--border);
}
.h-stat-num {
  font-family: var(--head) !important;
  font-size: 2rem;
  color: var(--glow) !important;
  line-height: 1;
}
.h-stat-lbl {
  font-family: var(--mono) !important;
  font-size: 0.58rem;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-top: 0.15rem;
}

/* ═══ TICKER ═══ */
.ticker-strip {
  display: flex;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  background: var(--panel);
  margin-bottom: 2rem;
}
.t-item {
  flex: 1;
  padding: 0.9rem 1.2rem;
  border-right: 1px solid var(--border);
  position: relative;
}
.t-item:last-child { border-right: none; }
.t-item::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
}
.t-green::after  { background: var(--glow); }
.t-amber::after  { background: var(--amber); }
.t-red::after    { background: var(--crimson); }
.t-ice::after    { background: var(--ice); }
.t-purple::after { background: #b47aff; }
.t-lbl {
  font-family: var(--mono) !important;
  font-size: 0.6rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--muted) !important;
  margin-bottom: 0.3rem;
}
.t-val {
  font-family: var(--head) !important;
  font-size: 1.9rem;
  color: #fff !important;
  line-height: 1;
}
.t-sub {
  font-size: 0.68rem;
  color: var(--muted) !important;
  margin-top: 0.2rem;
  font-family: var(--mono) !important;
}

/* ═══ SECTION HEAD ═══ */
.sec-head {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1.4rem;
}
.sec-head-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--border), transparent);
}
.sec-head-text {
  font-family: var(--mono) !important;
  font-size: 0.68rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--glow) !important;
  white-space: nowrap;
}

/* ═══ INPUT ═══ */
.input-wrap {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.6rem;
  margin-bottom: 1.2rem;
  position: relative;
}
.input-wrap-label {
  position: absolute;
  top: -0.55rem; left: 1.2rem;
  font-family: var(--mono) !important;
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--glow) !important;
  background: var(--panel);
  padding: 0 0.5rem;
}

[data-testid="stNumberInput"] input {
  background: rgba(52,211,121,0.04) !important;
  border: 1px solid rgba(52,211,121,0.22) !important;
  border-radius: 7px !important;
  color: #fff !important;
  font-family: var(--mono) !important;
  font-size: 0.98rem !important;
}
[data-testid="stNumberInput"] input:focus {
  border-color: var(--glow) !important;
  box-shadow: 0 0 0 2px rgba(52,211,121,0.12) !important;
  outline: none !important;
}
[data-testid="stSelectbox"] > div > div {
  background: rgba(52,211,121,0.04) !important;
  border: 1px solid rgba(52,211,121,0.22) !important;
  border-radius: 7px !important;
  color: #fff !important;
}
label {
  font-family: var(--mono) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
}
.stRadio > label { text-transform: none !important; font-size: 0.85rem !important; letter-spacing: 0 !important; }

/* ═══ BUTTON ═══ */
.stButton > button {
  background: var(--glow) !important;
  color: var(--ink) !important;
  font-family: var(--head) !important;
  font-size: 1.05rem !important;
  letter-spacing: 0.14em !important;
  border: none !important;
  border-radius: 7px !important;
  padding: 0.72rem 2.5rem !important;
  width: 100% !important;
  transition: all 0.2s ease !important;
  text-transform: uppercase;
}
.stButton > button:hover {
  background: #4dffa0 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(52,211,121,0.35) !important;
}

/* ═══ RESULT PANEL ═══ */
.result-panel {
  border-radius: 14px;
  padding: 1.8rem 2.2rem;
  margin: 1.4rem 0;
  border: 1px solid;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.4rem;
  align-items: center;
  position: relative;
  overflow: hidden;
}
.result-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 100%;
}
.result-panel.healthy  { background: rgba(52,211,121,0.05); border-color: rgba(52,211,121,0.28); }
.result-panel.healthy::before  { background: var(--glow); box-shadow: 2px 0 10px var(--glow); }
.result-panel.moderate { background: rgba(245,166,35,0.05); border-color: rgba(245,166,35,0.28); }
.result-panel.moderate::before { background: var(--amber); box-shadow: 2px 0 10px var(--amber); }
.result-panel.severe   { background: rgba(255,59,92,0.05); border-color: rgba(255,59,92,0.28); }
.result-panel.severe::before   { background: var(--crimson); box-shadow: 2px 0 10px var(--crimson); }

.res-icon { font-size: 2.8rem; line-height: 1; }
.res-tag {
  font-family: var(--mono) !important;
  font-size: 0.62rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}
.res-tag.healthy  { color: var(--glow) !important; }
.res-tag.moderate { color: var(--amber) !important; }
.res-tag.severe   { color: var(--crimson) !important; }
.res-title {
  font-family: var(--head) !important;
  font-size: 2rem;
  color: #fff !important;
  letter-spacing: 0.06em;
  line-height: 1;
  margin-bottom: 0.45rem;
}
.res-desc { font-size: 0.85rem; color: var(--muted) !important; line-height: 1.6; }
.urgency-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.75rem;
  padding: 0.3rem 0.85rem;
  border-radius: 4px;
  font-family: var(--mono) !important;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  border: 1px solid;
}
.urgency-chip.healthy  { border-color: rgba(52,211,121,0.35); color: var(--glow) !important; background: rgba(52,211,121,0.07); }
.urgency-chip.moderate { border-color: rgba(245,166,35,0.35); color: var(--amber) !important; background: rgba(245,166,35,0.07); }
.urgency-chip.severe   { border-color: rgba(255,59,92,0.35); color: var(--crimson) !important; background: rgba(255,59,92,0.07); }

/* ═══ REC ITEMS ═══ */
.rec-item {
  display: flex;
  gap: 0.9rem;
  align-items: flex-start;
  padding: 0.75rem 1rem;
  border-radius: 7px;
  margin-bottom: 0.45rem;
  background: rgba(52,211,121,0.03);
  border: 1px solid rgba(52,211,121,0.09);
  transition: all 0.2s;
}
.rec-item:hover {
  background: rgba(52,211,121,0.07);
  border-color: rgba(52,211,121,0.22);
  transform: translateX(4px);
}
.rec-num {
  font-family: var(--mono) !important;
  font-size: 0.62rem;
  border-radius: 3px;
  padding: 0.18rem 0.45rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
  letter-spacing: 0.05em;
}
.rec-num.rn-green  { color: var(--glow) !important; background: rgba(52,211,121,0.12); }
.rec-num.rn-amber  { color: var(--amber) !important; background: rgba(245,166,35,0.12); }
.rec-num.rn-red    { color: var(--crimson) !important; background: rgba(255,59,92,0.12); }
.rec-text { font-size: 0.83rem; color: var(--text) !important; line-height: 1.5; }

/* ═══ GAUGE ═══ */
.gauge-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.1rem 1.2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.gauge-card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.gc-green::after { background: var(--glow); }
.gc-amber::after { background: var(--amber); }
.gc-red::after   { background: var(--crimson); }
.gc-lbl { font-family: var(--mono) !important; font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted) !important; margin-bottom: 0.45rem; }
.gc-val { font-family: var(--head) !important; font-size: 2.1rem; line-height: 1; margin-bottom: 0.25rem; }
.gc-status { font-size: 0.72rem; font-family: var(--mono) !important; letter-spacing: 0.04em; }

/* ═══ WHO TABLE ═══ */
.who-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.who-table th {
  background: rgba(52,211,121,0.06);
  color: var(--glow) !important;
  font-family: var(--mono) !important;
  font-size: 0.63rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.7rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.who-table td {
  padding: 0.6rem 1rem;
  border-bottom: 1px solid rgba(52,211,121,0.07);
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.78rem;
}
.who-table tr:hover td { background: rgba(52,211,121,0.03); }

/* File uploader */
[data-testid="stFileUploader"] {
  background: rgba(52,211,121,0.03) !important;
  border: 2px dashed rgba(52,211,121,0.22) !important;
  border-radius: 10px !important;
}
[data-testid="stExpander"] {
  background: var(--panel) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: rgba(52,211,121,0.28); border-radius: 2px; }

/* Download button */
[data-testid="stDownloadButton"] button {
  background: transparent !important;
  border: 1px solid rgba(52,211,121,0.35) !important;
  color: var(--glow) !important;
  font-family: var(--mono) !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.1em !important;
  border-radius: 5px !important;
}
[data-testid="stDownloadButton"] button:hover {
  background: rgba(52,211,121,0.09) !important;
  box-shadow: 0 0 14px rgba(52,211,121,0.18) !important;
}

code {
  font-family: var(--mono) !important;
  background: rgba(52,211,121,0.1) !important;
  color: var(--glow) !important;
  border-radius: 3px;
  padding: 0.1em 0.4em;
  font-size: 0.85em;
}

/* Tabs */
[data-baseweb="tab-list"] {
  background: var(--panel) !important;
  border-radius: 7px;
  border: 1px solid var(--border) !important;
}
[data-baseweb="tab"] { color: var(--muted) !important; font-family: var(--mono) !important; font-size: 0.78rem !important; }
[aria-selected="true"][data-baseweb="tab"] { color: var(--glow) !important; }

hr { border-color: rgba(52,211,121,0.1) !important; }

[data-testid="stRadio"] label {
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-size: 0.88rem !important;
  color: var(--text) !important;
}

/* Animations */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero-grid { animation: fadeUp 0.45s ease both; }
.ticker-strip { animation: fadeUp 0.5s ease 0.1s both; }

.pulse-dot {
  display: inline-block;
  width: 7px; height: 7px;
  background: var(--glow);
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(52,211,121,0.7);
  animation: pring 2.2s infinite;
  vertical-align: middle;
  margin-right: 5px;
}
@keyframes pring {
  0%   { box-shadow: 0 0 0 0 rgba(52,211,121,0.7); }
  70%  { box-shadow: 0 0 0 9px rgba(52,211,121,0); }
  100% { box-shadow: 0 0 0 0 rgba(52,211,121,0); }
}

/* Footer */
.app-footer {
  text-align: center;
  padding: 2rem 0 1.5rem;
  margin-top: 3rem;
  border-top: 1px solid var(--border);
  position: relative;
}
.app-footer::before {
  content: '';
  position: absolute;
  top: -1px; left: 50%; transform: translateX(-50%);
  width: 60px; height: 2px;
  background: var(--glow);
}
.footer-text {
  font-family: var(--mono) !important;
  font-size: 0.65rem;
  letter-spacing: 0.14em;
  color: var(--muted) !important;
  text-transform: uppercase;
}
.footer-text a { color: var(--glow) !important; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS & MODEL
# ─────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,26,20,0.55)",
    font=dict(family="JetBrains Mono", color="#5a8a70", size=11),
    xaxis=dict(gridcolor="rgba(52,211,121,0.08)", zerolinecolor="rgba(52,211,121,0.1)", color="#5a8a70"),
    yaxis=dict(gridcolor="rgba(52,211,121,0.08)", zerolinecolor="rgba(52,211,121,0.1)", color="#5a8a70"),
    margin=dict(l=20, r=20, t=45, b=20),
    hoverlabel=dict(bgcolor="#0d1a14", bordercolor="rgba(52,211,121,0.4)", font_color="#d6f5e6", font_family="JetBrains Mono"),
    title_font=dict(family="Bebas Neue", size=17, color="#d6f5e6"),
)


def classify_muac(muac: float) -> str:
    if muac < 11.5: return "severe"
    elif muac < 12.5: return "moderate"
    else: return "healthy"


def classify_wfa(age_months: float, weight: float) -> str:
    median = 3.3 + 0.19 * age_months - 0.0013 * age_months ** 2
    sd = 0.45 + 0.008 * age_months
    z = (weight - median) / sd
    if z < -3: return "severe"
    elif z < -2: return "moderate"
    else: return "healthy"


@st.cache_resource
def get_reference_model():
    rng = np.random.default_rng(42)
    n = 800
    ages_h = rng.uniform(0, 60, n)
    weights_h = 3.3 + 0.19 * ages_h - 0.0013 * ages_h**2 + rng.normal(0, 0.6, n)
    heights_h = 50 + 0.45 * ages_h + rng.normal(0, 1.5, n)
    muac_h = 13.5 + 0.02 * ages_h + rng.normal(0, 0.5, n)
    weights_m = (3.3 + 0.19 * ages_h - 0.0013 * ages_h**2) * 0.82 + rng.normal(0, 0.5, n)
    heights_m = (50 + 0.45 * ages_h) * 0.97 + rng.normal(0, 1.2, n)
    muac_m = 11.8 + 0.01 * ages_h + rng.normal(0, 0.3, n)
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
    return label_map[cluster], proba, cluster


def get_recommendations(status, age, muac, weight):
    return {
        "healthy": {
            "icon": "🟢", "css": "healthy",
            "title": "HEALTHY — NO MALNUTRITION",
            "summary": "This child's anthropometric measurements fall within WHO healthy reference ranges.",
            "urgency": "ROUTINE CHECK-UP RECOMMENDED",
            "actions": [
                "Continue balanced diet — fruits, vegetables, proteins & grains",
                "Schedule routine growth monitoring every 3 months",
                "Ensure adequate micronutrient intake (iron, zinc, vitamin A)",
                "Maintain breastfeeding if child is under 24 months",
            ],
        },
        "moderate": {
            "icon": "🟡", "css": "moderate",
            "title": "MODERATE ACUTE MALNUTRITION (MAM)",
            "summary": "MUAC and/or weight measurements indicate moderate malnutrition. Intervention needed.",
            "urgency": "CLINICAL REVIEW WITHIN 1 WEEK",
            "actions": [
                "Enroll in Supplementary Feeding Programme (SFP)",
                "Provide Ready-to-Use Supplementary Food (RUSF) — 500 kcal/day",
                "Screen for infections: diarrhea, pneumonia, malaria",
                "Monitor weight weekly and MUAC every 2 weeks",
                "Provide nutrition counselling to caregivers",
            ],
        },
        "severe": {
            "icon": "🔴", "css": "severe",
            "title": "SEVERE ACUTE MALNUTRITION (SAM)",
            "summary": "Critical malnutrition detected. Immediate medical intervention is required.",
            "urgency": "⚠ IMMEDIATE REFERRAL REQUIRED",
            "actions": [
                "URGENT: Refer to inpatient Therapeutic Feeding Centre (TFC)",
                "Initiate Ready-to-Use Therapeutic Food (RUTF) — F-75 / F-100 protocol",
                "Screen for: hypoglycaemia, hypothermia, dehydration",
                "Administer antibiotics per WHO SAM protocol",
                "Daily clinical monitoring until stabilisation",
                "Intensive caregiver counselling on home care",
            ],
        },
    }[status]


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sb-logo'>
      <span class='sb-logo-icon'>🧬</span>
      <div class='sb-logo-name'>NUTRISCAN</div>
      <div class='sb-logo-sub'>Pediatric AI · WHO v2024</div>
    </div>
    <div class='sb-divider'></div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "**Analysis Mode**",
        ["🔍 Single Child Assessment", "📊 Batch CSV Analysis"],
        label_visibility="visible"
    )

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding:0 0.3rem;'>
      <div class='sb-feature-item'><div class='sb-dot'></div>WHO MUAC thresholds</div>
      <div class='sb-feature-item'><div class='sb-dot'></div>Gaussian Mixture Model</div>
      <div class='sb-feature-item'><div class='sb-dot'></div>3-tier severity scoring</div>
      <div class='sb-feature-item'><div class='sb-dot'></div>Clinical recommendations</div>
      <div class='sb-feature-item'><div class='sb-dot'></div>Batch CSV processing</div>
      <div class='sb-feature-item'><div class='sb-dot'></div>Interactive visualisations</div>
    </div>
    <div class='sb-divider'></div>
    <div style='font-size:0.62rem; font-family:JetBrains Mono,monospace; color:#3a6a50; text-align:center; padding: 0 0.5rem; line-height:1.6;'>
      Based on <a href='https://www.who.int/tools/child-growth-standards' style='color:#34d379;'>WHO Child Growth Standards</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BUILD MODEL STATS
# ─────────────────────────────────────────────
gmm_model, scaler_obj, label_map_obj, ref_df = get_reference_model()
X_all = scaler_obj.transform(ref_df[["AGE", "WEIGHT", "HEIGHT", "MUAC"]])
labels_all = gmm_model.predict(X_all)
sil = silhouette_score(X_all, labels_all)
db = davies_bouldin_score(X_all, labels_all)


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='hero-grid'>
  <div>
    <div class='hero-eyebrow'><span class='pulse-dot'></span>System Online &nbsp;·&nbsp; GMM Active &nbsp;·&nbsp; WHO v2024</div>
    <h1 class='hero-title'>PEDIATRIC<br><em>HEALTH</em><br>GUARDIAN</h1>
    <p class='hero-desc'>Enter a child's anthropometric measurements — age, weight, height, 
    and MUAC — and the Gaussian Mixture Model classifies nutritional status in real time 
    against WHO reference populations.</p>
    <div class='hero-badges'>
      <span class='hbadge'>GMM Clustering</span>
      <span class='hbadge'>WHO Standards</span>
      <span class='hbadge'>3-Tier Detection</span>
      <span class='hbadge'>Real-Time Analysis</span>
    </div>
  </div>
  <div class='hero-stats-col'>
    <div class='h-stat'>
      <div class='h-stat-num'>{sil:.3f}</div>
      <div class='h-stat-lbl'>Silhouette Score</div>
    </div>
    <div class='h-stat'>
      <div class='h-stat-num'>{db:.3f}</div>
      <div class='h-stat-lbl'>Davies-Bouldin</div>
    </div>
    <div class='h-stat'>
      <div class='h-stat-num'>2400</div>
      <div class='h-stat-lbl'>Training Records</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TICKER STRIP
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='ticker-strip'>
  <div class='t-item t-ice'>
    <div class='t-lbl'>Model</div>
    <div class='t-val'>GMM</div>
    <div class='t-sub'>Gaussian Mixture</div>
  </div>
  <div class='t-item t-green'>
    <div class='t-lbl'>Silhouette</div>
    <div class='t-val'>{sil:.3f}</div>
    <div class='t-sub'>Higher = Better</div>
  </div>
  <div class='t-item t-amber'>
    <div class='t-lbl'>Davies-Bouldin</div>
    <div class='t-val'>{db:.3f}</div>
    <div class='t-sub'>Lower = Better</div>
  </div>
  <div class='t-item t-purple'>
    <div class='t-lbl'>WHO Tiers</div>
    <div class='t-val'>3</div>
    <div class='t-sub'>Healthy · MAM · SAM</div>
  </div>
  <div class='t-item t-red'>
    <div class='t-lbl'>Features</div>
    <div class='t-val'>4</div>
    <div class='t-sub'>Age · Wt · Ht · MUAC</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  MODE 1 : SINGLE CHILD
# ═══════════════════════════════════════════════
if "Single" in mode:

    st.markdown("""
    <div class='sec-head'>
      <span style='font-size:0.9rem;'>👶</span>
      <span class='sec-head-text'>Anthropometric Input</span>
      <div class='sec-head-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='input-wrap'><div class='input-wrap-label'>Patient Info</div>", unsafe_allow_html=True)
        gender = st.selectbox("Gender", ["Male", "Female"])
        age_input = st.number_input("Age (months)", min_value=0.0, max_value=60.0, value=24.0, step=0.5)
        weight_input = st.number_input("Weight (kg)", min_value=1.0, max_value=30.0, value=10.5, step=0.1)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='input-wrap'><div class='input-wrap-label'>Measurements</div>", unsafe_allow_html=True)
        height_input = st.number_input("Height (cm)", min_value=40.0, max_value=130.0, value=82.0, step=0.5)
        muac_input = st.number_input("MUAC (cm)", min_value=5.0, max_value=20.0, value=13.2, step=0.1)
        st.markdown("""
        <div style='margin-top:0.8rem; padding:0.55rem 0.85rem;
             background:rgba(52,211,121,0.04); border:1px solid rgba(52,211,121,0.14);
             border-radius:5px; font-family:JetBrains Mono,monospace; font-size:0.66rem;
             color:#5a8a70; letter-spacing:0.04em;'>
          💡 MUAC — measure left upper arm midpoint between shoulder &amp; elbow
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("RUN MALNUTRITION ASSESSMENT  →")

    if predict_btn:
        status, proba, cluster_id = predict_child(age_input, weight_input, height_input, muac_input)
        recs = get_recommendations(status, age_input, muac_input, weight_input)
        css = recs["css"]

        st.markdown(f"""
        <div class='result-panel {css}'>
          <div class='res-icon'>{recs["icon"]}</div>
          <div>
            <div class='res-tag {css}'>{css.upper()} STATUS DETECTED</div>
            <div class='res-title'>{recs["title"]}</div>
            <div class='res-desc'>{recs["summary"]}</div>
            <div class='urgency-chip {css}'>⏱ {recs["urgency"]}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        r1, r2 = st.columns([1, 1], gap="large")

        with r1:
            st.markdown("""
            <div class='sec-head'>
              <span style='font-size:0.9rem;'>📊</span>
              <span class='sec-head-text'>Model Confidence</span>
              <div class='sec-head-line'></div>
            </div>
            """, unsafe_allow_html=True)

            ordered_proba = {lbl: proba[cid] for cid, lbl in label_map_obj.items()}
            bar_values = [ordered_proba.get("healthy", 0), ordered_proba.get("moderate", 0), ordered_proba.get("severe", 0)]

            fig_bar = go.Figure(go.Bar(
                x=["Healthy", "Moderate", "Severe"],
                y=[v * 100 for v in bar_values],
                marker_color=["#34d379", "#f5a623", "#ff3b5c"],
                text=[f"{v*100:.1f}%" for v in bar_values],
                textposition="outside",
                marker_line_width=0,
            ))
            fig_bar.update_layout(
                **PLOTLY_LAYOUT,
                yaxis_title="Probability (%)",
                yaxis_range=[0, 118],
                showlegend=False,
                height=300,
                title="GMM Classification Probability",
                bargap=0.38,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with r2:
            st.markdown("""
            <div class='sec-head'>
              <span style='font-size:0.9rem;'>🏥</span>
              <span class='sec-head-text'>Clinical Recommendations</span>
              <div class='sec-head-line'></div>
            </div>
            """, unsafe_allow_html=True)
            num_cls = {"healthy": "rn-green", "moderate": "rn-amber", "severe": "rn-red"}[status]
            for i, action in enumerate(recs["actions"], 1):
                st.markdown(f"""
                <div class='rec-item'>
                  <span class='rec-num {num_cls}'>0{i}</span>
                  <span class='rec-text'>{action}</span>
                </div>
                """, unsafe_allow_html=True)

        # WHO Gauges
        st.markdown("""
        <br>
        <div class='sec-head'>
          <span style='font-size:0.9rem;'>📏</span>
          <span class='sec-head-text'>WHO Threshold Check</span>
          <div class='sec-head-line'></div>
        </div>
        """, unsafe_allow_html=True)

        g1, g2, g3 = st.columns(3)
        muac_s2 = classify_muac(muac_input)
        muac_gc = {"healthy": "gc-green", "moderate": "gc-amber", "severe": "gc-red"}[muac_s2]
        muac_col = {"healthy": "#34d379", "moderate": "#f5a623", "severe": "#ff3b5c"}[muac_s2]
        muac_lbl2 = {"healthy": "✓ Normal (≥12.5 cm)", "moderate": "△ MAM (11.5–12.5)", "severe": "✕ SAM (<11.5 cm)"}[muac_s2]

        bmi = weight_input / ((height_input / 100) ** 2)
        bmi_gc = "gc-green" if bmi >= 15 else ("gc-amber" if bmi >= 13 else "gc-red")
        bmi_col = "#34d379" if bmi >= 15 else ("#f5a623" if bmi >= 13 else "#ff3b5c")

        wfa_s = classify_wfa(age_input, weight_input)
        wfa_gc = {"healthy": "gc-green", "moderate": "gc-amber", "severe": "gc-red"}[wfa_s]
        wfa_col = {"healthy": "#34d379", "moderate": "#f5a623", "severe": "#ff3b5c"}[wfa_s]
        wfa_lbl2 = {"healthy": "✓ Normal", "moderate": "△ Moderate", "severe": "✕ Severe"}[wfa_s]

        with g1:
            st.markdown(f"""
            <div class='gauge-card {muac_gc}'>
              <div class='gc-lbl'>MUAC Reading</div>
              <div class='gc-val' style='color:{muac_col};'>{muac_input} cm</div>
              <div class='gc-status' style='color:{muac_col};'>{muac_lbl2}</div>
            </div>
            """, unsafe_allow_html=True)
        with g2:
            st.markdown(f"""
            <div class='gauge-card {bmi_gc}'>
              <div class='gc-lbl'>Body Mass Index</div>
              <div class='gc-val' style='color:{bmi_col};'>{bmi:.1f}</div>
              <div class='gc-status' style='color:{bmi_col};'>Weight / Height²</div>
            </div>
            """, unsafe_allow_html=True)
        with g3:
            st.markdown(f"""
            <div class='gauge-card {wfa_gc}'>
              <div class='gc-lbl'>Weight-for-Age</div>
              <div class='gc-val' style='color:{wfa_col};'>{weight_input} kg</div>
              <div class='gc-status' style='color:{wfa_col};'>{wfa_lbl2}</div>
            </div>
            """, unsafe_allow_html=True)

        # Reference scatter
        st.markdown("""
        <br>
        <div class='sec-head'>
          <span style='font-size:0.9rem;'>🗺️</span>
          <span class='sec-head-text'>Population Reference Chart</span>
          <div class='sec-head-line'></div>
        </div>
        """, unsafe_allow_html=True)

        ref_sample = ref_df.sample(600, random_state=1).copy()
        ref_sample["label"] = ref_sample["cluster"].map(label_map_obj).str.capitalize()
        color_map = {"Healthy": "#34d379", "Moderate": "#f5a623", "Severe": "#ff3b5c"}

        fig_scatter = px.scatter(
            ref_sample, x="HEIGHT", y="WEIGHT",
            color="label", color_discrete_map=color_map,
            opacity=0.28, size_max=6,
            labels={"HEIGHT": "Height (cm)", "WEIGHT": "Weight (kg)", "label": "Status"},
        )
        child_color = {"healthy": "#34d379", "moderate": "#f5a623", "severe": "#ff3b5c"}[status]
        fig_scatter.add_trace(go.Scatter(
            x=[height_input], y=[weight_input],
            mode="markers",
            marker=dict(size=20, color=child_color, symbol="star",
                        line=dict(color="#fff", width=2)),
            name="This Child",
        ))
        fig_scatter.update_layout(**PLOTLY_LAYOUT, height=400, title="Child Position in WHO Reference Population")
        st.plotly_chart(fig_scatter, use_container_width=True)


# ═══════════════════════════════════════════════
#  MODE 2 : BATCH CSV
# ═══════════════════════════════════════════════
else:
    st.markdown("""
    <div class='sec-head'>
      <span style='font-size:0.9rem;'>📂</span>
      <span class='sec-head-text'>Batch CSV Upload</span>
      <div class='sec-head-line'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(52,211,121,0.04); border:1px solid rgba(52,211,121,0.16);
         border-radius:9px; padding:0.95rem 1.3rem; margin-bottom:1.1rem;'>
      <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; letter-spacing:0.15em;
           text-transform:uppercase; color:#34d379; margin-bottom:0.4rem;'>Required Columns (case-insensitive)</div>
      <div style='font-family:JetBrains Mono,monospace; font-size:0.78rem; color:#5a8a70;'>
        <code>AGE</code> (months) &nbsp;·&nbsp; <code>WEIGHT</code> (kg) &nbsp;·&nbsp;
        <code>HEIGHT</code> (cm) &nbsp;·&nbsp; <code>MUAC</code> (cm)
      </div>
      <div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#3a6a50; margin-top:0.35rem;'>
        Optional: <code>GENDER</code> · <code>NAME</code> · <code>ID</code>
      </div>
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

        counts = df_upload["Status"].value_counts()
        total = len(df_upload)
        h = counts.get("Healthy", 0)
        m = counts.get("Moderate", 0)
        s = counts.get("Severe", 0)

        st.markdown(f"""
        <div class='ticker-strip' style='margin-top:1.4rem;'>
          <div class='t-item t-ice'>
            <div class='t-lbl'>Total</div>
            <div class='t-val'>{total}</div>
          </div>
          <div class='t-item t-green'>
            <div class='t-lbl'>Healthy</div>
            <div class='t-val'>{h}</div>
            <div class='t-sub'>{h/total*100:.1f}%</div>
          </div>
          <div class='t-item t-amber'>
            <div class='t-lbl'>Moderate (MAM)</div>
            <div class='t-val'>{m}</div>
            <div class='t-sub'>{m/total*100:.1f}%</div>
          </div>
          <div class='t-item t-red'>
            <div class='t-lbl'>Severe (SAM)</div>
            <div class='t-val'>{s}</div>
            <div class='t-sub'>{s/total*100:.1f}%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            fig_pie = go.Figure(go.Pie(
                labels=["Healthy", "Moderate (MAM)", "Severe (SAM)"],
                values=[h, m, s], hole=0.6,
                marker_colors=["#34d379", "#f5a623", "#ff3b5c"],
                textinfo="percent+label",
                hovertemplate="%{label}: %{value} children<extra></extra>",
            ))
            fig_pie.update_layout(
                **PLOTLY_LAYOUT, height=320,
                title="Nutritional Status Distribution",
                showlegend=False,
                annotations=[dict(text=f"<b>{total}</b><br>total", x=0.5, y=0.5,
                                  font_size=14, font_color="#d6f5e6", showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            fig_age = px.histogram(
                df_upload, x="AGE", color="Status",
                color_discrete_map={"Healthy": "#34d379", "Moderate": "#f5a623", "Severe": "#ff3b5c"},
                nbins=20, barmode="stack",
                labels={"AGE": "Age (months)", "count": "Children"},
            )
            fig_age.update_layout(**PLOTLY_LAYOUT, height=320, title="Age Distribution by Status")
            st.plotly_chart(fig_age, use_container_width=True)

        fig_sc = px.scatter(
            df_upload, x="HEIGHT", y="WEIGHT", color="Status",
            color_discrete_map={"Healthy": "#34d379", "Moderate": "#f5a623", "Severe": "#ff3b5c"},
            size="MUAC", hover_data=["AGE", "MUAC"],
            labels={"HEIGHT": "Height (cm)", "WEIGHT": "Weight (kg)"},
        )
        fig_sc.update_layout(**PLOTLY_LAYOUT, height=420, title="Height vs Weight — Sized by MUAC")
        st.plotly_chart(fig_sc, use_container_width=True)

        st.markdown("""
        <div class='sec-head'>
          <span style='font-size:0.9rem;'>📋</span>
          <span class='sec-head-text'>Full Results</span>
          <div class='sec-head-line'></div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_upload, use_container_width=True, height=350)

        csv_out = df_upload.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ DOWNLOAD RESULTS CSV", data=csv_out, file_name="nutriscan_results.csv", mime="text/csv")

    else:
        st.markdown("""
        <div class='sec-head'>
          <span style='font-size:0.9rem;'>🧪</span>
          <span class='sec-head-text'>Try a Demo Dataset</span>
          <div class='sec-head-line'></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ GENERATE DEMO DATASET (50 CHILDREN)"):
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
            st.download_button("⬇ Download demo.csv", demo.to_csv(index=False).encode("utf-8"), "demo_children.csv", "text/csv")


# ─────────────────────────────────────────────
#  ABOUT / WHO TABLE
# ─────────────────────────────────────────────
with st.expander("◈  About this tool & WHO Reference Standards"):
    st.markdown("""
    <div style='font-size:0.83rem; color:#5a8a70; line-height:1.8; font-family:JetBrains Mono,monospace;'>
    <b style='color:#d6f5e6;'>NutriScan AI</b> uses a 
    <b style='color:#34d379;'>Gaussian Mixture Model (GMM)</b> trained on WHO synthetic reference 
    data to classify child nutritional status into three tiers:
    </div><br>
    <table class='who-table'>
      <tr><th>Indicator</th><th>✓ Healthy</th><th>△ Moderate (MAM)</th><th>✕ Severe (SAM)</th></tr>
      <tr>
        <td>MUAC</td>
        <td style='color:#34d379;'>≥ 12.5 cm</td>
        <td style='color:#f5a623;'>11.5 – 12.4 cm</td>
        <td style='color:#ff3b5c;'>&lt; 11.5 cm</td>
      </tr>
      <tr>
        <td>Weight-for-Height (WHZ)</td>
        <td style='color:#34d379;'>≥ -2 SD</td>
        <td style='color:#f5a623;'>-3 to -2 SD</td>
        <td style='color:#ff3b5c;'>&lt; -3 SD</td>
      </tr>
      <tr>
        <td>Weight-for-Age (WAZ)</td>
        <td style='color:#34d379;'>≥ -2 SD</td>
        <td style='color:#f5a623;'>-3 to -2 SD</td>
        <td style='color:#ff3b5c;'>&lt; -3 SD</td>
      </tr>
    </table><br>
    <div style='font-size:0.72rem; color:#3a6a50; font-family:JetBrains Mono,monospace;'>
    ⚠ <b style='color:#f5a623;'>Disclaimer:</b> For screening and educational purposes only. 
    All clinical decisions must be made by qualified healthcare professionals.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='app-footer'>
  <div class='footer-text'>
    Built with ❤ using <a href='https://streamlit.io'>Streamlit</a> &nbsp;·&nbsp;
    Powered by <a href='https://scikit-learn.org'>scikit-learn GMM</a> &nbsp;·&nbsp;
    Standards from <a href='https://www.who.int'>WHO</a>
  </div>
</div>
""", unsafe_allow_html=True)
