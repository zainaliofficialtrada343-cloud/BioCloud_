import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

def get_full_data():
    """Sheet1 se patients ka sara record uthana"""
    try:
        df = conn.read(worksheet="Sheet1", ttl=0)
        return df.dropna(how="all")
    except:
        cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    """Sheet2 se tests ki list uthana"""
    try:
        df_tests = conn.read(worksheet="Sheet2", ttl=0)
        return df_tests.dropna(how="all")
    except:
        return pd.DataFrame(columns=["Test_Name", "Rate"])

def save_record_online(new_row_df):
    """Naya patient record Sheet1 mein save karna"""
    existing_data = get_full_data()
    updated_df = pd.concat([existing_data, new_row_df], ignore_index=True)
    # Naya method for saving
    conn.update(worksheet="Sheet1", data=updated_df)
    st.cache_data.clear()

def save_test_online(new_test_df):
    """Naya test Sheet2 mein add karna"""
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    # Naya method for saving
    conn.update(worksheet="Sheet2", data=updated_tests)
    st.cache_data.clear()