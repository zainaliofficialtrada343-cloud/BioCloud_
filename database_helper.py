import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

def get_full_data():
    try:
        # worksheet=0 ka matlab pehli tab (Sheet1)
        return conn.read(worksheet=0, ttl=0).dropna(how="all")
    except Exception as e:
        st.error(f"Sheet1 Connection Error: {e}")
        cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    try:
        # worksheet=1 ka matlab dusri tab (Sheet2)
        return conn.read(worksheet=1, ttl=0).dropna(how="all")
    except Exception as e:
        st.error(f"Sheet2 Connection Error: {e}")
        return pd.DataFrame(columns=["Test_Name", "Rate"])

def save_record_online(new_row_df):
    try:
        existing_data = get_full_data()
        updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
        conn.update(data=updated_data, worksheet=0) # Yahan bhi 0 kar diya
        st.cache_data.clear()
    except Exception as e:
        st.error(f"Save Record Error: {e}")

def save_test_online(new_test_df):
    try:
        existing_tests = get_tests_list()
        updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
        conn.update(data=updated_tests, worksheet=1) # Yahan bhi 1 kar diya
        st.cache_data.clear()
    except Exception as e:
        st.error(f"Save Test Error: {e}")