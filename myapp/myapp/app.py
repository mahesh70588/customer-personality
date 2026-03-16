# ─────────────────────────────────────────────────────────────────────────────
# app.py  —  Marketing Campaign Response Predictor (Streamlit App)
# Run with:  streamlit run app.py
# ─────────────────────────────────────────────────────────────────────────────

import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Campaign Response Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS  — Full design overhaul
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0e1a !important;
    color: #e8eaf0 !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 4rem 3rem !important;
    max-width: 1300px !important;
}

/* ── Animated gradient background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1530 40%, #0a1628 70%, #0e0a1a 100%) !important;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(16,185,129,0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 60% 10%, rgba(245,158,11,0.04) 0%, transparent 40%);
    pointer-events: none;
    z-index: 0;
}

/* ── Hero header ── */
.hero-wrapper {
    text-align: center;
    padding: 3.5rem 2rem 2.5rem;
    position: relative;
    margin-bottom: 1rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 0.75rem;
    font-weight: 500;
    color: #a5b4fc;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.4rem);
    font-weight: 800;
    line-height: 1.1;
    color: #ffffff;
    margin-bottom: 0.8rem;
    letter-spacing: -0.03em;
}
.hero-title span {
    background: linear-gradient(135deg, #6366f1, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    font-weight: 300;
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Stat bar ── */
.stat-bar {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    padding: 1.5rem 2rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    margin: 1.5rem 0 2.5rem;
    flex-wrap: wrap;
}
.stat-item {
    text-align: center;
}
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #ffffff;
}
.stat-number.green { color: #10b981; }
.stat-number.indigo { color: #818cf8; }
.stat-number.amber { color: #fbbf24; }
.stat-label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 3px;
}

/* ── Section headings ── */
.section-head {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,0.3), transparent);
}

/* ── Input cards ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.6rem 1.8rem 1.8rem;
    height: 100%;
    transition: border-color 0.3s;
}
.input-card:hover {
    border-color: rgba(99,102,241,0.2);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-icon {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}
.icon-indigo { background: rgba(99,102,241,0.15); }
.icon-green  { background: rgba(16,185,129,0.15); }
.icon-amber  { background: rgba(245,158,11,0.15); }

/* ── Streamlit inputs restyling — full coverage ── */

/* Number input wrapper */
[data-testid="stNumberInput"] > div {
    background: #1e2438 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}
/* Number input actual text field */
[data-testid="stNumberInput"] input {
    background: #1e2438 !important;
    color: #f1f5f9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 10px !important;
    caret-color: #6366f1 !important;
}
[data-testid="stNumberInput"] input::placeholder {
    color: #475569 !important;
}
[data-testid="stNumberInput"] input:focus {
    outline: none !important;
    box-shadow: none !important;
    background: #242b42 !important;
    color: #f1f5f9 !important;
}
/* +/- stepper buttons */
[data-testid="stNumberInput"] button {
    background: rgba(99,102,241,0.15) !important;
    color: #a5b4fc !important;
    border: none !important;
    border-radius: 6px !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(99,102,241,0.3) !important;
}
/* Focus ring on wrapper */
[data-testid="stNumberInput"] > div:focus-within {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* Selectbox full stack */
[data-testid="stSelectbox"] > div > div {
    background: #1e2438 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}
/* Selected value text inside selectbox */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #f1f5f9 !important;
}
/* Dropdown arrow */
[data-testid="stSelectbox"] svg {
    fill: #64748b !important;
}
/* Dropdown open state */
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}
/* ── Dropdown popup — aggressive full override ── */

/* Outer popover wrapper */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] > div > div {
    background: #1e2438 !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.6) !important;
}

/* Menu container and list */
[data-baseweb="menu"],
[data-baseweb="menu"] ul,
[role="listbox"],
[role="listbox"] > div {
    background: #1e2438 !important;
    border-radius: 12px !important;
    padding: 4px !important;
}

/* Every list item — catch all variants */
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"],
[role="listbox"] li,
[role="option"],
ul[data-baseweb="menu"] > li,
[data-baseweb="menu"] > ul > li {
    background: #1e2438 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 9px 14px !important;
}

/* ALL text nodes inside options */
[data-baseweb="menu"] li *,
[data-baseweb="menu"] [role="option"] *,
[role="option"] *,
[role="listbox"] li * {
    color: #e2e8f0 !important;
    background: transparent !important;
}

/* Hover + selected states */
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover,
[role="option"]:hover {
    background: rgba(99,102,241,0.18) !important;
    color: #ffffff !important;
}
[data-baseweb="menu"] li:hover *,
[data-baseweb="menu"] [role="option"]:hover *,
[role="option"]:hover * {
    color: #ffffff !important;
}

[data-baseweb="menu"] li[aria-selected="true"],
[role="option"][aria-selected="true"] {
    background: rgba(99,102,241,0.25) !important;
    color: #ffffff !important;
}
[data-baseweb="menu"] li[aria-selected="true"] *,
[role="option"][aria-selected="true"] * {
    color: #ffffff !important;
}

/* Highlighted/focused item (keyboard nav) */
[data-baseweb="menu"] li[data-highlighted="true"],
[role="option"][data-highlighted="true"] {
    background: rgba(99,102,241,0.18) !important;
    color: #ffffff !important;
}
/* Widget labels */
label[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Predict button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.9rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    cursor: pointer !important;
    box-shadow: 0 4px 30px rgba(99,102,241,0.35) !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
    box-shadow: 0 6px 40px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Metric boxes ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Syne', sans-serif !important; font-size: 1.6rem !important; font-weight: 700 !important; }

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.06) !important; margin: 2rem 0 !important; }

/* ── Result cards ── */
.result-respond {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(16,185,129,0.04));
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 2rem 2.4rem;
    text-align: center;
    margin: 1rem 0;
}
.result-no-respond {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.04));
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 20px;
    padding: 2rem 2.4rem;
    text-align: center;
    margin: 1rem 0;
}
.result-icon { font-size: 2.8rem; margin-bottom: 0.5rem; }
.result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.3rem;
}
.result-sub { font-size: 0.9rem; color: #94a3b8; }

/* ── Recommendation card ── */
.rec-card {
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin: 1rem 0;
}
.rec-high   { background: rgba(16,185,129,0.08);  border: 1px solid rgba(16,185,129,0.2); }
.rec-mod    { background: rgba(99,102,241,0.08);   border: 1px solid rgba(99,102,241,0.2); }
.rec-low    { background: rgba(245,158,11,0.08);   border: 1px solid rgba(245,158,11,0.2); }
.rec-vlow   { background: rgba(100,116,139,0.08);  border: 1px solid rgba(100,116,139,0.2); }
.rec-emoji  { font-size: 1.8rem; flex-shrink: 0; }
.rec-title  { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: #ffffff; margin-bottom: 0.25rem; }
.rec-body   { font-size: 0.85rem; color: #94a3b8; line-height: 1.6; }

/* ── Summary table ── */
.summary-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}
.summary-table tr { border-bottom: 1px solid rgba(255,255,255,0.05); }
.summary-table tr:last-child { border-bottom: none; }
.summary-table td { padding: 0.65rem 0.5rem; }
.summary-table td:first-child { color: #64748b; font-weight: 500; }
.summary-table td:last-child  { color: #e2e8f0; font-weight: 500; text-align: right; }

/* ── Info box ── */
[data-testid="stInfo"] {
    background: rgba(99,102,241,0.08) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 12px !important;
    color: #a5b4fc !important;
    font-size: 0.82rem !important;
}
[data-testid="stInfo"] p { color: #a5b4fc !important; }

/* ── Probability bar ── */
.prob-bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    height: 8px;
    margin: 8px 0 4px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #6366f1, #10b981);
    transition: width 0.6s ease;
}
.prob-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #64748b;
    margin-bottom: 2px;
}

/* ── Footer ── */
.footer-text {
    text-align: center;
    font-size: 0.75rem;
    color: #334155;
    letter-spacing: 0.05em;
    padding: 1rem 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("myapp/myapp/model.pkl",     "rb") as f: model     = pickle.load(f)
    with open("myapp/myapp/threshold.pkl", "rb") as f: threshold = pickle.load(f)
    return model, threshold

model, best_threshold = load_model()

# ── Feature engineering ───────────────────────────────────────────────────────
def build_features(inp):
    data = pd.DataFrame([inp])
    data["TotalSpend"] = (data["MntWines"] + data["MntFruits"] + data["MntMeatProducts"]
                          + data["MntFishProducts"] + data["MntSweetProducts"] + data["MntGoldProds"])
    data["TotalChildren"]          = data["Kidhome"] + data["Teenhome"]
    data["IsParent"]               = (data["TotalChildren"] > 0).astype(int)
    data["Income_Per_Person"]      = data["Income"] / (data["TotalChildren"] + 1)
    data["TotalPurchases"]         = (data["NumWebPurchases"] + data["NumCatalogPurchases"]
                                      + data["NumStorePurchases"])
    data["AvgPurchaseValue"]       = data["TotalSpend"] / (data["TotalPurchases"] + 1)
    data["Spend_to_Income_Ratio"]  = data["TotalSpend"] / (data["Income"] + 1)
    data["TotalCampaignsAccepted"] = (data["AcceptedCmp1"] + data["AcceptedCmp2"]
                                      + data["AcceptedCmp3"] + data["AcceptedCmp4"]
                                      + data["AcceptedCmp5"])
    return data

# ══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">⚡ AI-Powered · Random Forest + SMOTE</div>
    <div class="hero-title">Campaign <span>Response</span> Predictor</div>
    <div class="hero-subtitle">
        Identify which customers will respond to your campaign before spending a rupee.
        Enter customer details below to get an instant prediction.
    </div>
</div>

<div class="stat-bar">
    <div class="stat-item">
        <div class="stat-number indigo">5,237</div>
        <div class="stat-label">Training Records</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">82.4%</div>
        <div class="stat-label">Model Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-number green">0.71</div>
        <div class="stat-label">ROC-AUC Score</div>
    </div>
    <div class="stat-item">
        <div class="stat-number amber">8</div>
        <div class="stat-label">Models Compared</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">36</div>
        <div class="stat-label">Input Features</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">Customer Profile Input</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

# ── COLUMN 1 — Personal ───────────────────────────────────────────────────────
with col1:
    st.markdown("""
    <div class="input-card">
        <div class="card-title">
            <span class="card-icon icon-indigo">👤</span> Personal Details
        </div>
    </div>
    """, unsafe_allow_html=True)

    year_birth = st.number_input("Year of Birth", min_value=1940, max_value=2005, value=1980)
    age = 2025 - year_birth
    education      = st.selectbox("Education Level", ["Graduation", "PhD", "Master", "2n Cycle", "Basic"])
    marital_status = st.selectbox("Marital Status",  ["Married", "Single", "Together", "Divorced", "Widow"])
    income         = st.number_input("Annual Income (Rs)", min_value=0, max_value=500000, value=60000, step=1000)
    kidhome        = st.number_input("Kids at Home",       min_value=0, max_value=5, value=0)
    teenhome       = st.number_input("Teens at Home",      min_value=0, max_value=5, value=0)
    recency        = st.number_input("Days Since Last Purchase", min_value=0, max_value=365, value=30)
    tenure_days    = st.number_input("Days Since Enrolled",      min_value=0, max_value=5000, value=365)
    complain       = st.selectbox("Filed a Complaint?", ["No", "Yes"])
    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);
    border-radius:10px;padding:10px 14px;margin-top:8px;font-size:0.82rem;color:#a5b4fc;">
    📅 &nbsp; Computed Age: <strong style="color:#ffffff">{age} years</strong>
    </div>
    """, unsafe_allow_html=True)

# ── COLUMN 2 — Spending ───────────────────────────────────────────────────────
with col2:
    st.markdown("""
    <div class="input-card">
        <div class="card-title">
            <span class="card-icon icon-green">💳</span> Spending (Last 2 Years)
        </div>
    </div>
    """, unsafe_allow_html=True)

    mnt_wines  = st.number_input("🍷 Wines (Rs)",         min_value=0, max_value=5000, value=200, step=10)
    mnt_fruits = st.number_input("🍎 Fruits (Rs)",        min_value=0, max_value=2000, value=30,  step=5)
    mnt_meat   = st.number_input("🥩 Meat Products (Rs)", min_value=0, max_value=2000, value=100, step=10)
    mnt_fish   = st.number_input("🐟 Fish Products (Rs)", min_value=0, max_value=2000, value=40,  step=5)
    mnt_sweets = st.number_input("🍬 Sweet Products (Rs)",min_value=0, max_value=2000, value=30,  step=5)
    mnt_gold   = st.number_input("🏅 Gold Products (Rs)", min_value=0, max_value=2000, value=50,  step=5)

    total_spend = mnt_wines + mnt_fruits + mnt_meat + mnt_fish + mnt_sweets + mnt_gold
    pct = min(int((total_spend / 2525) * 100), 100)
    st.markdown(f"""
    <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.18);
    border-radius:14px;padding:14px 18px;margin-top:16px;">
        <div style="font-size:0.72rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">
            Total Spend
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;color:#10b981;">
            Rs {total_spend:,}
        </div>
        <div class="prob-bar-wrap" style="margin-top:10px;">
            <div class="prob-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#10b981,#34d399);"></div>
        </div>
        <div style="font-size:0.72rem;color:#64748b;margin-top:4px;">{pct}% of max observed spend</div>
    </div>
    """, unsafe_allow_html=True)

# ── COLUMN 3 — Purchases + Campaigns ─────────────────────────────────────────
with col3:
    st.markdown("""
    <div class="input-card">
        <div class="card-title">
            <span class="card-icon icon-amber">🛒</span> Purchases & Campaigns
        </div>
    </div>
    """, unsafe_allow_html=True)

    num_deals   = st.number_input("Discount Purchases", min_value=0, max_value=30, value=2)
    num_web     = st.number_input("Web Purchases",      min_value=0, max_value=30, value=3)
    num_catalog = st.number_input("Catalog Purchases",  min_value=0, max_value=30, value=2)
    num_store   = st.number_input("Store Purchases",    min_value=0, max_value=30, value=4)
    num_web_vis = st.number_input("Web Visits / Month", min_value=0, max_value=30, value=5)

    st.markdown("""
    <div style="font-size:0.78rem;color:#64748b;text-transform:uppercase;
    letter-spacing:0.07em;margin:16px 0 8px;font-weight:600;">
        Past Campaign Responses
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: cmp1 = st.selectbox("Cmp 1", [0,1], index=0, label_visibility="visible")
    with c2: cmp2 = st.selectbox("Cmp 2", [0,1], index=0, label_visibility="visible")
    with c3: cmp3 = st.selectbox("Cmp 3", [0,1], index=0, label_visibility="visible")
    with c4: cmp4 = st.selectbox("Cmp 4", [0,1], index=0, label_visibility="visible")
    with c5: cmp5 = st.selectbox("Cmp 5", [0,1], index=0, label_visibility="visible")

    total_cmp = cmp1 + cmp2 + cmp3 + cmp4 + cmp5
    cmp_color = "#10b981" if total_cmp >= 3 else "#fbbf24" if total_cmp >= 1 else "#64748b"
    cmp_label = "Strong engagement" if total_cmp >= 3 else "Some engagement" if total_cmp >= 1 else "No prior engagement"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
    border-radius:12px;padding:12px 16px;margin-top:10px;display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:0.82rem;color:#94a3b8;">Accepted</span>
        <span style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:{cmp_color};">
            {total_cmp}/5
        </span>
        <span style="font-size:0.72rem;color:{cmp_color};">{cmp_label}</span>
    </div>
    """, unsafe_allow_html=True)

# ── PREDICT BUTTON ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-head">Prediction Engine</div>', unsafe_allow_html=True)

predict_clicked = st.button("⚡  Run Prediction Analysis", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if predict_clicked:

    customer_input = {
        "Age": age, "Year_Birth": year_birth, "Income": income,
        "Kidhome": kidhome, "Teenhome": teenhome, "Recency": recency,
        "MntWines": mnt_wines, "MntFruits": mnt_fruits, "MntMeatProducts": mnt_meat,
        "MntFishProducts": mnt_fish, "MntSweetProducts": mnt_sweets, "MntGoldProds": mnt_gold,
        "NumDealsPurchases": num_deals, "NumWebPurchases": num_web,
        "NumCatalogPurchases": num_catalog, "NumStorePurchases": num_store,
        "NumWebVisitsMonth": num_web_vis,
        "AcceptedCmp1": cmp1, "AcceptedCmp2": cmp2, "AcceptedCmp3": cmp3,
        "AcceptedCmp4": cmp4, "AcceptedCmp5": cmp5,
        "Complain": 1 if complain == "Yes" else 0,
        "Tenure_Days": tenure_days, "Education": education, "Marital_Status": marital_status,
    }

    data        = build_features(customer_input)
    probability = model.predict_proba(data)[0][1]
    prediction  = 1 if probability >= best_threshold else 0
    prob_pct    = int(probability * 100)
    bar_pct     = min(prob_pct, 100)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-head">Analysis Results</div>', unsafe_allow_html=True)

    # ── Metric row ────────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Response Probability",    f"{prob_pct}%")
    with m2: st.metric("Decision Threshold",       f"{best_threshold:.2f}")
    with m3: st.metric("Past Campaigns Accepted",  f"{total_cmp} / 5")
    with m4: st.metric("Total Spend",              f"Rs {total_spend:,}")

    # ── Probability bar ───────────────────────────────────────────────────────
    bar_color = "#10b981" if prediction == 1 else "#ef4444"
    st.markdown(f"""
    <div style="margin: 1.2rem 0;">
        <div class="prob-label">
            <span>Response Likelihood</span>
            <span style="color:#ffffff;font-weight:600;">{prob_pct}%</span>
        </div>
        <div class="prob-bar-wrap" style="height:12px;">
            <div class="prob-bar-fill" style="width:{bar_pct}%;background:linear-gradient(90deg,
            {'#6366f1, #10b981' if prediction==1 else '#991b1b, #ef4444'});"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#334155;margin-top:4px;">
            <span>0% — Very Unlikely</span>
            <span>Threshold: {best_threshold:.0%}</span>
            <span>100% — Certain</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Verdict ───────────────────────────────────────────────────────────────
    if prediction == 1:
        st.markdown(f"""
        <div class="result-respond">
            <div class="result-icon">✅</div>
            <div class="result-verdict">Will Respond to Campaign</div>
            <div class="result-sub">This customer has a <strong style="color:#10b981">{prob_pct}%</strong>
             probability of responding — above the {best_threshold:.0%} threshold.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-no-respond">
            <div class="result-icon">❌</div>
            <div class="result-verdict">Will Not Respond to Campaign</div>
            <div class="result-sub">This customer has only a <strong style="color:#ef4444">{prob_pct}%</strong>
             probability of responding — below the {best_threshold:.0%} threshold.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Recommendation ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-head">Marketing Recommendation</div>', unsafe_allow_html=True)

    if probability >= 0.6:
        st.markdown("""
        <div class="rec-card rec-high">
            <div class="rec-emoji">🔥</div>
            <div>
                <div class="rec-title">HIGH Priority — Include in Campaign</div>
                <div class="rec-body">Strong candidate. Allocate premium outreach — personal call, personalised email, and exclusive offer. Excellent ROI expected.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif probability >= best_threshold:
        st.markdown("""
        <div class="rec-card rec-mod">
            <div class="rec-emoji">✅</div>
            <div>
                <div class="rec-title">MODERATE Priority — Worth Targeting</div>
                <div class="rec-body">Decent candidate. Include in standard campaign outreach. Monitor response and follow up if no engagement after 7 days.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif probability >= 0.25:
        st.markdown("""
        <div class="rec-card rec-low">
            <div class="rec-emoji">⚠️</div>
            <div>
                <div class="rec-title">LOW Priority — Minimal Outreach Only</div>
                <div class="rec-body">Unlikely to respond. If budget allows, include in low-cost email-only campaign. Do not allocate phone call or premium budget.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="rec-card rec-vlow">
            <div class="rec-emoji">🚫</div>
            <div>
                <div class="rec-title">SKIP — Not Cost-Effective to Target</div>
                <div class="rec-body">Very unlikely to respond. Exclude from this campaign entirely. Re-evaluate after customer shows new purchase activity.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Customer Summary ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-head">Customer Profile Summary</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2, gap="medium")
    with s1:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.4rem 1.6rem;">
            <div style="font-size:0.72rem;color:#6366f1;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:1rem;">Demographics</div>
            <table class="summary-table">
                <tr><td>Age</td><td>{age} years</td></tr>
                <tr><td>Year of Birth</td><td>{year_birth}</td></tr>
                <tr><td>Education</td><td>{education}</td></tr>
                <tr><td>Marital Status</td><td>{marital_status}</td></tr>
                <tr><td>Children at Home</td><td>{kidhome + teenhome}</td></tr>
                <tr><td>Annual Income</td><td>Rs {income:,}</td></tr>
                <tr><td>Days Since Purchase</td><td>{recency} days</td></tr>
                <tr><td>Member Since</td><td>{tenure_days} days ago</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.4rem 1.6rem;">
            <div style="font-size:0.72rem;color:#10b981;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:1rem;">Behaviour & Spend</div>
            <table class="summary-table">
                <tr><td>Total Spend</td><td>Rs {total_spend:,}</td></tr>
                <tr><td>Web Purchases</td><td>{num_web}</td></tr>
                <tr><td>Catalog Purchases</td><td>{num_catalog}</td></tr>
                <tr><td>Store Purchases</td><td>{num_store}</td></tr>
                <tr><td>Discount Purchases</td><td>{num_deals}</td></tr>
                <tr><td>Web Visits / Month</td><td>{num_web_vis}</td></tr>
                <tr><td>Campaigns Accepted</td><td>{total_cmp} of 5</td></tr>
                <tr><td>Filed Complaint</td><td>{complain}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer-text">
    Marketing Campaign Response Predictor &nbsp;·&nbsp;
    Random Forest + SMOTE &nbsp;·&nbsp;
    Built with Streamlit &nbsp;·&nbsp;
    Accuracy 82.4% &nbsp;·&nbsp; ROC-AUC 0.71
</div>
""", unsafe_allow_html=True)
