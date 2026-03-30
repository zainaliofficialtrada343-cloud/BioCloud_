import streamlit as st

def show_receipt(v):
    try:
        # 1. Lab Settings se data uthana
        # Agar settings khali hon toh default values show hongi
        l_name = st.session_state.get('lab_name', 'JAWAD MEDICAL CENTER')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2906075')

        # 2. Details (Tests/Meds) ko saaf karna
        details_raw = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_html = ""
        for item in details_raw.split(", "):
            if item.strip():
                items_html += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        # 3. Pure Design ka HTML (Pixels aur fonts bilkul purane hain)
        receipt_style = f"""
        <style>
            .main-receipt {{
                width: 330px;
                border: 2px solid #000;
                padding: 15px;
                font-family: 'Courier New', Courier, monospace;
                background-color: white;
                color: black;
                margin: auto;
            }}
            .header-txt {{ text-align: center; margin: 0; text-transform: uppercase; }}
            .token-style {{ 
                text-align: center; 
                border: 2px solid #000; 
                margin: 10px 0; 
                padding: 5px; 
                font-size: 18px; 
                font-weight: bold; 
            }}
        </style>
        """

        receipt_body = f"""
        <div class="main-receipt">
            <h2 class="header-txt" style="font-size: 20px; font-weight: 900;">{l_name}</h2>
            <p class="header-txt" style="font-size: 11px; font-weight: bold;">{l_addr}</p>
            <p class="header-txt" style="font-size: 11px; font-weight: bold;">{l_phone}</p>
            
            <div class="token-style">TOKEN NO: {v[0]}</div>

            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 12px; line-height: 1.5;">
                <tr><td><b>Patient:</b> {v[3]}</td><td align="right"><b>Inv:</b> {v[1]}</td></tr>
                <tr><td><b>Age/Gen:</b> {v[5]}/{v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td><b>Ref By:</b> {v[7] if len(v)>7 else 'SELF'}</td><td align="right"><b>Lab Box:</b> ____</td></tr>
                <tr><td><b>Mobile:</b> {v[4]}</td><td></td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;">
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
                <div style="display: flex; justify-content: space-between; font-size: 16px; background: #eee; padding: 2px;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 20px;">Developed by Zain - 03702906075</p>
        </div>
        """

        # 4. Render as Markdown with HTML enabled
        st.markdown(receipt_style + receipt_body, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Design Error: {e}")