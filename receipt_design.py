import streamlit as st
import os

def show_receipt(v):
    try:
        # 1. CSS aur HTML files ko read karein
        with open('style.css', 'r') as f:
            css = f.read()
        
        with open('receipt_template.html', 'r') as f:
            template = f.read()

        # 2. Items ki rows banayein
        items_html = ""
        tests_list = str(v[8]).replace("Tests: ", "").replace(" | ", ", ").split(", ")
        for t in tests_list:
            if t.strip():
                items_html += f"<tr><td>{t}</td><td align='right'>-</td></tr>"

        # 3. Template mein data replace karein
        final_html = template.replace("{{LAB_NAME}}", "JAWAD MEDICAL CENTER") \
                             .replace("{{TOKEN}}", str(v[0])) \
                             .replace("{{PATIENT}}", str(v[3])) \
                             .replace("{{INV}}", str(v[1])) \
                             .replace("{{AGE_GEN}}", f"{v[5]} / {v[6]}") \
                             .replace("{{DATE}}", str(v[2])) \
                             .replace("{{ITEMS_ROWS}}", items_html) \
                             .replace("{{TOTAL}}", str(v[9])) \
                             .replace("{{PAID}}", str(v[10])) \
                             .replace("{{BALANCE}}", str(v[11]))

        # 4. CSS aur HTML ko jor kar display karein
        full_content = f"<style>{css}</style>{final_html}"
        st.markdown(full_content, unsafe_allow_html=True)
        
        st.button("Print (Ctrl+P)", key=f"p_{v[1]}")

    except Exception as e:
        st.error(f"File Loading Error: {e}. Make sure style.css and receipt_template.html exist.")