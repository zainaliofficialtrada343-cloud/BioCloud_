import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- 2. GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_full_data():
    try:
        df = conn.read(worksheet="data_db", ttl="0")
        return df
    except:
        return pd.DataFrame(columns=["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"])

# --- 3. CUSTOM CSS FOR MODERN UI ---
st.markdown("""
    <style>
    /* Hide Default Streamlit Menu & Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Modern Navigation Bar */
    .nav-container {
        display: flex;
        justify-content: center;
        background-color: #ffffff;
        padding: 10px;
        border-bottom: 2px solid #1a73e8;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    /* Hero Section Style */
    .hero-box {
        background: linear-gradient(90deg, #f0f4f8 50%, transparent 50%), 
                    url('https://images.unsplash.com/photo-1579152276506-5d5e7d6b350d?auto=format&fit=crop&w=1000&q=80');
        background-size: cover;
        height: 400px;
        padding: 60px;
        border-radius: 20px;
        margin-top: 50px;
        display: flex;
        align-items: center;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { font-size: 28px; color: #1a73e8; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SESSION STATE & NAVIGATION LOGIC ---
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "🏠 Home"

# --- 5. TOP NAVIGATION BUTTONS (Replacing Sidebar) ---
# Hum yahan columns use kar rahe hain taake ye top bar ki tarah lage
st.markdown("<br><br>", unsafe_allow_html=True) # Space for fixed nav
cols = st.columns(7)
menu_items = {
    "🏠 Home": "Home",
    "📝 Registration": "Reg",
    "💰 Dues": "Dues",
    "💸 Expense": "Exp",
    "🔍 Search": "Search",
    "📊 History": "History",
    "⚙️ Settings": "Settings"
}

# Navbar Buttons
for i, (label, key) in enumerate(menu_items.items()):
    if cols[i].button(label, use_container_width=True):
        st.session_state.menu_choice = label

# --- 6. APP CONTENT ---
df = get_full_data()
today_dt = datetime.now().date()

if st.session_state.menu_choice == "🏠 Home":
    # Hero Section like the screenshot
    st.markdown(f"""
        <div class="hero-box">
            <div style="max-width: 50%;">
                <h1 style='font-size: 45px; color: #202124;'>Award Winning<br><span style='color: #1a73e8;'>Laboratory</span> Center</h1>
                <p style='color: #5f6368;'>Welcome to BioCloud Pro. Managing your lab diagnostics with cloud-precision.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    total_p = len(df[df['Date'] == str(today_dt)]) if not df.empty else 0
    total_cash = pd.to_numeric(df[df['Date'] == str(today_dt)]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
    
    c1.metric("Today's Patients", total_p)
    c2.metric("Today's Cash", f"Rs. {total_cash}")
    c3.metric("Lab Status", "Online ✅")
    c4.metric("Database", "G-Sheets ☁️")

elif st.session_state.menu_choice == "📝 Registration":
    st.header("📝 Patient Registration")
    # Aapka purana Registration ka saara code yahan aayega
    with st.form("reg_form"):
        p_name = st.text_input("Patient Name")
        p_mobile = st.text_input("Mobile")
        submitted = st.form_submit_button("Save Record")
        if submitted:
            st.success(f"Record for {p_name} saved!")

elif st.session_state.menu_choice == "🔍 Search":
    st.header("🔍 Advanced Search")
    search = st.text_input("Search Name or Invoice")
    if search:
        res = df[df['Name'].str.contains(search, case=False)]
        st.dataframe(res)

# ... Bakki saare sections (Dues, Expense, etc.) isi tarah elif mein aayenge

# --- SIDEBAR (Optional - for Logout/Admin) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063205.png", width=100)
    st.title("Admin Panel")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()