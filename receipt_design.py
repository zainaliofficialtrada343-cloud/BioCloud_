import streamlit as st

def show_receipt(v):
    """
    v is the list of patient data.
    ⚙️ Lab Settings wala data 'st.session_state.lab_name' wagera se uthayega.
    """
    try:
        # Settings se data uthana (Agar settings khali hain toh purana naam rakhega)
        l_name = st.session_state.get('lab_name', 'JAWAD MEDICAL CENTER')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2906075')

        receipt_html = f"""
        <style>
            @media print {{
                @page {{ size: auto; margin: 0mm; }}
                body {{ background: white !important; margin: 0 !important; padding: 0 !important; }}
                header, footer, .sidebar, [data-testid="stSidebar"], [data-testid="stHeader"], .stButton {{ 
                    display: none !important; 
                }}
                .receipt-container {{
                    width: 350px !important;
                    border: none !important;
                    margin: 0 !important;
                    padding: 10px !important;
                    visibility: visible !important;
                    position: absolute;
                    left: 0;
                    top: 0;
                }}
                body * {{ visibility: hidden; }}
                .receipt-container, .receipt-container * {{ visibility: visible !important; }}
            }}
            .receipt-container {{
                width: 350px;
                border: 2px solid #000;
                padding: 15px;
                font-family: 'Courier New', Courier, monospace;
                margin: 20px auto;
                background: white;
                color: black;
            }}
            .header-title {{ text-align: center; margin: 0; font-size: 22px; font-weight: 900; text-transform: uppercase; }}
            .header-sub {{ text-align: center; font-size: 12px; font-weight: bold; margin: 2px 0; }}
            .token-box {{ text-align: center; border: 2px solid #000; margin: 8px 0; padding: 4px; font-size: 18px; font-weight: bold; }}
        </style>

        <div class="receipt-container">
            <h2 class="header-title">{l_name}</h2>
            <p class="header-sub">{l_addr}</p>
            <p style="text-align: center; font-size: 12px; font-weight: bold; margin: 2px 0;">{l_phone}</p>
            
            <div class="token-box">TOKEN NO: {v[0]}</div>
            
            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>Patient:</b> {v[3]}</td><td align="right"><b>Inv:</b> {v[1]}</td></tr>
                <tr><td><b>Age/Gen:</b> {v[5]} / {v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td><b>Ref By:</b> {v[7] if len(v)>7 else 'SELF'}</td><td align="right"><b>Lab Box:</b> ____</td></tr>
                <tr><td><b>Mobile:</b> {v[4]}</td><td></td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;">
                <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;">
                    <th align="left">Description</th>
                    <th align="center">Qty</th>
                    <th align="right">Amt</th>
                </tr>
        """
        
        # Details (Tests + Meds) split logic
        raw_items = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_list = raw_items.split(", ")
        
        for item in items_list:
            if item.strip():
                receipt_html += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        receipt_html += f"""
            </table>

            <div style="margin-top: 15px; border-top: 2px solid #000; padding-top: 5px; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;"><span>Total:</span> <span>Rs. {v[9]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Paid:</span> <span>Rs. {v[10]}</span></div>
                <div style="display: flex; justify-content: space-between; font-size: 15px; background: #eee; padding: 2px;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 20px;">Developed by Zain - 03702906075</p>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)
        st.button("Print Slip (Ctrl+P)", key="print_final_v2")
            
    except Exception as e:
        st.error(f"Receipt Error: {e}")