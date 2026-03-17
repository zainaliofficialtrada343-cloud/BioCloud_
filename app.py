import streamlit as st
import pandas as pd
from datetime import datetime
from login_ui import show_login_page, local_css
from receipt_design import show_receipt

# --- NEW IMPORTS FROM YOUR NEW FILES ---
from settings_config import LAB_DETAILS, TEST_COMPONENTS, apply_custom_style
from database_manager import (
    get_full_data, get_tests_list, get_expense_data, 
    save_patient_record, save_new_test, update_existing_record
)
from pdf_generator import generate_receipt_pdf, generate_lab_report_pdf

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- 2. STYLE & DESIGN ---
apply_custom_style() # Settings file se style apply ho raha hai
st.markdown("""
    <style>
    .main-header { background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); margin-bottom: 25px; }
    .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #4CAF50; }
    .stat-val { font-size: 24px; font-weight: bold; color: #2E7D32; }
    .stat-label { font-size: 14px; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE & LOGIN ---
if 'menu_choice' not in st.session_state: st.session_state.menu_choice = "Home"
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
    today_dt = datetime.now().date()
    today = str(today_dt)
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("Navigation", ["🏠 Home", "📝 Registration", "💰 Dues & Reports", "🧪 Test Master", "💸 Expense Manager", "🔍 History Search", "📊 Excel History", "⚙️ Lab Settings"])
        st.divider()
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    # --- HOME PAGE ---
    if menu == "🏠 Home":
        st.markdown(f"## Welcome to {LAB_DETAILS['name']}")
        st.write(f"Today's Date: {today_dt.strftime('%d %B, %Y')}")
        c1, c2, c3, c4 = st.columns(4)
        total_p = len(df[df['Date'] == today]) if not df.empty else 0
        total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
        pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0
        with c1: st.metric("Today's Patients", total_p)
        with c2: st.metric("Today's Cash", f"Rs. {total_cash}")
        with c3: st.metric("Total Pending", pending_p)
        with c4: st.metric("Lab Status", "Online ✅")

    # --- REGISTRATION PAGE ---
    elif menu == "📝 Registration":
        st.header("New Patient Registration")
        if st.session_state.show_slip:
            st.success("✅ Record Saved to Cloud!")
            # Using pdf_generator function
            pdf_bytes = generate_receipt_pdf(st.session_state.show_slip)
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
                    save_patient_record(pd.DataFrame([data_list], columns=required_cols))
                    st.session_state.show_slip = data_list 
                    st.session_state.temp_tests = [] 
                    st.rerun()

    # --- DUES & REPORTS PAGE ---
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
                    st.subheader(f"Enter Lab Values for {p_data['Name']}")
                    for bt in booked_tests:
                        if bt.upper() in TEST_COMPONENTS:
                            st.write(f"🔬 **{bt} Details**")
                            for comp in TEST_COMPONENTS[bt.upper()]:
                                c1, c2, c3 = st.columns([3, 2, 2])
                                val = c1.text_input(f"{comp['name']}", key=f"{p_data['ID']}_{comp['name']}")
                                c2.info(f"Range: {comp['range']}")
                                c3.write(f"Unit: {comp['unit']}")
                                results_entry.append({"name": comp['name'], "val": val, "range": comp['range'], "unit": comp['unit']})
                        else:
                            val = st.text_input(f"{bt} Result", key=f"{p_data['ID']}_{bt}")
                            results_entry.append({"name": bt, "val": val, "range": "-", "unit": "-"})

                add_p = st.number_input("Add More Payment (Rs.)", 0)
                
                if st.button("💾 Save Results & Generate PDF", use_container_width=True):
                    new_paid = p_data["Paid_Amount"] + add_p
                    new_rem = p_data["Total_Bill"] - new_paid
                    res_summary = ", ".join([f"{r['name']}:{r['val']}" for r in results_entry])
                    
                    df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res_summary]
                    update_existing_record(df)
                    
                    report_pdf = generate_lab_report_pdf(p_data, results_entry)
                    st.download_button("📥 Download Final Lab Report", data=report_pdf, file_name=f"Report_{p_data['Name']}.pdf", mime="application/pdf")
                    st.success("Record Updated!")
            else: st.info("Koi Pending record nahi hai.")

    # --- EXCEL HISTORY PAGE ---
    elif menu == "📊 Excel History":
        st.header("📊 Full History & Old Prints")
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            st.subheader("🖨️ Reprint Section")
            sel_p = st.selectbox("Select Patient to Reprint", df["Name"].tolist(), key="old_print")
            p_row = df[df["Name"] == sel_p].iloc[-1].tolist()
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                old_receipt = generate_receipt_pdf(p_row)
                st.download_button(f"📥 Print Receipt ({p_row[1]})", data=old_receipt, file_name=f"Receipt_{p_row[1]}.pdf")
            with col_p2:
                if p_row[12] != "-":
                    sample_res = [{"name": r.split(":")[0], "val": r.split(":")[1], "range": "-", "unit": "-"} for r in p_row[12].split(", ")]
                    p_data_dict = dict(zip(required_cols, p_row))
                    old_report = generate_lab_report_pdf(p_data_dict, sample_res)
                    st.download_button(f"📥 Print Report ({p_row[3]})", data=old_report, file_name=f"Report_{p_row[3]}.pdf")

    # --- OTHER MENUS (Logic remains same as your original) ---
    elif menu == "⚙️ Lab Settings":
        st.info(f"Current Lab: {LAB_DETAILS['name']}\n\nTo change permanent settings, edit 'settings_config.py' file.")