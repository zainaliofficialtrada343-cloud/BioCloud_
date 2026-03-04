import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css

# --- 1. CSV DATABASE CONFIG ---
PATIENT_FILE = "data_db.csv"
TESTS_FILE = "tests_db.csv"

def get_full_data():
    cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
    if os.path.exists(PATIENT_FILE):
        df = pd.read_csv(PATIENT_FILE)
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

# --- 2. YOUR NEW "THA LIFE CARE" DESIGN ---
def show_receipt(val):
    # val order: [ID, Invoice, Date, Name, Mobile, Age, Gender, Collected, Test, Total_Bill, Paid_Amount, Remaining, Result, Unit, Status]
    
    st.markdown("""
        <style>
        .slip-container {
            width: 450px; background: white; padding: 25px; color: black;
            border: 1px solid #ddd; font-family: 'Segoe UI', Arial, sans-serif; margin: auto;
        }
        .header { text-align: center; }
        .header h1 { font-size: 28px; font-weight: 900; text-transform: uppercase; margin: 0; }
        .header p { font-size: 14px; font-weight: bold; margin: 2px 0; }
        .title-bar {
            border-top: 3px solid black; border-bottom: 3px solid black;
            text-align: center; margin: 15px 0; padding: 5px 0;
        }
        .title-bar h2 { font-size: 20px; letter-spacing: 2px; font-weight: bold; margin: 0; }
        .info-table { width: 100%; font-size: 16px; margin-bottom: 10px; border-collapse: collapse; }
        .dotted-line { border-top: 2px dotted black; margin: 10px 0; }
        .charges-table { width: 100%; border-collapse: collapse; }
        .charges-table th { border-bottom: 2px solid black; text-align: left; padding: 5px 0; font-size: 16px; }
        .charges-table td { padding: 8px 0; font-size: 16px; }
        .summary-section { margin-top: 15px; border-top: 3px solid black; }
        .summary-row { display: flex; justify-content: space-between; font-weight: bold; font-size: 18px; padding: 5px 0; }
        
        @media print {
            header, footer, .stSidebar, .stButton, [data-testid="stExpander"] { display: none !important; }
            .slip-container { border: none; width: 100%; box-shadow: none; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Test rows creation
    tests = str(val[8]).split(", ")
    test_rows = ""
    for i, t in enumerate(tests, 1):
        test_rows += f"<tr><td>{i}</td><td>{t}</td><td>-</td><td>1</td><td style='text-align: right;'>-</td></tr>"

    slip_html = f"""
    <div class="slip-container">
        <div class="header">
            <h1>( THA LIFE CARE )</h1>
            <p>MAJEED COLONY SEC 2</p>
        </div>
        <div class="title-bar"><h2>PATIENT SLIP</h2></div>
        <table class="info-table">
            <tr>
                <td>Slip No: <b>{val[1]}</b></td>
                <td style="text-align: right;"><b>{val[2]}</b></td>
            </tr>
            <tr><td>Shift: <b>Evening</b></td></tr>
        </table>
        <div class="dotted-line"></div>
        <table class="info-table">
            <tr><td>Patient:</td><td style="text-align: right;"><b>{val[3]}</b></td></tr>
            <tr><td>Cell/Gen/Age:</td><td style="text-align: right;"><b>{val[4]} / ({val[6]}/{val[5]})</b></td></tr>
            <tr><td>Ref By:</td><td style="text-align: right;"><b>SELF</b></td></tr>
            <tr><td>Doctor:</td><td style="text-align: right;"><b>DR. ZAIN</b></td></tr>
        </table>
        <table class="charges-table">
            <thead>
                <tr><th>S#</th><th>CHARGES</th><th>Rate</th><th>Qty</th><th style="text-align: right;">AMT</th></tr>
            </thead>
            <tbody>
                {test_rows}
            </tbody>
        </table>
        <div class="summary-section">
            <div class="summary-row"><span>TOTAL:</span><span>{val[9]}</span></div>
            <div class="summary-row" style="font-size: 16px; border-top: 2px dotted black;">
                <span>RECEIVED:</span><span>{val[10]}</span>
            </div>
            <div class="summary-row" style="border-top: 2px dotted black;">
                <span>BALANCE:</span><span>{val[11]}</span>
            </div>
        </div>
        <div style="text-align: center; margin-top: 20px; font-size: 12px; font-weight: bold; border-top: 1px solid #ccc; padding-top: 5px;">
            Developed by zain 03702906075
        </div>
    </div>
    """
    st.markdown(slip_html, unsafe_allow_html=True)
    if st.button("🖨️ Print Now", key=f"print_{val[1]}"):
        st.info("Keyboard se **Ctrl + P** dabayein.")

# --- 3. MAIN APP LOGIC (NO CHANGES) ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

if 'temp_tests' not in st.session_state: st.session_state.temp_tests = [] 
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'show_slip' not in st.session_state: st.session_state.show_slip = None
if 'saved_mobile' not in st.session_state: st.session_state.saved_mobile = ""

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else: st.error("Invalid Username or Password")

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
        else: total_cash, total_dues = 0, 0
        st.metric("Aaj Ka Cash", f"Rs. {total_cash}")
        st.metric("Aaj Ke Dues", f"Rs. {total_dues}")
        st.divider()
        menu = st.radio("Navigation", ["Registration", "Dues & Reports", "Excel History"])
        
        st.divider()
        if st.checkbox("Enable Delete Option"):
            if st.button("⚠️ Delete All Patient Data", type="primary"):
                if os.path.exists(PATIENT_FILE):
                    os.remove(PATIENT_FILE)
                    st.success("Sabh data delete ho gaya!")
                    st.rerun()

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

        with st.expander("➕ Add New Test Type"):
            c_n1, c_n2, c_n3 = st.columns([2, 1, 1])
            new_t_name = c_n1.text_input("New Test Name")
            new_t_rate = c_n2.number_input("Standard Rate", 0)
            if c_n3.button("Save New Test"):
                if new_t_name:
                    save_test_local(pd.DataFrame([{"Test_Name": new_t_name, "Rate": new_t_rate}]))
                    st.success("Test Added!")
                    st.rerun()

        with st.expander("Patient Information", expanded=True):
            r1c1, r1c2, r1c3 = st.columns([2, 1, 1])
            p_name = r1c1.text_input("Patient Name")
            p_mobile = r1c2.text_input("Mobile No", value=st.session_state.saved_mobile)
            st.session_state.saved_mobile = p_mobile
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
            total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
            for i, t in enumerate(st.session_state.temp_tests):
                st.write(f"{i+1}. ✅ {t['Test']} --- Rs. {t['Rate']}")
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
    
    # ... Baki menus (Dues & History) wese hi rahenge ...