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
            if c not in df.columns: df[c] = "-"
        return df
    else: return pd.DataFrame(columns=cols)

def get_tests_list():
    if os.path.exists(TESTS_FILE): return pd.read_csv(TESTS_FILE)
    else: return pd.DataFrame([{"Test_Name": "CBC", "Rate": 500}, {"Test_Name": "Sugar", "Rate": 200}])

def save_record_local(new_row_df):
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    updated_data.to_csv(PATIENT_FILE, index=False)

def save_test_local(new_test_df):
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    updated_tests.to_csv(TESTS_FILE, index=False)

# --- 2. CLEAN RECEIPT FUNCTION ---
def show_receipt(val):
    v = val.tolist() if hasattr(val, 'tolist') else val
    try:
        if os.path.exists("invoice_template.html"):
            with open("invoice_template.html", "r") as f:
                template = f.read()
            
            # Test Rows Fix (Description ke niche paisa aur Amt center)
            tests_list = str(v[8]).split(", ")
            test_html = ""
            for t in tests_list:
                test_html += f"<tr><td style='padding:5px;'>{t}</td><td class='amt-center'>1</td><td style='text-align:right; padding:5px;'>-</td></tr>"

            final_invoice = template.replace("{{invoice}}", str(v[1])) \
                                   .replace("{{date}}", str(v[2])) \
                                   .replace("{{name}}", str(v[3])) \
                                   .replace("{{mobile}}", str(v[4])) \
                                   .replace("{{age}}", str(v[5])) \
                                   .replace("{{gender}}", str(v[6])) \
                                   .replace("{{test_rows}}", test_html) \
                                   .replace("{{total}}", str(v[9])) \
                                   .replace("{{paid}}", str(v[10])) \
                                   .replace("{{balance}}", str(v[11]))

            st.markdown(final_invoice, unsafe_allow_html=True)
        else: st.error("Error: 'invoice_template.html' nahi mili!")
    except Exception as e: st.error(f"Slip error: {e}")

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

# --- 4. SESSION STATE ---
if 'temp_tests' not in st.session_state: st.session_state.temp_tests = [] 
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'show_slip' not in st.session_state: st.session_state.show_slip = None
if 'saved_mobile' not in st.session_state: st.session_state.saved_mobile = ""

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else: st.error("Invalid Username or Password")

# --- 5. MAIN LOGIC ---
if not st.session_state['auth']:
    show_login_page(check_login)
else:
    local_css("style.css")
    df = get_full_data()
    today = str(datetime.now().date())
    required_cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud Pro</h1>", unsafe_allow_html=True)
        if not df.empty:
            cash_df = df[df['Date'] == today]
            total_cash = pd.to_numeric(cash_df['Paid_Amount'], errors='coerce').sum()
            total_dues = pd.to_numeric(cash_df['Remaining'], errors='coerce').sum()
            st.metric("Aaj Ka Cash", f"Rs. {total_cash}")
            st.metric("Aaj Ke Dues", f"Rs. {total_dues}")
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
        else:
            tdf = get_tests_list()
            test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
            test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}

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
            entered_rate = col_t2.number_input("Rate (Rs.)", value=int(test_rate_dict.get(selected_t, 0)) if selected_t != "--- Select ---" else 0)

            if col_t3.button("➕ Add Test"):
                if selected_t != "--- Select ---":
                    st.session_state.temp_tests.append({"Test": selected_t, "Rate": entered_rate})
                    st.rerun()

            # --- DELETE TEST LOGIC ---
            if st.session_state.temp_tests:
                st.write("---")
                for i, t in enumerate(st.session_state.temp_tests):
                    tc1, tc2 = st.columns([4, 1])
                    tc1.write(f"✅ {t['Test']} --- Rs. {t['Rate']}")
                    if tc2.button("❌", key=f"del_{i}"):
                        st.session_state.temp_tests.pop(i)
                        st.rerun()

                total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
                paid_amt = st.number_input("Paid Amount", 0)
                if st.button("💾 Final Save Record", use_container_width=True):
                    if p_name:
                        all_tests_str = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                        rem = total_bill - paid_amt
                        new_row = [len(df)+1, p_inv, today, p_name, p_mobile, p_age, p_gender, p_coll, all_tests_str, total_bill, paid_amt, rem, "-", "-", ("Paid" if rem<=0 else "Pending")]
                        save_record_local(pd.DataFrame([new_row], columns=required_cols))
                        st.session_state.show_slip = new_row 
                        st.session_state.temp_tests = [] 
                        st.rerun()

    elif menu == "Dues & Reports":
        st.header("Update Pending Records")
        if not df.empty:
            # --- ONLY PENDING FILTER ---
            pending_df = df[df["Status"] == "Pending"]
            if not pending_df.empty:
                sel_patient = st.selectbox("Search Patient", pending_df["Name"].tolist())
                p_data = df[df["Name"] == sel_patient].iloc[-1]
                st.info(f"Test: {p_data['Test']} | Dues: Rs. {p_data['Remaining']}")
                c_a, c_b = st.columns(2)
                add_p = c_a.number_input("Add Payment", 0)
                res_v = c_b.text_input("Enter Result", value=p_data['Result'])
                if st.button("Update Record"):
                    new_paid = p_data["Paid_Amount"] + add_p
                    new_rem = p_data["Total_Bill"] - new_paid
                    df.loc[df["ID"] == p_data["ID"], ["Paid_Amount", "Remaining", "Status", "Result"]] = [new_paid, new_rem, ("Paid" if new_rem<=0 else "Pending"), res_v]
                    df.to_csv(PATIENT_FILE, index=False)
                    st.success("Updated!")
                    st.rerun()
            else: st.info("Koi Pending record nahi hai.")

    elif menu == "Excel History":
        st.header("📊 Lab Database History")
        with st.expander("🖨️ Reprint Old Slip"):
            if not df.empty:
                selected_p = st.selectbox("Select Patient", ["-- Select --"] + df["Name"].tolist())
                if selected_p != "-- Select --":
                    p_to_print = df[df["Name"] == selected_p].iloc[-1]
                    show_receipt(p_to_print)
                    st.markdown('<button onclick="window.print()" class="no-print" style="width:100%; padding:10px; background:black; color:white; cursor:pointer;">PRINT SLIP</button>', unsafe_allow_html=True)
        st.divider()
        st.dataframe(df, use_container_width=True, hide_index=True)