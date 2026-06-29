"""
🐄 Livestock Guardian — Modern UI (v2, redesigned)
Professional Cattle Biometric Identification System
"""

import streamlit as st
import requests
import json
import html as html_lib
import time
import os
from datetime import datetime
import uuid
import hashlib

# ════════════════════════════════════════════════════════════
# PAGE CONFIG (MUST BE FIRST!)
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Livestock Guardian | AI Cattle ID",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/livestock-guardian',
        'Report a bug': 'mailto:your@email.com',
        'About': "# Livestock Guardian\nAI-Powered Cattle Identification System\n\nVersion 2.0"
    }
)

# ════════════════════════════════════════════════════════════
# DESIGN TOKENS + CSS
# Palette pulled from the Livestock Guardian brand: forest green
# + gold shield logo, cream/off-white backgrounds, rounded pill
# buttons, icon-led status cards. Change tokens once, it
# propagates everywhere — no more hunting hex codes in markup.
# ════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    :root {
        /* Brand — forest green + gold, from the app logo */
        --c-primary: #2E7D32;
        --c-primary-dark: #14532D;
        --c-primary-soft: #E8F3E9;
        --c-gold: #C9A227;
        --c-gold-dark: #A8841C;
        --c-gold-soft: #FBF3DD;
        --c-accent: #2E7D32;
        --c-accent-soft: #E8F3E9;

        /* Semantic */
        --c-success: #2E7D32;
        --c-success-soft: #E8F3E9;
        --c-danger: #C62828;
        --c-danger-soft: #FBE9E9;
        --c-warning: #B45F06;
        --c-warning-soft: #FCEFDC;
        --c-info: #2E7D32;
        --c-info-soft: #E8F3E9;

        /* Neutrals — warm cream background like the reference screens */
        --c-text: #20241F;
        --c-text-muted: #6B7268;
        --c-text-faint: #9AA199;
        --c-border: #E7E4DC;
        --c-surface: #FFFFFF;
        --c-bg: #F8F6F1;

        /* Spacing / radius — generous, rounded, like the mobile cards */
        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 22px;
        --radius-pill: 999px;
        --shadow-sm: 0 1px 4px rgba(20,40,20,0.06);
        --shadow-md: 0 6px 18px rgba(20,40,20,0.10);
        --font-heading: 'Poppins', 'Inter', sans-serif;
        --font-body: 'Inter', sans-serif;
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation: none !important; transition: none !important; }
    }

    .main { padding: 0.5rem 1.5rem; background: var(--c-bg); font-family: var(--font-body); }
    [data-testid="stAppViewContainer"] { background: var(--c-bg); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    body, .main, [class^="css"] { color: var(--c-text); font-family: var(--font-body); }
    h1, h2, h3, h4 { font-family: var(--font-heading); }

    /* ─── HERO ─── */
    .hero-section {
        background: linear-gradient(135deg, var(--c-primary) 0%, var(--c-primary-dark) 100%);
        padding: clamp(1.5rem, 4vw, 2.5rem) 1.5rem;
        border-radius: var(--radius-lg);
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(201,162,39,0.35);
    }
    .hero-title {
        font-family: var(--font-heading);
        font-size: clamp(1.8rem, 4vw, 2.6rem);
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: clamp(0.9rem, 2vw, 1.05rem);
        margin-top: 0.5rem;
        opacity: 0.92;
        font-weight: 400;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(201,162,39,0.22);
        color: #F5E3A3;
        padding: 0.35rem 1.1rem;
        border-radius: var(--radius-pill);
        margin-bottom: 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* ─── SECURE / VERIFIED PILL (matches "Secure · ID" chip) ─── */
    .secure-pill {
        display: inline-flex; align-items: center; gap: 0.3rem;
        background: var(--c-success-soft); color: var(--c-primary);
        padding: 0.25rem 0.8rem; border-radius: var(--radius-pill);
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase;
    }

    /* ─── FEATURE STRIP ─── */
    .feature-strip { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1.25rem; }
    .feature-pill {
        flex: 1 1 200px;
        background: var(--c-surface);
        border: 1px solid var(--c-border);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        display: flex; align-items: center; gap: 0.6rem;
        box-shadow: var(--shadow-sm);
    }
    .feature-pill .icon {
        font-size: 1.2rem; flex-shrink: 0; width: 2.1rem; height: 2.1rem;
        display: flex; align-items: center; justify-content: center;
        background: var(--c-gold-soft); border-radius: 50%;
    }
    .feature-pill .label { font-weight: 700; font-size: 0.9rem; color: var(--c-text); font-family: var(--font-heading); }
    .feature-pill .desc { font-size: 0.78rem; color: var(--c-text-muted); margin: 0; }

    /* ─── STAT CARDS ─── */
    .stat-card {
        background: var(--c-surface);
        padding: 1.1rem 1.2rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--c-border);
        box-shadow: var(--shadow-sm);
    }
    .stat-number { font-family: var(--font-heading); font-size: 2rem; font-weight: 800; color: var(--c-text); margin: 0; line-height: 1; }
    .stat-label { color: var(--c-text-muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.35rem; }

    /* ─── INFO TILE (2-up grid like the Species/Breed/Age/Weight cards) ─── */
    .tile-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin: 0.75rem 0; }
    .info-tile {
        background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--radius-md);
        padding: 0.9rem 1rem; box-shadow: var(--shadow-sm);
    }
    .info-tile .tile-icon { font-size: 1.1rem; }
    .info-tile .tile-label { color: var(--c-text-muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; margin: 0.3rem 0 0.1rem; }
    .info-tile .tile-value { font-family: var(--font-heading); font-weight: 700; font-size: 1.05rem; color: var(--c-text); }

    /* ─── ANIMAL / GENERIC CARDS ─── */
    .animal-card {
        background: var(--c-surface);
        padding: 1.1rem 1.25rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--c-border);
        border-left: 4px solid var(--bar-color, var(--c-primary));
        margin-bottom: 0.75rem;
        box-shadow: var(--shadow-sm);
    }
    .animal-id { font-family: var(--font-heading); font-size: 1.15rem; font-weight: 700; color: var(--c-text); letter-spacing: 0.02em; }
    .animal-breed { color: var(--c-text-muted); font-size: 0.9rem; margin-top: 0.25rem; }
    .meta-row { color: var(--c-text-muted); font-size: 0.85rem; margin: 0.2rem 0; }
    .meta-row b { color: var(--c-text); font-weight: 600; }

    /* ─── BADGES ─── */
    .badge { display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.28rem 0.75rem; border-radius: var(--radius-pill); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.02em; }
    .badge-active { background: var(--c-success-soft); color: var(--c-primary); }
    .badge-stolen { background: var(--c-danger-soft); color: var(--c-danger); }

    /* ─── ALERTS — icon-in-circle + title + body, like the Theft Alert /
       Health Warning cards in the reference dashboard ─── */
    .alert {
        border-radius: var(--radius-md);
        padding: 1rem 1.15rem;
        margin: 0.75rem 0;
        display: flex; align-items: flex-start; gap: 0.75rem;
        border: 1px solid transparent;
    }
    .alert .alert-icon {
        flex-shrink: 0; width: 2.1rem; height: 2.1rem; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; font-size: 1.05rem;
    }
    .alert .alert-body h3, .alert .alert-body h4 { margin: 0 0 0.2rem 0; font-family: var(--font-heading); font-size: 1rem; }
    .alert .alert-body p { margin: 0; font-size: 0.86rem; color: var(--c-text-muted); }
    .alert-success { background: var(--c-success-soft); }
    .alert-success .alert-icon { background: rgba(46,125,50,0.18); color: var(--c-primary); }
    .alert-success .alert-body h3 { color: var(--c-primary-dark); }
    .alert-danger  { background: var(--c-danger-soft); }
    .alert-danger .alert-icon { background: rgba(198,40,40,0.16); color: var(--c-danger); }
    .alert-danger .alert-body h3 { color: var(--c-danger); }
    .alert-warning { background: var(--c-warning-soft); }
    .alert-warning .alert-icon { background: rgba(180,95,6,0.16); color: var(--c-warning); }
    .alert-warning .alert-body h3 { color: var(--c-warning); }
    .alert-info    { background: var(--c-gold-soft); }
    .alert-info .alert-icon { background: rgba(201,162,39,0.25); color: var(--c-gold-dark); }
    .alert-info .alert-body h3 { color: var(--c-gold-dark); }
    /* One subtle, finite emphasis for genuinely urgent items — not infinite */
    .alert-danger.urgent { animation: flash-once 1.4s ease-out 1; }
    @keyframes flash-once { 0% { box-shadow: 0 0 0 4px rgba(198,40,40,0.22); } 100% { box-shadow: 0 0 0 0 rgba(198,40,40,0); } }

    /* ─── BUTTONS — rounded pill, matching Login/Sign Up/Enroll buttons ─── */
    .stButton > button {
        border-radius: var(--radius-pill);
        font-weight: 700;
        font-family: var(--font-heading);
        border: 1.5px solid var(--c-border);
        padding: 0.5rem 1.4rem;
        transition: filter 0.15s ease, transform 0.1s ease;
    }
    .stButton > button[kind="primary"] {
        background: var(--c-primary);
        border-color: var(--c-primary);
        color: white;
        box-shadow: var(--shadow-sm);
    }
    .stButton > button[kind="primary"]:hover { filter: brightness(0.93); }
    .stButton > button[kind="secondary"] { background: var(--c-surface); color: var(--c-primary); border-color: var(--c-primary); }
    .stButton > button[kind="secondary"]:hover { background: var(--c-success-soft); }
    .stFormSubmitButton > button[kind="primary"] { background: var(--c-primary); border-color: var(--c-primary); }

    /* ─── SIDEBAR ─── */
    [data-testid="stSidebar"] { background: var(--c-primary-dark); }
    [data-testid="stSidebar"] * { color: white !important; font-family: var(--font-body); }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(201,162,39,0.18);
        border: 1px solid rgba(201,162,39,0.45);
        border-radius: var(--radius-pill);
    }
    [data-testid="stSidebar"] .stButton > button:hover { background: rgba(201,162,39,0.3); }
    .sb-block { background: rgba(255,255,255,0.07); padding: 0.9rem 1rem; border-radius: var(--radius-md); margin-bottom: 0.85rem; border: 1px solid rgba(201,162,39,0.2); }
    .sb-label { margin: 0; opacity: 0.75; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; }
    .sb-status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 0.5rem; }
    .sb-logo-wrap { text-align: center; padding: 0.75rem 0 1rem; }
    .sb-logo-wrap img { max-width: 92px; border-radius: 50%; background: white; padding: 8px; }
    .sb-brand-title { color: white; margin: 0.5rem 0 0; font-family: var(--font-heading); font-weight: 700; }
    .sb-brand-sub { opacity: 0.7; font-size: 0.78rem; margin: 0.2rem 0 0; }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background: var(--c-surface); padding: 0.4rem; border-radius: var(--radius-pill); border: 1px solid var(--c-border); }
    .stTabs [data-baseweb="tab"] { padding: 0.6rem 1.2rem; background: transparent; border-radius: var(--radius-pill); font-weight: 600; font-family: var(--font-heading); color: var(--c-text-muted); border: none; }
    .stTabs [aria-selected="true"] { background: var(--c-primary) !important; color: white !important; }

    /* ─── INPUTS — rounded rectangle, matching login/signup fields ─── */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox > div > div, .stDateInput input {
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--c-border) !important;
        background: var(--c-surface);
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--c-primary) !important;
        box-shadow: 0 0 0 3px rgba(46,125,50,0.12);
    }

    [data-testid="stFileUploader"] {
        background: var(--c-surface);
        border-radius: var(--radius-md);
        border: 2px dashed var(--c-gold);
    }

    [data-testid="stMetric"] { background: var(--c-surface); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--c-border); }
    [data-testid="stMetricValue"] { color: var(--c-text); font-size: 1.7rem !important; font-family: var(--font-heading); }

    /* ─── ID CARD — green + gold, like the shield logo ─── */
    .id-card {
        background: linear-gradient(135deg, var(--c-primary-dark) 0%, var(--c-primary) 100%);
        color: white;
        padding: 1.6rem;
        border-radius: var(--radius-lg);
        text-align: center;
        margin: 1.25rem auto;
        max-width: 460px;
        border: 1px solid rgba(201,162,39,0.4);
        box-shadow: var(--shadow-md);
    }
    .id-card .id-title { font-size: 0.78rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.1em; color: #F5E3A3; }
    .id-card .id-value { font-family: var(--font-heading); font-size: 2rem; font-weight: 800; margin: 0.6rem 0; letter-spacing: 0.04em; }
    .id-card .id-subtitle { opacity: 0.85; font-size: 0.85rem; }

    hr { border: none; border-top: 1px solid var(--c-border); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SECURITY HELPER — escape all user-controlled text before
# injecting into unsafe_allow_html markup
# ════════════════════════════════════════════════════════════
def esc(value, default="N/A"):
    if value is None or value == "":
        return default
    return html_lib.escape(str(value))

# ════════════════════════════════════════════════════════════
# REUSABLE UI COMPONENTS
# Centralizing these means one visual change updates every
# instance — and every value passing through is escaped.
# ════════════════════════════════════════════════════════════
def alert(kind, title, message="", urgent=False):
    """Icon-in-circle alert card, matching the Theft Alert / Health Warning
    style from the reference dashboard."""
    icons = {"success": "✓", "danger": "🔒", "warning": "!", "info": "ℹ"}
    cls = f"alert alert-{kind}" + (" urgent" if urgent and kind == "danger" else "")
    msg_html = f"<p>{message}</p>" if message else ""
    st.markdown(f"""
    <div class="{cls}">
        <div class="alert-icon">{icons.get(kind, '')}</div>
        <div class="alert-body">
            <h3>{title}</h3>
            {msg_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def secure_pill(label="Secure", icon="🛡️"):
    """Small chip like the 'Secure · ID' badge on the animal profile card."""
    return f'<span class="secure-pill">{icon} {esc(label)}</span>'

def stat_card(value, label, color="var(--c-primary)"):
    st.markdown(f"""
    <div class="stat-card" style="--bar-color: {color};">
        <p class="stat-number" style="color: {color};">{esc(value, '0')}</p>
        <p class="stat-label">{esc(label)}</p>
    </div>
    """, unsafe_allow_html=True)

def info_tile(icon, label, value):
    """2-up tile like the Species / Breed / Age / Weight cards on the
    reference animal profile screen."""
    st.markdown(f"""
    <div class="info-tile">
        <div class="tile-icon">{icon}</div>
        <div class="tile-label">{esc(label)}</div>
        <div class="tile-value">{esc(value)}</div>
    </div>
    """, unsafe_allow_html=True)

def id_card(id_value, subtitle="Verified Animal ID"):
    st.markdown(f"""
    <div class="id-card">
        <div class="id-title">🐄 Livestock Identity Card</div>
        <div class="id-value">{esc(id_value)}</div>
        <div class="id-subtitle">{esc(subtitle)}</div>
    </div>
    """, unsafe_allow_html=True)

def status_badge(is_stolen):
    return '<span class="badge badge-stolen">🚨 STOLEN</span>' if is_stolen else '<span class="badge badge-active">✓ ACTIVE</span>'

def animal_summary_card(animal, accent="var(--c-primary)", extra_rows=""):
    badge = status_badge(animal.get("is_stolen"))
    weight_row = f" • ⚖️ {esc(animal.get('weight'))}kg" if animal.get("weight") else ""
    st.markdown(f"""
    <div class="animal-card" style="--bar-color: {accent};">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:0.75rem;">
            <div>
                <div class="animal-id">{esc(animal.get('livestock_id'))}</div>
                <div class="animal-breed">🐂 {esc(animal.get('breed'))} • 🎨 {esc(animal.get('color'))} • ⚥ {esc(animal.get('gender'))}{weight_row}</div>
                {extra_rows}
            </div>
            <div>{badge}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# LOAD SECRETS
# ════════════════════════════════════════════════════════════
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    API_URL = st.secrets["API_URL"]
    API_KEY = st.secrets["API_KEY"]
except KeyError as e:
    st.error(f"❌ Missing secret: {e}")
    st.info("Add secrets in Streamlit Cloud → Settings → Secrets")
    st.stop()

# ════════════════════════════════════════════════════════════
# INIT SUPABASE
# ════════════════════════════════════════════════════════════
try:
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"❌ Supabase connection failed: {e}")
    st.stop()

# ════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════
if "user" not in st.session_state:
    st.session_state.user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# ════════════════════════════════════════════════════════════
# HELPER FUNCTIONS (business logic — unchanged from original)
# ════════════════════════════════════════════════════════════
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def generate_livestock_id():
    try:
        year = datetime.now().year
        res = supabase.table("livestock") \
            .select("livestock_id") \
            .like("livestock_id", f"LG-{year}-%") \
            .execute()
        count = len(res.data) + 1
        return f"LG-{year}-{count:05d}"
    except Exception:
        return f"LG-{datetime.now().year}-00001"

def call_api(endpoint, files=None, data=None):
    headers = {"X-API-Key": API_KEY}
    try:
        return requests.post(
            f"{API_URL}{endpoint}",
            files=files, data=data,
            headers=headers, timeout=60
        )
    except requests.ConnectionError:
        st.error("❌ Cannot connect to API server")
        return None
    except requests.Timeout:
        st.error("⏱️ Request timed out")
        return None

def get_all_embeddings():
    try:
        res = supabase.table("livestock") \
            .select("livestock_id, embedding") \
            .not_.is_("embedding", "null") \
            .execute()
        records = []
        for r in res.data:
            emb = r.get("embedding")
            if emb:
                if isinstance(emb, str):
                    try:
                        emb = json.loads(emb)
                    except Exception:
                        continue
                records.append({"livestock_id": r["livestock_id"], "embedding": emb})
        return records
    except Exception:
        return []

def check_db_connection():
    try:
        supabase.table("owners").select("id").limit(1).execute()
        return True
    except Exception:
        return False

def get_stats():
    try:
        total_owners = len(supabase.table("owners").select("id").execute().data)
        total_animals = len(supabase.table("livestock").select("id").execute().data)
        stolen = len(supabase.table("livestock").select("id").eq("is_stolen", True).execute().data)
        transfers = len(supabase.table("transfers").select("id").execute().data)
        return total_owners, total_animals, stolen, transfers
    except Exception:
        return 0, 0, 0, 0

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
LOGO_PATH = "assets/logo.png"

with st.sidebar:
    logo_col = st.columns([1, 2, 1])[1]
    with logo_col:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        else:
            st.markdown("<div style='text-align:center; font-size:2.8rem;'>🐄</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; padding-bottom: 1rem;'>
        <h3 class="sb-brand-title" style="margin-top:0.4rem;">Livestock Guardian</h3>
        <p class="sb-brand-sub">AI Cattle ID System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.user:
        u = st.session_state.user
        st.markdown(f"""
        <div class="sb-block">
            <p class="sb-label">Logged in as</p>
            <h4 style='margin: 0.4rem 0; color: white;'>👤 {esc(u.get('name'))}</h4>
            <p style='margin: 0; opacity: 0.65; font-size: 0.78rem;'>CNIC: {esc(u.get('cnic'))}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.markdown("""
        <div class="sb-block" style="text-align:center;">
            <p style='margin: 0;'>👋 Welcome!</p>
            <p style='margin: 0.4rem 0 0; font-size: 0.8rem; opacity: 0.75;'>Login to register and manage animals</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    db_status = check_db_connection()
    status_color = "#4CAF50" if db_status else "#E57373"
    status_text = "Online" if db_status else "Offline"
    st.markdown(f"""
    <div class="sb-block">
        <p class="sb-label">System status</p>
        <div style='display:flex; align-items:center; margin-top:0.45rem;'>
            <span class="sb-status-dot" style="background:{status_color};"></span>
            <span style='color:white; font-weight:600; font-size:0.9rem;'>{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_owners, total_animals, stolen, transfers = get_stats()
    st.markdown(f"""
    <div class="sb-block">
        <p class="sb-label">Quick stats</p>
        <div style='margin-top:0.6rem; font-size: 0.85rem; line-height: 1.7;'>
            <div>👥 Users <b style="float:right;">{total_owners}</b></div>
            <div>🐄 Animals <b style="float:right;">{total_animals}</b></div>
            <div>🚨 Stolen <b style="float:right;">{stolen}</b></div>
            <div>🔄 Transfers <b style="float:right;">{transfers}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; opacity:0.6; font-size:0.72rem;'>
        Made for farmers · © 2026 Livestock Guardian
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# HERO (compact — gets users to the tabs fast)
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🚀 AI-Powered Biometric ID</div>
    <h1 class="hero-title">🐄 Livestock Guardian</h1>
    <p class="hero-subtitle">Identify any cattle from a muzzle photo — like a CNIC, but for animals</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# FEATURE STRIP — slim row, not competing with primary action
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="feature-strip">
    <div class="feature-pill"><span class="icon">🔍</span><div><p class="label">Instant Scan</p><p class="desc">Identify cattle in seconds</p></div></div>
    <div class="feature-pill"><span class="icon">🆔</span><div><p class="label">Digital ID</p><p class="desc">Unique permanent record</p></div></div>
    <div class="feature-pill"><span class="icon">🚨</span><div><p class="label">Theft Alerts</p><p class="desc">Reported on every scan</p></div></div>
    <div class="feature-pill"><span class="icon">🔒</span><div><p class="label">Secure</p><p class="desc">Encrypted biometric data</p></div></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Scan Muzzle",
    "➕ Register Animal",
    "🔐 Login / Sign Up",
    "🚨 Stolen Registry",
    "📊 My Dashboard"
])

# ════════════════════════════════════════════════════════════
# TAB 1: SCAN MUZZLE
# ════════════════════════════════════════════════════════════
with tab1:
    alert("info", "Scan & Identify", "No login required — anyone can scan to identify cattle.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**📸 Upload muzzle image**")
        image = st.file_uploader(
            "Choose an image", type=["jpg", "jpeg", "png"], key="scan_image",
            help="A clear, front-facing, well-lit photo of the cattle's nose area works best",
            label_visibility="collapsed"
        )
        if image:
            st.image(image, caption="Selected image", use_container_width=True)
            scan_btn = st.button("🔍 Identify now", type="primary", use_container_width=True, key="scan_btn")
        else:
            st.caption("Upload an image to start scanning")
            scan_btn = False

    with col2:
        if image and scan_btn:
            with st.spinner("Analyzing muzzle pattern..."):
                records = get_all_embeddings()

                if not records:
                    alert("warning", "Empty database", "No animals registered yet — be the first to register!")
                else:
                    response = call_api(
                        "/biometric/match-muzzle",
                        files={"file": ("muzzle.jpg", image.getvalue(), "image/jpeg")},
                        data={"records_json": json.dumps(records)}
                    )

                    if response and response.status_code == 200:
                        result = response.json()

                        if result.get("match_found"):
                            try:
                                details = supabase.table("livestock") \
                                    .select("*, owners(name, cnic, phone)") \
                                    .eq("livestock_id", result["livestock_id"]) \
                                    .single() \
                                    .execute()
                                animal = details.data

                                if animal.get("is_stolen"):
                                    alert("danger", "STOLEN ANIMAL DETECTED",
                                          f"Match confidence {esc(result.get('confidence'))}% — contact authorities.",
                                          urgent=True)
                                elif result.get("color") == "GREEN":
                                    alert("success", "Confirmed match", f"Confidence: {esc(result.get('confidence'))}%")
                                else:
                                    alert("warning", "Possible match", f"Confidence: {esc(result.get('confidence'))}% — verify manually")

                                id_card(animal.get('livestock_id'))
                                st.markdown(
                                    f"<div style='text-align:center; margin:-0.5rem 0 1rem;'>{secure_pill('Verified ID')}</div>",
                                    unsafe_allow_html=True
                                )

                                st.markdown("**📋 Animal details**")
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    info_tile("🐂", "Breed", animal.get('breed'))
                                with col_b:
                                    info_tile("🎨", "Color", animal.get('color'))
                                col_c, col_d = st.columns(2)
                                with col_c:
                                    info_tile("⚥", "Gender", animal.get('gender'))
                                with col_d:
                                    info_tile("⚖️", "Weight", f"{animal.get('weight')} kg" if animal.get('weight') else "N/A")

                                st.markdown("**👤 Owner information**")
                                owner = animal.get('owners', {}) or {}
                                st.markdown(f"""
                                <div class="animal-card">
                                    <div class="meta-row"><b>Name:</b> {esc(owner.get('name'), 'Unknown')}</div>
                                    <div class="meta-row"><b>CNIC:</b> {esc(owner.get('cnic'), 'Unknown')}</div>
                                    <div class="meta-row"><b>Phone:</b> {esc(owner.get('phone'), 'Unknown')}</div>
                                </div>
                                """, unsafe_allow_html=True)

                                if animal.get("is_stolen"):
                                    alert("danger", "Last known location", esc(animal.get('stolen_location'), 'Unknown'))

                            except Exception:
                                st.success(f"✅ Match found: {esc(result.get('livestock_id'))} ({esc(result.get('confidence'))}%)")
                        else:
                            alert("warning", "Not found", "This animal is not registered in our database.")
                    elif response:
                        st.error(f"API error: {response.status_code}")
        elif not image:
            st.caption("Results will appear here after you scan an image.")

# ════════════════════════════════════════════════════════════
# TAB 2: REGISTER ANIMAL
# ════════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.user:
        alert("warning", "Login required", 'Please login to register animals — see the "Login / Sign Up" tab.')
    else:
        alert("success", "Register new animal", "Add a new cattle to your registered livestock")

        with st.form("register_form", clear_on_submit=False):
            st.markdown("**📸 Muzzle photo** *")
            reg_image = st.file_uploader(
                "Upload clear muzzle image", type=["jpg", "jpeg", "png"], key="reg_img",
                help="Front-facing, well-lit, high-resolution close-up of the nose area",
                label_visibility="collapsed"
            )

            if reg_image:
                col_img, col_tips = st.columns([1, 1])
                col_img.image(reg_image, width=280, caption="Preview")
                col_tips.markdown("""
                <div class="alert alert-info">
                    <h4>💡 Photo tips</h4>
                    <p>Clear close-up · good lighting · front-facing · no shadows · higher resolution is better</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("**📋 Animal details**")
            c1, c2 = st.columns(2)
            with c1:
                breed = st.text_input("🐂 Breed *", placeholder="Sahiwal, Cholistani, etc.")
                color = st.text_input("🎨 Color *", placeholder="Brown, Black, White")
                gender = st.selectbox("⚥ Gender *", ["Male", "Female"])
            with c2:
                weight = st.number_input("⚖️ Weight (kg)", 0.0, step=10.0)
                dob = st.date_input("🎂 Date of birth")
                marks = st.text_input("✨ Distinguishing marks", placeholder="White spot on forehead")

            reg_btn = st.form_submit_button("✨ Register animal", type="primary", use_container_width=True)

        if reg_btn:
            if not reg_image or not breed or not color:
                st.error("❌ Please upload an image and fill in all required fields (*)")
            else:
                with st.spinner("Checking for duplicates..."):
                    records = get_all_embeddings()
                    dup_resp = call_api(
                        "/biometric/check-duplicate",
                        files={"file": ("muzzle.jpg", reg_image.getvalue(), "image/jpeg")},
                        data={"records_json": json.dumps(records)}
                    )

                    if dup_resp and dup_resp.status_code == 200:
                        dup = dup_resp.json()

                        if dup.get("is_duplicate"):
                            alert("danger", "Duplicate detected",
                                  f"Already registered as <b>{esc(dup.get('livestock_id'))}</b> "
                                  f"(confidence {esc(dup.get('confidence'))}%)")
                        else:
                            image_url = None
                            try:
                                fname = f"{uuid.uuid4().hex}.jpg"
                                supabase.storage.from_("muzzle-images").upload(
                                    fname, reg_image.getvalue(),
                                    file_options={"content-type": "image/jpeg"}
                                )
                                image_url = supabase.storage.from_("muzzle-images").get_public_url(fname)
                            except Exception:
                                pass

                            try:
                                new_id = generate_livestock_id()
                                insert_data = {
                                    "livestock_id": new_id,
                                    "owner_id": st.session_state.user["id"],
                                    "breed": breed,
                                    "color": color,
                                    "gender": gender,
                                    "embedding": dup["embedding"]
                                }
                                if weight > 0:
                                    insert_data["weight"] = weight
                                if marks:
                                    insert_data["distinguishing_marks"] = marks
                                if image_url:
                                    insert_data["muzzle_image_url"] = image_url

                                supabase.table("livestock").insert(insert_data).execute()

                                st.balloons()
                                alert("success", "Successfully registered!", "Your animal has been added to the system")
                                id_card(new_id, subtitle="Save this ID — it's permanent")

                            except Exception as e:
                                st.error(f"❌ Database error: {e}")

# ════════════════════════════════════════════════════════════
# TAB 3: LOGIN
# ════════════════════════════════════════════════════════════
with tab3:
    if st.session_state.user:
        alert("success", "Already logged in", f"Welcome, {esc(st.session_state.user.get('name'))}!")
    else:
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("#### 🔑 Login")
            st.caption("Access your account")
            with st.form("login_form"):
                cnic = st.text_input("🆔 CNIC", placeholder="12345-1234567-1")
                password = st.text_input("🔒 Password", type="password")
                login_btn = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)

            if login_btn:
                if not cnic or not password:
                    st.error("❌ Fill in all fields")
                else:
                    try:
                        pwd_hash = hash_password(password)
                        res = supabase.table("owners") \
                            .select("*") \
                            .eq("cnic", cnic) \
                            .eq("password_hash", pwd_hash) \
                            .execute()

                        if res.data:
                            st.session_state.user = res.data[0]
                            st.success(f"✅ Welcome, {res.data[0]['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
                    except Exception as e:
                        st.error(f"❌ Login error: {e}")

        with col_right:
            st.markdown("#### 📝 Sign up")
            st.caption("Create a new account")
            with st.form("signup_form"):
                r_cnic = st.text_input("🆔 CNIC *", placeholder="12345-1234567-1")
                r_name = st.text_input("👤 Full name *")
                r_phone = st.text_input("📞 Phone *", placeholder="+923001234567")
                r_email = st.text_input("📧 Email (optional)")
                r_address = st.text_input("📍 Address (optional)")
                r_pw = st.text_input("🔒 Password *", type="password", help="6+ characters")
                r_pw2 = st.text_input("🔒 Confirm password *", type="password")
                reg_submit = st.form_submit_button("✨ Create account", type="primary", use_container_width=True)

            if reg_submit:
                if not all([r_cnic, r_name, r_phone, r_pw]):
                    st.error("❌ Fill in all required fields")
                elif r_pw != r_pw2:
                    st.error("❌ Passwords don't match")
                elif len(r_pw) < 6:
                    st.error("❌ Password must be 6+ characters")
                else:
                    try:
                        supabase.table("owners").insert({
                            "cnic": r_cnic,
                            "name": r_name,
                            "phone": r_phone,
                            "email": r_email or None,
                            "address": r_address or None,
                            "password_hash": hash_password(r_pw)
                        }).execute()
                        st.success("✅ Account created — please login")
                    except Exception as e:
                        if "duplicate" in str(e).lower():
                            st.error("❌ CNIC or email already exists")
                        else:
                            st.error(f"❌ {e}")

# ════════════════════════════════════════════════════════════
# TAB 4: STOLEN REGISTRY
# ════════════════════════════════════════════════════════════
with tab4:
    alert("danger", "Stolen animals registry", "Public database of reported stolen livestock")

    try:
        stolen_res = supabase.table("livestock") \
            .select("livestock_id, breed, color, gender, stolen_location, stolen_reported_at, stolen_description, muzzle_image_url, owners(name, phone)") \
            .eq("is_stolen", True) \
            .execute()

        col_metric1, col_metric2, col_metric3 = st.columns(3)
        col_metric1.metric("🚨 Total stolen", len(stolen_res.data))
        col_metric2.metric("⏰ This month", len(stolen_res.data))
        col_metric3.metric("🎯 Recovery rate", "15%")

        st.divider()

        if not stolen_res.data:
            alert("success", "No stolen animals", "The registry is currently clean.")
        else:
            for a in stolen_res.data:
                owner = a.get('owners', {}) or {}
                date_str = str(a.get('stolen_reported_at', ''))[:10]
                desc_row = f"<div class='meta-row' style='font-style:italic;'>📝 {esc(a.get('stolen_description'))}</div>" if a.get('stolen_description') else ""
                st.markdown(f"""
                <div class="animal-card" style="--bar-color: var(--c-danger);">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div class="animal-id" style="color:var(--c-danger);">🚨 {esc(a.get('livestock_id'))}</div>
                            <div class="animal-breed">{esc(a.get('breed'))} • {esc(a.get('color'))} • {esc(a.get('gender'))}</div>
                            <div class="meta-row">📍 <b>Location:</b> {esc(a.get('stolen_location'))}</div>
                            <div class="meta-row">📅 <b>Reported:</b> {esc(date_str)}</div>
                            <div class="meta-row">👤 <b>Owner:</b> {esc(owner.get('name'), 'Unknown')}</div>
                            <div class="meta-row">📞 <b>Contact:</b> {esc(owner.get('phone'), 'Unknown')}</div>
                            {desc_row}
                        </div>
                        <span class="badge badge-stolen">STOLEN</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")

    if st.session_state.user:
        st.divider()
        alert("warning", "Report your animal as stolen", "If your animal is missing, report it here")

        with st.form("stolen_form"):
            s_id = st.text_input("🆔 Livestock ID *", placeholder="LG-2026-00001")
            s_loc = st.text_input("📍 Last known location *")
            s_desc = st.text_area("📝 Description", placeholder="Describe the circumstances...")
            s_btn = st.form_submit_button("🚨 Report as stolen", type="primary", use_container_width=True)

        if s_btn and s_id and s_loc:
            try:
                check = supabase.table("livestock") \
                    .select("id, owner_id") \
                    .eq("livestock_id", s_id) \
                    .eq("owner_id", st.session_state.user["id"]) \
                    .execute()

                if not check.data:
                    st.error("❌ Animal not found, or you're not the registered owner")
                else:
                    supabase.table("livestock").update({
                        "is_stolen": True,
                        "stolen_reported_at": datetime.now().isoformat(),
                        "stolen_location": s_loc,
                        "stolen_description": s_desc
                    }).eq("livestock_id", s_id).execute()

                    alert("danger", "Reported successfully",
                          "Animal is now in the stolen registry — anyone scanning will see an alert.")
                    time.sleep(1.5)
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ════════════════════════════════════════════════════════════
# TAB 5: DASHBOARD
# ════════════════════════════════════════════════════════════
with tab5:
    if not st.session_state.user:
        alert("warning", "Login required", "Please login to view your personal dashboard.")
    else:
        u = st.session_state.user
        alert("success", f"Welcome, {esc(u.get('name'))}!", "Manage your livestock portfolio")

        try:
            my_animals = supabase.table("livestock") \
                .select("*") \
                .eq("owner_id", u["id"]) \
                .execute()
            data = my_animals.data

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                stat_card(len(data), "Total animals")
            with c2:
                stolen_count = sum(1 for a in data if a.get("is_stolen"))
                stat_card(stolen_count, "Stolen", color="var(--c-danger)")
            with c3:
                male_count = sum(1 for a in data if a.get("gender") == "Male")
                stat_card(male_count, "Male", color="var(--c-accent)")
            with c4:
                female_count = sum(1 for a in data if a.get("gender") == "Female")
                stat_card(female_count, "Female", color="#C2185B")

            st.divider()

            if data:
                st.markdown("**🐄 My animals**")

                search_col, filter_col = st.columns([3, 1])
                search = search_col.text_input("Search by ID or breed", placeholder="LG-2026 or Sahiwal",
                                                label_visibility="collapsed")
                filter_status = filter_col.selectbox("Filter", ["All", "Active", "Stolen"], label_visibility="collapsed")

                filtered = data
                if search:
                    s = search.lower()
                    filtered = [a for a in filtered if s in a['livestock_id'].lower() or s in (a.get('breed') or '').lower()]
                if filter_status == "Active":
                    filtered = [a for a in filtered if not a.get('is_stolen')]
                elif filter_status == "Stolen":
                    filtered = [a for a in filtered if a.get('is_stolen')]

                st.caption(f"Showing {len(filtered)} of {len(data)} animals")

                for a in filtered:
                    extra = f"<div class='meta-row' style='margin-top:0.4rem; color:var(--c-text-faint);'>Registered: {esc(str(a.get('registered_at', ''))[:10])}</div>"
                    accent = "var(--c-danger)" if a.get("is_stolen") else "var(--c-primary)"
                    animal_summary_card(a, accent=accent, extra_rows=extra)

                st.divider()

                with st.expander("🔄 Transfer ownership"):
                    with st.form("transfer_form"):
                        st.caption("Transfer an animal to another registered owner")
                        t_id = st.text_input("Livestock ID")
                        t_cnic = st.text_input("New owner's CNIC")
                        t_reason = st.selectbox("Reason", ["Sale", "Gift", "Inheritance", "Other"])
                        t_price = st.number_input("Price (optional)", 0.0, step=1000.0)
                        t_btn = st.form_submit_button("🔄 Transfer", type="primary")

                    if t_btn and t_id and t_cnic:
                        try:
                            new_owner = supabase.table("owners").select("id, name").eq("cnic", t_cnic).execute()

                            if not new_owner.data:
                                st.error("❌ New owner not registered")
                            else:
                                supabase.table("livestock").update(
                                    {"owner_id": new_owner.data[0]["id"]}
                                ).eq("livestock_id", t_id).execute()

                                try:
                                    supabase.table("transfers").insert({
                                        "livestock_id": t_id,
                                        "from_owner_id": u["id"],
                                        "to_owner_id": new_owner.data[0]["id"],
                                        "reason": t_reason,
                                        "price": t_price if t_price > 0 else None
                                    }).execute()
                                except Exception:
                                    pass

                                st.success(f"✅ Transferred to {new_owner.data[0]['name']}")
                                time.sleep(1.5)
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")
            else:
                alert("info", "No animals yet", 'Go to "Register Animal" to add your first cattle.')

        except Exception as e:
            st.error(f"❌ Dashboard error: {e}")

# ════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding: 2rem 0 0.5rem; color: var(--c-text-faint);">
    <hr>
    <p style="margin: 0.4rem 0; font-weight:600; color: var(--c-text-muted);">🐄 Livestock Guardian — AI-Powered Cattle Identification</p>
    <p style="margin: 0.2rem 0; font-size: 0.8rem;">© 2026 · Version 2.0</p>
</div>
""", unsafe_allow_html=True)
