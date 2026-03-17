import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css
from receipt_design import show_receipt
# --- GOOGLE SHEETS IMPORT ---
from streamlit_gsheets import GSheetsConnection
# --- PDF GENERATION ---
from fpdf import FPDF
import base64

# --- 1. CONNECTION CONFIG ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SMART TEST DATABASE ---
# Is list mein aap mazeed tests aur unki details add kar sakte hain
TEST_COMPONENTS = {
    "CBC": [
        {"name": "Hemoglobin (Hb)", "range": "13.0 - 17.0", "unit": "g/dL"},
        {"name": "RBC Count", "range": "4.5 - 5.5", "unit": "mill/cmm"},
        {"name": "WBC Count", "range": "4,000 - 10,000", "unit": "/cmm"},
        {"name": "Platelets", "range": "150,000 - 450,000", "unit": "/cmm"},
        {"name": "HCT / PCV", "range": "40 - 50", "unit": "%"},
        {"name": "MCV", "range": "80 - 100", "unit": "fL"},
        {"name": "MCH", "range": "27 - 32", "unit": "pg"}
    ],
    "SUGAR": [
        {"name": "Fasting Glucose", "range": "70 - 110", "unit": "mg/dL"},
        {"name": "Random Glucose", "range": "80 - 140", "unit": "mg/dL"}
    ],
    "LIPID PROFILE": [
        {"name": "Total Cholesterol", "range": "< 200", "unit": "mg/dL"},
        {"name": "Triglycerides", "range": "< 150", "unit": "mg/dL"}
    ]
}

# --- 2. DATA FETCH FUNCTIONS ---
def get_test_master_data():
    try:
        return conn.read(worksheet="master_tests_db", ttl="0")
    except:
        return pd.DataFrame(columns=["Test_Name", "Normal_Range", "Unit"])

def get_full_data():
    try:
        return conn.read(worksheet="data_db", ttl="0")
    except:
        cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    try:
        df = conn.read(worksheet="tests_db", ttl="0")
        if not df.empty:
            df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame([{"Test_Name": "CBC", "Rate": 500}, {"Test_Name": "Sugar", "Rate": 200}])

def get_expense_data():
    try:
        df = conn.read(worksheet="expenses_db", ttl="0")
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except:
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# --- 3. PROFESSIONAL REPORT GENERATOR (PDF) ---
def generate_professional_report(p_data, results_list):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(20, 80, 160)
    pdf.cell(0, 10, str(st.session_state.lab_name), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, "MAJEED COLONY SEC 2, KARACHI | " + str(st.session_state.lab_phone), ln=True, align='C')
    pdf.line(10, 32, 200, 32)
    
    # Patient Info Table
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Patient Name:", 0)
    pdf.set_font("Arial", '', 10)
    pdf.cell(70, 7, f"{p_data['Name']}", 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Date:", 0)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 7, f"{p_data['Date']}", 0, 1)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Age / Gender:", 0)
    pdf.set_font("Arial", '', 10)
    pdf.cell(70, 7, f"{p_data['Age']} / {p_data['Gender']}", 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Invoice #:", 0)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 7, f"{p_data['Invoice']}", 0, 1)
    
    pdf.line(10, 55, 200, 55)
    pdf.ln(10)

    # Table Header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 10, " TEST DESCRIPTION", 1, 0, 'L', True)
    pdf.cell(40, 10, " RESULT", 1, 0, 'C', True)
    pdf.cell(40, 10, " UNIT", 1, 0, 'C', True)
    pdf.cell(40, 10, " NORMAL RANGE", 1, 1, 'C', True)
    
    # Results Row
    pdf.set_font("Arial", '', 10)
    for res in results_list:
        pdf.cell(70, 9, f" {res['name']}", 1)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 9, f" {res['val']}", 1, 0, 'C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(40, 9, f" {res['unit']}", 1, 0, 'C')
        pdf.cell(40, 9, f" {res['range']}", 1, 1, 'C')
        
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 9)
    pdf.cell(0, 5, "Note: This is a computer generated report.", ln=True, align='C')
    pdf.cell(0, 5, "Powered by BioCloud Pro", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SAVE FUNCTIONS ---
def save_record_local(new_row_df):
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    conn.update(worksheet="data_db", data=updated_data)

def save_test_local(new_test_df):
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    conn.update(worksheet="tests_db", data=updated_tests)

# --- 5. PAGE CONFIG & UI ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'temp_tests' not in st.session_state: st.session_state.temp_tests = []
if 'lab_name' not in st.session_state: st.session_state.lab_name = "THE LIFE CARE CLINIC & LAB"
if 'lab_phone' not in st.session_state: st.session_state.lab_phone = "0370-2926075"

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
    today_dt = datetime.now().date()
    today = str(today_dt)

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("Navigation", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "🧪 Test Master", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    if menu == "🏠 Home":
        st.markdown(f"## Welcome to {st.session_state.lab_name}")
        c1, c2, c3, c4 = st.columns(4)
        total_p = len(df[df['Date'] == today]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0
        with c1: st.metric("Today's Patients", total_p)
        with c2: st.metric("Today's Cash", f"Rs. {total_cash}")
        with c3: st.metric("Total Pending", pending_p)
        with c4: st.metric("System", "Cloud Active ✅")

    elif menu == "📝 Registration":
        st.header("Patient Registration")
        tdf = get_tests_list()
        test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
        test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"]))

        with st.container(border=True):
            r1c1, r1c2, r1c3 = st.columns([2, 1, 1])
            p_name = r1c1.text_input("Patient Name")
            p_mobile = r1c2.text_input("Mobile No")
            p_inv = r1c3.text_input("Invoice #", value=f"INV-{len(df)+101}")
            
            r2c1, r2c2, r2c3 = st.columns(3)
            p_age = r2c1.number_input("Age", 1, 120, 25)
            p_gender = r2c2.selectbox("Gender", ["Male", "Female", "Other"])
            p_ref = r2c3.text_input("Ref By", "Self")

        st.subheader("Add Tests")
        t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
        sel_t = t_col1.selectbox("Select Test", ["-- Select --"] + test_options)
        rate_t = t_col2.number_input("Price", value=float(test_rate_dict.get(sel_t, 0)))
        if t_col3.button("➕ Add"):
            if sel_t != "-- Select --":
                st.session_state.temp_tests.append({"Test": sel_t, "Rate": rate_t})
                st.rerun()

        if st.session_state.temp_tests:
            total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
            st.write(f"**Total Bill: Rs. {total_bill}**")
            paid = st.number_input("Paid Amount", 0, int(total_bill))
            if st.button("💾 Save & Print Receipt", use_container_width=True):
                all_tests = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                new_data = [len(df)+1, p_inv, today, p_name, p_mobile, p_age, p_gender, "Lab", all_tests, total_bill, paid, total_bill-paid, "-", "-", ("Paid" if (total_bill-paid)<=0 else "Pending")]
                save_record_local(pd.DataFrame([new_data], columns=df.columns))
                st.session_state.temp_tests = []
                st.success("Record Saved!")
                st.rerun()

    elif menu == "💰 Dues & Reports":
        st.header("Update Records & Results")
        pending_df = df[df["Status"] == "Pending"]
        if not pending_df.empty:
            sel_p = st.selectbox("Select Pending Patient", pending_df["Name"].tolist())
            p_data = df[df["Name"] == sel_p].iloc[-1]
            
            results_entry = []
            booked_tests = p_data['Test'].split(", ")
            
            for bt in booked_tests:
                st.info(f"Test: {bt}")
                if bt.upper() in TEST_COMPONENTS:
                    for comp in TEST_COMPONENTS[bt.upper()]:
                        c1, c2, c3 = st.columns([3, 2, 2])
                        val = c1.text_input(f"{comp['name']}", key=f"{p_data['ID']}_{comp['name']}")
                        c2.caption(f"Range: {comp['range']}")
                        results_entry.append({"name": comp['name'], "val": val, "range": comp['range'], "unit": comp['unit']})
                else:
                    val = st.text_input(f"Result for {bt}", key=f"{p_data['ID']}_{bt}")
                    results_entry.append({"name": bt, "val": val, "range": "-", "unit": "-"})

            if st.button("Generate Final PDF Report"):
                report_pdf = generate_professional_report(p_data, results_entry)
                st.download_button("📥 Download Report", data=report_pdf, file_name=f"Report_{p_data['Name']}.pdf")
        else:
            st.info("No Pending Records.")

    elif menu == "📊 Excel History":
        st.header("Lab History")
        st.dataframe(df, use_container_width=True)
        st.download_button("Export CSV", df.to_csv(index=False), "history.csv")

    elif menu == "⚙️ Lab Settings":
        st.header("Settings")
        st.session_state.lab_name = st.text_input("Lab Name", st.session_state.lab_name)
        st.session_state.lab_phone = st.text_input("Lab Contact", st.session_state.lab_phone)
        st.success("Settings updated temporarily for this session.")