import streamlit as st
import pandas as pd
import os

# Files ke naam
PATIENT_FILE = "data_db.csv"
TESTS_FILE = "tests_db.csv"

def get_full_data():
    if os.path.exists(PATIENT_FILE):
        return pd.read_csv(PATIENT_FILE)
    else:
        cols = ["ID", "Date", "Name", "Age", "Gender", "Test", "Total_Bill", "Paid_Amount", "Remaining", "Result", "Unit", "Status"]
        return pd.DataFrame(columns=cols)

def get_tests_list():
    # Ye aapki tests_db.csv se data uthayega
    if os.path.exists(TESTS_FILE):
        return pd.read_csv(TESTS_FILE)
    else:
        # Agar file na mile toh ye default dikhayega
        return pd.DataFrame([{"Test_Name": "CBC", "Rate": 500}, {"Test_Name": "Sugar", "Rate": 200}])

def save_record_online(new_row_df):
    existing_data = get_full_data()
    updated_data = pd.concat([existing_data, new_row_df], ignore_index=True)
    updated_data.to_csv(PATIENT_FILE, index=False)
    st.success("Record Saved Locally!")

def save_test_online(new_test_df):
    existing_tests = get_tests_list()
    updated_tests = pd.concat([existing_tests, new_test_df], ignore_index=True)
    updated_tests.to_csv(TESTS_FILE, index=False)
    st.success("Test Added to List!")