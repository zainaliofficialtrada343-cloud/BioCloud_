import streamlit as st
import pandas as pd
import os
from datetime import datetime
from login_ui import show_login_page, local_css

# --- 1. CSV DATABASE CONFIG ---
PATIENT_FILE = "data_db.csv"
TESTS_FILE = "tests_db.csv"

def get_full_data():
    if os.path.exists(PATIENT_FILE):
        return pd.read_csv(PATIENT_FILE)
    else:
        cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
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

# --- SLIP GENERATOR FUNCTION ---
def show_receipt(data):
    st.markdown("""
        <style>
        .receipt-box {
            background-color: white;
            padding: 20px;
            border: 2px dashed #000;
            width: 350px;
            margin: auto;
            color: black;
            font-family: 'Courier New', Courier, monospace;
        }
        .lab-name { text-align: center; font-weight: bold; font-size: 22px; margin-bottom: 5px; }
        .receipt-info { font-size: 14px; margin-bottom: 10px; }
        .test-item { display: flex; justify-content: space-between; font-size: 13px; }
        .total-row { border-top: 1px solid #000; margin-top: 10px; padding-top: 5px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
            <div class="receipt-box">
                <div class="lab-name">🧪 BIOCLOUD LAB</div>
                <div style="text-align: center; font-size: 10px;">Quality & Excellence in Diagnostics</div>
                <hr>
                <div class="receipt-info">
                    <b>ID:</b> {data['ID']}<br>
                    <b>Date:</b> {data['Date']}<br>
                    <b>Name:</b> {data['Name']}<br>
                    <b>Age/Sex:</b> {data['Age']} / {data['Gender']}
                </div>
                <hr>
                <div style="font-weight: bold; margin-bottom: 5px;">Tests:</div>
                <div class="test-item"><span>{data['Test']}</span></div>
                <div class="total-row">
                    <div class="test-item"><span>Total:</span><span>Rs. {data['Total_Bill']}</span></div>
                    <div class="test-item"><span>Paid:</span><span>Rs. {data['Paid_Amount']}</span></div>
                    <div class="test-item"><span>Balance:</span><span>Rs. {data['Remaining']}</span></div>
                </div>
                <hr>
                <div style="text-align: center; font-size: 12px; font-weight: bold;">*** GET YOUR REPORT SOON ***</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🖨️ Print Slip (Ctrl + P)"):
            st.info("Browser ka print window khulega, wahan Printer select karke print kar dein.")

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="BioCloud Lab Pro", layout="wide", page_icon="🧪")

if 'temp_tests' not in st.session_state:
    st.session_state.temp_tests = [] 
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'last_saved_patient' not in st.session_state:
    st.session_state.last_saved_patient = None

def check_login(u, p):
    if u == "admin" and p == "lab786":
        st.session_state['auth'] = True
        st.rerun()
    else:
        st.error("Invalid Username or Password")

if not st.session_state['auth']:
    show_login_page(check_login)
else:
    local_css("style.css")
    df = get_full_data()
    today = str(datetime.now().date())

    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🧪 BioCloud</h1>", unsafe_allow_html=True)
        menu = st.radio("Navigation", ["Registration", "Dues & Reports", "Excel History"])
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

    if menu == "Registration":
        st.header("New Patient Registration")
        
        # SLIP PREVIEW (Agar record save ho gaya ho)
        if st.session_state.last_saved_patient:
            st.success("✅ Record Saved! Print Slip Below:")
            show_receipt(st.session_state.last_saved_patient)
            if st.button("➕ Register New Patient"):
                st.session_state.last_saved_patient = None
                st.rerun()
            st.divider()

        tdf = get_tests_list()
        test_options = sorted(tdf["Test_Name"].unique().tolist()) if not tdf.empty else []
        test_rate_dict = dict(zip(tdf["Test_Name"], tdf["Rate"])) if not tdf.empty else {}

        with st.expander("Patient Information", expanded=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            p_name = c1.text_input("Patient Name")
            p_age = c2.number_input("Age", 1, 120, 25)
            p_gender = c3.selectbox("Gender", ["Male", "Female", "Other"])

        st.subheader("Add Tests")
        col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
        selected_t = col_t1.selectbox("Select Test", ["--- Select ---"] + test_options)
        default_rate = int(test_rate_dict.get(selected_t, 0)) if selected_t != "--- Select ---" else 0
        entered_rate = col_t2.number_input("Rate (Rs.)", value=default_rate, key="r_in")

        if col_t3.button("➕ Add"):
            if selected_t != "--- Select ---":
                st.session_state.temp_tests.append({"Test": selected_t, "Rate": entered_rate})
                st.rerun()

        if st.session_state.temp_tests:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            total_bill = sum(t['Rate'] for t in st.session_state.temp_tests)
            for i, t in enumerate(st.session_state.temp_tests):
                st.write(f"{i+1}. ✅ {t['Test']} --- Rs. {t['Rate']}")
            st.markdown(f"<b>Total: Rs. {total_bill}</b>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            paid_amt = st.number_input("Paid Amount", 0)
            if st.button("💾 Final Save & Generate Slip", use_container_width=True):
                if p_name:
                    all_tests = ", ".join([t['Test'] for t in st.session_state.temp_tests])
                    rem = total_bill - paid_amt
                    new_id = len(df) + 1
                    
                    patient_data = {
                        "ID": new_id, "Date": today, "Name": p_name, "Age": p_age, "Gender": p_gender,
                        "Test": all_tests, "Total_Bill": total_bill, "Paid_Amount": paid_amt, 
                        "Remaining": rem, "Result": "-", "Unit": "-", "Status": ("Paid" if rem<=0 else "Pending")
                    }
                    
                    save_record_local(pd.DataFrame([patient_data]))
                    st.session_state.last_saved_patient = patient_data # Slip data save kiya
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
                st.info(f"Dues: Rs. {p_data['Remaining']}")
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
                st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "Excel History":
        st.header("📊 Lab Database History")
        search_query = st.text_input("🔍 Search History")
        if search_query:
            filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)