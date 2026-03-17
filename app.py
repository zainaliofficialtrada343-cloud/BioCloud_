import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css
from receipt_design import show_receipt
# --- NEW GOOGLE SHEETS IMPORT ---
from streamlit_gsheets import GSheetsConnection
# --- ADDED FOR PDF ---
from fpdf import FPDF
import base64

# --- IMPORTING EXTERNAL SETTINGS MODULE ---
# Humne dusri file (settings_config.py) ko yahan connect kar diya hai
try:
    from settings_config import show_lab_settings
except ImportError:
    # Agar file na ho to error na aaye, bas function define kar dein
    def show_lab_settings():
        st.info("Settings module is being connected...")

# --- 1. GOOGLE SHEETS CONNECTION CONFIG ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- [NEW] SMART TEST DATABASE (Ranges ke sath) ---
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
        {"name": "Fasting Glucose", "range": "70 - 110", "unit": "mg/dL"}
    ]
}

# --- NEW: FUNCTION TO GET NORMAL RANGES ---
def get_test_master_data():
    try:
        df = conn.read(worksheet="master_tests_db", ttl="0")
        return df
    except:
        return pd.DataFrame(columns=["Test_Name", "Normal_Range", "Unit"])

# --- [NEW] PROFESSIONAL LAB REPORT GENERATOR ---
def generate_professional_report(p_data, results_list):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(20, 80, 160)
    pdf.cell(0, 10, st.session_state.lab_name, ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"MAJEED COLONY SEC 2, KARACHI | {st.session_state.lab_phone}", ln=True, align='C')
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

    # Result Table Header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 10, " TEST DESCRIPTION", 1, 0, 'L', True)
    pdf.cell(40, 10, " RESULT", 1, 0, 'C', True)
    pdf.cell(40, 10, " UNIT", 1, 0, 'C', True)
    pdf.cell(40, 10, " NORMAL RANGE", 1, 1, 'C', True)
    
    # Results
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
    pdf.cell(0, 5, f"Developed by Zain - {st.session_state.lab_phone}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- RECEIPT PDF ---
def download_pdf_receipt(v, lab_phone):
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, st.session_state.lab_name, ln=True, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.cell(0, 4, "MAJEED COLONY SEC 2, KARACHI", ln=True, align='C')
    pdf.cell(0, 4, f"Contact: {lab_phone}", ln=True, align='C')
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 6, "PATIENT RECEIPT", border=1, ln=True, align='C')
    pdf.ln(4)
    pdf.set_font("Arial", '', 8)
    pdf.cell(30, 5, f"Inv #: {v[1]}")
    pdf.cell(0, 5, f"Date: {v[2]}", align='R', ln=True)
    pdf.cell(30, 5, f"Name: {v[3]}")
    pdf.cell(0, 5, f"Age/Sex: {v[5]}/{v[6]}", align='R', ln=True)
    pdf.ln(2)
    pdf.cell(0, 5, f"Ref By: {v[7]}", ln=True)
    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(40, 6, "Test Description")
    pdf.cell(20, 6, "Rate", align='R', ln=True)
    pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    tests_list = str(v[8]).split(", ")
    total_bill = float(v[9])
    per_test_rate = total_bill / len(tests_list) if len(tests_list) > 0 else 0
    pdf.set_font("Arial", '', 8)
    for t in tests_list:
        pdf.cell(40, 6, t)
        pdf.cell(20, 6, f"{per_test_rate:.0f}", align='R', ln=True)
    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(40, 7, "TOTAL BILL:")
    pdf.cell(20, 7, f"Rs. {v[9]}", align='R', ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 7, "BALANCE:")
    pdf.cell(20, 7, f"Rs. {v[11]}", align='R', ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 7)
    pdf.cell(0, 4, "Developed by Zain - 0370-2926075", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

def get_full_data():
    try:
        df = conn.read(worksheet="data_db", ttl="0")
        return df
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

# --- 4. STYLE & DESIGN (CSS) ---
st.markdown("""
    <style>
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-bottom: 4px solid #4CAF50;
    }
    .stat-val { font-size: 24px; font-weight: bold; color: #2E7D32; }
    .stat-label { font-size: 14px; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- 5. SESSION STATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'temp_tests' not in st.session_state: st.session_state.temp_tests = [] 
if 'show_slip' not in st.session_state: st.session_state.show_slip = None
if 'lab_name' not in st.session_state: st.session_state.lab_name = "THE LIFE CARE CLINIC & LAB"
if 'lab_phone' not in st.session_state: st.session_state.lab_phone = "0370-2926075"

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else: st.error("Invalid Username or Password")

# --- MAIN APP ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    local_css("style.css")
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), url("https://raw.githubusercontent.com/zainaliofficialtrada343-cloud/BioCloud_/main/lab_girl.jpg"); background-size: cover; background-position: center; background-attachment: fixed; }</style>""", unsafe_allow_html=True)

    df = get_full_data()
    today_dt = datetime.now().date()
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("Navigation", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "🧪 Test Master", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        st.divider()
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    if menu == "🏠 Home":
        st.markdown(f"## Welcome to {st.session_state.lab_name}")
        c1, c2, c3, c4 = st.columns(4)
        total_p = len(df[df['Date'] == str(today_dt)]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == str(today_dt)]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0
        with c1: st.metric("Today's Patients", total_p)
        with c2: st.metric("Today's Cash", f"Rs. {total_cash}")
        with c3: st.metric("Total Pending", pending_p)
        with c4: st.metric("Lab Status", "Online ✅")

    elif menu == "📝 Registration":
        st.header("New Patient Registration")
        if st.session_state.show_slip:
            st.success("✅ Record Saved to Cloud!")
            pdf_bytes = download_pdf_receipt(st.session_state.show_slip, st.session_state.lab_phone)
            st.download_button(label="📥 Download HD PDF Receipt", data=pdf_bytes, file_name=f"Receipt_{st.session_state.show_slip[1]}.pdf", mime="application/pdf")
            show_receipt(st.session_state.show_slip)
            if st.button("Register Another Patient"):
                st.session_state.show_slip = None
                st.rerun()
            st.divider()

        tdf = get_tests_list()
        test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
        test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}

        with st.expander("Patient Information", expanded=True):
            r1c1, r1c2, r1c3 = st.columns([2, 1, 1])
            p_name = r1c1.text_input("Patient Name")
            p_mobile = r1c2.text_input("Mobile No")
            inv_seq = f"INV-{len(df) + 101}"
            p_inv = r1c3.text_input("Invoice #", value=inv_seq)
            r2c1, r2c2, r2c3, r2c4 = st.columns([1, 1, 1, 1])
            p_age = r2c1.number_input("Age", 1, 120, value=25)
            p_gender = r2c2.selectbox("Gender", ["Male", "Female", "Other"])
            p_ref = r2c3.text_input("Doctor / Ref By", value="Self")
            p_coll = r2c4.selectbox("Collected From", ["Lab Box", "Home", "Hospital"]) 

        st.subheader("Add Tests to Bill")
        col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
        selected_t = col_t1.selectbox("Select Test", ["--- Select ---"] + test_options)
        default_rate = test_rate_dict.get(selected_t, 0) if selected_t != "--- Select ---" else 0
        entered_rate = col_t2.number_input("Rate (Rs.)", value=float(default_rate))

        if col_t3.button("➕ Add Test"):
            if selected_t != "--- Select ---":
                st.session_state.temp_tests.append({"Test": selected_t, "Rate": entered_rate})
                st.rerun()

        if st.session_state.temp_tests:
            for i, t in enumerate(st.session_state.temp_tests):
                cols = st.columns([4, 1])
                cols[0].write(f"{i+1}. ✅ {t['Test']} --- Rs. {t['Rate']}")
                if cols[1].button("❌", key=f"del_{i}"):
                    st.session_state.temp_tests.pop(i)
                    st.rerun()
            total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
            paid_amt = st.number_input("Paid Amount", 0, max_value=int(total_bill))
            if st.button("💾 Final Save Record", use_container_width=True):
                if p_name and st.session_state.temp_tests:
                    all_tests_str = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                    rem = total_bill - paid_amt
                    new_id = len(df) + 1
                    data_list = [new_id, p_inv, str(today_dt), p_name, p_mobile, p_age, p_gender, p_ref, all_tests_str, total_bill, paid_amt, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                    save_record_local(pd.DataFrame([data_list], columns=required_cols))
                    st.session_state.show_slip = data_list 
                    st.session_state.temp_tests = [] 
                    st.rerun()

    elif menu == "💰 Dues & Reports":
        st.header("Update Records & Results")
        if not df.empty:
            pending_df = df[df["Status"] == "Pending"]
            if not pending_df.empty:
                sel_patient = st.selectbox("Search Patient", pending_df["Name"].tolist())
                p_data = df[df["Name"] == sel_patient].iloc[-1]
                
                results_entry = []
                booked_tests = p_data['Test'].split(", ")
                with st.container(border=True):
                    for bt in booked_tests:
                        if bt.upper() in TEST_COMPONENTS:
                            st.write(f"🔬 **{bt} Details**")
                            for comp in TEST_COMPONENTS[bt.upper()]:
                                c1, c2, c3 = st.columns([3, 2, 2])
                                val = c1.text_input(f"{comp['name']}", key=f"{p_data['ID']}_{comp['name']}")
                                c2.info(f"Range: {comp['range']}")
                                results_entry.append({"name": comp['name'], "val": val, "range": comp['range'], "unit": comp['unit']})
                        else:
                            c1, c2 = st.columns(2)
                            val = c1.text_input(f"{bt} Result", key=f"{p_data['ID']}_{bt}")
                            results_entry.append({"name": bt, "val": val, "range": "-", "unit": "-"})

                add_p = st.number_input("Add More Payment (Rs.)", 0)
                if st.button("💾 Save Results & Generate PDF"):
                    new_paid = p_data["Paid_Amount"] + add_p
                    new_rem = p_data["Total_Bill"] - new_paid
                    res_summary = ", ".join([f"{r['name']}:{r['val']}" for r in results_entry])
                    df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res_summary]
                    conn.update(worksheet="data_db", data=df)
                    report_pdf = generate_professional_report(p_data, results_entry)
                    st.download_button("📥 Download Final Lab Report", data=report_pdf, file_name=f"Report_{p_data['Name']}.pdf", mime="application/pdf")
                    st.success("Updated!")

    elif menu == "📊 Excel History":
        st.header("📊 Patient Transaction History")
        # Old Invoice button removed as requested
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="Lab_History.csv")

    elif menu == "⚙️ Lab Settings":
        # Ab ye section settings_config file se handle hoga
        show_lab_settings()

    # --- OTHER SECTIONS REMAIN UNCHANGED ---
    elif menu == "🧪 Test Master":
        st.header("🧪 Test Database Settings")
        master_df = get_test_master_data()
        st.dataframe(master_df, use_container_width=True)
    
    elif menu == "💸 Expense Manager":
        st.header("💸 Expense Manager")
        ex_df = get_expense_data()
        st.dataframe(ex_df, use_container_width=True)

    elif menu == "🔍 History Search":
        st.header("🔍 Search Records")
        search_query = st.text_input("Search Name/ID/Invoice")
        if search_query:
            hist = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.dataframe(hist)