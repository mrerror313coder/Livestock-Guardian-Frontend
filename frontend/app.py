"""
🐄 Livestock Guardian — Streamlit Frontend
Complete UI for biometric livestock identification
"""

import streamlit as st
import requests
import json
from supabase import create_client
from datetime import datetime
import uuid

# ── CONFIG ──
st.set_page_config(
    page_title="🐄 Livestock Guardian",
    page_icon="🐄",
    layout="wide"
)

# ── CREDENTIALS (Use Streamlit secrets in production) ──
SUPABASE_URL = "https://oqbrhzxozjsgqadayfnp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xYnJoenhvempzZ3FhZGF5Zm5wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwNjIyNjIsImV4cCI6MjA5NTYzODI2Mn0.D7P51-O8dqRqtssSE9gIEg5YJUHt3IEZc0cd_ko9oOk"
API_URL = "https://livestock-guardian-biometric.onrender.com"
API_KEY = "LG_2bdb53afaf462bce8bcb23fc117d4096f76983e8e3beb922d1ab3d7715d7e0b0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── SESSION STATE ──
if "user" not in st.session_state:
    st.session_state.user = None

# ── HELPERS ──
def generate_livestock_id():
    year = datetime.now().year
    res = supabase.table("livestock").select("livestock_id").like("livestock_id", f"LG-{year}-%").execute()
    count = len(res.data) + 1
    return f"LG-{year}-{count:05d}"

def call_api(endpoint, files=None, data=None):
    headers = {"X-API-Key": API_KEY}
    try:
        return requests.post(f"{API_URL}{endpoint}", files=files, data=data, headers=headers, timeout=60)
    except requests.ConnectionError:
        st.error("❌ Cannot connect to API")
        return None

# ── SIDEBAR ──
with st.sidebar:
    st.title("🐄 Livestock Guardian")
    st.divider()
    
    if st.session_state.user:
        st.success(f"👤 {st.session_state.user['name']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Login to access features")

# ── MAIN ──
st.title("🐄 Livestock Guardian")
st.markdown("### AI-Powered Cattle Identification")

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Scan Muzzle", 
    "➕ Register", 
    "🔐 Login", 
    "🚨 Stolen", 
    "📊 Dashboard"
])

# ── TAB 1: SCAN ──
with tab1:
    st.subheader("Scan Cattle Muzzle")
    st.info("No login required — anyone can scan!")
    
    image = st.file_uploader("Upload muzzle image", type=["jpg", "jpeg", "png"])
    
    if image:
        col1, col2 = st.columns(2)
        col1.image(image, width=300)
        
        if col1.button("🔍 Identify", type="primary"):
            with col2:
                with st.spinner("Scanning..."):
                    # Get all livestock embeddings
                    livestock_data = supabase.table("livestock").select("livestock_id, embedding").execute()
                    
                    records = [{
                        "livestock_id": r["livestock_id"],
                        "embedding": json.loads(r["embedding"]) if isinstance(r["embedding"], str) else r["embedding"]
                    } for r in livestock_data.data]
                    
                    # Call API
                    response = call_api(
                        "/biometric/match-muzzle",
                        files={"file": image.getvalue()},
                        data={"records_json": json.dumps(records)}
                    )
                
                if response and response.status_code == 200:
                    result = response.json()
                    
                    if result["match_found"]:
                        # Get full details
                        details = supabase.table("livestock").select("*, owners(*)").eq("livestock_id", result["livestock_id"]).single().execute()
                        animal = details.data
                        
                        if animal["is_stolen"]:
                            st.error(f"🚨 STOLEN ANIMAL! ({result['confidence']}% match)")
                        elif result["color"] == "GREEN":
                            st.success(f"✅ Confirmed: {result['confidence']}%")
                        else:
                            st.warning(f"⚠️ Possible match: {result['confidence']}%")
                        
                        st.markdown(f"### 🆔 {animal['livestock_id']}")
                        st.markdown(f"**Breed:** {animal['breed']}")
                        st.markdown(f"**Color:** {animal['color']}")
                        st.markdown(f"**Gender:** {animal['gender']}")
                        st.markdown(f"**Owner:** {animal['owners']['name']}")
                        st.markdown(f"**Phone:** {animal['owners']['phone']}")
                    else:
                        st.warning("❌ Not found in database")
                else:
                    st.error("API request failed")

# ── TAB 2: REGISTER ──
with tab2:
    st.subheader("Register New Animal")
    
    if not st.session_state.user:
        st.warning("Please login first")
    else:
        with st.form("register_form"):
            image = st.file_uploader("Muzzle image *", type=["jpg", "jpeg", "png"], key="reg_img")
            if image:
                st.image(image, width=300)
            
            c1, c2 = st.columns(2)
            breed = c1.text_input("Breed *")
            color = c1.text_input("Color *")
            gender = c1.selectbox("Gender *", ["Male", "Female"])
            weight = c2.number_input("Weight (kg)", 0.0, step=10.0)
            dob = c2.date_input("Date of birth")
            marks = c2.text_input("Distinguishing marks")
            
            submitted = st.form_submit_button("➕ Register", type="primary")
        
        if submitted and image and breed and color:
            with st.spinner("Processing..."):
                # Get all embeddings for duplicate check
                livestock_data = supabase.table("livestock").select("livestock_id, embedding").execute()
                records = [{
                    "livestock_id": r["livestock_id"],
                    "embedding": json.loads(r["embedding"]) if isinstance(r["embedding"], str) else r["embedding"]
                } for r in livestock_data.data]
                
                # Check duplicate
                dup_response = call_api(
                    "/biometric/check-duplicate",
                    files={"file": image.getvalue()},
                    data={"records_json": json.dumps(records)}
                )
                
                if dup_response and dup_response.status_code == 200:
                    dup_result = dup_response.json()
                    
                    if dup_result["is_duplicate"]:
                        st.error(f"🚫 Duplicate! Already registered as {dup_result['livestock_id']} ({dup_result['confidence']}%)")
                    else:
                        # Upload image to Supabase Storage
                        filename = f"{uuid.uuid4().hex}.jpg"
                        supabase.storage.from_("muzzle-images").upload(filename, image.getvalue())
                        image_url = supabase.storage.from_("muzzle-images").get_public_url(filename)
                        
                        # Save to database
                        new_id = generate_livestock_id()
                        supabase.table("livestock").insert({
                            "livestock_id": new_id,
                            "owner_id": st.session_state.user["id"],
                            "breed": breed,
                            "color": color,
                            "gender": gender,
                            "weight": weight if weight > 0 else None,
                            "date_of_birth": str(dob),
                            "distinguishing_marks": marks,
                            "muzzle_image_url": image_url,
                            "embedding": dup_result["embedding"]
                        }).execute()
                        
                        st.balloons()
                        st.success(f"✅ Registered as {new_id}")

# ── TAB 3: LOGIN ──
with tab3:
    st.subheader("Login / Register")
    
    tab_l, tab_r = st.tabs(["Login", "Register Account"])
    
    with tab_l:
        with st.form("login"):
            cnic = st.text_input("CNIC")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")
        
        if submitted and cnic and password:
            import hashlib
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            res = supabase.table("owners").select("*").eq("cnic", cnic).eq("password_hash", pwd_hash).execute()
            
            if res.data:
                st.session_state.user = res.data[0]
                st.success(f"✅ Welcome, {res.data[0]['name']}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab_r:
        with st.form("signup"):
            cnic = st.text_input("CNIC *", key="r_cnic")
            name = st.text_input("Name *")
            phone = st.text_input("Phone *")
            email = st.text_input("Email")
            password = st.text_input("Password *", type="password", key="r_pw")
            submitted = st.form_submit_button("Register", type="primary")
        
        if submitted and all([cnic, name, phone, password]):
            import hashlib
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                supabase.table("owners").insert({
                    "cnic": cnic, "name": name, "phone": phone,
                    "email": email or None, "password_hash": pwd_hash
                }).execute()
                st.success("✅ Registered! Now login.")
            except Exception as e:
                st.error(f"Error: {e}")

# ── TAB 4: STOLEN ──
with tab4:
    st.subheader("🚨 Stolen Animals")
    stolen = supabase.table("livestock").select("*, owners(*)").eq("is_stolen", True).execute()
    
    st.metric("Total Stolen", len(stolen.data))
    
    for animal in stolen.data:
        with st.container():
            st.error(f"🚨 {animal['livestock_id']} — {animal['breed']}")
            c1, c2 = st.columns(2)
            c1.markdown(f"📍 {animal.get('stolen_location', 'Unknown')}")
            c2.markdown(f"📞 {animal['owners']['phone']}")
            st.divider()

# ── TAB 5: DASHBOARD ──
with tab5:
    if not st.session_state.user:
        st.warning("Login to see dashboard")
    else:
        animals = supabase.table("livestock").select("*").eq("owner_id", st.session_state.user["id"]).execute()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Animals", len(animals.data))
        c2.metric("Stolen", sum(1 for a in animals.data if a["is_stolen"]))
        c3.metric("Healthy", sum(1 for a in animals.data if not a["is_stolen"]))
        
        st.divider()
        for a in animals.data:
            st.markdown(f"**{a['livestock_id']}** | {a['breed']} | {a['color']}")
