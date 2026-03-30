import streamlit as st
import streamlit.components.v1 as components

def show_receipt(v):
    try:
        # Settings se data uthana
        l_name = st.session_state.get('lab_name', 'THE LIFE CARE')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2906075')

        # Data variables
        token = v[0]
        inv = v[1]
        date = v[2]
        patient = v[3]
        phone = v[4]
        age_gen = f"{v[5]} / {v[6]}"
        ref = v[7] if len(v)>7 else 'SELF'
        
        # Tests aur Meds ko saaf dikhane ke liye
        details = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_html = ""
        for item in details.split(", "):
            if item.strip():
                items_html += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        # Poora Design aik string mein
        raw_html = f"""
        <div style="width: 320px; border: 2px solid #000; padding: 10px; font-family: 'Courier New', Courier, monospace; background: white; color: black;">
            <h2 style="text-align: center; margin: 0; font-size: 20px; font-weight: 900; text-transform: uppercase;">{l_name}</h2>
            <p style="text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0;">{l_addr}</p>
            <p style="text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0;">{l_phone}</p>
            
            <div style="text-align: center; border: 1px solid #000; margin: 10px 0; padding: 5px; font-size: 18px; font-weight: bold;">TOKEN NO: {token}</div>
            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 11px;">
                <tr><td><b>Patient:</b> {patient}</td><td align="right"><b>Inv:</b> {inv}</td></tr>
                <tr><td><b>Age/Gen:</b> {age_gen}</td><td align="right"><b>Date:</b> {date}</td></tr>
                <tr><td><b>Ref By:</b> {ref}</td><td align="right"><b>Lab Box:</b> ____</td></tr>
                <tr><td><b>Mobile:</b> {phone}</td><td></td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px;">
                <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;">
                    <th align="left">Description</th>
                    <th align="center">Qty</th>
                    <th align="right">Amt</th>
                </tr>
                {items_html}
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
        
        # YEH HAI ASLI FIX: Is se code kabhi nazar nahi ayega
        components.html(raw_html, height=550)
            
    except Exception as e:
        st.error(f"Parchi Error: {e}")