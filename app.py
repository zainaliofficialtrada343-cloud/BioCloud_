import database_helper as db
import streamlit as st
import pandas as pd
from datetime import datetime
from login_ui import show_login_page, local_css

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- 2. SESSION STATE ---
if 'temp_tests' not in st.session_state:
    st.session_state.temp_tests = [] 
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else:
        st.error("Invalid Username or Password")

# --- 3. AUTH CHECK ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    local_css("style.css")
    
    # --- ONLINE DATA LOAD ---
    # Ab hum CSV se nahi, seedha Google Sheets se data uthayenge
    df = db.get_full_data()
    today = str(datetime.now().date())
    required_cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        
        # Aaj ka cash calculation (Online Data se)
        cash_df = df[df['Date'] == today]
        total_cash = pd.to_numeric(cash_df['Paid_Amount'], errors='coerce').sum()
        total_dues = pd.to_numeric(cash_df['Remaining'], errors='coerce').sum()
        
        st.metric("Aaj Ka Cash (Received)", f"Rs. {total_cash}")
        st.metric("Aaj Ke Dues (Pending)", f"Rs. {total_dues}")
        
        st.divider()
        menu = st.radio("Navigation", ["Registration", "Dues & Reports", "Excel History"])
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    # --- SECTION 1: REGISTRATION ---
    if menu == "Registration":
        st.header("New Patient Registration")
        
        # Tests ki list Sheet2 se uthayen
        tdf = db.get_tests_list()
        test_options = sorted(tdf["Test_Name"].unique().tolist())
        test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"]))

        with st.expander("➕ Add New Test Type to System", expanded=False):
            c_n1, c_n2, c_n3 = st.columns([2, 1, 1])
            new_t_name = c_n1.text_input("New Test Name")
            new_t_rate = c_n2.number_input("Standard Rate", 0, key="new_rate_input")
            if c_n3.button("Save New Test"):
                if new_t_name:
                    # Online save karein Sheet2 mein
                    new_test_df = pd.DataFrame([{"Test_Name": new_t_name, "Rate": new_t_rate}])
                    db.save_test_online(new_test_df)
                    st.success(f"Test '{new_t_name}' Added Online!")
                    st.rerun()

        with st.expander("Patient Information", expanded=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            p_name = c1.text_input("Patient Name")
            p_age = c2.number_input("Age", 1, 120, value=25)
            p_gender = c3.selectbox("Gender", ["Male", "Female", "Other"])

        st.subheader("Add Tests to Bill")
        col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
        selected_t = col_t1.selectbox("Select Test", ["--- Select ---"] + test_options)
        default_rate = int(test_rate_dict.get(selected_t, 0)) if selected_t != "--- Select ---" else 0
        entered_rate = col_t2.number_input("Rate (Rs.)", value=default_rate, key="entered_rate_input")

        if col_t3.button("➕ Add Test to List"):
            if selected_t != "--- Select ---":
                st.session_state.temp_tests.append({"Test": selected_t, "Rate": entered_rate})
                st.rerun()

        if st.session_state.temp_tests:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
            for i, t in enumerate(st.session_state.temp_tests):
                st.write(f"{i+1}. ✅ {t['Test']} --- Rs. {t['Rate']}")
            st.divider()
            st.write(f"**Total Bill: Rs. {total_bill}**")
            st.markdown('</div>', unsafe_allow_html=True)

            paid_amt = st.number_input("Paid Amount", 0, key="paid_amt_input")
            if st.button("💾 Final Save Record", use_container_width=True):
                if p_name and st.session_state.temp_tests:
                    all_tests_str = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                    rem = total_bill - paid_amt
                    new_id = len(df) + 1
                    
                    new_row = [new_id, today, p_name, p_age, p_gender, all_tests_str, total_bill, paid_amt, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                    
                    # Online save karein Sheet1 mein
                    db.save_record_online(pd.DataFrame([new_row], columns=required_cols))
                    
                    st.session_state.temp_tests = [] 
                    st.success("Record Saved Online to Google Sheet!")
                    st.rerun()
                else:
                    st.error("Please enter Name and add at least one test.")

    # --- SECTION 2: DUES & REPORTS (Online Update) ---
    elif menu == "Dues & Reports":
        st.header("Update Records & Results")
        # Online data se pending patients uthayen
        pending_df = df[(df["Remaining"] > 0) | (df["Result"] == "-")]
        
        if not pending_df.empty:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            sel_patient = st.selectbox("Search Patient to Update", pending_df["Name"].tolist())
            p_data = df[df["Name"] == sel_patient].iloc[-1]
            
            st.info(f"Tests: {p_data['Test']} | Total Bill: {p_data['Total_Bill']} | Already Paid: {p_data['Paid_Amount']}")
            st.warning(f"Remaining Dues: Rs. {p_data['Remaining']}")
            
            c_a, c_b = st.columns(2)
            add_p = c_a.number_input("Add More Payment (Rs.)", 0)
            res_v = c_b.text_input("Enter Test Result", value=p_data['Result'])
            
            if st.button("Update & Save Online"):
                new_paid = p_data["Paid_Amount"] + add_p
                new_rem = p_data["Total_Bill"] - new_paid
                
                # Naya data prepare karein
                df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res_v]
                
                # Poora updated data online bhej dein
                from database_helper import conn
                conn.update(worksheet="Sheet1", data=df)
                
                st.success("Record Updated Online Successfully!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No pending dues or reports found!")

    # --- SECTION 3: EXCEL HISTORY ---
    elif menu == "Excel History":
        st.header("📊 Full Lab Database (Online)")
        search_query = st.text_input("🔍 Search History (Name, ID, Date, or Test)")
        
        if search_query:
            filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)