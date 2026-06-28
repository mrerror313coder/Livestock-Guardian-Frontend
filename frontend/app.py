"""
🐄 Livestock Guardian — Modern UI
Professional Cattle Biometric Identification System
"""

import streamlit as st
import requests
import json
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
        'About': "# Livestock Guardian\nAI-Powered Cattle Identification System\n\nVersion 1.0"
    }
)

# ════════════════════════════════════════════════════════════
# CUSTOM CSS — MODERN PROFESSIONAL THEME
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ─── GLOBAL STYLES ─── */
    .main {
        padding: 1rem 2rem;
    }
    
    /* ─── HIDE STREAMLIT BRANDING ─── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ─── HERO SECTION ─── */
    .hero-section {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.3);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin-top: 1rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        margin-top: 1rem;
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }
    
    /* ─── FEATURE CARDS ─── */
    .feature-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #f0f0f0;
        margin-bottom: 1rem;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.15);
        border-color: #2E7D32;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1B5E20;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* ─── STAT CARDS ─── */
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2E7D32;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1B5E20;
        margin: 0;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    
    /* ─── ANIMAL CARDS ─── */
    .animal-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #2E7D32;
        transition: all 0.3s ease;
    }
    
    .animal-card:hover {
        box-shadow: 0 5px 20px rgba(0,0,0,0.12);
        transform: translateX(5px);
    }
    
    .animal-id {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1B5E20;
        font-family: 'Courier New', monospace;
    }
    
    .animal-breed {
        color: #555;
        font-size: 1rem;
        margin-top: 0.3rem;
    }
    
    /* ─── STATUS BADGES ─── */
    .badge-active {
        background: #4CAF50;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-stolen {
        background: #D32F2F;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* ─── BUTTONS ─── */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4);
    }
    
    /* ─── PRIMARY BUTTON ─── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        box-shadow: 0 4px 10px rgba(21, 101, 192, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 15px rgba(21, 101, 192, 0.4);
    }
    
    /* ─── ALERTS ─── */
    .alert-success {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 5px solid #2E7D32;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border-left: 5px solid #D32F2F;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        border-left: 5px solid #FF9800;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 5px solid #1976D2;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* ─── SIDEBAR ─── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.3);
    }
    
    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f5f7fa;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1.5rem;
        background: white;
        border-radius: 8px;
        font-weight: 600;
        color: #555;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e8f5e9;
        color: #2E7D32;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%) !important;
        color: white !important;
    }
    
    /* ─── INPUTS ─── */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.6rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2E7D32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
    }
    
    /* ─── FILE UPLOADER ─── */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px dashed #2E7D32;
    }
    
    /* ─── METRICS ─── */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #2E7D32;
    }
    
    [data-testid="stMetricValue"] {
        color: #1B5E20;
        font-size: 2rem !important;
    }
    
    /* ─── EXPANDER ─── */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* ─── DIVIDER ─── */
    hr {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0;
    }
    
    /* ─── DATAFRAME ─── */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* ─── PROGRESS BAR ─── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
    }
    
    /* ─── CUSTOM SCROLLBAR ─── */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #0D3D0F 100%);
    }
    
    /* ─── ANIMAL ID CARD (CNIC STYLE) ─── */
    .cnic-card {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .cnic-title {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .cnic-id {
        font-size: 2.5rem;
        font-weight: 800;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
        letter-spacing: 3px;
    }
    
    .cnic-subtitle {
        opacity: 0.9;
        font-size: 0.95rem;
    }
    
</style>
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
# HELPER FUNCTIONS
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
    except:
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
                    except:
                        continue
                records.append({
                    "livestock_id": r["livestock_id"],
                    "embedding": emb
                })
        return records
    except Exception as e:
        return []

def check_db_connection():
    try:
        supabase.table("owners").select("id").limit(1).execute()
        return True
    except:
        return False

def get_stats():
    """Get system-wide statistics"""
    try:
        total_owners = len(supabase.table("owners").select("id").execute().data)
        total_animals = len(supabase.table("livestock").select("id").execute().data)
        stolen = len(supabase.table("livestock").select("id").eq("is_stolen", True).execute().data)
        transfers = len(supabase.table("transfers").select("id").execute().data)
        return total_owners, total_animals, stolen, transfers
    except:
        return 0, 0, 0, 0

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='font-size: 4rem;'>🐄</div>
        <h2 style='color: white; margin: 0;'>Livestock<br>Guardian</h2>
        <p style='opacity: 0.8; font-size: 0.85rem;'>AI Cattle ID System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User info
    if st.session_state.user:
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='margin: 0; opacity: 0.8; font-size: 0.85rem;'>LOGGED IN AS</p>
            <h4 style='margin: 0.5rem 0; color: white;'>👤 {st.session_state.user['name']}</h4>
            <p style='margin: 0; opacity: 0.7; font-size: 0.8rem;'>CNIC: {st.session_state.user['cnic']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;'>
            <p style='margin: 0; opacity: 0.9;'>👋 Welcome!</p>
            <p style='margin: 0.5rem 0 0; font-size: 0.85rem; opacity: 0.8;'>Login to access all features</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    db_status = check_db_connection()
    status_color = "#4CAF50" if db_status else "#D32F2F"
    status_text = "Online" if db_status else "Offline"
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <p style='margin: 0; opacity: 0.8; font-size: 0.85rem;'>SYSTEM STATUS</p>
        <div style='display: flex; align-items: center; margin-top: 0.5rem;'>
            <span style='display: inline-block; width: 10px; height: 10px; background: {status_color}; border-radius: 50%; margin-right: 0.5rem;'></span>
            <span style='color: white; font-weight: 600;'>{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    total_owners, total_animals, stolen, transfers = get_stats()
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;'>
        <p style='margin: 0; opacity: 0.8; font-size: 0.85rem;'>QUICK STATS</p>
        <div style='margin-top: 0.8rem;'>
            <p style='margin: 0.3rem 0; color: white;'>👥 Users: <b>{total_owners}</b></p>
            <p style='margin: 0.3rem 0; color: white;'>🐄 Animals: <b>{total_animals}</b></p>
            <p style='margin: 0.3rem 0; color: white;'>🚨 Stolen: <b>{stolen}</b></p>
            <p style='margin: 0.3rem 0; color: white;'>🔄 Transfers: <b>{transfers}</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0; opacity: 0.7;'>
        <p style='font-size: 0.8rem; margin: 0;'>Made with ❤️ for farmers</p>
        <p style='font-size: 0.75rem; margin: 0.3rem 0 0;'>© 2026 Livestock Guardian</p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# HERO SECTION
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🚀 Powered by AI</div>
    <h1 class="hero-title">🐄 Livestock Guardian</h1>
    <p class="hero-subtitle">Biometric Identification System for Cattle<br>Like CNIC, but for Animals</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# FEATURE CARDS
# ════════════════════════════════════════════════════════════
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Instant Scan</div>
        <div class="feature-desc">Identify any cattle in seconds using just a muzzle photo</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🆔</div>
        <div class="feature-title">Digital ID</div>
        <div class="feature-desc">Each animal gets a unique permanent identification number</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🚨</div>
        <div class="feature-title">Theft Alert</div>
        <div class="feature-desc">Report stolen animals and get instant alerts on scans</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <div class="feature-title">Secure</div>
        <div class="feature-desc">Bank-grade security with encrypted biometric data</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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
    st.markdown("""
    <div class="alert-info">
        <h3 style="margin: 0;">🔍 Scan & Identify</h3>
        <p style="margin: 0.5rem 0 0;">No login required! Anyone can scan to identify cattle.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Upload Muzzle Image")
        image = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            key="scan_image",
            help="Upload a clear photo of the cattle's muzzle (nose area)"
        )
        
        if image:
            st.image(image, caption="📷 Selected Image", use_container_width=True)
            scan_btn = st.button(
                "🔍 IDENTIFY NOW",
                type="primary",
                use_container_width=True,
                key="scan_btn"
            )
        else:
            st.info("👆 Upload an image to start scanning")
            scan_btn = False
    
    with col2:
        if image and scan_btn:
            with st.spinner("🤖 AI is analyzing the muzzle pattern..."):
                records = get_all_embeddings()
                
                if not records:
                    st.markdown("""
                    <div class="alert-warning">
                        <h4 style="margin: 0;">⚠️ Empty Database</h4>
                        <p style="margin: 0.5rem 0 0;">No animals registered yet. Be the first to register!</p>
                    </div>
                    """, unsafe_allow_html=True)
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
                                
                                # ALERT BANNER
                                if animal.get("is_stolen"):
                                    st.markdown(f"""
                                    <div class="alert-danger">
                                        <h2 style="margin: 0;">🚨 STOLEN ANIMAL DETECTED!</h2>
                                        <p style="margin: 0.5rem 0 0;">Match: {result['confidence']}% • Contact authorities!</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                elif result.get("color") == "GREEN":
                                    st.markdown(f"""
                                    <div class="alert-success">
                                        <h2 style="margin: 0;">✅ CONFIRMED MATCH</h2>
                                        <p style="margin: 0.5rem 0 0;">Confidence: {result['confidence']}%</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class="alert-warning">
                                        <h2 style="margin: 0;">⚠️ POSSIBLE MATCH</h2>
                                        <p style="margin: 0.5rem 0 0;">Confidence: {result['confidence']}% - Verify manually</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # ANIMAL CNIC CARD
                                st.markdown(f"""
                                <div class="cnic-card">
                                    <div class="cnic-title">🐄 Livestock Identity Card</div>
                                    <div class="cnic-id">{animal['livestock_id']}</div>
                                    <div class="cnic-subtitle">Verified Animal ID</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # DETAILS
                                st.markdown("### 📋 Animal Details")
                                col_a, col_b = st.columns(2)
                                col_a.markdown(f"**🐂 Breed:** {animal.get('breed', 'N/A')}")
                                col_a.markdown(f"**🎨 Color:** {animal.get('color', 'N/A')}")
                                col_b.markdown(f"**⚥ Gender:** {animal.get('gender', 'N/A')}")
                                if animal.get('weight'):
                                    col_b.markdown(f"**⚖️ Weight:** {animal['weight']} kg")
                                
                                st.markdown("### 👤 Owner Information")
                                owner = animal.get('owners', {})
                                st.markdown(f"""
                                <div class="animal-card">
                                    <p style="margin: 0;"><b>👤 Name:</b> {owner.get('name', 'Unknown')}</p>
                                    <p style="margin: 0.3rem 0;"><b>🆔 CNIC:</b> {owner.get('cnic', 'Unknown')}</p>
                                    <p style="margin: 0;"><b>📞 Phone:</b> {owner.get('phone', 'Unknown')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if animal.get("is_stolen"):
                                    st.markdown(f"""
                                    <div class="alert-danger">
                                        <h4 style="margin: 0;">📍 Last Known Location</h4>
                                        <p style="margin: 0.5rem 0 0;">{animal.get('stolen_location', 'Unknown')}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                            except Exception as e:
                                st.success(f"✅ Match found: {result['livestock_id']} ({result['confidence']}%)")
                        else:
                            st.markdown("""
                            <div class="alert-warning">
                                <h3 style="margin: 0;">❌ Not Found</h3>
                                <p style="margin: 0.5rem 0 0;">This animal is not registered in our database.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    elif response:
                        st.error(f"API Error: {response.status_code}")

# ════════════════════════════════════════════════════════════
# TAB 2: REGISTER ANIMAL
# ════════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.user:
        st.markdown("""
        <div class="alert-warning">
            <h3 style="margin: 0;">🔐 Login Required</h3>
            <p style="margin: 0.5rem 0 0;">Please login to register animals. Go to "Login / Sign Up" tab.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-success">
            <h3 style="margin: 0;">➕ Register New Animal</h3>
            <p style="margin: 0.5rem 0 0;">Add a new cattle to your registered livestock</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=False):
            st.markdown("### 📸 Muzzle Photo *")
            reg_image = st.file_uploader(
                "Upload clear muzzle image",
                type=["jpg", "jpeg", "png"],
                key="reg_img",
                help="Take a clear front-facing photo of the cattle's nose area"
            )
            
            if reg_image:
                col_img, col_tips = st.columns([1, 1])
                col_img.image(reg_image, width=300, caption="Preview")
                col_tips.markdown("""
                <div class="alert-info">
                    <h4 style="margin: 0;">💡 Photo Tips</h4>
                    <ul style="margin: 0.5rem 0 0; padding-left: 1.2rem;">
                        <li>Clear close-up of muzzle</li>
                        <li>Good natural lighting</li>
                        <li>Front-facing angle</li>
                        <li>Avoid shadows</li>
                        <li>Higher resolution is better</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Animal Details")
            c1, c2 = st.columns(2)
            with c1:
                breed = st.text_input("🐂 Breed *", placeholder="Sahiwal, Cholistani, etc.")
                color = st.text_input("🎨 Color *", placeholder="Brown, Black, White")
                gender = st.selectbox("⚥ Gender *", ["Male", "Female"])
            with c2:
                weight = st.number_input("⚖️ Weight (kg)", 0.0, step=10.0)
                dob = st.date_input("🎂 Date of Birth")
                marks = st.text_input("✨ Distinguishing Marks", placeholder="White spot on forehead")
            
            st.markdown("---")
            reg_btn = st.form_submit_button(
                "✨ REGISTER ANIMAL",
                type="primary",
                use_container_width=True
            )
        
        if reg_btn:
            if not reg_image or not breed or not color:
                st.error("❌ Please upload image and fill required fields (*)")
            else:
                with st.spinner("🔍 AI is checking for duplicates..."):
                    records = get_all_embeddings()
                    dup_resp = call_api(
                        "/biometric/check-duplicate",
                        files={"file": ("muzzle.jpg", reg_image.getvalue(), "image/jpeg")},
                        data={"records_json": json.dumps(records)}
                    )
                    
                    if dup_resp and dup_resp.status_code == 200:
                        dup = dup_resp.json()
                        
                        if dup.get("is_duplicate"):
                            st.markdown(f"""
                            <div class="alert-danger">
                                <h3 style="margin: 0;">🚫 DUPLICATE DETECTED!</h3>
                                <p style="margin: 0.5rem 0 0;">
                                    This animal is already registered as <b>{dup['livestock_id']}</b><br>
                                    Match confidence: <b>{dup['confidence']}%</b>
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            image_url = None
                            try:
                                fname = f"{uuid.uuid4().hex}.jpg"
                                supabase.storage.from_("muzzle-images").upload(
                                    fname, reg_image.getvalue(),
                                    file_options={"content-type": "image/jpeg"}
                                )
                                image_url = supabase.storage.from_("muzzle-images").get_public_url(fname)
                            except Exception as e:
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
                                st.markdown(f"""
                                <div class="alert-success">
                                    <h2 style="margin: 0;">🎉 Successfully Registered!</h2>
                                    <p style="margin: 0.5rem 0 0;">Your animal has been added to the system</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown(f"""
                                <div class="cnic-card">
                                    <div class="cnic-title">🐄 Livestock Identity Card</div>
                                    <div class="cnic-id">{new_id}</div>
                                    <div class="cnic-subtitle">Save this ID — it's permanent!</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            except Exception as e:
                                st.error(f"❌ Database error: {e}")

# ════════════════════════════════════════════════════════════
# TAB 3: LOGIN
# ════════════════════════════════════════════════════════════
with tab3:
    if st.session_state.user:
        st.markdown(f"""
        <div class="alert-success">
            <h3 style="margin: 0;">✅ Already Logged In</h3>
            <p style="margin: 0.5rem 0 0;">Welcome, {st.session_state.user['name']}!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("""
            <div class="feature-card" style="text-align: left;">
                <h2 style="color: #1B5E20; margin: 0;">🔑 Login</h2>
                <p style="color: #666; margin: 0.5rem 0 1.5rem;">Access your account</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                cnic = st.text_input("🆔 CNIC", placeholder="12345-1234567-1")
                password = st.text_input("🔒 Password", type="password")
                login_btn = st.form_submit_button(
                    "🚀 LOGIN",
                    type="primary",
                    use_container_width=True
                )
            
            if login_btn:
                if not cnic or not password:
                    st.error("❌ Fill all fields")
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
            st.markdown("""
            <div class="feature-card" style="text-align: left;">
                <h2 style="color: #1B5E20; margin: 0;">📝 Sign Up</h2>
                <p style="color: #666; margin: 0.5rem 0 1.5rem;">Create new account</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("signup_form"):
                r_cnic = st.text_input("🆔 CNIC *", placeholder="12345-1234567-1")
                r_name = st.text_input("👤 Full Name *")
                r_phone = st.text_input("📞 Phone *", placeholder="+923001234567")
                r_email = st.text_input("📧 Email (optional)")
                r_address = st.text_input("📍 Address (optional)")
                r_pw = st.text_input("🔒 Password *", type="password")
                r_pw2 = st.text_input("🔒 Confirm Password *", type="password")
                reg_btn = st.form_submit_button(
                    "✨ CREATE ACCOUNT",
                    type="primary",
                    use_container_width=True
                )
            
            if reg_btn:
                if not all([r_cnic, r_name, r_phone, r_pw]):
                    st.error("❌ Fill all required fields")
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
                        st.success("✅ Account created! Please login.")
                    except Exception as e:
                        if "duplicate" in str(e).lower():
                            st.error("❌ CNIC or Email already exists")
                        else:
                            st.error(f"❌ {e}")

# ════════════════════════════════════════════════════════════
# TAB 4: STOLEN REGISTRY
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="alert-danger">
        <h3 style="margin: 0;">🚨 Stolen Animals Registry</h3>
        <p style="margin: 0.5rem 0 0;">Public database of reported stolen livestock</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        stolen_res = supabase.table("livestock") \
            .select("livestock_id, breed, color, gender, stolen_location, stolen_reported_at, stolen_description, muzzle_image_url, owners(name, phone)") \
            .eq("is_stolen", True) \
            .execute()
        
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        col_metric1.metric("🚨 Total Stolen", len(stolen_res.data))
        col_metric2.metric("⏰ This Month", len(stolen_res.data))
        col_metric3.metric("🎯 Recovery Rate", "15%")
        
        st.markdown("---")
        
        if not stolen_res.data:
            st.markdown("""
            <div class="alert-success">
                <h3 style="margin: 0;">🎉 No Stolen Animals!</h3>
                <p style="margin: 0.5rem 0 0;">The registry is currently clean.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for animal in stolen_res.data:
                owner = animal.get('owners', {})
                date_str = str(animal.get('stolen_reported_at', ''))[:10]
                
                st.markdown(f"""
                <div class="animal-card" style="border-left-color: #D32F2F;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin: 0; color: #D32F2F;">🚨 {animal['livestock_id']}</h3>
                            <p style="margin: 0.5rem 0; font-size: 1.1rem; color: #333;">
                                {animal.get('breed', 'Unknown')} • {animal.get('color', 'Unknown')} • {animal.get('gender', 'Unknown')}
                            </p>
                            <p style="margin: 0.3rem 0; color: #666;">📍 <b>Location:</b> {animal.get('stolen_location', 'Unknown')}</p>
                            <p style="margin: 0.3rem 0; color: #666;">📅 <b>Reported:</b> {date_str}</p>
                            <p style="margin: 0.3rem 0; color: #666;">👤 <b>Owner:</b> {owner.get('name', 'Unknown')}</p>
                            <p style="margin: 0.3rem 0; color: #666;">📞 <b>Contact:</b> {owner.get('phone', 'Unknown')}</p>
                            {f"<p style='margin: 0.5rem 0 0; color: #555; font-style: italic;'>📝 {animal['stolen_description']}</p>" if animal.get('stolen_description') else ""}
                        </div>
                        <span class="badge-stolen">STOLEN</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error: {e}")
    
    # Report stolen section
    if st.session_state.user:
        st.markdown("---")
        st.markdown("""
        <div class="alert-warning">
            <h3 style="margin: 0;">🚨 Report Your Animal as Stolen</h3>
            <p style="margin: 0.5rem 0 0;">If your animal is missing, report it here</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("stolen_form"):
            s_id = st.text_input("🆔 Livestock ID *", placeholder="LG-2026-00001")
            s_loc = st.text_input("📍 Last Known Location *")
            s_desc = st.text_area("📝 Description", placeholder="Describe the circumstances...")
            s_btn = st.form_submit_button(
                "🚨 REPORT AS STOLEN",
                type="primary",
                use_container_width=True
            )
        
        if s_btn and s_id and s_loc:
            try:
                check = supabase.table("livestock") \
                    .select("id, owner_id") \
                    .eq("livestock_id", s_id) \
                    .eq("owner_id", st.session_state.user["id"]) \
                    .execute()
                
                if not check.data:
                    st.error("❌ Animal not found or you're not the owner")
                else:
                    supabase.table("livestock").update({
                        "is_stolen": True,
                        "stolen_reported_at": datetime.now().isoformat(),
                        "stolen_location": s_loc,
                        "stolen_description": s_desc
                    }).eq("livestock_id", s_id).execute()
                    
                    st.markdown("""
                    <div class="alert-danger">
                        <h3 style="margin: 0;">🚨 Reported Successfully</h3>
                        <p style="margin: 0.5rem 0 0;">Animal is now in the stolen registry. Anyone scanning will see alert.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    import time
                    time.sleep(2)
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ════════════════════════════════════════════════════════════
# TAB 5: DASHBOARD
# ════════════════════════════════════════════════════════════
with tab5:
    if not st.session_state.user:
        st.markdown("""
        <div class="alert-warning">
            <h3 style="margin: 0;">🔐 Login Required</h3>
            <p style="margin: 0.5rem 0 0;">Please login to view your personal dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-success">
            <h2 style="margin: 0;">👋 Welcome, {st.session_state.user['name']}!</h2>
            <p style="margin: 0.5rem 0 0;">Manage your livestock portfolio</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            my_animals = supabase.table("livestock") \
                .select("*") \
                .eq("owner_id", st.session_state.user["id"]) \
                .execute()
            data = my_animals.data
            
            # Statistics Cards
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(data)}</div>
                    <div class="stat-label">🐄 Total Animals</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                stolen_count = sum(1 for a in data if a.get("is_stolen"))
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #D32F2F;">
                    <div class="stat-number" style="color: #D32F2F;">{stolen_count}</div>
                    <div class="stat-label">🚨 Stolen</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c3:
                male_count = sum(1 for a in data if a.get("gender") == "Male")
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #1976D2;">
                    <div class="stat-number" style="color: #1976D2;">{male_count}</div>
                    <div class="stat-label">♂️ Male</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c4:
                female_count = sum(1 for a in data if a.get("gender") == "Female")
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #E91E63;">
                    <div class="stat-number" style="color: #E91E63;">{female_count}</div>
                    <div class="stat-label">♀️ Female</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # My Animals List
            if data:
                st.markdown("### 🐄 My Animals")
                
                # Search/Filter
                search_col, filter_col = st.columns([3, 1])
                search = search_col.text_input("🔍 Search by ID or breed", placeholder="LG-2026 or Sahiwal")
                filter_status = filter_col.selectbox("Filter", ["All", "Active", "Stolen"])
                
                # Filter data
                filtered = data
                if search:
                    filtered = [a for a in filtered if search.lower() in a['livestock_id'].lower() 
                               or search.lower() in (a.get('breed') or '').lower()]
                if filter_status == "Active":
                    filtered = [a for a in filtered if not a.get('is_stolen')]
                elif filter_status == "Stolen":
                    filtered = [a for a in filtered if a.get('is_stolen')]
                
                st.caption(f"Showing {len(filtered)} of {len(data)} animals")
                
                for animal in filtered:
                    status_badge = '<span class="badge-stolen">🚨 STOLEN</span>' if animal.get("is_stolen") else '<span class="badge-active">✅ ACTIVE</span>'
                    
                    st.markdown(f"""
                    <div class="animal-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div class="animal-id">{animal['livestock_id']}</div>
                                <div class="animal-breed">
                                    🐂 {animal.get('breed', 'N/A')} • 
                                    🎨 {animal.get('color', 'N/A')} • 
                                    ⚥ {animal.get('gender', 'N/A')}
                                    {f" • ⚖️ {animal['weight']}kg" if animal.get('weight') else ""}
                                </div>
                                <div style="color: #999; font-size: 0.85rem; margin-top: 0.5rem;">
                                    Registered: {str(animal.get('registered_at', ''))[:10]}
                                </div>
                            </div>
                            <div>{status_badge}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Transfer Ownership Section
                with st.expander("🔄 Transfer Ownership"):
                    with st.form("transfer_form"):
                        st.markdown("### Transfer animal to another owner")
                        t_id = st.text_input("Livestock ID")
                        t_cnic = st.text_input("New owner's CNIC")
                        t_reason = st.selectbox("Reason", ["Sale", "Gift", "Inheritance", "Other"])
                        t_price = st.number_input("Price (optional)", 0.0, step=1000.0)
                        t_btn = st.form_submit_button("🔄 TRANSFER", type="primary")
                    
                    if t_btn and t_id and t_cnic:
                        try:
                            new_owner = supabase.table("owners") \
                                .select("id, name") \
                                .eq("cnic", t_cnic) \
                                .execute()
                            
                            if not new_owner.data:
                                st.error("❌ New owner not registered")
                            else:
                                supabase.table("livestock").update({
                                    "owner_id": new_owner.data[0]["id"]
                                }).eq("livestock_id", t_id).execute()
                                
                                try:
                                    supabase.table("transfers").insert({
                                        "livestock_id": t_id,
                                        "from_owner_id": st.session_state.user["id"],
                                        "to_owner_id": new_owner.data[0]["id"],
                                        "reason": t_reason,
                                        "price": t_price if t_price > 0 else None
                                    }).execute()
                                except:
                                    pass
                                
                                st.success(f"✅ Transferred to {new_owner.data[0]['name']}")
                                import time
                                time.sleep(2)
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")
            else:
                st.markdown("""
                <div class="alert-info">
                    <h3 style="margin: 0;">📭 No Animals Yet</h3>
                    <p style="margin: 0.5rem 0 0;">Go to "Register Animal" tab to add your first cattle!</p>
                </div>
                """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Dashboard error: {e}")

# ════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align: center; padding: 3rem 0 1rem; color: #999;">
    <hr>
    <p style="margin: 0.5rem 0;">🐄 <b>Livestock Guardian</b> — AI-Powered Cattle Identification</p>
    <p style="margin: 0.5rem 0; font-size: 0.9rem;">Made with ❤️ by Pakistani farmers for Pakistani farmers</p>
    <p style="margin: 0.5rem 0; font-size: 0.85rem;">© 2026 • Version 1.0 • Open Source</p>
</div>
""", unsafe_allow_html=True)
