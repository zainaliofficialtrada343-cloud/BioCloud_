import streamlit as st

# --- 1. LAB BASIC INFORMATION ---
LAB_DETAILS = {
    "name": "THE LIFE CARE CLINIC & LAB",
    "address": "MAJEED COLONY SEC 2, KARACHI",
    "phone": "0370-2926075",
    "developer": "Zain - 0370-2926075",
    "logo_url": "https://raw.githubusercontent.com/zainaliofficialtrada343-cloud/BioCloud_/main/lab_girl.jpg"
}

# --- 2. TEST COMPONENTS & RANGES (Master Database) ---
# Yahan aap naye tests aur unki details asani se add kar sakte hain
TEST_COMPONENTS = {
    "CBC": [
        {"name": "Hemoglobin (Hb)", "range": "13.0 - 17.0", "unit": "g/dL"},
        {"name": "RBC Count", "range": "4.5 - 5.5", "unit": "mill/cmm"},
        {"name": "WBC Count", "range": "4,000 - 10,000", "unit": "/cmm"},
        {"name": "Platelets", "range": "150,000 - 450,000", "unit": "/cmm"},
        {"name": "HCT / PCV", "range": "40 - 50", "unit": "%"},
        {"name": "MCV", "range": "80 - 100", "unit": "fL"},
        {"name": "MCH", "range": "27 - 32", "unit": "pg"}
    ],
    "SUGAR": [
        {"name": "Fasting Glucose", "range": "70 - 110", "unit": "mg/dL"},
        {"name": "Random Glucose", "range": "80 - 140", "unit": "mg/dL"}
    ],
    "LIPID PROFILE": [
        {"name": "Total Cholesterol", "range": "Up to 200", "unit": "mg/dL"},
        {"name": "Triglycerides", "range": "Up to 150", "unit": "mg/dL"}
    ]
}

# --- 3. UI THEME SETTINGS ---
def apply_custom_style():
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
            url("{LAB_DETAILS['logo_url']}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            border-bottom: 4px solid #4CAF50;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. APP DEFAULTS ---
LOGIN_CREDENTIALS = {
    "username": "admin",
    "password": "lab786"
}