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

# --- 1. GOOGLE SHEETS CONNECTION CONFIG ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- NEW: PDF GENERATION FUNCTION (DOES NOT CHANGE DESIGN) ---
def download_pdf_receipt(v, lab_phone):
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, "THE LIFE CARE", ln=True, align='C')
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
    /* Global Styles */
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 25px;
    }
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
    
    @media print {
        @page { size: auto; margin: 5mm; }
        .stApp { background: white !important; }
        .no-print { display: none !important; }
        #receipt-container { 
            width: 100% !important; 
            box-shadow: none !important; 
            margin: 0 !important; 
            padding: 0 !important; 
            background-color: white !important;
            text-rendering: optimizeLegibility !important;
            -webkit-font-smoothing: antialiased !important;
            image-rendering: -webkit-optimize-contrast !important;
        }
        h1, h2, h3, p, td, span, b, div { 
            color: #000000 !important; 
            font-family: 'Helvetica', 'Arial', sans-serif !important;
            letter-spacing: 0.2px !important;
            font-weight: 500 !important;
        }
        header, footer, .stSidebar, .stActionButton { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. SESSION STATE & LOGIN ---
if 'menu_choice' not in st.session_state: st.session_state.menu_choice = "Home"
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
    local_css("style.css")
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), url("https://raw.githubusercontent.com/zainaliofficialtrada343-cloud/BioCloud_/main/lab_girl.jpg"); background-size: cover; background-position: center; background-attachment: fixed; }</style>""", unsafe_allow_html=True)

    df = get_full_data()
    today_dt = datetime.now().date()
    today = str(today_dt)
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("Navigation", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        st.divider()
        if st.checkbox("Enable Delete Option"):
            if st.button("⚠️ Delete All Patient Data", type="primary"):
                empty_df = pd.DataFrame(columns=required_cols)
                conn.update(worksheet="data_db", data=empty_df)
                st.success("Google Sheet Clear Ho Gayi!")
                st.rerun()
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    if menu == "🏠 Home":
        st.markdown(f"## Welcome to {st.session_state.lab_name}")
        st.write(f"Today's Date: {today_dt.strftime('%d %B, %Y')}")
        c1, c2, c3, c4 = st.columns(4)
        total_p = len(df[df['Date'] == today]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0
        with c1: st.metric("Today's Patients", total_p)
        with c2: st.metric("Today's Cash", f"Rs. {total_cash}")
        with c3: st.metric("Total Pending", pending_p)
        with c4: st.metric("Lab Status", "Online ✅")

    elif menu == "📝 Registration":
        st.header("New Patient Registration")
        if st.session_state.show_slip:
            st.success("✅ Record Saved to Cloud!")
            # --- ADDED PDF DOWNLOAD OPTION ---
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

        with st.expander("➕ Add New Test Type"):
            c_n1, c_n2, c_n3 = st.columns([2, 1, 1])
            new_t_name = c_n1.text_input("New Test Name")
            new_t_rate = c_n2.number_input("Standard Rate", 0)
            if c_n3.button("Save New Test"):
                if new_t_name:
                    save_test_local(pd.DataFrame([{"Test_Name": new_t_name, "Rate": new_t_rate}]))
                    st.success("Test Saved to Cloud!")
                    st.rerun()

        with st.expander("Patient Information", expanded=True):
            r1c1, r1c2, r1c3 = st.columns([2, 1, 1])
            p_name = r1c1.text_input("Patient Name")
            p_mobile = r1c2.text_input("Mobile No", value=st.session_state.saved_mobile)
            st.session_state.saved_mobile = p_mobile
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
        entered_rate = col_t2.number_input("Rate (Rs.)", value=float(default_rate), key="rate_input")

        if col_t3.button("➕ Add Test"):
            if selected_t != "--- Select ---":
                st.session_state.temp_tests.append({"Test": selected_t, "Rate": entered_rate})
                st.rerun()

        if st.session_state.temp_tests:
            st.markdown("### Selected Tests")
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
                    data_list = [new_id, p_inv, today, p_name, p_mobile, p_age, p_gender, p_coll, all_tests_str, total_bill, paid_amt, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
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
                st.info(f"Test: {p_data['Test']} | Dues: Rs. {p_data['Remaining']}")
                c_a, c_b = st.columns(2)
                add_p = c_a.number_input("Add More Payment", 0)
                res_v = c_b.text_input("Enter Result", value=p_data['Result'])
                if st.button("Update & Save Record"):
                    new_paid = p_data["Paid_Amount"] + add_p
                    new_rem = p_data["Total_Bill"] - new_paid
                    df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res_v]
                    conn.update(worksheet="data_db", data=df)
                    st.success("Cloud Updated!")
                    st.rerun()
            else: st.info("Koi Pending record nahi hai.")

    elif menu == "💸 Expense Manager":
        st.header("💸 Kharcha Pani (Cloud Backup)")
        ex_df = get_expense_data()
        tab1, tab2 = st.tabs(["➕ Add Expense", "📊 Expense Reports"])
        with tab1:
            with st.expander("Enter New Expense Details", expanded=True):
                e_cat = st.selectbox("Category", ["Staff Salary", "Chemicals/Kits", "Rent/Bills", "Tea/Food", "Other"])
                e_desc = st.text_input("Description")
                e_amt = st.number_input("Amount", 0)
                if st.button("Save Expense"):
                    new_ex = pd.DataFrame([[today_dt, e_cat, e_desc, e_amt]], columns=["Date", "Category", "Description", "Amount"])
                    save_expense_gsheet(new_ex)
                    st.success("Expense Saved to Sheet!")
                    st.rerun()
        with tab2:
            st.subheader("Filter Expenses")
            f_col1, f_col2 = st.columns(2)
            view_type = f_col1.selectbox("View By", ["Daily", "Monthly", "Yearly", "All Time"])
            if not ex_df.empty:
                ex_df['Date'] = pd.to_datetime(ex_df['Date']).dt.date
                if view_type == "Daily": filtered_ex = ex_df[ex_df['Date'] == today_dt]
                elif view_type == "Monthly": filtered_ex = ex_df[pd.to_datetime(ex_df['Date']).dt.month == today_dt.month]
                elif view_type == "Yearly": filtered_ex = ex_df[pd.to_datetime(ex_df['Date']).dt.year == today_dt.year]
                else: filtered_ex = ex_df
                total_ex = filtered_ex['Amount'].sum()
                st.markdown(f"### Total Expense ({view_type}): **Rs. {total_ex}**")
                st.dataframe(filtered_ex, use_container_width=True)
                if st.button("🗑️ Clear Expense History"):
                    empty_ex = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
                    conn.update(worksheet="expenses_db", data=empty_ex)
                    st.rerun()

    elif menu == "🔍 History Search":
        st.header("🔍 Advanced Patient Search")
        search_query = st.text_input("Search by Name, Mobile, ID or Invoice #")
        if search_query:
            hist = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            if not hist.empty:
                st.write(f"Found {len(hist)} records:")
                st.dataframe(hist, use_container_width=True)
            else: st.warning("No record found.")

    elif menu == "📊 Excel History":
        st.header("📊 Lab Database History")
        if not df.empty:
            st.subheader("Filter Data")
            ex_search = st.text_input("Search anything in table...", key="ex_search")
            display_df = df[df.apply(lambda row: row.astype(str).str.contains(ex_search, case=False).any(), axis=1)] if ex_search else df
            st.dataframe(display_df, use_container_width=True)
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Filtered History", data=csv, file_name="BioCloud_History.csv", mime="text/csv")
        else: st.info("No data found in database.")
        st.divider()
        with st.expander("🖨️ Reprint Old Slip", expanded=True):
            if not df.empty:
                reprint_term = st.text_input("Reprint Search (Name/Mobile/Inv)")
                if reprint_term:
                    filtered_search = df[df.apply(lambda row: row.astype(str).str.contains(reprint_term, case=False).any(), axis=1)]
                    if not filtered_search.empty:
                        options = filtered_search.apply(lambda x: f"{x['Name']} | {x['Invoice']} | {x['Date']}", axis=1).tolist()
                        selected_option = st.selectbox("Select Patient to Print", ["-- Select --"] + options)
                        if selected_option != "-- Select --":
                            idx = options.index(selected_option)
                            p_to_print = filtered_search.iloc[idx]
                            # Reprint PDF Option
                            pdf_rep = download_pdf_receipt(p_to_print.tolist(), st.session_state.lab_phone)
                            st.download_button(label="📥 Reprint HD PDF", data=pdf_rep, file_name=f"Reprint_{p_to_print['Invoice']}.pdf", mime="application/pdf")
                            show_receipt(p_to_print.tolist())

    elif menu == "⚙️ Lab Settings":
        st.header("⚙️ Lab System Settings")
        st.subheader("💰 Cash & Profit")
        ex_df = get_expense_data()
        today_ex = find_today_ex = ex_df[ex_df['Date'] == today_dt]['Amount'].sum() if not ex_df.empty else 0
        if not df.empty:
            cash_df = df[df['Date'] == today]
            total_cash = pd.to_numeric(cash_df['Paid_Amount'], errors='coerce').sum()
            total_dues = pd.to_numeric(cash_df['Remaining'], errors='coerce').sum()
            net_profit = total_cash - today_ex
        else: total_cash, total_dues, net_profit = 0, 0, 0
        stat_c1, stat_c2, stat_c3 = st.columns(3)
        stat_c1.metric("Kul Cash", f"Rs. {total_cash}")
        stat_c2.metric("Aaj Ka Kharcha", f"Rs. {today_ex}")
        stat_c3.metric("Net Profit", f"Rs. {net_profit}")
        st.divider()
        st.subheader("📍 Lab Info")
        c1, c2 = st.columns(2)
        st.session_state.lab_name = c1.text_input("Lab Name", value=st.session_state.lab_name)
        st.session_state.lab_phone = c2.text_input("Contact", value=st.session_state.lab_phone)