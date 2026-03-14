import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css
from receipt_design import show_receipt
from streamlit_gsheets import GSheetsConnection

# --- 1. GOOGLE SHEETS CONNECTION ---
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

# --- 4. ADVANCED CSS (Merging your HTML Design) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Modern UI Tweaks */
        .stApp { background: #f0f4f8; }
        
        /* Navigation Style from your HTML */
        .custom-nav {
            background: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 5%;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin: -6rem -5rem 2rem -5rem;
        }
        .logo { font-size: 24px; font-weight: 800; color: #1a73e8; font-family: 'Segoe UI', sans-serif; }
        
        /* Hero Section Styling */
        .hero-container {
            display: flex;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .hero-text {
            flex: 1;
            padding: 60px;
            background: #fdfdfd;
        }
        .hero-text h1 { font-size: 45px; color: #202124; line-height: 1.2; }
        .hero-image-box {
            flex: 1;
            background: url('https://images.unsplash.com/photo-1581093458791-9f3c3900df4b?auto=format&fit=crop&w=1000&q=80');
            background-size: cover;
            background-position: center;
            clip-path: polygon(15% 0, 100% 0, 100% 100%, 0% 100%);
        }

        /* Stats Cards */
        .stat-card {
            background: white; padding: 20px; border-radius: 12px;
            text-align: center; border-bottom: 5px solid #1a73e8;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        
        /* Hide Streamlit default elements for cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 5. SESSION STATE ---
if 'menu_choice' not in st.session_state: st.session_state.menu_choice = "🏠 Home"
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

# --- MAIN APP ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    df = get_full_data()
    today_dt = datetime.now().date()
    today = str(today_dt)
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    # Sidebar Navigation (Functionality)
    with st.sidebar:
        st.markdown(f"<div class='logo'>LAB<span style='color: #34a853;'>PRO</span></div>", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("Go To:", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        
        st.divider()
        if st.checkbox("Enable Delete Option"):
            if st.button("⚠️ Delete All Data", type="primary"):
                conn.update(worksheet="data_db", data=pd.DataFrame(columns=required_cols))
                st.rerun()
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    # --- TOP CUSTOM NAV (Visual Only) ---
    st.markdown(f"""
        <div class="custom-nav">
            <div class="logo">LAB<span style="color: #34a853;">PRO</span></div>
            <div style="font-weight: 600; color: #5f6368;">
                <i class="fas fa-clinic-medical"></i> {st.session_state.lab_name}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 1. HOME PAGE (The Award Winning Design) ---
    if menu == "🏠 Home":
        st.markdown(f"""
            <div class="hero-container">
                <div class="hero-text">
                    <h1>Award Winning <br> <span style="color: #1a73e8;">Laboratory</span> Center</h1>
                    <p>We provide advanced diagnostic services with high precision and care. Managing your lab data has never been this easy and efficient.</p>
                    <div style="display: flex; gap: 10px; margin-top: 20px;">
                        <div style="padding: 10px 20px; background: #1a73e8; color: white; border-radius: 5px; font-weight: bold;">Precision</div>
                        <div style="padding: 10px 20px; background: #34a853; color: white; border-radius: 5px; font-weight: bold;">Care</div>
                    </div>
                </div>
                <div class="hero-image-box"></div>
            </div>
        """, unsafe_allow_html=True)

        # Dashboard Stats
        total_p = len(df[df['Date'] == today]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-card"><h4>Patients</h4><h2>{total_p}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-card" style="border-color:#34a853;"><h4>Cash Today</h4><h2>Rs. {total_cash}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-card" style="border-color:#ea4335;"><h4>Pending</h4><h2>{pending_p}</h2></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-card" style="border-color:#fbbc05;"><h4>Status</h4><h2>Online ✅</h2></div>', unsafe_allow_html=True)

    # --- 2. REGISTRATION (Same Logic, Cleaner Look) ---
    elif menu == "📝 Registration":
        st.markdown("## <i class='fas fa-user-plus'></i> New Registration", unsafe_allow_html=True)
        
        if st.session_state.show_slip:
            st.success("✅ Saved to Cloud!")
            show_receipt(st.session_state.show_slip)
            if st.button("New Patient"):
                st.session_state.show_slip = None
                st.rerun()
        else:
            tdf = get_tests_list()
            test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
            test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}

            with st.container(border=True):
                r1c1, r1c2, r1c3 = st.columns([2, 1, 1])
                p_name = r1c1.text_input("Patient Name")
                p_mobile = r1c2.text_input("Mobile", value=st.session_state.saved_mobile)
                p_inv = r1c3.text_input("Invoice", value=f"INV-{len(df) + 101}")

                r2c1, r2c2, r2c3, r2c4 = st.columns(4)
                p_age = r2c1.number_input("Age", 1, 100, 25)
                p_gender = r2c2.selectbox("Gender", ["Male", "Female", "Other"])
                p_ref = r2c3.text_input("Ref By", "Self")
                p_coll = r2c4.selectbox("Source", ["Lab", "Home", "Hospital"])

            st.write("---")
            col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
            sel_t = col_t1.selectbox("Select Test", ["--- Select ---"] + test_options)
            rate = col_t2.number_input("Rate", value=test_rate_dict.get(sel_t, 0) if sel_t != "--- Select ---" else 0)
            if col_t3.button("➕ Add Test", use_container_width=True):
                if sel_t != "--- Select ---":
                    st.session_state.temp_tests.append({"Test": sel_t, "Rate": rate})
                    st.rerun()

            if st.session_state.temp_tests:
                for i, t in enumerate(st.session_state.temp_tests):
                    st.info(f"{t['Test']} - Rs. {t['Rate']}")
                
                total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
                paid = st.number_input("Paid Amount", 0, total_bill)
                
                if st.button("💾 Final Save & Print", use_container_width=True, type="primary"):
                    all_tests = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                    rem = total_bill - paid
                    data = [len(df)+1, p_inv, today, p_name, p_mobile, p_age, p_gender, p_coll, all_tests, total_bill, paid, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                    save_record_local(pd.DataFrame([data], columns=required_cols))
                    st.session_state.show_slip = data
                    st.session_state.temp_tests = []
                    st.rerun()

    # --- 3. DUES & REPORTS ---
    elif menu == "💰 Dues & Reports":
        st.markdown("## <i class='fas fa-file-invoice-dollar'></i> Update Records", unsafe_allow_html=True)
        if not df.empty:
            pending = df[df["Status"] == "Pending"]
            if not pending.empty:
                sel = st.selectbox("Search Pending Patient", pending["Name"].tolist())
                p_data = df[df["Name"] == sel].iloc[-1]
                st.warning(f"Pending: Rs. {p_data['Remaining']} for {p_data['Test']}")
                
                c1, c2 = st.columns(2)
                add_p = c1.number_input("Add Payment", 0)
                res = c2.text_input("Enter Result", value=p_data['Result'])
                
                if st.button("Update Cloud Data"):
                    new_paid = p_row = p_data["Paid_Amount"] + add_p
                    new_rem = p_data["Total_Bill"] - new_paid
                    df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res]
                    conn.update(worksheet="data_db", data=df)
                    st.success("Updated Successfully!")
                    st.rerun()

    # --- 4. EXPENSE MANAGER ---
    elif menu == "💸 Expense Manager":
        st.markdown("## <i class='fas fa-wallet'></i> Lab Expenses", unsafe_allow_html=True)
        t1, t2 = st.tabs(["Add Expense", "Reports"])
        with t1:
            cat = st.selectbox("Category", ["Staff", "Rent", "Chemicals", "Utility", "Food", "Other"])
            amt = st.number_input("Amount", 0)
            desc = st.text_input("Description")
            if st.button("Save Expense"):
                save_expense_gsheet(pd.DataFrame([[today, cat, desc, amt]], columns=["Date", "Category", "Description", "Amount"]))
                st.success("Expense Recorded!")

    # --- 5. HISTORY SEARCH ---
    elif menu == "🔍 History Search":
        st.markdown("## <i class='fas fa-search'></i> Search Records", unsafe_allow_html=True)
        query = st.text_input("Enter Name, ID or Mobile No")
        if query:
            res = df[df.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
            st.dataframe(res, use_container_width=True)

    # --- 6. EXCEL HISTORY ---
    elif menu == "📊 Excel History":
        st.markdown("## <i class='fas fa-file-excel'></i> Master Database", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download Excel", df.to_csv(index=False), "Lab_History.csv", "text/csv")

    # --- 7. SETTINGS ---
    elif menu == "⚙️ Lab Settings":
        st.markdown("## <i class='fas fa-cog'></i> Configuration", unsafe_allow_html=True)
        st.session_state.lab_name = st.text_input("Lab Name", value=st.session_state.lab_name)
        st.session_state.lab_phone = st.text_input("Contact", value=st.session_state.lab_phone)
        st.success("Settings Updated locally!")