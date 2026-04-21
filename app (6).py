import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from datetime import datetime, date

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FinBridge Credit Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS — Professional Navy/Gold Theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --navy:       #080F1E;
    --navy-mid:   #0E1E35;
    --navy-card:  #111F38;
    --navy-light: #1A3355;
    --navy-hover: #1E3D65;
    --gold:       #C8960C;
    --gold-light: #F0B429;
    --gold-dim:   #A07209;
    --teal:       #0DD4BD;
    --teal-dim:   #0A9E8C;
    --red:        #E05C5C;
    --red-dim:    #B54444;
    --green:      #3EC87A;
    --green-dim:  #2FA05E;
    --purple:     #9B72CF;
    --text-1:     #EDF2FA;
    --text-2:     #8FA3C0;
    --text-3:     #4A6080;
    --border:     #1C3050;
    --border-2:   #243D5E;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--text-1);
}
.main { background-color: var(--navy); }
.block-container { padding: 1.8rem 2.5rem 3rem; max-width: 1440px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--navy-mid);
    border-right: 1px solid var(--border);
    min-width: 240px !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1rem 0.8rem; }

/* ── Typography ── */
h1,h2,h3 { font-family:'Playfair Display',serif; color:var(--text-1); }

/* ── Card system ── */
.fb-card {
    background:var(--navy-card);
    border:1px solid var(--border);
    border-radius:14px;
    padding:1.4rem 1.6rem;
    margin-bottom:1rem;
}
.fb-card-gold {
    background:linear-gradient(140deg,#162C4A 0%,#0A1628 100%);
    border:1px solid var(--gold);
    border-radius:14px;
    padding:1.4rem 1.6rem;
    margin-bottom:1rem;
}
.fb-card-teal {
    background:linear-gradient(140deg,#0D2B35 0%,#080F1E 100%);
    border:1px solid var(--teal);
    border-radius:14px;
    padding:1.4rem 1.6rem;
    margin-bottom:1rem;
}
.fb-card-red {
    background:linear-gradient(140deg,#2A1A1A 0%,#080F1E 100%);
    border:1px solid var(--red);
    border-radius:14px;
    padding:1.4rem 1.6rem;
    margin-bottom:1rem;
}
.fb-card-purple {
    background:linear-gradient(140deg,#1E1835 0%,#080F1E 100%);
    border:1px solid var(--purple);
    border-radius:14px;
    padding:1.4rem 1.6rem;
    margin-bottom:1rem;
}

/* ── Score hero ── */
.score-hero {
    text-align:center;
    padding:2.2rem 1.5rem;
    background:linear-gradient(140deg,var(--navy-card) 0%,var(--navy-light) 100%);
    border-radius:18px;
    border:2px solid var(--gold);
    position:relative;
    overflow:hidden;
}
.score-hero::before {
    content:'';
    position:absolute;
    top:-40%;left:-40%;
    width:180%;height:180%;
    background:radial-gradient(ellipse at center,rgba(240,180,41,0.04) 0%,transparent 70%);
    pointer-events:none;
}
.score-num {
    font-family:'Playfair Display',serif;
    font-size:5.5rem;
    font-weight:700;
    background:linear-gradient(135deg,var(--gold-light) 30%,var(--teal) 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    line-height:1;
}

/* ── Metric cards ── */
.metric-card {
    background:var(--navy-card);
    border:1px solid var(--border);
    border-radius:12px;
    padding:1.1rem 0.9rem;
    text-align:center;
}
.metric-val {
    font-family:'Playfair Display',serif;
    font-size:1.75rem;
    font-weight:600;
    color:var(--gold-light);
}
.metric-lab { font-size:0.72rem; color:var(--text-2); margin-top:0.25rem; letter-spacing:0.03em; }

/* ── Badges ── */
.badge {
    display:inline-block;
    padding:0.28rem 0.85rem;
    border-radius:50px;
    font-size:0.72rem;
    font-weight:700;
    letter-spacing:0.06em;
    text-transform:uppercase;
}
.badge-green  { background:rgba(62,200,122,0.12);  color:var(--green);  border:1px solid var(--green); }
.badge-gold   { background:rgba(240,180,41,0.12);   color:var(--gold-light); border:1px solid var(--gold-light); }
.badge-red    { background:rgba(224,92,92,0.12);    color:var(--red);    border:1px solid var(--red); }
.badge-teal   { background:rgba(13,212,189,0.12);   color:var(--teal);   border:1px solid var(--teal); }
.badge-purple { background:rgba(155,114,207,0.12);  color:var(--purple); border:1px solid var(--purple); }

/* ── Section titles ── */
.section-title {
    font-family:'Playfair Display',serif;
    font-size:1.55rem;
    color:var(--gold-light);
    border-left:4px solid var(--gold);
    padding-left:1rem;
    margin-bottom:0.4rem;
}
.section-sub { font-size:0.83rem; color:var(--text-2); margin-bottom:1.5rem; padding-left:1.1rem; }

/* ── Perspective labels ── */
.perspective-label {
    display:inline-flex;
    align-items:center;
    gap:0.4rem;
    padding:0.25rem 0.75rem;
    border-radius:6px;
    font-size:0.72rem;
    font-weight:600;
    letter-spacing:0.08em;
    text-transform:uppercase;
    margin-bottom:0.8rem;
}
.pl-nbfc   { background:rgba(224,92,92,0.15);    color:var(--red);    border:1px solid var(--red); }
.pl-consumer{ background:rgba(62,200,122,0.15);  color:var(--green);  border:1px solid var(--green); }
.pl-bank   { background:rgba(13,212,189,0.15);   color:var(--teal);   border:1px solid var(--teal); }
.pl-bureau { background:rgba(155,114,207,0.15);  color:var(--purple); border:1px solid var(--purple); }

/* ── Buttons ── */
.stButton>button {
    background:linear-gradient(135deg,var(--gold-light),var(--gold-dim));
    color:var(--navy);
    font-weight:700;
    border:none;
    border-radius:9px;
    padding:0.6rem 2rem;
    font-family:'DM Sans',sans-serif;
    letter-spacing:0.02em;
    transition:all 0.2s;
}
.stButton>button:hover { opacity:0.87; transform:translateY(-1px); }

/* ── Info banners ── */
.info-banner {
    background:rgba(13,212,189,0.07);
    border:1px solid var(--teal);
    border-radius:10px;
    padding:0.9rem 1.1rem;
    color:var(--teal);
    font-size:0.85rem;
    margin-bottom:1rem;
}
.warn-banner {
    background:rgba(240,180,41,0.07);
    border:1px solid var(--gold-light);
    border-radius:10px;
    padding:0.9rem 1.1rem;
    color:var(--gold-light);
    font-size:0.85rem;
    margin-bottom:1rem;
}
.danger-banner {
    background:rgba(224,92,92,0.07);
    border:1px solid var(--red);
    border-radius:10px;
    padding:0.9rem 1.1rem;
    color:var(--red);
    font-size:0.85rem;
    margin-bottom:1rem;
}

/* ── KFS / document styling ── */
.kfs-doc {
    background:var(--navy-mid);
    border:2px solid var(--border-2);
    border-radius:12px;
    padding:2rem;
    font-size:0.83rem;
    line-height:1.7;
}
.kfs-header {
    font-family:'Playfair Display',serif;
    font-size:1.2rem;
    color:var(--gold-light);
    border-bottom:2px solid var(--border-2);
    padding-bottom:0.8rem;
    margin-bottom:1.2rem;
}
.kfs-row {
    display:grid;
    grid-template-columns:220px 1fr;
    gap:0.5rem 1rem;
    padding:0.5rem 0;
    border-bottom:1px solid var(--border);
}
.kfs-key { color:var(--text-2); }
.kfs-val { color:var(--text-1); font-weight:500; }

/* ── AA Flow ── */
.aa-node {
    background:var(--navy-card);
    border:1px solid var(--border-2);
    border-radius:10px;
    padding:0.8rem 1rem;
    text-align:center;
    font-size:0.8rem;
}
.aa-node.active { border-color:var(--teal); background:rgba(13,212,189,0.06); }
.aa-arrow { text-align:center; color:var(--teal); font-size:1.2rem; margin:0.2rem 0; }

/* ── Path to Prime ── */
.whatif-card {
    background:var(--navy-card);
    border:1px solid var(--border-2);
    border-radius:12px;
    padding:1.2rem;
    margin-bottom:0.7rem;
    display:flex;
    align-items:center;
    gap:1rem;
}
.whatif-delta {
    font-family:'Playfair Display',serif;
    font-size:1.5rem;
    font-weight:700;
    min-width:70px;
    text-align:center;
}

/* ── Mono numbers ── */
.mono { font-family:'JetBrains Mono',monospace; }

/* ── Dividers ── */
.fb-divider { border:none; border-top:1px solid var(--border); margin:1.8rem 0; }

/* ── Inputs ── */
.stNumberInput input,.stTextInput input { background:var(--navy-light)!important; color:var(--text-1)!important; border:1px solid var(--border)!important; border-radius:8px!important; }
.stSlider [data-baseweb="slider"] { accent-color:var(--gold-light); }

/* ── Logo ── */
.logo-area { text-align:center; padding:1.2rem 0 0.8rem; }
.logo-text  { font-family:'Playfair Display',serif; font-size:1.7rem; font-weight:700; background:linear-gradient(135deg,var(--gold-light),var(--teal)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.logo-sub   { font-size:0.62rem; color:var(--text-3); letter-spacing:0.2em; text-transform:uppercase; margin-top:0.1rem; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background:var(--navy-mid); border-radius:10px; padding:0.25rem; gap:2px; }
.stTabs [data-baseweb="tab"]      { color:var(--text-2); border-radius:8px; font-size:0.83rem; }
.stTabs [aria-selected="true"]    { background:var(--gold-light)!important; color:var(--navy)!important; font-weight:700; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--navy); }
::-webkit-scrollbar-thumb { background:var(--navy-light); border-radius:3px; }

/* ── Nav buttons ── */
.nav-btn { width:100%; text-align:left; padding:0.5rem 0.8rem; border-radius:8px; font-size:0.84rem; cursor:pointer; border:none; }

label { color:var(--text-2)!important; font-size:0.82rem!important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
PROFILE_TYPES = ["Student", "Freelancer / Gig Worker", "Salaried Professional", "Self-Employed / Business Owner"]

LOAN_PURPOSES = {
    "🏠 Home Purchase / Construction":     {"rate_range": (8.50, 10.50), "max_tenure": 30, "industry": "Housing Finance"},
    "🚗 Vehicle Purchase":                  {"rate_range": (7.50, 12.00), "max_tenure":  7, "industry": "Auto Finance"},
    "🎓 Education Loan":                    {"rate_range": (8.00, 13.50), "max_tenure": 15, "industry": "Education Finance"},
    "💼 Business Expansion / Working Capital": {"rate_range": (10.50, 16.00), "max_tenure": 10, "industry": "MSME Finance"},
    "🏥 Medical Emergency":                 {"rate_range": (11.00, 14.50), "max_tenure":  5, "industry": "Healthcare Finance"},
    "⚙️ Equipment / Machinery":             {"rate_range": (10.00, 15.00), "max_tenure":  7, "industry": "Asset Finance"},
    "🌏 Travel / Lifestyle":               {"rate_range": (13.00, 18.00), "max_tenure":  3, "industry": "Personal Finance"},
    "🔄 Debt Consolidation":               {"rate_range": (12.00, 16.50), "max_tenure":  5, "industry": "Refinancing"},
    "🏗️ Renovation / Home Improvement":    {"rate_range": (9.50, 13.00), "max_tenure": 10, "industry": "Home Finance"},
    "💡 Start-Up / New Venture":           {"rate_range": (12.00, 18.00), "max_tenure":  7, "industry": "Venture Finance"},
}

SCORE_BANDS = {
    (750, 900): ("Excellent",  "badge-green",  "#3EC87A", 0.02, 0.30),
    (700, 749): ("Good",       "badge-green",  "#7CC87E", 0.05, 0.50),
    (650, 699): ("Fair",       "badge-gold",   "#F0B429", 0.10, 0.65),
    (600, 649): ("Marginal",   "badge-gold",   "#E08929", 0.18, 0.75),
    (300, 599): ("Poor",       "badge-red",    "#E05C5C", 0.30, 0.85),
}

# PD, LGD defaults per band: (PD, LGD)
RISK_PARAMS = {
    "Excellent":  (0.005, 0.25),
    "Good":       (0.015, 0.35),
    "Fair":       (0.040, 0.45),
    "Marginal":   (0.090, 0.55),
    "Poor":       (0.200, 0.65),
}

COLLATERAL_LGD = {
    "No":               0.65,
    "Yes – Property":   0.25,
    "Yes – FD/Savings": 0.10,
    "Yes – Gold":       0.20,
    "Yes – Vehicle":    0.40,
}

WHATIF_ACTIONS = [
    ("Stop using BNPL / Pay-Later apps for 3 months",        30, "Reduces revolving obligations signal"),
    ("Maintain ₹10,000 minimum balance for 6 months",         25, "Eliminates near-overdraft risk flag"),
    ("Reduce credit card utilisation below 30%",              20, "Lowers revolving credit pressure"),
    ("File ITR on time for next 2 consecutive years",         35, "Proves income regularity to lenders"),
    ("Start a SIP of ₹5,000/month for 12 months",            40, "Builds demonstrable savings behaviour"),
    ("Close 1 inactive loan account",                         15, "Reduces open obligation count"),
    ("Zero bounces for next 12 months",                       45, "Clears the highest negative signal"),
    ("Increase monthly income by 15% (side income / raise)", 50, "Directly improves income stability score"),
]

ORTHOGONAL_SIGNALS = [
    ("Utility Bill Consistency",      "Cannot track",     "Identifies regular monthly obligations", "Positive if consistent"),
    ("UPI Receipt Seasonality",       "Cannot track",     "Detects income peaks/troughs",           "Flags irregular earners"),
    ("Salary Credit Day Pattern",     "Not available",    "Day-of-month salary credit consistency",  "Strong stability signal"),
    ("Weekend vs Weekday Spending",   "Not available",    "Lifestyle expenditure behaviour",         "Risk profiling signal"),
    ("Cash Deposit Frequency",        "Partial only",     "Informal income detection",               "Flags cash-heavy businesses"),
    ("Merchant Category Spending",    "Cannot see",       "Where money is spent monthly",            "Budget discipline scoring"),
    ("Overdraft Day Frequency",       "Not captured",     "Days account went negative",              "Major default predictor"),
    ("Inward Remittance Pattern",     "Not available",    "Foreign income / NRI signals",            "Income diversification"),
    ("Auto-debit Failure Rate",       "Post-default only","Failed recurring payment rate",           "Early warning trigger"),
    ("Average Quarterly Balance",     "Not available",    "Liquidity buffer maintained",             "Resilience indicator"),
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def get_score_band(score):
    for (lo, hi), (label, badge, color, _pd, _lgd) in SCORE_BANDS.items():
        if lo <= score <= hi:
            return label, badge, color
    return "Poor", "badge-red", "#E05C5C"

def get_risk_params(label):
    return RISK_PARAMS.get(label, (0.30, 0.65))

def calc_emi(principal, annual_rate, months):
    if annual_rate <= 0 or months <= 0:
        return principal / months if months > 0 else 0
    r = annual_rate / (12 * 100)
    emi = principal * r * ((1 + r) ** months) / (((1 + r) ** months) - 1)
    return round(emi, 2)

def calc_apr(nominal_rate, processing_fee_pct, tenure_months):
    """Approximate APR including processing fee."""
    processing_adj = (processing_fee_pct / 100) * 12 / tenure_months
    return round(nominal_rate + processing_adj, 2)

def format_inr(amount):
    if amount >= 1e7:
        return f"₹{amount/1e7:.2f} Cr"
    elif amount >= 1e5:
        return f"₹{amount/1e5:.2f} L"
    return f"₹{amount:,.0f}"

def months_to_label(months):
    if months >= 12:
        y, m = divmod(int(months), 12)
        return f"{y}Y {m}M" if m else f"{y} Years"
    return f"{int(months)} Months"

def compute_finbridge_score(data):
    """
    FinBridge 6-Dimension Proprietary Score — 300 to 900 scale.
    Weights: Income 25 | CashFlow 20 | Savings 18 | DSCR 17 | Expenditure 12 | Account 8
    """
    incomes  = np.array(data.get("annual_income",  [1]),   dtype=float)
    expenses = np.array(data.get("annual_expense", [0.8]), dtype=float)
    savings  = np.array(data.get("annual_savings", [0.2]), dtype=float)
    emis     = np.array(data.get("existing_emis",  [0]),   dtype=float)
    bounces  = np.array(data.get("bounce_count",   [0]),   dtype=float)
    incomes  = np.where(incomes == 0, 1, incomes)

    # 1. Income Stability & Growth (25)
    growth = np.diff(incomes) / incomes[:-1] if len(incomes) > 1 else np.array([0.0])
    avg_g  = float(np.mean(growth))
    cov    = float(np.std(incomes) / np.mean(incomes))
    s1     = max(0, min(25, 25 * (0.5 * (1 - min(cov, 1)) + 0.5 * min(avg_g / 0.12, 1))))

    # 2. Cash-Flow Consistency (20)
    net     = incomes - expenses - emis
    pos_r   = float(np.sum(net > 0) / len(net))
    cf_cov  = float(np.std(net) / (np.mean(incomes) + 1e-9))
    s2      = max(0, min(20, 20 * (0.6 * pos_r + 0.4 * max(0, 1 - cf_cov))))

    # 3. Savings Behaviour (18)
    sav_r   = savings / incomes
    avg_sr  = float(np.mean(sav_r))
    s3      = max(0, min(18, 18 * min(avg_sr / 0.22, 1)))

    # 4. Debt Service Coverage (17)
    dscr    = incomes / (emis + 1)
    avg_d   = float(np.mean(dscr))
    s4      = max(0, min(17, 17 * min((avg_d - 1) / 4.5, 1)))

    # 5. Expenditure Discipline (12)
    exp_r   = expenses / incomes
    avg_er  = float(np.mean(exp_r))
    s5      = max(0, min(12, 12 * max(0, 1 - avg_er / 0.82)))

    # 6. Account Behaviour / Bounces (8)
    tot_bnc = float(np.sum(bounces))
    s6      = max(0, min(8, 8 * max(0, 1 - tot_bnc / 8)))

    raw = s1 + s2 + s3 + s4 + s5 + s6
    score = int(300 + (raw / 100) * 600)
    score = max(300, min(900, score))

    comps = {
        "Income Stability":        round(s1, 2),
        "Cash-Flow Consistency":   round(s2, 2),
        "Savings Behaviour":       round(s3, 2),
        "Debt Coverage (DSCR)":    round(s4, 2),
        "Expenditure Discipline":  round(s5, 2),
        "Account Behaviour":       round(s6, 2),
    }
    return score, comps, round(raw, 2)

def estimate_cibil_score(data):
    incomes = np.array(data.get("annual_income",  [1]),  dtype=float)
    emis    = np.array(data.get("existing_emis",  [0]),  dtype=float)
    bounces = np.array(data.get("bounce_count",   [0]),  dtype=float)
    avg_inc = float(np.mean(incomes))
    avg_emi = float(np.mean(emis))
    pti     = avg_emi / (avg_inc + 1e-9)
    pti_sc  = max(0, 350 * (1 - min(pti, 0.6) / 0.6))
    bnc_pen = min(float(np.sum(bounces)) * 35, 200)
    score   = int(560 + pti_sc - bnc_pen)
    return max(300, min(900, score))

def max_loan_eligible(data, interest_rate, tenure_months, foir=0.55):
    incomes  = np.array(data.get("annual_income",  [1]),  dtype=float)
    expenses = np.array(data.get("annual_expense", [0.8]),dtype=float)
    emis     = np.array(data.get("existing_emis",  [0]),  dtype=float)
    m_inc    = float(np.mean(incomes))   / 12
    m_exp    = float(np.mean(expenses))  / 12
    m_emi    = float(np.mean(emis))      / 12
    disp     = max(0, m_inc * foir - m_emi)
    if interest_rate <= 0 or tenure_months <= 0:
        return disp * tenure_months, disp
    r        = interest_rate / (12 * 100)
    max_loan = disp * ((1 + r) ** tenure_months - 1) / (r * (1 + r) ** tenure_months)
    return round(max_loan, 0), round(disp, 0)

def apply_adjustments(score, cibil, data):
    itr      = data.get("itr_filed", "Yes, all years")
    defaults = data.get("prev_defaults", "No")
    cc_util  = data.get("credit_card_util", 30)
    acc_age  = data.get("oldest_account_yr", 5)

    if itr == "Yes, all years":  score = min(900, score + 15)
    elif itr == "Occasionally":  score = max(300, score - 20)
    elif itr == "No":            score = max(300, score - 45)

    if defaults == "Yes – pending":
        score = max(300, score - 85); cibil = max(300, cibil - 110)
    elif defaults == "Yes – resolved":
        score = max(300, score - 30); cibil = max(300, cibil - 55)

    if cc_util > 75:
        score = max(300, score - 25); cibil = max(300, cibil - 30)
    elif cc_util < 30:
        score = min(900, score + 10); cibil = min(900, cibil + 15)

    if acc_age >= 10: score = min(900, score + 15); cibil = min(900, cibil + 20)
    elif acc_age >= 5: score = min(900, score + 5)

    return score, cibil

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = dict(
    step="profile",
    profile_data={},
    stmt_data={},
    scores_computed=False,
    finbridge_score=0,
    cibil_score=0,
    components={},
    raw_score=0,
    loan_purpose=list(LOAN_PURPOSES.keys())[0],
    loan_amount=1500000.0,
    loan_tenure=10,
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
NAV = [
    ("👤", "Profile Setup",            "profile"),
    ("📊", "Bank Statement Input",     "statement"),
    ("🏅", "FinBridge Score",          "score"),
    ("━━━ EXPERT PERSPECTIVES ━━━",   None,           None),
    ("🏛️", "NBFC Risk Desk",           "nbfc"),
    ("💚", "Consumer Transparency",    "consumer"),
    ("⚖️", "CIBIL vs FinBridge",       "comparison"),
    ("🏦", "Bank & Compliance",        "bank"),
    ("━━━ DECISION TOOLS ━━━",        None,           None),
    ("💰", "Loan Eligibility",         "loan"),
    ("📅", "EMI Planner",             "emi"),
    ("📋", "Credit Report",           "report"),
]

with st.sidebar:
    st.markdown("""
    <div class="logo-area">
        <div class="logo-text">FinBridge</div>
        <div class="logo-sub">Credit Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1C3050;margin:0.5rem 0 0.8rem;'>", unsafe_allow_html=True)

    for item in NAV:
        if len(item) == 2:   # section divider
            st.markdown(f"<div style='font-size:0.62rem;color:#2A4060;font-weight:700;letter-spacing:0.12em;padding:0.6rem 0.3rem 0.2rem;'>{item[0]}</div>", unsafe_allow_html=True)
            continue
        icon, label, key = item
        if key is None:
            st.markdown(f"<div style='font-size:0.62rem;color:#2A4060;font-weight:700;letter-spacing:0.12em;padding:0.6rem 0.3rem 0.2rem;'>{icon} {label}</div>", unsafe_allow_html=True)
            continue
        active = st.session_state.step == key
        bg = "background:linear-gradient(90deg,rgba(26,51,85,0.9),rgba(17,34,64,0.6));border-left:3px solid #F0B429;" if active else "background:transparent;border-left:3px solid transparent;"
        col_style = "color:#F0B429;font-weight:600;" if active else "color:#8FA3C0;"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.step = key
            st.rerun()

    st.markdown("<hr style='border-color:#1C3050;margin:0.8rem 0;'>", unsafe_allow_html=True)

    if st.session_state.scores_computed:
        fb = st.session_state.finbridge_score
        lbl, bdg, col = get_score_band(fb)
        st.markdown(f"""
        <div style='text-align:center;padding:1rem;background:var(--navy-card);border-radius:12px;border:1px solid var(--border);'>
            <div style='font-size:0.62rem;color:#4A6080;letter-spacing:0.12em;text-transform:uppercase;'>FinBridge Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:2.8rem;font-weight:700;color:#F0B429;line-height:1;margin:0.3rem 0;'>{fb}</div>
            <span class='badge {bdg}'>{lbl}</span>
            <div style='font-size:0.65rem;color:#4A6080;margin-top:0.6rem;'>{st.session_state.profile_data.get("name","")}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:1.5rem;text-align:center;font-size:0.6rem;color:#2A4060;line-height:1.6;'>
        FinBridge © 2025<br>Credit Intelligence Platform<br>
        <span style='color:#1A3355;'>Not a Registered Credit Bureau</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: PROFILE SETUP ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == "profile":
    st.markdown("<div class='section-title'>👤 Applicant Profile Setup</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Tell us about yourself. Statement period required adapts automatically by profile type.</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    p = st.session_state.profile_data

    with c1:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        st.markdown("**Personal Information**")
        name     = st.text_input("Full Name",              value=p.get("name",""),       placeholder="e.g. Arjun Mehta")
        age      = st.number_input("Age",                  min_value=18, max_value=80,   value=p.get("age",28), step=1)
        profile  = st.selectbox("Profile Type",            PROFILE_TYPES,                index=PROFILE_TYPES.index(p.get("profile_type",PROFILE_TYPES[2])))
        occ      = st.text_input("Occupation / Industry",  value=p.get("occupation",""), placeholder="e.g. Software Engineer")
        city     = st.text_input("City of Residence",      value=p.get("city",""),       placeholder="e.g. Mumbai")
        pan      = st.text_input("PAN (optional)",         value=p.get("pan",""),        placeholder="ABCDE1234F", max_chars=10)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        st.markdown("**Financial Profile**")
        credit_cards    = st.number_input("Active Credit Cards",     min_value=0, max_value=20, value=p.get("credit_cards",1))
        loans_active    = st.number_input("Active Loans",           min_value=0, max_value=10, value=p.get("loans_active",0))
        collateral      = st.selectbox("Collateral Available?",     list(COLLATERAL_LGD.keys()), index=list(COLLATERAL_LGD.keys()).index(p.get("has_collateral","No")))
        emp_years       = st.slider("Years in Current Occupation",  0, 40, value=p.get("employment_years",3))
        monthly_rent    = st.number_input("Monthly Rent / Housing Cost (₹)", min_value=0.0, value=float(p.get("monthly_rent",0)), step=500.0, format="%.0f")
        monthly_food    = st.number_input("Monthly Food & Groceries (₹)",    min_value=0.0, value=float(p.get("monthly_food",0)), step=500.0, format="%.0f")
        st.markdown("</div>", unsafe_allow_html=True)

    is_short = profile in ["Student", "Freelancer / Gig Worker"]
    stmt_years = 3 if is_short else 5

    st.markdown(f"""
    <div class='info-banner'>
        📌 <b>{profile}</b> — requires <b>{stmt_years}-year</b> bank statement history.
        {'3 years for Students & Freelancers.' if is_short else '5 years for Salaried & Business profiles.'}
        Expenses like rent and food feed directly into your FOIR transparency report.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Save Profile & Continue →", use_container_width=True):
        if not name.strip():
            st.error("Please enter your full name.")
        else:
            st.session_state.profile_data = dict(
                name=name.strip(), age=age, profile_type=profile, occupation=occ,
                city=city, pan=pan.upper(), credit_cards=credit_cards,
                loans_active=loans_active, has_collateral=collateral,
                employment_years=emp_years, stmt_years=stmt_years,
                monthly_rent=monthly_rent, monthly_food=monthly_food,
            )
            st.session_state.step = "statement"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: BANK STATEMENT INPUT ────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "statement":
    prof       = st.session_state.profile_data
    stmt_years = prof.get("stmt_years", 5)
    current_yr = 2025
    years      = [current_yr - i for i in range(stmt_years - 1, -1, -1)]
    saved      = st.session_state.stmt_data

    def pad(lst, n, dv=0.0):
        return (list(lst) + [dv] * n)[:n]

    def_inc  = pad(saved.get("annual_income",    []), stmt_years)
    def_exp  = pad(saved.get("annual_expense",   []), stmt_years)
    def_sav  = pad(saved.get("annual_savings",   []), stmt_years)
    def_emi  = pad(saved.get("existing_emis",    []), stmt_years)
    def_bnc  = pad(saved.get("bounce_count",     []), stmt_years, 0)
    def_od   = pad(saved.get("overdraft_count",  []), stmt_years, 0)
    def_cash = pad(saved.get("cash_deposits",    []), stmt_years)
    def_upi  = pad(saved.get("upi_txn_count",    []), stmt_years, 0)
    def_util = pad(saved.get("utility_payments", []), stmt_years)

    st.markdown("<div class='section-title'>📊 Bank Statement Data Input</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-sub'>Enter annual figures for all {stmt_years} years. The richer the data, the more powerful the analysis.</div>", unsafe_allow_html=True)

    tabs = st.tabs([f"FY {y}-{str(y+1)[2:]}" for y in years])

    inc_v=[];exp_v=[];sav_v=[];emi_v=[];bnc_v=[];od_v=[];cash_v=[];upi_v=[];util_v=[]

    for i, (tab, year) in enumerate(zip(tabs, years)):
        with tab:
            r1, r2, r3 = st.columns(3, gap="medium")
            with r1:
                inc  = st.number_input("Annual Income (₹)",       min_value=0.0, value=float(def_inc[i]),  step=10000.0, key=f"inc_{year}",  format="%.0f")
                exp  = st.number_input("Annual Expenses (₹)",     min_value=0.0, value=float(def_exp[i]),  step=10000.0, key=f"exp_{year}",  format="%.0f")
                sav  = st.number_input("Net Savings / FD (₹)",   min_value=0.0, value=float(def_sav[i]),  step=5000.0,  key=f"sav_{year}",  format="%.0f")
            with r2:
                emi  = st.number_input("Existing EMIs / Year (₹)",min_value=0.0, value=float(def_emi[i]),  step=5000.0,  key=f"emi_{year}",  format="%.0f")
                cash = st.number_input("Cash Deposits (₹)",       min_value=0.0, value=float(def_cash[i]), step=5000.0,  key=f"cash_{year}", format="%.0f")
                util = st.number_input("Utility Bill Payments (₹)",min_value=0.0,value=float(def_util[i]), step=1000.0,  key=f"util_{year}", format="%.0f",
                                        help="Total electricity, water, gas, telecom bills paid")
            with r3:
                bnc  = st.number_input("Cheque / ECS Bounces",    min_value=0, value=int(def_bnc[i]),  step=1, key=f"bnc_{year}")
                od   = st.number_input("Overdraft Days",          min_value=0, value=int(def_od[i]),   step=1, key=f"od_{year}",
                                        help="Days account balance went negative / overdraft triggered")
                upi  = st.number_input("UPI Transactions (count)",min_value=0, value=int(def_upi[i]),  step=10, key=f"upi_{year}",
                                        help="Total UPI credit+debit transactions this year")

            net = inc - exp - emi
            sr  = (sav/inc*100) if inc > 0 else 0
            er  = (exp/inc*100) if inc > 0 else 0
            c1, c2, c3, c4 = st.columns(4)
            for col, lbl, val, col_c in zip([c1,c2,c3,c4],
                ["Net Cash Flow","Savings Rate","Expense Ratio","Bounce Count"],
                [format_inr(net), f"{sr:.1f}%", f"{er:.1f}%", str(int(bnc))],
                ["#3EC87A" if net>=0 else "#E05C5C", "#F0B429", "#E08929" if er>75 else "#8FA3C0", "#E05C5C" if bnc>0 else "#3EC87A"]):
                with col:
                    st.markdown(f"<div class='metric-card' style='padding:0.6rem;'><div class='metric-val' style='font-size:1rem;color:{col_c};'>{val}</div><div class='metric-lab'>{lbl}</div></div>", unsafe_allow_html=True)

            inc_v.append(inc); exp_v.append(exp); sav_v.append(sav); emi_v.append(emi)
            bnc_v.append(bnc); od_v.append(od);   cash_v.append(cash); upi_v.append(upi); util_v.append(util)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        itr        = st.selectbox("ITR Filed Regularly?",         ["Yes, all years","Most years","Occasionally","No"])
        gst        = st.selectbox("GST Registered?",              ["No","Yes"])
        bank_count = st.number_input("Number of Bank Accounts",   min_value=1, max_value=10, value=1)
    with c2:
        prev_def   = st.selectbox("Previous Loan Default?",       ["No","Yes – resolved","Yes – pending"])
        cc_util    = st.slider("Avg Credit Card Utilisation (%)", 0, 100, 30)
        acc_age    = st.number_input("Age of Oldest Bank Account (Years)", min_value=0, max_value=50, value=5)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    if st.button("🔍 Compute FinBridge Credit Score", use_container_width=True):
        if sum(inc_v) == 0:
            st.error("Please enter income data for at least one year.")
        else:
            st.session_state.stmt_data = dict(
                years=years, annual_income=inc_v, annual_expense=exp_v,
                annual_savings=sav_v, existing_emis=emi_v, bounce_count=bnc_v,
                overdraft_count=od_v, cash_deposits=cash_v, upi_txn_count=upi_v,
                utility_payments=util_v, itr_filed=itr, has_gst=gst,
                bank_count=bank_count, prev_defaults=prev_def,
                credit_card_util=cc_util, oldest_account_yr=acc_age,
            )
            score, comps, raw = compute_finbridge_score(st.session_state.stmt_data)
            cibil = estimate_cibil_score(st.session_state.stmt_data)
            score, cibil = apply_adjustments(score, cibil, st.session_state.stmt_data)
            st.session_state.finbridge_score = score
            st.session_state.cibil_score     = cibil
            st.session_state.components      = comps
            st.session_state.raw_score       = raw
            st.session_state.scores_computed = True
            st.session_state.step = "score"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: FINBRIDGE SCORE ─────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "score":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb    = st.session_state.finbridge_score
    ci    = st.session_state.cibil_score
    comps = st.session_state.components
    stmt  = st.session_state.stmt_data
    prof  = st.session_state.profile_data
    lbl, bdg, col = get_score_band(fb)

    st.markdown("<div class='section-title'>🏅 FinBridge Credit Score</div>", unsafe_allow_html=True)

    col_score, col_gauge = st.columns([1, 1.6], gap="large")
    with col_score:
        st.markdown(f"""
        <div class='score-hero'>
            <div style='font-size:0.7rem;color:#4A6080;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;'>FinBridge Score</div>
            <div class='score-num'>{fb}</div>
            <div style='margin:0.7rem 0;'><span class='badge {bdg}' style='font-size:0.88rem;padding:0.4rem 1.2rem;'>{lbl}</span></div>
            <div style='font-size:0.75rem;color:#4A6080;'>Range: 300 – 900 &nbsp;|&nbsp; {prof.get("name","Applicant")}</div>
            <div style='font-size:0.75rem;color:#4A6080;margin-top:0.2rem;'>{prof.get("profile_type","")}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"<div class='metric-card'><div class='metric-val'>{fb}</div><div class='metric-lab'>FinBridge Score</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#0DD4BD;'>{ci}</div><div class='metric-lab'>Est. Traditional Score</div></div>", unsafe_allow_html=True)

        diff = fb - ci
        diff_col = "#3EC87A" if diff >= 0 else "#E05C5C"
        diff_sign = "+" if diff >= 0 else ""
        st.markdown(f"""
        <div style='text-align:center;padding:0.7rem;background:rgba(0,0,0,0.2);border-radius:10px;border:1px solid var(--border);margin-top:0.5rem;'>
            <span style='font-size:0.75rem;color:#4A6080;'>FinBridge vs Traditional: </span>
            <span style='font-family:"Playfair Display",serif;font-size:1.3rem;color:{diff_col};font-weight:700;'>{diff_sign}{diff} pts</span>
        </div>
        """, unsafe_allow_html=True)

    with col_gauge:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fb,
            number={"font": {"size": 52, "color": col}, "suffix": ""},
            title={"text": "FinBridge Score", "font": {"size": 13, "color": "#8FA3C0"}},
            gauge={
                "axis": {"range": [300, 900], "tickwidth": 1, "tickcolor": "#1C3050",
                         "tickvals": [300,450,550,650,700,750,900],
                         "tickfont": {"color": "#4A6080", "size": 9}},
                "bar": {"color": col, "thickness": 0.22},
                "bgcolor": "#111F38",
                "borderwidth": 0,
                "steps": [
                    {"range": [300, 599], "color": "rgba(224,92,92,0.12)"},
                    {"range": [600, 649], "color": "rgba(224,137,41,0.12)"},
                    {"range": [650, 699], "color": "rgba(240,180,41,0.12)"},
                    {"range": [700, 749], "color": "rgba(124,200,126,0.12)"},
                    {"range": [750, 900], "color": "rgba(62,200,122,0.12)"},
                ],
                "threshold": {"line": {"color": "#F0B429", "width": 3}, "thickness": 0.75, "value": fb},
            }
        ))
        fig_g.update_layout(height=290, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font={"color":"#E8EDF5"}, margin=dict(t=40,b=10,l=30,r=30))
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Component charts
    cr, cb = st.columns(2, gap="large")
    cats = list(comps.keys())
    vals = list(comps.values())
    maxes = [25, 20, 18, 17, 12, 8]

    with cr:
        st.markdown("**Score Radar — Component Breakdown**")
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=cats+[cats[0]], fill='toself',
            fillcolor="rgba(240,180,41,0.12)", line=dict(color="#F0B429",width=2), name="Your Score"))
        fig_r.add_trace(go.Scatterpolar(r=maxes+[maxes[0]], theta=cats+[cats[0]], fill='toself',
            fillcolor="rgba(13,212,189,0.04)", line=dict(color="#0DD4BD",width=1,dash="dot"), name="Max"))
        fig_r.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,range=[0,26],gridcolor="#1C3050",tickfont=dict(color="#4A6080",size=8)),
            angularaxis=dict(tickfont=dict(color="#EDF2FA",size=10),gridcolor="#1C3050")),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=True,
            legend=dict(font=dict(color="#8FA3C0",size=9)), height=320, margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_r, use_container_width=True)

    with cb:
        st.markdown("**Score Efficiency per Component**")
        bar_colors = ["#3EC87A" if v/m>=0.75 else "#F0B429" if v/m>=0.50 else "#E05C5C" for v,m in zip(vals,maxes)]
        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(x=cats, y=maxes, name="Max", marker_color="rgba(255,255,255,0.05)",
            marker_line=dict(color="#1C3050",width=1)))
        fig_b.add_trace(go.Bar(x=cats, y=vals, name="Score", marker_color=bar_colors,
            text=[f"{v:.1f}" for v in vals], textposition="outside", textfont=dict(color="#EDF2FA",size=9)))
        fig_b.update_layout(barmode="overlay", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8FA3C0",size=9),
            xaxis=dict(gridcolor="#1C3050",tickfont=dict(color="#EDF2FA",size=8)),
            yaxis=dict(gridcolor="#1C3050"),
            legend=dict(font=dict(color="#8FA3C0",size=9)),
            height=320, margin=dict(t=20,b=60,l=10,r=10))
        st.plotly_chart(fig_b, use_container_width=True)

    # Trend
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**5-Year Cash-Flow Trend**")
    yrs    = stmt.get("years",[])
    incs   = stmt.get("annual_income",[])
    exps   = stmt.get("annual_expense",[])
    savs   = stmt.get("annual_savings",[])
    emis_y = stmt.get("existing_emis",[])
    net_cf = [i-e-em for i,e,em in zip(incs,exps,emis_y)]

    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(x=yrs,y=incs, name="Income",  line=dict(color="#3EC87A",width=2.5), mode="lines+markers", marker=dict(size=7)))
    fig_t.add_trace(go.Scatter(x=yrs,y=exps, name="Expenses",line=dict(color="#E05C5C",width=2,dash="dash"), mode="lines+markers",marker=dict(size=6)))
    fig_t.add_trace(go.Scatter(x=yrs,y=emis_y,name="EMIs",   line=dict(color="#F0B429",width=2,dash="dot"),  mode="lines+markers",marker=dict(size=6)))
    fig_t.add_trace(go.Bar(x=yrs,y=savs, name="Savings",marker_color="rgba(13,212,189,0.25)",marker_line=dict(color="#0DD4BD",width=1)))
    fig_t.add_trace(go.Bar(x=yrs,y=net_cf,name="Net CF",
        marker_color=["rgba(62,200,122,0.3)" if v>=0 else "rgba(224,92,92,0.3)" for v in net_cf]))
    fig_t.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8FA3C0"), xaxis=dict(gridcolor="#1C3050"),
        yaxis=dict(gridcolor="#1C3050", title="Amount (₹)"),
        legend=dict(orientation="h",y=1.05,x=1,xanchor="right",font=dict(color="#EDF2FA",size=9)),
        height=300, margin=dict(t=20,b=30,l=10,r=10))
    st.plotly_chart(fig_t, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: NBFC RISK DESK ──────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "nbfc":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb   = st.session_state.finbridge_score
    stmt = st.session_state.stmt_data
    prof = st.session_state.profile_data
    lbl, bdg, col = get_score_band(fb)
    PD_base, LGD_base = get_risk_params(lbl)

    # Collateral adjustment to LGD
    collateral = prof.get("has_collateral","No")
    LGD_adj    = COLLATERAL_LGD.get(collateral, LGD_base)

    st.markdown("<div class='section-title'>🏛️ NBFC Risk Desk</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Institutional-grade risk analytics — Expected Loss, Risk-Based Pricing, Provisioning & Portfolio Intelligence.</div>", unsafe_allow_html=True)
    st.markdown("<div class='perspective-label pl-nbfc'>🏛️ CREDIT PROVIDER / NBFC PERSPECTIVE</div>", unsafe_allow_html=True)

    # ── Section 1: Expected Loss Calculator ───────────────────────────────────
    st.markdown("<div class='fb-card-red'>", unsafe_allow_html=True)
    st.markdown("### 📉 Expected Loss (EL) Calculator")
    st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>EL = Probability of Default (PD) × Loss Given Default (LGD) × Exposure at Default (EAD)</div>", unsafe_allow_html=True)

    rc1, rc2, rc3 = st.columns(3, gap="medium")
    with rc1:
        ead = st.number_input("Exposure at Default / Loan Amount (₹)", min_value=10000.0, value=1500000.0, step=50000.0, format="%.0f", key="ead_input")
    with rc2:
        pd_override = st.slider("Probability of Default (%)", 0.1, 50.0, float(PD_base*100), 0.1, key="pd_slider",
                                help=f"Auto-set from FinBridge score band ({lbl}). Override if needed.")
        pd_val = pd_override / 100
    with rc3:
        lgd_override = st.slider("Loss Given Default (%)", 5.0, 90.0, float(LGD_adj*100), 1.0, key="lgd_slider",
                                 help=f"Auto-adjusted for collateral: {collateral}")
        lgd_val = lgd_override / 100

    el        = pd_val * lgd_val * ead
    ecl_pct   = pd_val * lgd_val * 100
    provision  = el

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#E05C5C;'>{format_inr(el)}</div><div class='metric-lab'>Expected Loss (EL)</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#F0B429;'>{ecl_pct:.2f}%</div><div class='metric-lab'>ECL Rate (PD × LGD)</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#E08929;'>{format_inr(provision)}</div><div class='metric-lab'>Provisioning Required</div></div>", unsafe_allow_html=True)
    with m4:
        rwa = ead * pd_val * 12.5  # simplified risk-weighted asset
        st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#9B72CF;'>{format_inr(rwa)}</div><div class='metric-lab'>Risk-Weighted Asset</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 2: Risk Classification ───────────────────────────────────────
    st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
    st.markdown("### 🗂️ NPA & Risk Bucket Classification")

    risk_data = [
        ("Standard Asset",     fb >= 700,         "#3EC87A", "Regular income; no overdue > 90 days"),
        ("Special Mention",    650 <= fb < 700,   "#F0B429", "Early stress signals; watch-listed"),
        ("Sub-Standard",       600 <= fb < 650,   "#E08929", "NPAs up to 12 months"),
        ("Doubtful",           450 <= fb < 600,   "#E05C5C", "NPAs > 12 months; recovery uncertain"),
        ("Loss Asset",         fb < 450,           "#B54444", "Unrecoverable; write-off recommended"),
    ]
    active_bucket = next(((name,desc) for name,cond,_,desc in risk_data if cond), ("Loss Asset","Write-off recommended"))

    for name, cond, c, desc in risk_data:
        is_active = cond
        bg = f"border:2px solid {c};background:rgba(0,0,0,0.15);" if is_active else "border:1px solid var(--border);opacity:0.4;"
        indicator = f"<span style='color:{c};font-size:1.2rem;'>●</span>" if is_active else "<span style='color:#2A4060;font-size:1.2rem;'>○</span>"
        st.markdown(f"""
        <div style='display:grid;grid-template-columns:24px 140px 1fr;gap:0.8rem;align-items:center;{bg}border-radius:8px;padding:0.6rem 1rem;margin-bottom:0.4rem;'>
            <div>{indicator}</div>
            <div style='font-weight:600;color:#EDF2FA;font-size:0.85rem;'>{name}</div>
            <div style='font-size:0.8rem;color:#8FA3C0;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-top:0.8rem;padding:0.8rem 1rem;background:rgba(0,0,0,0.2);border-radius:8px;font-size:0.82rem;'>
        <b style='color:#F0B429;'>Classified as:</b> <span style='color:#EDF2FA;'>{active_bucket[0]}</span>
        &nbsp;|&nbsp; <span style='color:#8FA3C0;'>{active_bucket[1]}</span>
        &nbsp;|&nbsp; <b style='color:#F0B429;'>Provisioning norm:</b> <span style='color:#EDF2FA;'>{int(ecl_pct)}% of outstanding</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 3: Risk-Based Pricing Engine ──────────────────────────────────
    st.markdown("<div class='fb-card-gold'>", unsafe_allow_html=True)
    st.markdown("### 💹 Risk-Based Pricing Engine")
    st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>Competitive pricing strategy calibrated to FinBridge score. Reward prime borrowers; protect margins on sub-prime.</div>", unsafe_allow_html=True)

    purpose = st.selectbox("Loan Product", list(LOAN_PURPOSES.keys()), key="rbpe_purpose")
    pd_info  = LOAN_PURPOSES[purpose]
    rate_lo, rate_hi = pd_info["rate_range"]

    # Risk-based pricing tiers
    score_pct   = max(0, (fb - 300) / 600)
    base_rate   = rate_hi - score_pct * (rate_hi - rate_lo)

    # Score ≥ 750: apply 1.5% acquisition discount
    prime_discount = 1.5 if fb >= 750 else (0.75 if fb >= 700 else 0.0)
    final_rate     = max(rate_lo, round(base_rate - prime_discount, 2))

    # ROA estimator
    cost_of_funds   = st.slider("Lender's Cost of Funds (%)", 5.0, 12.0, 7.5, 0.25, key="cof_slider")
    opex_pct        = 1.2  # operational costs
    nim             = final_rate - cost_of_funds - opex_pct - (ecl_pct)
    roa             = nim

    pricing_tiers = [
        ("Excellent (750–900)", rate_lo,                            rate_lo + 0.5,  "-1.5% Prime Discount"),
        ("Good (700–749)",      rate_lo + 0.5,                     rate_lo + 1.5,  "-0.75% Preferred"),
        ("Fair (650–699)",      rate_lo + 1.5,                     rate_lo + 2.5,  "Standard Rate"),
        ("Marginal (600–649)", rate_lo + 2.5,                     rate_hi - 0.5,  "+Risk Premium"),
        ("Poor (<600)",         rate_hi - 0.5,                     rate_hi,        "+Maximum Risk Premium"),
    ]

    fig_p = go.Figure()
    for tier_name, lo_r, hi_r, note in pricing_tiers:
        is_current = (lbl in tier_name or (lbl == "Poor" and "Poor" in tier_name))
        fig_p.add_trace(go.Bar(
            y=[tier_name], x=[hi_r - lo_r],
            base=[lo_r], orientation='h',
            marker_color="#F0B429" if is_current else "#1C3050",
            marker_line=dict(color="#F0B429" if is_current else "#1C3050", width=2),
            text=f"{lo_r:.1f}–{hi_r:.1f}% | {note}",
            textposition="inside", textfont=dict(color="#EDF2FA", size=9),
            name=tier_name, showlegend=False,
        ))

    fig_p.add_vline(x=final_rate, line_color="#0DD4BD", line_width=2, line_dash="dot",
                    annotation_text=f"Your Rate: {final_rate:.2f}%", annotation_font_color="#0DD4BD",
                    annotation_position="top")
    fig_p.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Interest Rate (%)", gridcolor="#1C3050", range=[rate_lo-0.5, rate_hi+0.5]),
        yaxis=dict(gridcolor="#1C3050"), font=dict(color="#8FA3C0",size=9),
        height=240, margin=dict(t=20,b=40,l=10,r=10), barmode="stack")
    st.plotly_chart(fig_p, use_container_width=True)

    p1, p2, p3, p4 = st.columns(4)
    with p1: st.markdown(f"<div class='metric-card'><div class='metric-val'>{final_rate:.2f}%</div><div class='metric-lab'>Assigned Rate (p.a.)</div></div>", unsafe_allow_html=True)
    with p2: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#0DD4BD;'>-{prime_discount:.2f}%</div><div class='metric-lab'>Prime Discount Applied</div></div>", unsafe_allow_html=True)
    with p3: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:{'#3EC87A' if roa>0 else '#E05C5C'};'>{roa:.2f}%</div><div class='metric-lab'>Est. Net ROA</div></div>", unsafe_allow_html=True)
    with p4: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#9B72CF;'>{format_inr(provision)}</div><div class='metric-lab'>Provision Requirement</div></div>", unsafe_allow_html=True)

    if prime_discount > 0:
        st.markdown(f"""
        <div class='info-banner'>
            🌟 <b>Prime Borrower Identified.</b> A {prime_discount:.1f}% rate concession applied over standard pricing.
            This borrower is an ideal acquisition target — low provisioning ({ecl_pct:.1f}%), strong cash-flow coverage, and
            {'collateral-backed loan' if collateral != 'No' else 'clean repayment history'}.
            Recommend: Priority processing with streamlined KYC.
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 4: Portfolio Stress Test ──────────────────────────────────────
    st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Portfolio-Level Stress Test")

    pc1, pc2 = st.columns([1, 2])
    with pc1:
        portfolio_size = st.number_input("Number of Similar Borrowers in Portfolio", min_value=10, max_value=10000, value=500, step=10)
        avg_loan_size  = st.number_input("Average Loan Size (₹)", min_value=100000.0, value=float(ead), step=100000.0, format="%.0f")
        stress_pd      = st.slider("Stress PD Multiplier", 1.0, 5.0, 2.0, 0.1, help="Simulate economic downturn scenario")

    with pc2:
        total_portfolio = portfolio_size * avg_loan_size
        base_el_total   = pd_val * lgd_val * total_portfolio
        stress_el_total = min(pd_val * stress_pd, 1.0) * lgd_val * total_portfolio
        capital_buffer  = stress_el_total * 1.15  # 15% capital buffer

        stress_rows = [
            ("Total Portfolio Exposure",   format_inr(total_portfolio),  "#8FA3C0"),
            ("Base Case Expected Loss",    format_inr(base_el_total),    "#F0B429"),
            ("Stress Case Expected Loss",  format_inr(stress_el_total),  "#E05C5C"),
            ("Required Capital Buffer",    format_inr(capital_buffer),   "#9B72CF"),
            ("Portfolio NIM (est.)",       f"{(final_rate - cost_of_funds - opex_pct):.2f}%", "#3EC87A"),
        ]
        for label_r, val_r, col_r in stress_rows:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:0.5rem 0.8rem;border-bottom:1px solid var(--border);font-size:0.83rem;'>
                <span style='color:#8FA3C0;'>{label_r}</span>
                <span style='color:{col_r};font-weight:600;font-family:"JetBrains Mono",monospace;'>{val_r}</span>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: CONSUMER TRANSPARENCY ──────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "consumer":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb   = st.session_state.finbridge_score
    stmt = st.session_state.stmt_data
    prof = st.session_state.profile_data
    lbl, bdg, col = get_score_band(fb)

    st.markdown("<div class='section-title'>💚 Consumer Transparency Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Empowering you with full visibility into how your score was built and exactly what you can do to improve it.</div>", unsafe_allow_html=True)
    st.markdown("<div class='perspective-label pl-consumer'>💚 CONSUMER / BORROWER PERSPECTIVE</div>", unsafe_allow_html=True)

    # ── FOIR Income Pie Chart ─────────────────────────────────────────────────
    st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
    st.markdown("### 🥧 FOIR Transparency — Your Income Allocation")
    st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>This is exactly what a lender sees when they evaluate your application. Fixed Obligation-to-Income Ratio (FOIR) is the single most important factor in loan approval.</div>", unsafe_allow_html=True)

    avg_m_income  = float(np.mean(stmt.get("annual_income", [600000]))) / 12
    avg_m_expense = float(np.mean(stmt.get("annual_expense",[400000]))) / 12
    avg_m_emi     = float(np.mean(stmt.get("existing_emis", [0])))     / 12
    monthly_rent  = float(prof.get("monthly_rent", 0))
    monthly_food  = float(prof.get("monthly_food", 0))

    # Decompose expenses
    rent_amt   = monthly_rent if monthly_rent > 0 else avg_m_expense * 0.35
    food_amt   = monthly_food if monthly_food > 0 else avg_m_expense * 0.18
    utility_amt = float(np.mean(stmt.get("utility_payments", [0]))) / 12
    utility_amt = utility_amt if utility_amt > 0 else avg_m_expense * 0.08
    emi_amt    = avg_m_emi
    other_exp  = max(0, avg_m_expense - rent_amt - food_amt - utility_amt - emi_amt)
    disposable = max(0, avg_m_income - avg_m_expense - emi_amt)

    pie_labels = ["🏠 Rent/Housing","🍱 Food & Groceries","⚡ Utilities","💳 Existing EMIs","🛍️ Other Expenses","💰 Disposable for New EMI"]
    pie_values = [rent_amt, food_amt, utility_amt, emi_amt, other_exp, disposable]
    pie_colors = ["#9B72CF","#F0B429","#0DD4BD","#E05C5C","#8FA3C0","#3EC87A"]

    ic1, ic2 = st.columns([1.2, 1], gap="large")
    with ic1:
        fig_pie = go.Figure(go.Pie(
            labels=pie_labels, values=[max(0,v) for v in pie_values],
            hole=0.52, marker=dict(colors=pie_colors, line=dict(color="#080F1E",width=2)),
            textinfo="label+percent", textfont=dict(color="#EDF2FA",size=10),
            hovertemplate="%{label}<br>₹%{value:,.0f}/month<extra></extra>",
            sort=False,
        ))
        fig_pie.add_annotation(text=f"Monthly<br>Income<br>{format_inr(avg_m_income)}",
            x=0.5, y=0.5, showarrow=False, font=dict(size=11, color="#EDF2FA"))
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            height=340, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    with ic2:
        st.markdown("<br>", unsafe_allow_html=True)
        foir = ((emi_amt) / avg_m_income * 100) if avg_m_income > 0 else 0
        foir_with_new = min(100, (emi_amt + disposable * 0.5) / avg_m_income * 100) if avg_m_income > 0 else 0

        for lbl_p, val, c in [
            ("Monthly Income",        f"₹{avg_m_income:,.0f}",   "#3EC87A"),
            ("Rent & Housing",        f"₹{rent_amt:,.0f}",        "#9B72CF"),
            ("Food & Groceries",      f"₹{food_amt:,.0f}",        "#F0B429"),
            ("Utilities",             f"₹{utility_amt:,.0f}",     "#0DD4BD"),
            ("Existing EMIs",         f"₹{emi_amt:,.0f}",         "#E05C5C"),
            ("Other Expenses",        f"₹{other_exp:,.0f}",       "#8FA3C0"),
            ("✅ Available for EMI",   f"₹{disposable:,.0f}",      "#3EC87A"),
        ]:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid var(--border);font-size:0.82rem;'>
                <span style='color:#8FA3C0;'>{lbl_p}</span>
                <span style='color:{c};font-weight:600;'>{val}</span>
            </div>""", unsafe_allow_html=True)

        foir_col = "#3EC87A" if foir < 40 else "#F0B429" if foir < 55 else "#E05C5C"
        st.markdown(f"""
        <div style='margin-top:0.8rem;padding:0.8rem;background:rgba(0,0,0,0.2);border-radius:8px;'>
            <div style='font-size:0.75rem;color:#8FA3C0;'>Current FOIR</div>
            <div style='font-family:"Playfair Display",serif;font-size:1.8rem;color:{foir_col};font-weight:700;'>{foir:.1f}%</div>
            <div style='font-size:0.72rem;color:#4A6080;'>{"✅ Within 55% lender threshold" if foir < 55 else "⚠️ Exceeds 55% FOIR — loan approval at risk"}</div>
        </div>
        """, unsafe_allow_html=True)

    # Why was I rejected? / Why was I approved?
    approved = foir < 55 and fb >= 600
    if approved:
        st.markdown("""<div class='info-banner'>✅ <b>Why you'd be approved:</b> Your FOIR is within the 55% threshold AND your FinBridge score meets the minimum cut-off. A lender can comfortably offer you a loan with the disposable income available above.</div>""", unsafe_allow_html=True)
    else:
        reasons = []
        if foir >= 55: reasons.append(f"FOIR of {foir:.1f}% exceeds the 55% maximum allowed by most lenders")
        if fb < 600:   reasons.append(f"FinBridge score {fb} is below the 600 minimum threshold for standard loans")
        st.markdown(f"""<div class='danger-banner'>❌ <b>Why you might be rejected:</b> {' | '.join(reasons)}. The pie chart above shows exactly where your income is going — this is precisely what underwriters see.</div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Path to Prime Simulator ───────────────────────────────────────────────
    st.markdown("<div class='fb-card-teal'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Path to Prime — Score Improvement Simulator")
    st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>Select the actions you can realistically take. Watch your score climb in real-time.</div>", unsafe_allow_html=True)

    selected_actions = []
    total_delta = 0

    for i, (action_name, delta, rationale) in enumerate(WHATIF_ACTIONS):
        checked = st.checkbox(f"{action_name} (+{delta} pts)", key=f"wi_{i}",
                              help=rationale)
        if checked:
            selected_actions.append((action_name, delta, rationale))
            total_delta += delta

    projected_score = min(900, fb + total_delta)
    proj_lbl, proj_bdg, proj_col = get_score_band(projected_score)

    st.markdown("<br>", unsafe_allow_html=True)
    wc1, wc2 = st.columns([1, 1.5])
    with wc1:
        st.markdown(f"""
        <div style='text-align:center;padding:1.5rem;background:rgba(0,0,0,0.25);border-radius:14px;border:1px solid var(--teal);'>
            <div style='font-size:0.72rem;color:#4A6080;letter-spacing:0.1em;text-transform:uppercase;'>Current Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:3rem;color:{col};font-weight:700;'>{fb}</div>
            <div style='color:#4A6080;font-size:1.5rem;'>↓</div>
            <div style='font-size:0.72rem;color:#4A6080;letter-spacing:0.1em;text-transform:uppercase;'>Projected Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:3rem;color:{proj_col};font-weight:700;'>{projected_score}</div>
            <div style='margin-top:0.5rem;'>
                <span class='badge {proj_bdg}'>{proj_lbl}</span>
            </div>
            <div style='margin-top:0.5rem;font-size:0.82rem;color:#0DD4BD;font-weight:600;'>+{total_delta} points from {len(selected_actions)} action{'s' if len(selected_actions)!=1 else ''}</div>
        </div>
        """, unsafe_allow_html=True)

    with wc2:
        if selected_actions:
            # Build projected timeline
            timeline_x = [0]
            timeline_y = [fb]
            cumulative  = fb
            for _, delta, _ in selected_actions:
                cumulative = min(900, cumulative + delta)
                timeline_x.append(timeline_x[-1] + 3)
                timeline_y.append(cumulative)

            fig_pp = go.Figure()
            fig_pp.add_trace(go.Scatter(x=timeline_x, y=timeline_y,
                mode="lines+markers", line=dict(color="#0DD4BD",width=2.5),
                marker=dict(size=8, color="#0DD4BD"),
                fill="tozeroy", fillcolor="rgba(13,212,189,0.06)"))
            for band_y, band_lbl, band_c in [(750,"Excellent","#3EC87A"),(700,"Good","#7CC87E"),(650,"Fair","#F0B429")]:
                fig_pp.add_hline(y=band_y, line_dash="dot", line_color=band_c,
                    annotation_text=band_lbl, annotation_font_color=band_c,
                    annotation_position="right")
            fig_pp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="Months →", gridcolor="#1C3050"),
                yaxis=dict(range=[max(280,fb-20), min(920, projected_score+30)], gridcolor="#1C3050"),
                font=dict(color="#8FA3C0",size=9), showlegend=False,
                height=260, margin=dict(t=10,b=30,l=10,r=60))
            st.plotly_chart(fig_pp, use_container_width=True)
        else:
            st.markdown("<div style='text-align:center;color:#4A6080;padding:4rem 1rem;font-size:0.88rem;'>Select actions above to see your score trajectory →</div>", unsafe_allow_html=True)

    # Action breakdown
    if selected_actions:
        st.markdown("<br>**Action Breakdown**")
        for act, delta, rationale in selected_actions:
            st.markdown(f"""
            <div class='whatif-card'>
                <div class='whatif-delta' style='color:#0DD4BD;'>+{delta}</div>
                <div>
                    <div style='font-size:0.85rem;color:#EDF2FA;font-weight:500;'>{act}</div>
                    <div style='font-size:0.75rem;color:#8FA3C0;margin-top:0.2rem;'>{rationale}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Financial Wellness Score ──────────────────────────────────────────────
    st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
    st.markdown("### 🌱 Financial Wellness Snapshot")

    incomes = np.array(stmt.get("annual_income",[1]), dtype=float)
    savings = np.array(stmt.get("annual_savings",[0]), dtype=float)
    emis_a  = np.array(stmt.get("existing_emis",[0]),  dtype=float)

    avg_sr       = float(np.mean(savings / np.where(incomes==0,1,incomes))) * 100
    avg_dscr     = float(np.mean(incomes / (emis_a + 1)))
    bounce_total = int(sum(stmt.get("bounce_count",[0])))

    wellness_items = [
        ("Savings Rate",           f"{avg_sr:.1f}%",     avg_sr >= 20,    avg_sr >= 10,    "Aim for 20%+"),
        ("Debt-Service Coverage",  f"{avg_dscr:.1f}x",   avg_dscr >= 3.0, avg_dscr >= 1.5, "Aim for 3x+"),
        ("Payment Discipline",     f"{bounce_total} bounces", bounce_total==0, bounce_total<3, "Zero bounces = ideal"),
        ("Income Growth",          f"+{float(np.mean(np.diff(incomes)/np.where(incomes[:-1]==0,1,incomes[:-1])))*100:.1f}% YoY" if len(incomes)>1 else "N/A",
                                   True if len(incomes)<=1 else float(np.mean(np.diff(incomes)/np.where(incomes[:-1]==0,1,incomes[:-1])))>0.10,
                                   True if len(incomes)<=1 else float(np.mean(np.diff(incomes)/np.where(incomes[:-1]==0,1,incomes[:-1])))>0.05,
                                   "Aim for 10%+ annual growth"),
        ("FOIR Status",            f"{foir:.1f}%",        foir < 40,       foir < 55,       "Below 40% is ideal"),
    ]

    ww_cols = st.columns(5, gap="small")
    for wc, (wlbl, wval, good, ok, tip) in zip(ww_cols, wellness_items):
        wc_color = "#3EC87A" if good else "#F0B429" if ok else "#E05C5C"
        wc_icon  = "✅" if good else "⚠️" if ok else "❌"
        with wc:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.4rem;'>{wc_icon}</div>
                <div class='metric-val' style='font-size:1.1rem;color:{wc_color};'>{wval}</div>
                <div class='metric-lab'>{wlbl}</div>
                <div style='font-size:0.65rem;color:#2A4060;margin-top:0.3rem;'>{tip}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: CIBIL vs FINBRIDGE COMPARISON ─────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "comparison":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb  = st.session_state.finbridge_score
    ci  = st.session_state.cibil_score
    stmt = st.session_state.stmt_data
    lbl_fb, bdg_fb, col_fb = get_score_band(fb)
    lbl_ci, bdg_ci, col_ci = get_score_band(ci)
    diff = fb - ci

    st.markdown("<div class='section-title'>⚖️ Traditional CIBIL vs FinBridge</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>A side-by-side methodology breakdown — and where FinBridge sees financial signals that bureau scores simply cannot.</div>", unsafe_allow_html=True)
    st.markdown("<div class='perspective-label pl-bureau'>🔬 CREDIT BUREAU / HYBRID MODEL PERSPECTIVE</div>", unsafe_allow_html=True)

    # Score cards
    cc1, cc2 = st.columns(2, gap="large")
    with cc1:
        st.markdown(f"""
        <div style='text-align:center;padding:2rem 1.5rem;background:var(--navy-card);border:1px solid var(--border);border-radius:16px;'>
            <div style='font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#4A6080;margin-bottom:0.5rem;'>Traditional CIBIL Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:4.5rem;font-weight:700;color:{col_ci};line-height:1;'>{ci}</div>
            <span class='badge {bdg_ci}' style='font-size:0.85rem;margin-top:0.5rem;display:inline-block;'>{lbl_ci}</span>
            <div style='font-size:0.72rem;color:#4A6080;margin-top:1rem;'>Bureau-based | Payment History Driven<br>Thin-file penalty for new borrowers</div>
        </div>
        """, unsafe_allow_html=True)

    with cc2:
        st.markdown(f"""
        <div style='text-align:center;padding:2rem 1.5rem;background:linear-gradient(140deg,#162C4A,#080F1E);border:2px solid #F0B429;border-radius:16px;position:relative;'>
            <div style='position:absolute;top:10px;right:14px;font-size:0.62rem;background:#F0B429;color:#080F1E;padding:2px 8px;border-radius:50px;font-weight:700;'>PROPRIETARY</div>
            <div style='font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#F0B429;margin-bottom:0.5rem;'>FinBridge Credit Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:4.5rem;font-weight:700;color:{col_fb};line-height:1;'>{fb}</div>
            <span class='badge {bdg_fb}' style='font-size:0.85rem;margin-top:0.5rem;display:inline-block;'>{lbl_fb}</span>
            <div style='font-size:0.72rem;color:#8FA3C0;margin-top:1rem;'>Bank Statement Intelligence | 6-Dimension<br>Inclusive of informal & gig economy earners</div>
        </div>
        """, unsafe_allow_html=True)

    diff_color = "#3EC87A" if diff > 0 else "#E05C5C" if diff < 0 else "#8FA3C0"
    diff_msg   = (f"FinBridge scores you <b>{abs(diff)} points HIGHER</b> than CIBIL — capturing real cash-flow strength that bureaus miss."
                  if diff > 0 else
                  f"Traditional score exceeds FinBridge by <b>{abs(diff)} pts</b> — possible credit-card gaming or declared-income inflation."
                  if diff < 0 else "Both models agree on your creditworthiness profile.")
    st.markdown(f"""
    <div style='text-align:center;padding:0.9rem;background:rgba(0,0,0,0.2);border-radius:10px;border:1px solid {diff_color};margin:1rem 0;font-size:0.87rem;color:{diff_color};'>
        {diff_msg}
    </div>
    """, unsafe_allow_html=True)

    # Methodology table
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**Methodology Comparison**")

    comp_data = [
        ("Primary Data Source",      "Credit Report / Bureau",          "Actual Bank Statements (3–5 yrs)"),
        ("Income Verification",      "Declared income only",             "Actual credited amounts verified"),
        ("Payment History Weight",   "~35% — dominant factor",           "One of 6 balanced dimensions (8–25%)"),
        ("Cash-Flow Analysis",       "❌ Not considered",                 "✅ 20% weight — core dimension"),
        ("Savings Behaviour",        "❌ Not assessed",                   "✅ 18% weight — directly scored"),
        ("Debt Service Coverage",    "Estimated only",                   "Calculated from real outflows (17%)"),
        ("Informal Income",          "❌ Cannot capture",                 "✅ Reflected in cash-flow patterns"),
        ("Freelancer / Gig Workers", "⚠️ Often penalised (irregular)",   "✅ Assessed via income stability + DSCR"),
        ("Students / Thin-file",     "❌ No score possible",              "✅ Scored on 3-year history"),
        ("Utility Payment Signal",   "❌ Not tracked",                    "✅ Consistency weighted (orthogonal)"),
        ("UPI / Digital Patterns",   "❌ Not tracked",                    "✅ Transaction seasonality assessed"),
        ("Manipulation Risk",        "⚠️ Credit-card cycling possible",  "✅ Difficult to fake actual bank records"),
        ("Update Frequency",         "Quarterly refresh",                "Real-time re-assessment possible"),
        ("Rural / Semi-urban",       "⚠️ Urban salaried bias",           "✅ Cash deposit patterns captured"),
        ("DPDP Act 2023 Compliance", "Bureau-framework exempted",        "Full AA consent-based architecture"),
    ]

    header = """
    <div style='display:grid;grid-template-columns:220px 1fr 1fr;gap:6px;margin-bottom:6px;'>
        <div style='background:var(--navy-mid);border:1px solid var(--border);border-radius:8px;padding:0.6rem 0.9rem;font-size:0.72rem;font-weight:700;color:#4A6080;text-transform:uppercase;letter-spacing:0.08em;'>Parameter</div>
        <div style='background:var(--navy-mid);border:1px solid var(--border);border-radius:8px;padding:0.6rem 0.9rem;font-size:0.72rem;font-weight:700;color:#4A6080;text-transform:uppercase;letter-spacing:0.08em;'>Traditional CIBIL</div>
        <div style='background:linear-gradient(135deg,#162C4A,#080F1E);border:1px solid #F0B429;border-radius:8px;padding:0.6rem 0.9rem;font-size:0.72rem;font-weight:700;color:#F0B429;text-transform:uppercase;letter-spacing:0.08em;'>FinBridge</div>
    </div>"""
    rows = ""
    for param, trad, fb_v in comp_data:
        rows += f"""
        <div style='display:grid;grid-template-columns:220px 1fr 1fr;gap:6px;margin-bottom:4px;'>
            <div style='background:var(--navy-card);border:1px solid var(--border);border-radius:6px;padding:0.5rem 0.9rem;font-size:0.8rem;color:#EDF2FA;font-weight:500;'>{param}</div>
            <div style='background:var(--navy-card);border:1px solid var(--border);border-radius:6px;padding:0.5rem 0.9rem;font-size:0.8rem;color:#8FA3C0;'>{trad}</div>
            <div style='background:linear-gradient(135deg,#162C4A,#080F1E);border:1px solid rgba(240,180,41,0.25);border-radius:6px;padding:0.5rem 0.9rem;font-size:0.8rem;color:#EDF2FA;'>{fb_v}</div>
        </div>"""
    st.markdown(header + rows, unsafe_allow_html=True)

    # Orthogonal Signals
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("### 🔭 Orthogonal Data Signals — Where FinBridge Sees What Bureaus Cannot")
    st.markdown("<div class='perspective-label pl-bureau'>🔬 BUREAU DIVERGENCE ANALYSIS</div>", unsafe_allow_html=True)

    utils    = np.array(stmt.get("utility_payments",[0]), dtype=float)
    upis     = np.array(stmt.get("upi_txn_count",[0]),    dtype=float)
    cash_dep = np.array(stmt.get("cash_deposits",[0]),    dtype=float)
    incs     = np.array(stmt.get("annual_income",[1]),    dtype=float)

    # Compute orthogonal scores
    util_consistency = max(0, min(100, 100 * (1 - np.std(utils)/(np.mean(utils)+1e-9))))
    upi_adoption     = min(100, float(np.mean(upis)) / 200 * 100)
    cash_dep_ratio   = min(100, float(np.mean(cash_dep)) / (float(np.mean(incs))+1e-9) * 100)
    income_seasonality = max(0, min(100, 100 * (1 - np.std(incs)/(np.mean(incs)+1e-9))))

    orth_signals = [
        ("Utility Bill Consistency",    util_consistency,     "CIBIL cannot track",  "Tracked by FinBridge (utility expense pattern)"),
        ("UPI Transaction Adoption",    upi_adoption,         "CIBIL cannot track",  "High UPI usage = digital financial inclusion"),
        ("Salary/Income Regularity",    income_seasonality,   "Not available",        "Day-of-month consistency in income credits"),
        ("Cash Economy Indicator",      min(100,cash_dep_ratio*3), "Partial only",   "Cash deposit frequency vs. income ratio"),
    ]

    for sig_name, sig_val, bureau_view, fb_view in orth_signals:
        sig_col = "#3EC87A" if sig_val >= 70 else "#F0B429" if sig_val >= 40 else "#E05C5C"
        st.markdown(f"""
        <div style='background:var(--navy-card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.6rem;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;'>
                <span style='font-size:0.87rem;color:#EDF2FA;font-weight:500;'>{sig_name}</span>
                <span style='font-family:"JetBrains Mono",monospace;font-size:0.85rem;color:{sig_col};font-weight:600;'>{sig_val:.0f}/100</span>
            </div>
            <div style='background:#1C3050;border-radius:50px;height:6px;margin-bottom:0.6rem;'>
                <div style='width:{sig_val:.1f}%;background:{sig_col};border-radius:50px;height:6px;'></div>
            </div>
            <div style='display:flex;gap:1.5rem;font-size:0.75rem;'>
                <span style='color:#E05C5C;'>🚫 Bureau: {bureau_view}</span>
                <span style='color:#3EC87A;'>✅ FinBridge: {fb_view}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Full orthogonal table
    with st.expander("📋 Full Orthogonal Signal Catalogue (10 Signals)"):
        header2 = """<div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:5px;margin-bottom:5px;'>"""
        for h in ["Signal","CIBIL Visibility","What FinBridge Sees","Credit Impact"]:
            header2 += f"<div style='background:var(--navy-mid);border:1px solid var(--border);border-radius:6px;padding:0.4rem 0.7rem;font-size:0.7rem;font-weight:700;color:#4A6080;text-transform:uppercase;'>{h}</div>"
        header2 += "</div>"
        rows2 = ""
        for sig, bureau, fb_s, impact in ORTHOGONAL_SIGNALS:
            rows2 += "<div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:5px;margin-bottom:4px;'>"
            for cell, c in [(sig,"#EDF2FA"),(bureau,"#E05C5C"),(fb_s,"#3EC87A"),(impact,"#F0B429")]:
                rows2 += f"<div style='background:var(--navy-card);border:1px solid var(--border);border-radius:6px;padding:0.4rem 0.7rem;font-size:0.77rem;color:{c};'>{cell}</div>"
            rows2 += "</div>"
        st.markdown(header2+rows2, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: BANK & COMPLIANCE ───────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "bank":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb   = st.session_state.finbridge_score
    stmt = st.session_state.stmt_data
    prof = st.session_state.profile_data
    lbl, bdg, col = get_score_band(fb)

    st.markdown("<div class='section-title'>🏦 Bank & Regulatory Compliance Desk</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>RBI Digital Lending Guidelines (2022) compliance tooling — KFS generation, Account Aggregator (AA) consent simulation, and DPDP Act 2023 readiness.</div>", unsafe_allow_html=True)
    st.markdown("<div class='perspective-label pl-bank'>🏦 BANK / REGULATORY PERSPECTIVE</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Key Fact Statement (KFS)", "🔗 AA Consent Flow", "🛡️ DPDP Compliance"])

    # ── Tab 1: KFS ────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("**Generate KFS per RBI Digital Lending Guidelines (2022)**")
        st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>Under RBI DLG 2022, every lender must provide a standardised Key Fact Statement before loan disbursement. Generate yours below.</div>", unsafe_allow_html=True)

        kc1, kc2 = st.columns(2)
        with kc1:
            kfs_purpose = st.selectbox("Loan Product", list(LOAN_PURPOSES.keys()), key="kfs_purpose")
            kfs_amount  = st.number_input("Loan Amount (₹)", min_value=10000.0, value=1500000.0, step=50000.0, format="%.0f", key="kfs_amt")
            kfs_tenure  = st.slider("Tenure (Years)", 1, 30, 10, key="kfs_tenure")
        with kc2:
            pd_k     = LOAN_PURPOSES[kfs_purpose]
            lo_r, hi_r = pd_k["rate_range"]
            sc_pct   = max(0, (fb-300)/600)
            kfs_rate = max(lo_r, round(hi_r - sc_pct*(hi_r-lo_r) - (1.5 if fb>=750 else 0), 2))
            kfs_emi  = calc_emi(kfs_amount, kfs_rate, kfs_tenure*12)
            kfs_proc_fee = st.slider("Processing Fee (%)", 0.0, 3.0, 1.0, 0.1, key="kfs_proc")
            kfs_apr  = calc_apr(kfs_rate, kfs_proc_fee, kfs_tenure*12)
            kfs_total_interest = kfs_emi * kfs_tenure * 12 - kfs_amount
            kfs_insur = st.slider("Insurance Premium (₹)", 0, 50000, 5000, 500, key="kfs_ins")
            cooling   = st.selectbox("Cooling-Off Period (Days)", [3, 5, 7], index=0, key="kfs_cool")

        st.markdown("<br>", unsafe_allow_html=True)

        today_str = datetime.today().strftime("%d %B %Y")
        kfs_html = f"""
        <div class='kfs-doc'>
            <div class='kfs-header'>
                KEY FACT STATEMENT (KFS)<br>
                <span style='font-size:0.75rem;color:#8FA3C0;font-family:"DM Sans",sans-serif;font-weight:400;'>
                    As per RBI Digital Lending Guidelines (DLG) – September 2022 | Ref: FinBridge/KFS/{datetime.today().strftime("%Y%m%d")}-{fb}
                </span>
            </div>

            <div style='display:grid;grid-template-columns:1fr 1fr;gap:0 2rem;'>
                <div>
                    <div class='kfs-row'><span class='kfs-key'>Borrower Name</span><span class='kfs-val'>{prof.get("name","—")}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Loan Product</span><span class='kfs-val'>{kfs_purpose}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Sanctioned Amount</span><span class='kfs-val' style='color:#F0B429;'>{format_inr(kfs_amount)}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Net Disbursement</span><span class='kfs-val'>{format_inr(kfs_amount - kfs_amount*kfs_proc_fee/100)}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Interest Rate (p.a.)</span><span class='kfs-val'>{kfs_rate:.2f}% — Fixed</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Annual Percentage Rate (APR)</span><span class='kfs-val' style='color:#0DD4BD;'>{kfs_apr:.2f}% p.a.</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Processing Fee</span><span class='kfs-val'>{kfs_proc_fee:.1f}% = {format_inr(kfs_amount*kfs_proc_fee/100)}</span></div>
                </div>
                <div>
                    <div class='kfs-row'><span class='kfs-key'>Loan Tenure</span><span class='kfs-val'>{kfs_tenure} Years ({kfs_tenure*12} months)</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Monthly EMI</span><span class='kfs-val' style='color:#F0B429;'>₹{kfs_emi:,.0f}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Total Interest Payable</span><span class='kfs-val' style='color:#E05C5C;'>{format_inr(kfs_total_interest)}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Total Amount Payable</span><span class='kfs-val'>{format_inr(kfs_emi*kfs_tenure*12)}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Insurance Premium</span><span class='kfs-val'>₹{kfs_insur:,}</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Prepayment Charges</span><span class='kfs-val'>Nil (floating rate borrowers)</span></div>
                    <div class='kfs-row'><span class='kfs-key'>Penal Interest</span><span class='kfs-val'>2% p.m. on overdue EMI</span></div>
                </div>
            </div>

            <div style='margin-top:1.5rem;border-top:1px solid var(--border);padding-top:1rem;'>
                <div style='font-weight:600;color:#F0B429;margin-bottom:0.5rem;font-size:0.85rem;'>RECOVERY MECHANISM</div>
                <div style='color:#8FA3C0;font-size:0.8rem;line-height:1.7;'>
                    1. Automated ECS/NACH debit on due date from primary bank account<br>
                    2. SMS + Email reminder 5 days prior to EMI date<br>
                    3. 7-day grace period before penal interest levy<br>
                    4. Recovery proceedings under SARFAESI Act 2002 (secured loans) or DRT (above ₹20L)<br>
                    5. Credit bureau reporting within 30 days of NPA classification
                </div>
            </div>

            <div style='margin-top:1rem;border-top:1px solid var(--border);padding-top:1rem;'>
                <div style='font-weight:600;color:#F0B429;margin-bottom:0.5rem;font-size:0.85rem;'>BORROWER RIGHTS & GRIEVANCE REDRESSAL</div>
                <div style='color:#8FA3C0;font-size:0.8rem;line-height:1.7;'>
                    • <b style='color:#EDF2FA;'>Cooling-Off Period:</b> {cooling} days from disbursement to cancel without penalty<br>
                    • <b style='color:#EDF2FA;'>Grievance Officer:</b> grievances@finbridge.in | 1800-XXX-XXXX (Toll-Free)<br>
                    • <b style='color:#EDF2FA;'>RBI Ombudsman:</b> cms.rbi.org.in | sachet.rbi.org.in<br>
                    • <b style='color:#EDF2FA;'>DPDP Rights:</b> Data access, correction, and deletion under DPDP Act 2023
                </div>
            </div>

            <div style='margin-top:1.2rem;border-top:1px solid var(--border);padding-top:0.8rem;display:flex;justify-content:space-between;align-items:center;font-size:0.72rem;color:#4A6080;'>
                <span>Generated: {today_str} | FinBridge Credit Intelligence</span>
                <span>Valid for 30 days | FinBridge Score: <b style='color:#F0B429;'>{fb}</b></span>
            </div>
        </div>
        """
        st.markdown(kfs_html, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='info-banner' style='margin-top:1rem;'>
            📋 <b>APR Disclosure:</b> The Annual Percentage Rate of <b>{kfs_apr:.2f}%</b> includes processing fee amortised over the loan tenure.
            This is your true cost of borrowing, as mandated by RBI DLG 2022.
            The net amount disbursed after deducting processing fee is <b>{format_inr(kfs_amount - kfs_amount*kfs_proc_fee/100)}</b>.
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 2: AA Consent Flow ─────────────────────────────────────────────────
    with tab2:
        st.markdown("**Account Aggregator (AA) Framework — Consent Flow Simulation**")
        st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>India's AA framework (RBI 2021) enables consent-based financial data sharing. This visual demonstrates how FinBridge ingests your bank statement data compliantly.</div>", unsafe_allow_html=True)

        # Consent parameters
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            aa_purpose = st.selectbox("Consent Purpose", ["Credit Underwriting","Loan Monitoring","Portfolio Review"], key="aa_purpose")
            aa_fi_type = st.selectbox("FI Data Type",    ["DEPOSIT","RECURRING_DEPOSIT","TERM_DEPOSIT","CREDIT_CARD","SIP"], key="aa_fi")
        with ac2:
            aa_fetch_type = st.selectbox("Fetch Type",  ["ONE_TIME","PERIODIC"], key="aa_fetch")
            aa_consent_dur= st.slider("Consent Duration (Months)", 1, 24, 6, key="aa_dur")
        with ac3:
            aa_data_range  = st.slider("Data Range Requested (Years)", 1, 5, prof.get("stmt_years",5), key="aa_range")
            aa_frequency   = st.selectbox("Data Fetch Frequency", ["MONTHLY","QUARTERLY","ANNUAL","ONE_TIME"], key="aa_freq")

        # Flow diagram
        aa_steps = [
            ("👤 Borrower / Customer", "Initiates loan application on FinBridge", True, "FIU (Financial Info User)"),
            ("🔗 Account Aggregator", f"AA receives consent request\nPurpose: {aa_purpose}", True, "Licensed AA Entity"),
            ("📲 Customer Consent", f"Borrower authenticates via AA app\nGrants {aa_consent_dur}-month consent", True, "DPDP Consent Artifact"),
            ("🏦 Bank / FIP", f"Financial Info Provider releases\n{aa_fi_type} data ({aa_data_range} years)", True, "FIP (Financial Info Provider)"),
            ("🧠 FinBridge Engine", f"Data fetched {aa_frequency}\nScored & analysed securely", True, "FIU — Data Consumer"),
            ("✅ Credit Decision", f"FinBridge Score: {fb} | {lbl}\nConsent audit trail preserved", True, "Output"),
        ]

        for i, (node_name, node_desc, active, role) in enumerate(aa_steps):
            st.markdown(f"""
            <div style='display:flex;align-items:stretch;gap:1rem;margin-bottom:4px;'>
                <div style='width:4px;background:{"#0DD4BD" if active else "#1C3050"};border-radius:2px;flex-shrink:0;'></div>
                <div style='flex:1;background:{"rgba(13,212,189,0.06)" if active else "var(--navy-card)"};border:1px solid {"#0DD4BD" if active else "var(--border)"};border-radius:10px;padding:0.8rem 1.1rem;'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <span style='font-size:0.9rem;color:#EDF2FA;font-weight:600;'>{node_name}</span>
                        <span class='badge badge-teal' style='font-size:0.65rem;'>{role}</span>
                    </div>
                    <div style='font-size:0.78rem;color:#8FA3C0;margin-top:0.3rem;white-space:pre-line;'>{node_desc}</div>
                </div>
            </div>
            {"<div style='margin-left:1.1rem;color:#0DD4BD;font-size:1.1rem;line-height:1;padding:1px 0;'>↓</div>" if i < len(aa_steps)-1 else ""}
            """, unsafe_allow_html=True)

        # Consent artifact
        consent_id = f"AA-CONSENT-{fb}-{datetime.today().strftime('%Y%m%d')}"
        st.markdown(f"""
        <div style='margin-top:1rem;background:var(--navy-mid);border:1px solid var(--teal);border-radius:10px;padding:1rem 1.3rem;font-family:"JetBrains Mono",monospace;font-size:0.75rem;color:#8FA3C0;'>
            <div style='color:#0DD4BD;font-weight:600;margin-bottom:0.5rem;'>📝 CONSENT ARTIFACT (Simulated)</div>
            consentId   : "{consent_id}"<br>
            status      : "ACTIVE"<br>
            purpose     : "{aa_purpose}"<br>
            fiTypes     : ["{aa_fi_type}"]<br>
            fetchType   : "{aa_fetch_type}"<br>
            frequency   : {{"unit": "{aa_frequency}", "value": 1}}<br>
            dataRange   : {{"from": "{current_year - aa_data_range}", "to": "{current_year}"}}<br>
            consentExpiry: "{datetime.today().year + aa_consent_dur//12}-{(datetime.today().month + aa_consent_dur%12-1)%12+1:02d}-01"<br>
            createdAt   : "{datetime.today().isoformat()[:19]}Z"<br>
            dataLife    : {{"unit": "YEAR", "value": 2}}<br>
            digitalSignature : "SHA256:finbridge-consent-signed-artifact"
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 3: DPDP Compliance ────────────────────────────────────────────────
    with tab3:
        st.markdown("**Digital Personal Data Protection (DPDP) Act 2023 — Compliance Checklist**")
        st.markdown("<div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:1rem;'>India's DPDP Act 2023 mandates consent, purpose limitation, data minimisation, and individual rights. FinBridge's architecture is designed to comply.</div>", unsafe_allow_html=True)

        dpdp_checks = [
            ("✅", "Informed Consent",         "Borrower explicitly consents before any data is fetched via AA framework",               True),
            ("✅", "Purpose Limitation",       "Data used only for credit scoring — not sold or shared with third parties",              True),
            ("✅", "Data Minimisation",        "Only bank statement data required for the scoring period is requested",                  True),
            ("✅", "Accuracy",                 "Borrower can correct self-declared data before score computation",                       True),
            ("✅", "Storage Limitation",       "Statement data purged after 24 months per data life policy",                             True),
            ("✅", "Right to Access",          "Borrower can view all data used in their score computation",                             True),
            ("✅", "Right to Correction",      "Incorrect data can be disputed and re-scored within 7 working days",                     True),
            ("✅", "Right to Erasure",         "Account deletion triggers complete data purge from FinBridge systems",                   True),
            ("✅", "Grievance Mechanism",      "Dedicated Data Protection Officer (DPO) and 30-day grievance resolution SLA",            True),
            ("⚠️", "Cross-border Transfer",   "International data transfer only with Board-approved Standard Contractual Clauses",      False),
            ("⚠️", "Children's Data",         "Parental consent required; no credit scoring for minors under 18",                       False),
        ]

        for status, title, desc, is_green in dpdp_checks:
            c = "#3EC87A" if is_green else "#F0B429"
            st.markdown(f"""
            <div style='display:flex;gap:1rem;align-items:flex-start;padding:0.7rem 1rem;background:var(--navy-card);border:1px solid {"rgba(62,200,122,0.2)" if is_green else "rgba(240,180,41,0.2)"};border-radius:8px;margin-bottom:4px;'>
                <div style='font-size:1.2rem;min-width:24px;'>{status}</div>
                <div>
                    <div style='font-size:0.85rem;color:{c};font-weight:600;'>{title}</div>
                    <div style='font-size:0.78rem;color:#8FA3C0;margin-top:0.15rem;'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        compliant_count = sum(1 for _,_,_,g in dpdp_checks if g)
        st.markdown(f"""
        <div style='margin-top:1rem;padding:0.9rem 1.2rem;background:rgba(62,200,122,0.06);border:1px solid #3EC87A;border-radius:10px;font-size:0.85rem;color:#3EC87A;'>
            ✅ <b>DPDP Compliance Score: {compliant_count}/{len(dpdp_checks)} provisions met.</b>
            The 2 flagged items require legal counsel review before cross-border operations or minor borrower onboarding.
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: LOAN ELIGIBILITY ────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "loan":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb   = st.session_state.finbridge_score
    stmt = st.session_state.stmt_data
    prof = st.session_state.profile_data
    lbl, bdg, col = get_score_band(fb)

    st.markdown("<div class='section-title'>💰 Loan Eligibility Analyser</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Score-matched interest rates from 10 industry segments, FOIR-based maximum loan computation, and collateral-adjusted LTV.</div>", unsafe_allow_html=True)

    lc1, lc2 = st.columns([1, 1.2], gap="large")

    with lc1:
        st.markdown("<div class='fb-card-gold'>", unsafe_allow_html=True)
        st.markdown("**Loan Configuration**")
        purpose  = st.selectbox("Financing Purpose", list(LOAN_PURPOSES.keys()), key="loan_purpose_sel")
        pd_info  = LOAN_PURPOSES[purpose]
        lo_r, hi_r = pd_info["rate_range"]
        max_yr   = pd_info["max_tenure"]

        sc_pct   = max(0, (fb-300)/600)
        prime_d  = 1.5 if fb >= 750 else 0.75 if fb >= 700 else 0.0
        assigned = max(lo_r, round(hi_r - sc_pct*(hi_r-lo_r) - prime_d, 2))

        desired_amt = st.number_input("Desired Loan Amount (₹)", min_value=10000.0, value=1500000.0, step=50000.0, format="%.0f", key="desired_amt")
        tenure_yr   = st.slider("Preferred Tenure (Years)", 1, max_yr, min(5, max_yr), key="tenure_yr_sel")
        tenure_mo   = tenure_yr * 12

        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.2);border:1px solid rgba(240,180,41,0.3);border-radius:8px;padding:0.9rem;margin:0.8rem 0;font-size:0.82rem;'>
            <div><span style='color:#8FA3C0;'>Industry:</span> <span style='color:#EDF2FA;'>{pd_info["industry"]}</span></div>
            <div style='margin-top:0.3rem;'><span style='color:#8FA3C0;'>Market Range:</span> <span style='color:#EDF2FA;'>{lo_r:.1f}% – {hi_r:.1f}% p.a.</span></div>
            <div style='margin-top:0.3rem;'><span style='color:#8FA3C0;'>Your Assigned Rate:</span> <span style='color:#F0B429;font-weight:600;font-size:1rem;'>{assigned:.2f}% p.a.</span></div>
            <div style='margin-top:0.3rem;'><span style='color:#8FA3C0;'>Prime Discount:</span> <span style='color:#0DD4BD;'>-{prime_d:.2f}%</span></div>
        </div>
        """, unsafe_allow_html=True)

        # LTV for collateral
        collateral = prof.get("has_collateral","No")
        ltv_map    = {"No":0,"Yes – Property":80,"Yes – FD/Savings":90,"Yes – Gold":75,"Yes – Vehicle":70}
        ltv        = ltv_map.get(collateral, 0)
        if collateral != "No":
            coll_value = st.number_input(f"Estimated Collateral Value (₹) — {collateral}", min_value=0.0, value=2000000.0, step=100000.0, format="%.0f", key="coll_val")
            max_coll_loan = coll_value * ltv / 100
            st.markdown(f"<div class='info-banner'>🏛️ LTV {ltv}% on {collateral} → Max collateral-backed loan: <b>{format_inr(max_coll_loan)}</b></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with lc2:
        max_eligible, disp_emi = max_loan_eligible(stmt, assigned, tenure_mo)
        desired_emi = calc_emi(desired_amt, assigned, tenure_mo)
        max_emi     = calc_emi(max_eligible, assigned, tenure_mo)
        can_afford  = desired_emi <= disp_emi
        elig_pct    = min(100, max_eligible / desired_amt * 100) if desired_amt > 0 else 0

        st.markdown("<div class='fb-card-gold'>", unsafe_allow_html=True)
        st.markdown("**Eligibility Results**")

        m1, m2 = st.columns(2)
        with m1: st.markdown(f"<div class='metric-card'><div class='metric-val'>{format_inr(max_eligible)}</div><div class='metric-lab'>Max Eligible Loan</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#0DD4BD;'>{format_inr(disp_emi)}/mo</div><div class='metric-lab'>Disposable for EMI (FOIR 55%)</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        m3, m4 = st.columns(2)
        with m3: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#0DD4BD;'>{format_inr(desired_emi)}/mo</div><div class='metric-lab'>EMI on Desired Amount</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#F0B429;'>{assigned:.2f}%</div><div class='metric-lab'>Interest Rate</div></div>", unsafe_allow_html=True)

        bar_c = "#3EC87A" if elig_pct >= 90 else "#F0B429" if elig_pct >= 60 else "#E05C5C"
        st.markdown(f"""
        <div style='margin:0.8rem 0;'>
            <div style='display:flex;justify-content:space-between;font-size:0.78rem;color:#8FA3C0;margin-bottom:0.3rem;'>
                <span>Eligibility Coverage</span><span style='color:{bar_c};font-weight:600;'>{elig_pct:.1f}% of desired amount</span>
            </div>
            <div style='background:#1C3050;border-radius:50px;height:10px;'>
                <div style='width:{min(elig_pct,100):.1f}%;background:{bar_c};border-radius:50px;height:10px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        vc = "#3EC87A" if can_afford else "#E05C5C"
        vi = "✅" if can_afford else "❌"
        vm = ("Desired loan is within repayment capacity." if can_afford
              else f"Desired EMI ₹{desired_emi:,.0f}/mo exceeds capacity ₹{disp_emi:,.0f}/mo. Max eligible: {format_inr(max_eligible)}.")
        st.markdown(f"<div style='padding:0.9rem 1rem;border:1px solid {vc};border-radius:8px;color:{vc};font-size:0.85rem;margin-top:0.5rem;'>{vi} {vm}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # All purposes table
    st.markdown("**Eligibility Matrix — All Loan Categories**")
    rows = []
    for p_name, p_data in LOAN_PURPOSES.items():
        lo, hi = p_data["rate_range"]
        psc    = max(0, (fb-300)/600)
        pd_val = max(0.75 if fb>=750 else 0.0)
        arate  = max(lo, round(hi - psc*(hi-lo) - pd_val, 2))
        t_mo   = min(60, p_data["max_tenure"]*12)
        mel, _ = max_loan_eligible(stmt, arate, t_mo)
        rows.append({"Purpose": p_name, "Industry": p_data["industry"],
                     "Rate": f"{arate:.2f}%", "Max Tenure": f"{p_data['max_tenure']}Y",
                     "Max Eligible": format_inr(mel)})

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={
                     "Purpose":    st.column_config.TextColumn("Loan Purpose"),
                     "Industry":   st.column_config.TextColumn("Segment"),
                     "Rate":       st.column_config.TextColumn("Interest Rate"),
                     "Max Tenure": st.column_config.TextColumn("Max Tenure"),
                     "Max Eligible": st.column_config.TextColumn("Max Eligible Amount"),
                 })


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: EMI PLANNER ─────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "emi":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb   = st.session_state.finbridge_score
    stmt = st.session_state.stmt_data

    st.markdown("<div class='section-title'>📅 EMI Planner & Repayment Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Full amortisation, cash-flow stress test, prepayment simulation, and multi-scenario comparison.</div>", unsafe_allow_html=True)

    ec1, ec2 = st.columns([1, 1.5], gap="large")

    with ec1:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        principal   = st.number_input("Loan Amount (₹)",        min_value=10000.0, value=1500000.0, step=50000.0, format="%.0f")
        int_rate    = st.slider("Annual Interest Rate (%)",      6.0, 28.0, 10.5, 0.25)
        tenure_yr_e = st.slider("Loan Tenure (Years)",          1, 30, 10)
        tenure_mo_e = tenure_yr_e * 12

        emi        = calc_emi(principal, int_rate, tenure_mo_e)
        total_pay  = emi * tenure_mo_e
        total_int  = total_pay - principal
        int_ratio  = (total_int / principal * 100) if principal > 0 else 0
        st.markdown("</div>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1: st.markdown(f"<div class='metric-card'><div class='metric-val'>{format_inr(emi)}/mo</div><div class='metric-lab'>Monthly EMI</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#E05C5C;'>{format_inr(total_int)}</div><div class='metric-lab'>Total Interest</div></div>", unsafe_allow_html=True)
        m3, m4 = st.columns(2)
        with m3: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#0DD4BD;'>{format_inr(total_pay)}</div><div class='metric-lab'>Total Payable</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#F0B429;'>{int_ratio:.1f}%</div><div class='metric-lab'>Interest/Principal</div></div>", unsafe_allow_html=True)

    with ec2:
        fig_donut = go.Figure(go.Pie(
            labels=["Principal", "Total Interest"],
            values=[principal, total_int], hole=0.56,
            marker=dict(colors=["#0DD4BD","#E05C5C"], line=dict(color="#080F1E",width=2)),
            textinfo="label+percent", textfont=dict(color="#EDF2FA",size=11),
            hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>"
        ))
        fig_donut.add_annotation(text=f"Total<br>{format_inr(total_pay)}", x=0.5, y=0.5,
                                 showarrow=False, font=dict(size=12,color="#EDF2FA"))
        fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=True,
            legend=dict(font=dict(color="#8FA3C0"),orientation="h",y=-0.1),
            height=290, margin=dict(t=10,b=30,l=10,r=10))
        st.plotly_chart(fig_donut, use_container_width=True)

    # Amortisation chart
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**Year-by-Year Amortisation Schedule**")

    yrs_list, prins, ints_paid, balances = [], [], [], []
    bal = principal
    r   = int_rate / (12 * 100) if int_rate > 0 else 0

    for yr in range(1, tenure_yr_e + 1):
        yr_p = yr_i = 0
        for _ in range(12):
            if bal <= 0: break
            i_p = bal * r
            p_p = min(emi - i_p, bal)
            bal -= p_p; yr_p += p_p; yr_i += i_p
        yrs_list.append(f"Y{yr}"); prins.append(round(yr_p)); ints_paid.append(round(yr_i)); balances.append(max(0,round(bal)))

    fig_am = go.Figure()
    fig_am.add_trace(go.Bar(name="Principal",x=yrs_list,y=prins,  marker_color="#0DD4BD"))
    fig_am.add_trace(go.Bar(name="Interest", x=yrs_list,y=ints_paid,marker_color="#E05C5C"))
    fig_am.add_trace(go.Scatter(name="Balance",x=yrs_list,y=balances,mode="lines+markers",
        line=dict(color="#F0B429",width=2),yaxis="y2"))
    fig_am.update_layout(barmode="stack", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#1C3050"), yaxis=dict(title="Payment (₹)",gridcolor="#1C3050"),
        yaxis2=dict(overlaying="y",side="right",title="Balance (₹)"),
        font=dict(color="#8FA3C0",size=9),
        legend=dict(orientation="h",y=1.05,font=dict(color="#EDF2FA",size=9)),
        height=300, margin=dict(t=20,b=30,l=10,r=60))
    st.plotly_chart(fig_am, use_container_width=True)

    # Cash-flow stress test
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**Monthly Cash-Flow Stress Test**")

    avg_m_inc  = float(np.mean(stmt.get("annual_income",[600000]))) / 12
    avg_m_exp  = float(np.mean(stmt.get("annual_expense",[400000]))) / 12
    ex_m_emi   = float(np.mean(stmt.get("existing_emis",[0])))       / 12
    net_surplus= avg_m_inc - avg_m_exp - ex_m_emi - emi

    sc1,sc2,sc3,sc4,sc5 = st.columns(5)
    for col_s, lbl_s, val_s, c_s in zip(
        [sc1,sc2,sc3,sc4,sc5],
        ["Monthly Income","Monthly Expenses","Existing EMIs","New EMI","Net Surplus"],
        [avg_m_inc, avg_m_exp, ex_m_emi, emi, net_surplus],
        ["#3EC87A","#E05C5C","#E08929","#F0B429","#3EC87A" if net_surplus>0 else "#E05C5C"]
    ):
        with col_s:
            st.markdown(f"<div class='metric-card'><div class='metric-val' style='font-size:1rem;color:{c_s};'>₹{val_s:,.0f}</div><div class='metric-lab'>{lbl_s}</div></div>", unsafe_allow_html=True)

    surplus_c = "#3EC87A" if net_surplus > avg_m_inc*0.1 else "#F0B429" if net_surplus>0 else "#E05C5C"
    surplus_m = ("✅ Comfortable repayment buffer. Loan is financially sustainable." if net_surplus>avg_m_inc*0.1
                 else "⚠️ Tight cash-flow. Consider extending tenure or reducing principal." if net_surplus>0
                 else "❌ Negative monthly balance after obligations. Reduce loan amount.")
    st.markdown(f"<div style='padding:1rem 1.2rem;border:1px solid {surplus_c};border-radius:10px;color:{surplus_c};font-size:0.87rem;margin-top:0.5rem;'>{surplus_m}</div>", unsafe_allow_html=True)

    # Prepayment simulator
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**Prepayment Benefit Simulator**")
    pp1, pp2 = st.columns([1,2])
    with pp1:
        prepay_annual = st.number_input("Annual Prepayment (₹)", min_value=0.0, value=50000.0, step=10000.0, format="%.0f")

    if prepay_annual > 0 and r > 0:
        bal_pp = principal; mo_pp = 0; int_pp = 0
        for m in range(tenure_mo_e):
            if bal_pp <= 0: break
            i_p2 = bal_pp * r; p_p2 = min(emi - i_p2, bal_pp)
            bal_pp -= p_p2; int_pp += i_p2; mo_pp += 1
            if (m+1) % 12 == 0: bal_pp = max(0, bal_pp - prepay_annual)
        int_saved  = total_int - int_pp
        months_saved = tenure_mo_e - mo_pp

        with pp2:
            ppc1, ppc2, ppc3 = st.columns(3)
            with ppc1: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#3EC87A;'>{format_inr(max(0,int_saved))}</div><div class='metric-lab'>Interest Saved</div></div>", unsafe_allow_html=True)
            with ppc2: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#0DD4BD;'>{months_to_label(max(0,months_saved))}</div><div class='metric-lab'>Tenure Reduced</div></div>", unsafe_allow_html=True)
            with ppc3: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#F0B429;'>{format_inr(int_pp+principal)}</div><div class='metric-lab'>New Total Payable</div></div>", unsafe_allow_html=True)

    # Multi-rate comparison
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**Multi-Rate Scenario Comparison**")
    rates_comp = [int_rate - 2, int_rate - 1, int_rate, int_rate + 1, int_rate + 2]
    rates_comp = [max(4,r) for r in rates_comp]
    comp_rows  = []
    for rc in rates_comp:
        emi_c = calc_emi(principal, rc, tenure_mo_e)
        int_c = emi_c*tenure_mo_e - principal
        comp_rows.append({"Rate": f"{rc:.2f}%", "Monthly EMI": f"₹{emi_c:,.0f}",
                          "Total Interest": format_inr(int_c), "Total Payable": format_inr(emi_c*tenure_mo_e),
                          "Marker": "← YOUR RATE" if rc == int_rate else ""})
    st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE: CREDIT REPORT ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == "report":
    if not st.session_state.scores_computed:
        st.warning("Complete bank statement input first."); st.stop()

    fb    = st.session_state.finbridge_score
    ci    = st.session_state.cibil_score
    comps = st.session_state.components
    stmt  = st.session_state.stmt_data
    prof  = st.session_state.profile_data
    lbl, bdg, col = get_score_band(fb)

    incomes  = np.array(stmt.get("annual_income",  [1]), dtype=float)
    expenses = np.array(stmt.get("annual_expense", [0]), dtype=float)
    savings  = np.array(stmt.get("annual_savings", [0]), dtype=float)
    emis_a   = np.array(stmt.get("existing_emis",  [0]), dtype=float)
    bounces  = stmt.get("bounce_count", [0])

    avg_income   = float(np.mean(incomes))
    avg_savings  = float(np.mean(savings))
    total_bounces= int(sum(bounces))
    savings_rate = (avg_savings / avg_income * 100) if avg_income > 0 else 0
    avg_dscr     = float(np.mean(incomes / (emis_a + 1)))
    avg_m_income = avg_income / 12

    st.markdown("<div class='section-title'>📋 FinBridge Credit Intelligence Report</div>", unsafe_allow_html=True)

    # Report header
    today_str2 = datetime.today().strftime("%d %B %Y")
    ref_id = f"FB/CR/{fb}/{datetime.today().strftime('%Y%m%d')}"

    st.markdown(f"""
    <div style='background:linear-gradient(140deg,#162C4A 0%,#080F1E 100%);border:1px solid #F0B429;border-radius:16px;padding:2rem;margin-bottom:1.5rem;'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;'>
            <div>
                <div style='font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:700;color:#F0B429;'>FinBridge Credit Intelligence Report</div>
                <div style='color:#4A6080;font-size:0.78rem;margin-top:0.2rem;'>Ref: {ref_id} &nbsp;|&nbsp; Generated: {today_str2} &nbsp;|&nbsp; Confidential</div>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:0.68rem;color:#4A6080;text-transform:uppercase;letter-spacing:0.1em;'>FinBridge Score</div>
                <div style='font-family:"Playfair Display",serif;font-size:3rem;color:{col};font-weight:700;line-height:1;'>{fb}</div>
                <span class='badge {bdg}'>{lbl}</span>
            </div>
        </div>
        <hr style='border-color:#1C3050;margin:1rem 0;'>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;font-size:0.8rem;'>
            <div><span style='color:#4A6080;'>Name:</span> <span style='color:#EDF2FA;'>{prof.get("name","N/A")}</span></div>
            <div><span style='color:#4A6080;'>Age:</span> <span style='color:#EDF2FA;'>{prof.get("age","N/A")}</span></div>
            <div><span style='color:#4A6080;'>Profile:</span> <span style='color:#EDF2FA;'>{prof.get("profile_type","N/A")}</span></div>
            <div><span style='color:#4A6080;'>City:</span> <span style='color:#EDF2FA;'>{prof.get("city","N/A")}</span></div>
            <div><span style='color:#4A6080;'>Occupation:</span> <span style='color:#EDF2FA;'>{prof.get("occupation","N/A")}</span></div>
            <div><span style='color:#4A6080;'>Credit Cards:</span> <span style='color:#EDF2FA;'>{prof.get("credit_cards","N/A")}</span></div>
            <div><span style='color:#4A6080;'>Active Loans:</span> <span style='color:#EDF2FA;'>{prof.get("loans_active","N/A")}</span></div>
            <div><span style='color:#4A6080;'>Collateral:</span> <span style='color:#EDF2FA;'>{prof.get("has_collateral","N/A")}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    r1,r2,r3,r4,r5,r6 = st.columns(6, gap="small")
    kpis = [
        ("FinBridge Score",    str(fb),                       col),
        ("Traditional Score",  str(ci),                       "#0DD4BD"),
        ("Avg Annual Income",  format_inr(avg_income),         "#3EC87A"),
        ("Savings Rate",       f"{savings_rate:.1f}%",         "#F0B429"),
        ("DSCR",               f"{avg_dscr:.2f}x",            "#9B72CF"),
        ("Bounce Count",       str(total_bounces),             "#E05C5C" if total_bounces>2 else "#8FA3C0"),
    ]
    for rc, (kl, kv, kc) in zip([r1,r2,r3,r4,r5,r6], kpis):
        with rc:
            st.markdown(f"<div class='metric-card'><div class='metric-val' style='font-size:1.2rem;color:{kc};'>{kv}</div><div class='metric-lab'>{kl}</div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Score component breakdown
    st.markdown("**Score Component Breakdown**")
    maxes_map = {"Income Stability":25,"Cash-Flow Consistency":20,"Savings Behaviour":18,
                 "Debt Coverage (DSCR)":17,"Expenditure Discipline":12,"Account Behaviour":8}
    for comp_name, sc_val in comps.items():
        max_v = maxes_map.get(comp_name, 25)
        pct   = sc_val / max_v * 100 if max_v > 0 else 0
        bc    = "#3EC87A" if pct>=75 else "#F0B429" if pct>=50 else "#E05C5C"
        st_l  = "Strong" if pct>=75 else "Moderate" if pct>=50 else "Weak"
        bdg_c = "badge-green" if pct>=75 else "badge-gold" if pct>=50 else "badge-red"
        st.markdown(f"""
        <div style='display:grid;grid-template-columns:200px 1fr 80px 80px;gap:1rem;align-items:center;margin-bottom:0.5rem;'>
            <div style='font-size:0.83rem;color:#EDF2FA;'>{comp_name}</div>
            <div style='background:#1C3050;border-radius:50px;height:7px;'>
                <div style='width:{pct:.1f}%;background:{bc};border-radius:50px;height:7px;'></div>
            </div>
            <div style='font-size:0.82rem;color:{bc};text-align:right;font-family:"JetBrains Mono",monospace;'>{sc_val:.1f}/{max_v}</div>
            <div><span class='badge {bdg_c}' style='font-size:0.65rem;'>{st_l}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Strengths & Improvements
    col_s, col_i = st.columns(2, gap="large")
    with col_s:
        st.markdown("**💪 Key Strengths**")
        strengths = []
        if comps.get("Income Stability",0) >= 18:    strengths.append("Consistent income growth — above-average stability")
        if comps.get("Savings Behaviour",0) >= 13:   strengths.append("Strong savings discipline — above 20% savings rate")
        if comps.get("Cash-Flow Consistency",0)>=15: strengths.append("Positive cash-flow sustained across all years")
        if comps.get("Debt Coverage (DSCR)",0)>=12:  strengths.append("Healthy DSCR — income comfortably covers obligations")
        if comps.get("Expenditure Discipline",0)>=9: strengths.append("Controlled expenditure relative to income earned")
        if total_bounces == 0: strengths.append("Zero bounce record — exemplary payment discipline")
        if avg_dscr >= 3: strengths.append(f"DSCR of {avg_dscr:.1f}x — significantly above 2x minimum benchmark")
        if not strengths: strengths.append("Build financial discipline consistently for a stronger score")
        for s in strengths:
            st.markdown(f"<div style='background:rgba(62,200,122,0.05);border:1px solid rgba(62,200,122,0.15);border-radius:8px;padding:0.55rem 0.9rem;margin-bottom:4px;font-size:0.82rem;color:#EDF2FA;'>✅ {s}</div>", unsafe_allow_html=True)

    with col_i:
        st.markdown("**🔧 Improvement Areas**")
        improvements = []
        if comps.get("Savings Behaviour",0) < 10:    improvements.append("Raise monthly savings to 20%+ of income")
        if comps.get("Cash-Flow Consistency",0) < 12: improvements.append("Reduce discretionary outflows for consistent positive CF")
        if comps.get("Income Stability",0) < 15:     improvements.append("Diversify income sources; reduce income volatility")
        if comps.get("Debt Coverage (DSCR)",0) < 10: improvements.append("Reduce existing EMI obligations — improve DSCR")
        if comps.get("Account Behaviour",0) < 6:     improvements.append("Eliminate all bounces — maintain minimum balance")
        if total_bounces > 2: improvements.append(f"{total_bounces} bounces recorded — highest negative signal for lenders")
        if not improvements: improvements.append("Excellent profile — sustain current financial discipline")
        for im in improvements:
            st.markdown(f"<div style='background:rgba(240,180,41,0.05);border:1px solid rgba(240,180,41,0.15);border-radius:8px;padding:0.55rem 0.9rem;margin-bottom:4px;font-size:0.82rem;color:#EDF2FA;'>⚠️ {im}</div>", unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # All 4 perspectives summary
    st.markdown("**Multi-Stakeholder Assessment Summary**")
    PD_base, LGD_base = get_risk_params(lbl)
    loan_est = 1500000
    el_est   = PD_base * LGD_base * loan_est

    persp_data = [
        ("🏛️ NBFC / Credit Provider",  "pl-nbfc",
         f"EL: {format_inr(el_est)} | ECL Rate: {PD_base*LGD_base*100:.1f}% | Bucket: {'Standard' if fb>=700 else 'Special Mention' if fb>=650 else 'Sub-Standard'}",
         f"{'Prime borrower — priority acquisition target.' if fb>=750 else 'Acceptable risk — standard processing.' if fb>=650 else 'Elevated risk — enhanced due diligence required.'}"),
        ("💚 Consumer / Borrower",      "pl-consumer",
         f"Monthly surplus for EMI: {format_inr(avg_m_income*0.55)} | FOIR capacity: {'✅ Good' if avg_m_income>0 else 'N/A'}",
         f"{'Strong disposable income — multiple loan options available.' if avg_m_income*0.55 > 10000 else 'Limited EMI capacity — smaller loan recommended.'}"),
        ("🏦 Bank / Regulatory",        "pl-bank",
         f"DPDP Compliance: ✅ | AA Consent: Ready | KFS: Generated | RBI DLG 2022: Compliant",
         "Full regulatory framework met. Ready for digital onboarding via AA ecosystem."),
        ("🔬 Credit Bureau / Hybrid",   "pl-bureau",
         f"FinBridge: {fb} | Traditional Est.: {ci} | Divergence: {'+' if fb>ci else ''}{fb-ci} pts",
         f"{'FinBridge captures superior signals vs. bureau — real cash-flow strength.' if fb>ci else 'Both models agree — robust creditworthiness.' if fb==ci else 'Bureau score higher — review credit card behaviour.'}"),
    ]

    for persp_title, persp_cls, persp_detail, persp_verdict in persp_data:
        st.markdown(f"""
        <div style='background:var(--navy-card);border:1px solid var(--border-2);border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:0.6rem;'>
            <div style='display:flex;align-items:center;gap:0.7rem;margin-bottom:0.5rem;flex-wrap:wrap;'>
                <span style='font-size:0.88rem;color:#EDF2FA;font-weight:600;'>{persp_title}</span>
                <span class='perspective-label {persp_cls}' style='margin:0;'>{persp_cls.replace("pl-","").upper()}</span>
            </div>
            <div style='font-size:0.8rem;color:#8FA3C0;margin-bottom:0.3rem;font-family:"JetBrains Mono",monospace;'>{persp_detail}</div>
            <div style='font-size:0.82rem;color:#EDF2FA;'>{persp_verdict}</div>
        </div>
        """, unsafe_allow_html=True)

    # Score projection
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**📈 24-Month Score Projection**")
    months_p = list(range(0, 25, 3))
    base_vel = 3.0 if savings_rate >= 20 and total_bounces == 0 else 1.5 if total_bounces == 0 else 0.8
    proj_sc  = [min(900, fb + int(m * base_vel)) for m in months_p]

    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(
        x=[f"M+{m}" for m in months_p], y=proj_sc,
        mode="lines+markers", line=dict(color="#F0B429",width=2.5),
        marker=dict(size=8,color="#F0B429"),
        fill="tozeroy", fillcolor="rgba(240,180,41,0.05)"))
    for hy, hl, hc in [(750,"Excellent","#3EC87A"),(700,"Good","#7CC87E"),(650,"Fair","#F0B429")]:
        fig_proj.add_hline(y=hy, line_dash="dot", line_color=hc,
            annotation_text=hl, annotation_font_color=hc, annotation_position="right")
    fig_proj.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#1C3050"), yaxis=dict(gridcolor="#1C3050",range=[max(280,fb-30),min(930,proj_sc[-1]+30)]),
        font=dict(color="#8FA3C0"), showlegend=False, height=240, margin=dict(t=10,b=30,l=10,r=60))
    st.plotly_chart(fig_proj, use_container_width=True)

    st.markdown("""
    <div style='text-align:center;font-size:0.68rem;color:#2A4060;margin-top:1.5rem;border-top:1px solid #1C3050;padding-top:1rem;line-height:2;'>
        FinBridge Credit Intelligence Platform &nbsp;|&nbsp;
        This report is for analytical and informational purposes only &nbsp;|&nbsp;
        FinBridge is NOT a registered Credit Information Company under the CIC (Regulation) Act, 2005 &nbsp;|&nbsp;
        All data is self-declared and unverified &nbsp;|&nbsp;
        Scores do not constitute a formal credit assessment &nbsp;|&nbsp;
        DPDP Act 2023 Compliant Architecture
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FALLBACK
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.session_state.step = "profile"
    st.rerun()
