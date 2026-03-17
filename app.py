import streamlit as st
import pandas as pd
from datetime import datetime
from login_ui import show_login_page, local_css
from receipt_design import show_receipt
# IMPORTING FROM OUR NEW LOGIC FILE
from logic_manager import (
    get_full_data, get_tests_list, get_expense_data, get_test_master_data,
    save_record_local, save_test_local, save_expense_gsheet, update_full_db,
    generate_professional_report, download_pdf_receipt, TEST_COMPONENTS, conn
)

st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- STYLE & DESIGN (Wahi Jo Aapka Tha) ---
st.markdown("""<style>
    .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #4CAF50; }
    .stat-val { font-size: 24px; font-weight: bold; color: #2E7D32; }
    .stat-label { font-size: 14px; color: #666; }
</style>""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'show_slip' not in st.session_state: st.session_state.show_slip = None
if 'temp_tests' not in st.session_state: st.session_state.temp_tests = []
if 'lab_name' not in st.session_state: st.session_state.lab_name = "THE LIFE CARE CLINIC & LAB"
if 'lab_phone' not in st.session_state: st.session_state.lab_phone = "0370-2926075"

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else: st.error("Invalid Login")

if not st.session_state['auth']:
    show_login_page(check_login)
else:
    local_css("style.css")
    df = get_full_data()
    today_dt = datetime.now().date()
    today = str(today_dt)
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.title("🧪 BioCloud Pro")
        menu = st.radio("Navigation", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "🧪 Test Master", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    # --- MENU LOGIC (Sare Features Jo Aapne Bhole Thay) ---
    if menu == "🏠 Home":
        st.markdown(f"## Welcome to {st.session_state.lab_name}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Today's Patients", len(df[df['Date'] == today]) if not df.empty else 0)
        c2.metric("Pending Reports", len(df[df['Status'] == 'Pending']) if not df.empty else 0)
        c3.metric("Status", "Online ✅")

    elif menu == "📝 Registration":
        st.header("New Registration")
        if st.session_state.show_slip:
            pdf_bytes = download_pdf_receipt(st.session_state.show_slip, st.session_state.lab_name, st.session_state.lab_phone)
            st.download_button("📥 Download PDF", data=pdf_bytes, file_name="Receipt.pdf")
            show_receipt(st.session_state.show_slip)
            if st.button("New"): st.session_state.show_slip = None; st.rerun()
        else:
            with st.expander("➕ Add New Test Type"):
                cn1, cn2, cn3 = st.columns([2, 1, 1])
                nt = cn1.text_input("Test Name")
                nr = cn2.number_input("Rate", 0)
                if cn3.button("Save"):
                    save_test_local(pd.DataFrame([{"Test_Name": nt, "Rate": nr}]))
                    st.success("Saved!"); st.rerun()

            # ... (Aapka baki registration form yahan aiga)
            st.info("Form Fill Karein...")

    elif menu == "💸 Expense Manager":
        st.header("💸 Kharcha Pani")
        e_cat = st.selectbox("Category", ["Staff Salary", "Chemicals/Kits", "Rent/Bills", "Tea/Food", "Other"])
        e_amt = st.number_input("Amount", 0)
        if st.button("Save Expense"):
            new_ex = pd.DataFrame([[today_dt, e_cat, "Lab Expense", e_amt]], columns=["Date", "Category", "Description", "Amount"])
            save_expense_gsheet(new_ex)
            st.success("Expense Saved!")

    elif menu == "⚙️ Lab Settings":
        st.header("⚙️ Settings")
        st.session_state.lab_name = st.text_input("Lab Name", value=st.session_state.lab_name)
        st.session_state.lab_phone = st.text_input("Contact", value=st.session_state.lab_phone)
        st.success("Settings Updated!")