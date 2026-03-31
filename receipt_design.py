import streamlit as st
import os

def show_receipt(v):
    try:
        # CSS File load karne ka tarika
        if os.path.exists("style.css"):
            with open("style.css") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Aapka Data
        lab_name = "JAWAD MEDICAL CENTER"
        token_no = v[0]
        inv_no = v[1]
        p_name = v[3]
        age_gen = f"{v[5]} / {v[6]}"
        date_val = v[2]
        mobile = v[4]
        ref_by = v[7] if v[7] else "SELF"

        # HTML Structure (No CSS here)
        html_content = f"""
        <div class="receipt-container">
            <h2 class="header-title">{lab_name}</h2>
            <p class="header-sub">MAJEED COLONY SEC 2, KARACHI</p>
            <p class="header-sub">0370-2906075</p>
            
            <div class="token-box">TOKEN NO: {token_no}</div>
            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>Patient:</b> {p_name}</td><td align="right"><b>Inv:</b> {inv_no}</td></tr>
                <tr><td><b>Age/Gen:</b> {age_gen}</td><td align="right"><b>Date:</b> {date_val}</td></tr>
                <tr><td><b>Mobile:</b> {mobile}</td><td align="right"><b>Ref:</b> {ref_by}</td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;">
                <thead>
                    <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;">
                        <th align="left">Description</th>
                        <th align="center">Qty</th>
                        <th align="right">Amt</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Tests logic
        items = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ").split(", ")
        for item in items:
            if item.strip():
                html_content += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        html_content += f"""
                </tbody>
            </table>

            <div style="margin-top: 15px; border-top: 2px solid #000; padding-top: 5px; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;"><span>Total:</span> <span>Rs. {v[9]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Paid:</span> <span>Rs. {v[10]}</span></div>
                <div style="display: flex; justify-content: space-between; font-size: 15px; background: #eee; padding: 2px; border: 1px solid #000;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 20px;">Developed by Zain - 03702906075</p>
        </div>
        """

        st.markdown(html_content, unsafe_allow_html=True)
        st.button("Print Slip (Ctrl+P)", key=f"print_final_{inv_no}")

    except Exception as e:
        st.error(f"Error: {e}")