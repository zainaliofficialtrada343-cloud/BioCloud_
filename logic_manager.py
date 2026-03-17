import streamlit as st
import pandas as pd
from fpdf import FPDF
from streamlit_gsheets import GSheetsConnection

# --- GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SMART TEST DATABASE ---
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

# --- DATA FETCHING FUNCTIONS ---
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

def get_test_master_data():
    try:
        return conn.read(worksheet="master_tests_db", ttl="0")
    except:
        return pd.DataFrame(columns=["Test_Name", "Normal_Range", "Unit"])

# --- SAVE FUNCTIONS ---
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

def update_full_db(df):
    conn.update(worksheet="data_db", data=df)

# --- PDF GENERATORS ---
def generate_professional_report(p_data, results_list, lab_name, lab_phone):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(20, 80, 160)
    pdf.cell(0, 10, lab_name, ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"MAJEED COLONY SEC 2, KARACHI | {lab_phone}", ln=True, align='C')
    pdf.line(10, 32, 200, 32)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Patient Name:", 0); pdf.set_font("Arial", '', 10); pdf.cell(70, 7, f"{p_data['Name']}", 0)
    pdf.set_font("Arial", 'B', 10); pdf.cell(30, 7, "Date:", 0); pdf.set_font("Arial", '', 10); pdf.cell(0, 7, f"{p_data['Date']}", 0, 1)
    pdf.line(10, 55, 200, 55); pdf.ln(10)
    pdf.set_fill_color(230, 230, 230); pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 10, " TEST DESCRIPTION", 1, 0, 'L', True)
    pdf.cell(40, 10, " RESULT", 1, 0, 'C', True)
    pdf.cell(40, 10, " UNIT", 1, 0, 'C', True)
    pdf.cell(40, 10, " NORMAL RANGE", 1, 1, 'C', True)
    pdf.set_font("Arial", '', 10)
    for res in results_list:
        pdf.cell(70, 9, f" {res['name']}", 1)
        pdf.set_font("Arial", 'B', 10); pdf.cell(40, 9, f" {res['val']}", 1, 0, 'C')
        pdf.set_font("Arial", '', 10); pdf.cell(40, 9, f" {res['unit']}", 1, 0, 'C'); pdf.cell(40, 9, f" {res['range']}", 1, 1, 'C')
    pdf.ln(20); pdf.set_font("Arial", 'I', 9)
    pdf.cell(0, 5, "Note: This is a computer generated report.", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

def download_pdf_receipt(v, lab_name, lab_phone):
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14); pdf.cell(0, 8, lab_name, ln=True, align='C')
    pdf.set_font("Arial", '', 8); pdf.cell(0, 4, "MAJEED COLONY SEC 2, KARACHI", ln=True, align='C')
    pdf.cell(0, 4, f"Contact: {lab_phone}", ln=True, align='C'); pdf.ln(2)
    pdf.set_font("Arial", 'B', 9); pdf.cell(0, 6, "PATIENT RECEIPT", border=1, ln=True, align='C'); pdf.ln(4)
    pdf.set_font("Arial", '', 8); pdf.cell(30, 5, f"Inv #: {v[1]}"); pdf.cell(0, 5, f"Date: {v[2]}", align='R', ln=True)
    pdf.cell(30, 5, f"Name: {v[3]}"); pdf.cell(0, 5, f"Age/Sex: {v[5]}/{v[6]}", align='R', ln=True)
    pdf.ln(2); pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    pdf.set_font("Arial", 'B', 8); pdf.cell(40, 6, "Test Description"); pdf.cell(20, 6, "Rate", align='R', ln=True)
    pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    tests_list = str(v[8]).split(", "); total_bill = float(v[9])
    per_test_rate = total_bill / len(tests_list) if len(tests_list) > 0 else 0
    pdf.set_font("Arial", '', 8)
    for t in tests_list:
        pdf.cell(40, 6, t); pdf.cell(20, 6, f"{per_test_rate:.0f}", align='R', ln=True)
    pdf.ln(2); pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    pdf.set_font("Arial", 'B', 9); pdf.cell(40, 7, "TOTAL BILL:"); pdf.cell(20, 7, f"Rs. {v[9]}", align='R', ln=True)
    pdf.set_font("Arial", 'B', 10); pdf.cell(40, 7, "BALANCE:"); pdf.cell(20, 7, f"Rs. {v[11]}", align='R', ln=True)
    return pdf.output(dest='S').encode('latin-1')