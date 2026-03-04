import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

def get_full_data():
    """Sheet1 se patients ka record parhna"""
    try:
        return conn.read(worksheet="Sheet1", ttl=0).dropna(how="all")
    except:
        cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    """Sheet2 se tests ki list parhna"""
    try:
        return conn.read(worksheet="Sheet2", ttl=0).dropna(how="all")
    except:
        return pd.DataFrame(columns=["Test_Name", "Rate"])

def save_record_online(new_row_df):
    """Sheet1 mein naya record save karna"""
    existing_data = get_full_data()
    updated_df = pd.concat([existing_data, new_row_df], ignore_index=True)
    # Sahi order: data pehle, worksheet baad mein
    conn.update(data=updated_df, worksheet="Sheet1")
    st.cache_data.clear()

def save_test_online(new_test_df):
    """Sheet2 mein naya test save karna"""
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    # Sahi order: data pehle, worksheet baad mein
    conn.update(data=updated_tests, worksheet="Sheet2")
    st.cache_data.clear()