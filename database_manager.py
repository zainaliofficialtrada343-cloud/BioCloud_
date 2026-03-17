import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Connection initialize karna
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 1. DATA READ KARNE KE FUNCTIONS ---

def get_full_data():
    """Sath patients ka data read karta hai"""
    try:
        return conn.read(worksheet="data_db", ttl="0")
    except Exception as e:
        # Agar sheet khali ho toh ye columns wali empty dataframe return karega
        cols = ["ID", "Invoice", "Date", "Name", "Mobile", "Age", "Gender", "Collected", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    """Tests aur unke rates ki list lata hai"""
    try:
        df = conn.read(worksheet="tests_db", ttl="0")
        if not df.empty:
            df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce').fillna(0)
        return df
    except:
        # Default tests agar sheet na mile
        return pd.DataFrame([{"Test_Name": "CBC", "Rate": 500}, {"Test_Name": "Sugar", "Rate": 200}])

def get_expense_data():
    """Kharchon ka data lata hai"""
    try:
        df = conn.read(worksheet="expenses_db", ttl="0")
        return df
    except:
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# --- 2. DATA SAVE KARNE KE FUNCTIONS ---

def save_patient_record(new_row_df):
    """Naya patient save karta hai"""
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    conn.update(worksheet="data_db", data=updated_data)

def save_new_test(test_name, rate):
    """Test database mein naya test add karta hai"""
    existing_tests = get_tests_list()
    new_t = pd.DataFrame([{"Test_Name": test_name, "Rate": rate}])
    updated_tests = pd.concat([existing_tests, new_t], ignore_index=True)
    conn.update(worksheet="tests_db", data=updated_tests)

def update_existing_record(updated_df):
    """Purane record ko update karta hai (Dues ya Results ke liye)"""
    conn.update(worksheet="data_db", data=updated_df)