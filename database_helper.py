import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Google Sheets se connection banana
conn = st.connection("gsheets", type=GSheetsConnection)

def get_full_data():
    """Sheet1 se patients ka sara record uthana"""
    try:
        df = conn.read(worksheet="Sheet1")
        # Khali rows khatam karne ke liye
        return df.dropna(how="all")
    except:
        # Agar sheet khali ho toh required columns ke saath khali DataFrame dena
        cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    """Sheet2 se tests ki list uthana"""
    try:
        # Sheet2 se data parhna
        df_tests = conn.read(worksheet="Sheet2")
        return df_tests.dropna(how="all")
    except:
        # Agar sheet khali ho toh khali DataFrame dena
        return pd.DataFrame(columns=["Test_Name", "Rate"])

def save_record_online(new_row_df):
    """Naya patient record Sheet1 mein save karna (Registration)"""
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated_data)

def save_test_online(new_test_df):
    """Naya test Sheet2 mein save karna (Add New Test)"""
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    conn.update(worksheet="Sheet2", data=updated_tests)