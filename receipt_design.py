import streamlit as st

def show_receipt(v):
    try:
        # Lab Settings se data lena
        l_name = st.session_state.get('lab_name', 'JAWAD MEDICAL CENTER')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2906075')

        # Items (Tests/Meds) taiyar karna
        details_raw = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_list = details_raw.split(", ")
        items_html = ""
        for item in items_list:
            if item.strip():
                items_html += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        # Ref Doctor ka data
        dr_name = v[7] if len(v)>7 else 'SELF'

        # ASLI DESIGN (Purana Style + 350px Pixel Fix)
        # Maine f-string ko break kiya hai taake code display wala error na aaye
        style = """
        <style>
            .slip-main {
                width: 350px;
                border: 2px solid #000;
                padding: 15px;
                font-family: 'Courier New', Courier, monospace;
                background-color: white;
                color: black;
                margin: auto;
            }
            .txt-center { text-align: center; margin: 0; }
            .token-style { 
                text-align: center; border: 2px solid #000; 
                margin: 10px 0; padding: 5px; font-size: 18px; font-weight: bold; 
            }
            .dr-box { border: 1px solid #000; margin-top: 5px; padding: 5px; font-size: 12px; }
        </style>
        """

        body = f"""
        <div class="slip-main">
            <h2 class="txt-center" style="font-size: 22px; font-weight: 900;">{l_name}</h2>
            <p class="txt-center" style="font-size: 12px; font-weight: bold;">{l_addr}</p>
            <p class="txt-center" style="font-size: 12px; font-weight: bold;">{l_phone}</p>
            
            <div class="token-style">TOKEN NO: {v[0]}</div>
            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>Patient:</b> {v[3]}</td><td align="right"><b>Inv:</b> {v[1]}</td></tr>
                <tr><td><b>Age/Gen:</b> {v[5]}/{v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td><b>Mobile:</b> {v[4]}</td><td align="right"><b>Lab Box:</b> ____</td></tr>
            </table>

            <div class="dr-box">
                <b>Ref By / Doctor:</b> {dr_name}
            </div>

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
                <div style="display: flex; justify-content: space-between; font-size: 16px; background: #eee; padding: 2px; border: 1px solid #000;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 20px;">Developed by Zain - 03702906075</p>
        </div>
        """

        # Render as HTML
        st.markdown(style + body, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Parchi Error: {e}")