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

# --- 4. CSS FOR NAVIGATION & HERO (HTML Look) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Modern Navigation Bar */
        .nav-container {
            background: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 5%;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin: -6rem -5rem 2rem -5rem;
            position: sticky;
            top: 0;
            z-index: 999;
        }
        .logo { font-size: 22px; font-weight: 800; color: #1a73e8; font-family: 'Segoe UI', sans-serif; }
        
        /* Hero Section Styling */
        .hero-section {
            display: flex;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            min-height: 400px;
        }
        .hero-text-box {
            flex: 1; padding: 50px;
        }
        .hero-text-box h1 { font-size: 50px; color: #202124; line-height: 1.1; margin-bottom: 20px; }
        .hero-img-box {
            flex: 1;
            background: url('https://images.unsplash.com/photo-1581093458791-9f3c3900df4b?auto=format&fit=crop&w=1000&q=80');
            background-size: cover;
            background-position: center;
            clip-path: polygon(15% 0, 100% 0, 100% 100%, 0% 100%);
        }
        
        /* Stats Cards */
        .card-box {
            background: white; padding: 20px; border-radius: 12px;
            text-align: center; border-bottom: 4px solid #1a73e8;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }

        /* Hide Default Streamlit Header */
        header {visibility: hidden;}
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

# --- MAIN LOGIC ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    df = get_full_data()
    today_dt = datetime.now().date()
    today = str(today_dt)
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    # --- TOP NAVIGATION BAR (HTML Buttons Integrated with Streamlit) ---
    # Humne columns use kiye hain taake clickable buttons ban saken
    st.markdown(f"""<div class="nav-container"><div class="logo">LAB<span style="color: #34a853;">PRO</span></div><div style="color: #5f6368; font-weight: bold;">{st.session_state.lab_name}</div></div>""", unsafe_allow_html=True)
    
    # Custom Menu Buttons
    nav_cols = st.columns(7)
    menu_options = ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"]
    
    for i, option in enumerate(menu_options):
        if nav_cols[i].button(option, use_container_width=True):
            st.session_state.menu_choice = option
            st.rerun()

    st.write("---")

    # --- PAGE ROUTING ---
    menu = st.session_state.menu_choice

    # 1. HOME PAGE
    if menu == "🏠 Home":
        st.markdown(f"""
            <div class="hero-section">
                <div class="hero-text-box">
                    <h1>Award Winning <br> <span style="color: #1a73e8;">Laboratory</span> Center</h1>
                    <p style="color: #5f6368; font-size: 18px;">We provide advanced diagnostic services with high precision and care. Managing your lab data has never been this easy and efficient.</p>
                    <br>
                    <div style="display: flex; gap: 15px;">
                        <span style="background: #1a73e8; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;">Precision</span>
                        <span style="background: #34a853; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;">Certified</span>
                    </div>
                </div>
                <div class="hero-img-box"></div>
            </div>
        """, unsafe_allow_html=True)

        # Dashboard Metrics
        total_p = len(df[df['Date'] == today]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f'<div class="card-box"><h5>Total Patients</h5><h2>{total_p}</h2></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="card-box" style="border-color:#34a853;"><h5>Today Cash</h5><h2>Rs. {total_cash}</h2></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="card-box" style="border-color:#ea4335;"><h5>Pending</h5><h2>{pending_p}</h2></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="card-box" style="border-color:#fbbc05;"><h5>Lab Status</h5><h2>Online ✅</h2></div>', unsafe_allow_html=True)

    # 2. REGISTRATION
    elif menu == "📝 Registration":
        st.header("📝 Patient Registration")
        if st.session_state.show_slip:
            st.success("Record Saved!")
            show_receipt(st.session_state.show_slip)
            if st.button("New Registration"):
                st.session_state.show_slip = None
                st.rerun()
        else:
            with st.expander("Patient Details", expanded=True):
                c1, c2, c3 = st.columns([2,1,1])
                p_name = c1.text_input("Full Name")
                p_mobile = c2.text_input("Mobile", value=st.session_state.saved_mobile)
                p_inv = c3.text_input("Invoice", f"INV-{len(df)+101}")
                
                c4, c5, c6 = st.columns(3)
                p_age = c4.number_input("Age", 1, 120, 25)
                p_gen = c5.selectbox("Gender", ["Male", "Female", "Other"])
                p_coll = c6.selectbox("Sample Source", ["Lab", "Home", "Hospital"])

            st.subheader("Add Tests")
            tdf = get_tests_list()
            test_list = tdf["Test_Name"].tolist() if not tdf.empty else []
            t_rate_map = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}
            
            tc1, tc2, tc3 = st.columns([2,1,1])
            sel_t = tc1.selectbox("Select Test", ["--- Select ---"] + test_list)
            rate = tc2.number_input("Rate", value=t_rate_map.get(sel_t, 0) if sel_t != "--- Select ---" else 0)
            if tc3.button("➕ Add"):
                if sel_t != "--- Select ---":
                    st.session_state.temp_tests.append({"Test": sel_t, "Rate": rate})
                    st.rerun()

            if st.session_state.temp_tests:
                for i, t in enumerate(st.session_state.temp_tests):
                    st.text(f"✅ {t['Test']} - Rs. {t['Rate']}")
                
                total = sum(item['Rate'] for item in st.session_state.temp_tests)
                paid = st.number_input("Paid Amount", 0, total)
                
                if st.button("💾 Save & Print", type="primary"):
                    all_t = ", ".join([x['Test'] for x in st.session_state.temp_tests])
                    rem = total - paid
                    row = [len(df)+1, p_inv, today, p_name, p_mobile, p_age, p_gen, p_coll, all_t, total, paid, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                    save_record_local(pd.DataFrame([row], columns=required_cols))
                    st.session_state.show_slip = row
                    st.session_state.temp_tests = []
                    st.rerun()

    # 3. DUES & REPORTS
    elif menu == "💰 Dues & Reports":
        st.header("💰 Manage Dues & Results")
        if not df.empty:
            pend = df[df["Status"] == "Pending"]
            if not pend.empty:
                sel_p = st.selectbox("Select Patient", pend["Name"].tolist())
                p_row = df[df["Name"] == sel_p].iloc[-1]
                st.info(f"Test: {p_row['Test']} | Remaining: {p_row['Remaining']}")
                
                cc1, cc2 = st.columns(2)
                add_cash = cc1.number_input("Clear Dues (Amount)", 0)
                res_val = cc2.text_input("Result Value", value=p_row['Result'])
                
                if st.button("Update Record"):
                    new_p = p_row["Paid_Amount"] + add_cash
                    new_r = p_row["Total_Bill"] - new_p
                    df.loc[df["ID"] == p_row["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_p, new_r, ("Paid" if new_r<=0 else "Pending"), res_val]
                    conn.update(worksheet="data_db", data=df)
                    st.success("Cloud Updated!")
                    st.rerun()
            else: st.write("No pending dues.")

    # 4. EXPENSE MANAGER
    elif menu == "💸 Expense Manager":
        st.header("💸 Lab Expenses")
        ex_cat = st.selectbox("Category", ["Salary", "Rent", "Chemicals", "Tea/Food", "Other"])
        ex_desc = st.text_input("Description")
        ex_amt = st.number_input("Amount", 0)
        if st.button("Save Expense"):
            save_expense_gsheet(pd.DataFrame([[today, ex_cat, ex_desc, ex_amt]], columns=["Date", "Category", "Description", "Amount"]))
            st.success("Expense Saved!")

    # 5. HISTORY SEARCH
    elif menu == "🔍 History Search":
        st.header("🔍 Search Patient History")
        s_q = st.text_input("Enter Name, Mobile or Invoice #")
        if s_q:
            res = df[df.apply(lambda r: r.astype(str).str.contains(s_q, case=False).any(), axis=1)]
            st.dataframe(res, use_container_width=True)

    # 6. EXCEL HISTORY
    elif menu == "📊 Excel History":
        st.header("📊 Full Database")
        st.dataframe(df, use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "History.csv")

    # 7. SETTINGS
    elif menu == "⚙️ Lab Settings":
        st.header("⚙️ Settings")
        st.session_state.lab_name = st.text_input("Lab Name", st.session_state.lab_name)
        st.session_state.lab_phone = st.text_input("Lab Contact", st.session_state.lab_phone)
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()
