import streamlit as st

def show_receipt(v):
    try:
        # 1. Lab Details (Jo aapne maangi hain)
        l_name = st.session_state.get('lab_name', 'THE LIFE CARE CLINIC & LAB')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2926075')

        # 2. CSS Part (Alag rakha hai taake error na aaye)
        style = """
        <style>
            .slip-body {
                width: 350px; border: 2px solid #000; padding: 15px;
                font-family: 'Courier New', Courier, monospace;
                background: white; color: black; margin: auto;
            }
            .header { text-align: center; margin: 0; }
            .token { 
                text-align: center; border: 1px solid #000; 
                margin: 10px 0; padding: 5px; font-size: 18px; font-weight: bold; 
            }
            @media print {
                .stButton, header, footer, .sidebar { display: none !important; }
                body { background: white; }
            }
        </style>
        """

        # 3. HTML Content
        content = f"""
        <div class="slip-body">
            <h2 class="header" style="font-size: 22px;">{l_name}</h2>
            <p class="header" style="font-size: 12px; font-weight: bold;">{l_addr}</p>
            <p class="header" style="font-size: 12px; font-weight: bold;">{l_phone}</p>
            
            <div class="token">TOKEN NO: {v[0]}</div>
            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>Patient:</b> {v[3]}</td><td align="right"><b>Inv:</b> {v[1]}</td></tr>
                <tr><td><b>Age/Gen:</b> {v[5]} / {v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td><b>Mobile:</b> {v[4]}</td><td align="right"><b>Ref:</b> {v[7] if v[7] else 'SELF'}</td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;">
                <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;">
                    <th align="left">Description</th>
                    <th align="center">Qty</th>
                    <th align="right">Amt</th>
                </tr>
        """

        # Tests handling
        raw_items = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        for item in raw_items.split(", "):
            if item.strip():
                content += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        content += f"""
            </table>

            <div style="margin-top: 15px; border-top: 2px solid #000; padding-top: 5px; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;"><span>Total:</span> <span>Rs. {v[9]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Paid:</span> <span>Rs. {v[10]}</span></div>
                <div style="display: flex; justify-content: space-between; font-size: 15px; background: #eee; border:1px solid #000; padding: 2px;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 20px;">Developed by Zain - 03702906075</p>
        </div>
        """

        # Final Display
        st.markdown(style + content, unsafe_allow_html=True)
        st.button("Direct Print (Ctrl+P)", key=f"p_btn_{v[1]}")

    except Exception as e:
        st.error(f"Design Error: {e}")