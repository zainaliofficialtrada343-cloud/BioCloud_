import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css

# --- 1. CSV DATABASE CONFIG ---
PATIENT_FILE = "data_db.csv"
TESTS_FILE = "tests_db.csv"

def get_full_data():
    # Adding extra columns to the structure to support new fields
    cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
    if os.path.exists(PATIENT_FILE):
        df = pd.read_csv(PATIENT_FILE)
        # Check if new columns exist, if not add them to prevent errors
        for c in cols:
            if c not in df.columns:
                df[c] = "-"
        return df
    else:
        return pd.DataFrame(columns=cols)

def get_tests_list():
    if os.path.exists(TESTS_FILE):
        return pd.read_csv(TESTS_FILE)
    else:
        return pd.DataFrame([{"Test_Name": "CBC", "Rate": 500}, {"Test_Name": "Sugar", "Rate": 200}])

def save_record_local(new_row_df):
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    updated_data.to_csv(PATIENT_FILE, index=False)

def save_test_local(new_test_df):
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    updated_tests.to_csv(TESTS_FILE, index=False)

# --- NEW: SLIP DESIGN FUNCTION ---
def show_receipt(data):
    val = data.tolist() if hasattr(data, 'tolist') else data
    # Map data to variables for clarity (adjusting index based on our cols)
    st.markdown(f"""
        <div style="background-color: white; padding: 15px; border: 1px solid #000; width: 320px; color: black; font-family: 'Arial', sans-serif; margin: auto;">
            <div style="text-align: center; font-weight: bold; font-size: 22px; margin-bottom: 2px;">🧪 THE LIFE CARE</div>
            <div style="text-align: center; font-size: 10px; margin-bottom: 10px;">Modern Diagnostic Center</div>
            
            <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                <tr><td style="border: 1px solid #ddd; padding: 3px;"><b>Inv #:</b> {val[1]}</td><td style="border: 1px solid #ddd; padding: 3px;"><b>Date:</b> {val[2]}</td></tr>
                <tr><td colspan="2" style="border: 1px solid #ddd; padding: 3px;"><b>Name:</b> {val[3]}</td></tr>
                <tr><td style="border: 1px solid #ddd; padding: 3px;"><b>Mob:</b> {val[4]}</td><td style="border: 1px solid #ddd; padding: 3px;"><b>Age/Sex:</b> {val[5]}/{val[6]}</td></tr>
                <tr><td colspan="2" style="border: 1px solid #ddd; padding: 3px;"><b>Collected From:</b> {val[7]}</td></tr>
            </table>

            <div style="font-size: 12px; font-weight: bold; margin-top: 8px; border-bottom: 1px solid black;">Tests:</div>
            <div style="font-size: 11px; padding: 5px 0;">{val[8]}</div>
            
            <hr style="margin: 5px 0; border-top: 1px dashed black;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold;">
                <span>Total:</span> <span>Rs. {val[9]}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 12px;">
                <span>Paid:</span> <span>Rs. {val[10]}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: red; font-weight: bold;">
                <span>Remaining:</span> <span>Rs. {val[11]}</span>
            </div>

            <div style="text-align: center; font-size: 10px; margin-top: 15px; border-top: 1px solid black; padding-top: 5px;">
                <b>Developed by zain 03702906075</b>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.button("🖨️ Print Receipt", key=f"prnt_{val[1]}", on_click=lambda: st.write("Browser ka Print (Ctrl+P) use karein"))

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- 3. SESSION STATE ---
if 'temp_tests' not in st.session_state:
    st.session_state.temp_tests = [] 
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'show_slip' not in st.session_state:
    st.session_state.show_slip = None

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else:
        st.error("Invalid Username or Password")

# --- 4. AUTH CHECK ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    local_css("style.css")
    
    df = get_full_data()
    today = str(datetime.now().date())
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        
        if not df.empty and 'Date' in df.columns:
            cash_df = df[df['Date'] == today]
            total_cash = pd.to_numeric(cash_df['Paid_Amount'], errors='coerce').sum()
            total_dues = pd.to_numeric(cash_df['Remaining'], errors='coerce').sum()
        else:
            total_cash, total_dues = 0, 0
            
        st.metric("Aaj Ka Cash", f"Rs. {total_cash}")
        st.metric("Aaj Ke Dues", f"Rs. {total_dues}")
        
        st.divider()
        menu = st.radio("Navigation", ["Registration", "Dues & Reports", "Excel History"])
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    if menu == "Registration":
        st.header("New Patient Registration")
        
        if st.session_state.show_slip:
            st.success("✅ Record Saved!")
            show_receipt(st.session_state.show_slip)
            if st.button("Register Another Patient"):
                st.session_state.show_slip = None
                st.rerun()
            st.divider()

        tdf = get_tests_list()
        test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
        test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}

        with st.expander("➕ Add New Test Type to System", expanded=False):
            c_n1, c_n2, c_n3 = st.columns([2, 1, 1])
            new_t_name = c_n1.text_input("New Test Name")
            new_t_rate = c_n2.number_input("Standard Rate", 0)
            if c_n3.button("Save New Test"):
                if new_t_name:
                    save_test_local(pd.DataFrame([{"Test_Name": new_t_name, "Rate": new_t_rate}]))
                    st.success(f"Test '{new_t_name}' Added!")
                    st.rerun()

        with st.expander("Patient Information", expanded=True):
            r1c1, r1c2, r1c3 = st.columns([2, 1, 1])
            p_name = r1c1.text_input("Patient Name")
            p_mobile = r1c2.text_input("Mobile No")
            p_inv = r1c3.text_input("Invoice #", value=f"INV-{datetime.now().strftime('%H%M%S')}")
            
            r2c1, r2c2, r2c3 = st.columns([1, 1, 2])
            p_age = r2c1.number_input("Age", 1, 120, value=25)
            p_gender = r2c2.selectbox("Gender", ["Male", "Female", "Other"])
            p_coll = r2c3.text_input("Collected From", value="Lab")

        st.subheader("Add Tests to Bill")
        col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
        selected_t = col_t1.selectbox("Select Test", ["--- Select ---"] + test_options)
        default_rate = int(test_rate_dict.get(selected_t, 0)) if selected_t != "--- Select ---" else 0
        entered_rate = col_t2.number_input("Rate (Rs.)", value=default_rate, key="rate_input")

        if col_t3.button("➕ Add Test"):
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
            
            paid_amt = st.number_input("Paid Amount", 0)
            if st.button("💾 Final Save Record", use_container_width=True):
                if p_name and st.session_state.temp_tests:
                    all_tests_str = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                    rem = total_bill - paid_amt
                    new_id = len(df) + 1
                    new_row = [new_id, p_inv, today, p_name, p_mobile, p_age, p_gender, p_coll, all_tests_str, total_bill, paid_amt, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                    
                    save_record_local(pd.DataFrame([new_row], columns=required_cols))
                    st.session_state.show_slip = new_row 
                    st.session_state.temp_tests = [] 
                    st.rerun()

    elif menu == "Dues & Reports":
        st.header("Update Records & Results")
        if not df.empty:
            pending_df = df[(df["Remaining"] > 0) | (df["Result"] == "-")]
            if not pending_df.empty:
                st.markdown('<div class="login-card">', unsafe_allow_html=True)
                sel_patient = st.selectbox("Search Patient", pending_df["Name"].tolist())
                p_data = df[df["Name"] == sel_patient].iloc[-1]
                
                st.info(f"Test: {p_data['Test']} | Total Bill: {p_data['Total_Bill']} | Already Paid: {p_data['Paid_Amount']}")
                st.warning(f"Remaining Dues: Rs. {p_data['Remaining']}")
                
                c_a, c_b = st.columns(2)
                add_p = c_a.number_input("Add More Payment", 0)
                res_v = c_b.text_input("Enter Result", value=p_data['Result'])
                
                if st.button("Update & Save Record"):
                    new_paid = p_data["Paid_Amount"] + add_p
                    new_rem = p_data["Total_Bill"] - new_paid
                    df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res_v]
                    df.to_csv(PATIENT_FILE, index=False)
                    st.success("Updated Successfully!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.success("No pending records found!")

    elif menu == "Excel History":
        st.header("📊 Lab Database History")
        
        with st.expander("🖨️ Reprint Old Receipt", expanded=False):
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            if not df.empty:
                patient_list = df["Name"].tolist()
                selected_for_print = st.selectbox("Select Patient to Reprint Slip", ["-- Select --"] + patient_list)
                if selected_for_print != "-- Select --":
                    p_to_print = df[df["Name"] == selected_for_print].iloc[-1]
                    show_receipt(p_to_print)
            else:
                st.write("No data available.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.divider()
        
        search_query = st.text_input("🔍 Search History (Name, ID, Date, or Test)")
        if search_query:
            filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)