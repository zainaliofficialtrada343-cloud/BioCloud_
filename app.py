import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css
from receipt_design import show_receipt
from streamlit_gsheets import GSheetsConnection

# --- 1. CONNECTION & DATA FETCHING ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_full_data():
    try:
        df = conn.read(worksheet="data_db", ttl="0")
        return df
    except:
        cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    try:
        return conn.read(worksheet="tests_db", ttl="0")
    except:
        return pd.DataFrame([{"Test_Name": "CBC", "Rate": 500}, {"Test_Name": "Sugar", "Rate": 200}])

def get_expense_data():
    try:
        df = conn.read(worksheet="expenses_db", ttl="0")
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except:
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# --- 2. SAVE FUNCTIONS ---
def save_record_local(new_row_df):
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    conn.update(worksheet="data_db", data=updated_data)

def save_test_local(new_test_df):
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    conn.update(worksheet="tests_db", data=updated_tests)

def save_expense_gsheet(new_ex_df):
    existing_ex = get_expense_data()
    updated_ex = pd.concat([existing_ex, new_ex_df], ignore_index=True)
    conn.update(worksheet="expenses_db", data=updated_ex)

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- 4. ADVANCED CSS (Like your uploaded images) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://raw.githubusercontent.com/zainaliofficialtrada343-cloud/BioCloud_/main/lab_girl.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* Top Premium Bar */
    .top-bar {
        background-color: #1E3A8A;
        color: white;
        padding: 8px 60px;
        display: flex;
        justify-content: space-between;
        margin: -75px -100px 10px -100px;
        font-family: sans-serif;
    }

    /* Web Style Header */
    .nav-header {
        background: white;
        padding: 15px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 0 -100px 30px -100px;
        border-bottom: 3px solid #3B82F6;
    }
    .logo-text { font-size: 26px; font-weight: 800; color: #1E3A8A; }
    .logo-text span { color: #3B82F6; }

    /* Modern Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #3B82F6;
    }
    
    /* Input Form Styling */
    div[data-baseweb="input"] { border-radius: 8px !important; }
    .stButton>button {
        border-radius: 8px;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #3B82F6; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- 5. SESSION STATE ---
if 'temp_tests' not in st.session_state: st.session_state.temp_tests = [] 
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'show_slip' not in st.session_state: st.session_state.show_slip = None
if 'saved_mobile' not in st.session_state: st.session_state.saved_mobile = ""
if 'lab_name' not in st.session_state: st.session_state.lab_name = "MAJEED COLONY SEC 2, KARACHI"
if 'lab_phone' not in st.session_state: st.session_state.lab_phone = "03XX-XXXXXXX"

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else: st.error("Invalid Username or Password")

# --- MAIN LOGIC ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    df = get_full_data()
    today_dt = datetime.now().date()
    today = str(today_dt)
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🧪 BioCloud Pro</h2>", unsafe_allow_html=True)
        menu = st.radio("MAIN MENU", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        st.divider()
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    # --- TOP HEADER (Appears on all pages for consistency) ---
    st.markdown(f"""
        <div class="top-bar">
            <span>📞 {st.session_state.lab_phone}</span>
            <span>📍 {st.session_state.lab_name}</span>
            <span>📅 {today_dt.strftime('%d %b, %Y')}</span>
        </div>
        <div class="nav-header">
            <div class="logo-text">BIOCLOUD <span>PRO</span></div>
            <div style="font-weight: 600; color: #666;">LABORATORY MANAGEMENT SYSTEM</div>
        </div>
    """, unsafe_allow_html=True)

    # --- MENU NAVIGATION ---
    if menu == "🏠 Home":
        st.markdown(f"<h1 style='color: #1E3A8A;'>Welcome, Administrator</h1>", unsafe_allow_html=True)
        
        # Dashboard Metrics
        c1, c2, c3, c4 = st.columns(4)
        total_p = len(df[df['Date'] == today]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0
        
        with c1: st.markdown(f'<div class="metric-card"><h3>{total_p}</h3><p>Today Patients</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card" style="border-top-color: #10B981;"><h3>Rs. {total_cash}</h3><p>Today Cash</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card" style="border-top-color: #EF4444;"><h3>{pending_p}</h3><p>Pending Reports</p></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card" style="border-top-color: #F59E0B;"><h3>Online</h3><p>Cloud Sync</p></div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("🚀 Quick Shortcuts")
        q1, q2, q3 = st.columns(3)
        if q1.button("New Patient Registration", use_container_width=True): st.info("Go to '📝 Registration' from sidebar")
        if q2.button("Check Pending Dues", use_container_width=True): st.info("Go to '💰 Dues & Reports' from sidebar")
        if q3.button("Daily Expense Entry", use_container_width=True): st.info("Go to '💸 Expense Manager' from sidebar")

    elif menu == "📝 Registration":
        st.markdown("<h2 style='color: #1E3A8A;'>Patient Registration</h2>", unsafe_allow_html=True)
        
        if st.session_state.show_slip:
            st.success("✅ Record Saved Successfully!")
            show_receipt(st.session_state.show_slip)
            if st.button("Close & New Registration"):
                st.session_state.show_slip = None
                st.rerun()
        else:
            # Registration Form Logic
            tdf = get_tests_list()
            test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
            test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}

            with st.container(border=True):
                r1, r2 = st.columns(2)
                p_name = r1.text_input("Patient Full Name")
                p_mobile = r2.text_input("Mobile Number", value=st.session_state.saved_mobile)
                
                r3, r4, r5 = st.columns(3)
                p_age = r3.number_input("Age", 1, 100, 25)
                p_gender = r4.selectbox("Gender", ["Male", "Female", "Other"])
                p_coll = r5.selectbox("Sample Collection", ["Lab Box", "Home", "Hospital"])

            st.markdown("### Add Tests")
            t_col1, t_col2, t_col3 = st.columns([2,1,1])
            sel_t = t_col1.selectbox("Select Test", ["-- Choose --"] + test_options)
            rate = t_col2.number_input("Rate", value=test_rate_dict.get(sel_t, 0) if sel_t != "-- Choose --" else 0)
            if t_col3.button("➕ Add to List", use_container_width=True):
                if sel_t != "-- Choose --":
                    st.session_state.temp_tests.append({"Test": sel_t, "Rate": rate})
                    st.rerun()

            if st.session_state.temp_tests:
                for i, t in enumerate(st.session_state.temp_tests):
                    st.write(f"Item {i+1}: {t['Test']} - Rs. {t['Rate']}")
                
                total = sum(item['Rate'] for item in st.session_state.temp_tests)
                paid = st.number_input("Amount Paid", 0, total)
                
                if st.button("💾 SAVE & PRINT RECEIPT", use_container_width=True):
                    all_t = ", ".join([x['Test'] for x in st.session_state.temp_tests])
                    new_id = len(df) + 1
                    inv = f"INV-{100+new_id}"
                    rem = total - paid
                    data = [new_id, inv, today, p_name, p_mobile, p_age, p_gender, p_coll, all_t, total, paid, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                    save_record_local(pd.DataFrame([data], columns=required_cols))
                    st.session_state.show_slip = data
                    st.session_state.temp_tests = []
                    st.rerun()

    elif menu == "💰 Dues & Reports":
        st.markdown("<h2 style='color: #1E3A8A;'>Update Dues & Test Results</h2>", unsafe_allow_html=True)
        pending_df = df[df["Status"] == "Pending"]
        if not pending_df.empty:
            sel_p = st.selectbox("Select Pending Patient", pending_df["Name"].tolist())
            p_row = df[df["Name"] == sel_p].iloc[-1]
            
            with st.container(border=True):
                st.write(f"**Current Dues:** Rs. {p_row['Remaining']}")
                c_1, c_2 = st.columns(2)
                add_cash = c_1.number_input("Receive Payment", 0)
                result = c_2.text_input("Test Result", value=p_row['Result'])
                
                if st.button("Update Cloud Record"):
                    new_paid = p_row["Paid_Amount"] + add_cash
                    new_rem = p_row["Total_Bill"] - new_paid
                    df.loc[df["ID"] == p_row["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), result]
                    conn.update(worksheet="data_db", data=df)
                    st.success("Cloud Updated!")
                    st.rerun()
        else:
            st.info("No pending records found.")

    elif menu == "💸 Expense Manager":
        st.markdown("<h2 style='color: #1E3A8A;'>Lab Expenses</h2>", unsafe_allow_html=True)
        # Expense logic is same as your code but with clean columns
        with st.form("ex_form"):
            cat = st.selectbox("Category", ["Staff", "Chemicals", "Rent", "Food", "Other"])
            amt = st.number_input("Amount", 0)
            desc = st.text_input("Description")
            if st.form_submit_button("Save Expense"):
                save_expense_gsheet(pd.DataFrame([[today, cat, desc, amt]], columns=["Date", "Category", "Description", "Amount"]))
                st.success("Expense Added!")

    elif menu == "📊 Excel History":
        st.markdown("<h2 style='color: #1E3A8A;'>Complete Database</h2>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Excel Report", csv, "Lab_Data.csv", "text/csv")

    elif menu == "⚙️ Lab Settings":
        st.markdown("<h2 style='color: #1E3A8A;'>System Settings</h2>", unsafe_allow_html=True)
        with st.container(border=True):
            st.session_state.lab_name = st.text_input("Lab Name", value=st.session_state.lab_name)
            st.session_state.lab_phone = st.text_input("Contact Info", value=st.session_state.lab_phone)
            if st.button("Update Lab Profile"):
                st.success("Settings Saved!")
