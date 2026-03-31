import streamlit as st

def show_receipt(v):
    """
    v is the list of patient data.
    """
    try:
        # Settings se Dynamic Data uthana
        l_name = st.session_state.get('lab_name', '( THE LIFE CARE )')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2906075')

        # Formatting Patient Details
        patient_name = v[3]
        inv_no = v[1]
        age_gen = f"{v[5]} / {v[6]}"
        date_val = v[2]
        mobile = v[4]
        ref_by = v[7] if len(v) > 7 and v[7] else "SELF"
        token_no = v[0]

        # Receipt HTML with Fix for CSS Brackets
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
                margin: 10px auto;
                background: white;
                color: black;
            }}
            .header-title {{ text-align: center; margin: 0; font-size: 20px; font-weight: 900; text-transform: uppercase; }}
            .header-sub {{ text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0; }}
            .info-table {{ width: 100%; font-size: 12px; margin-top: 10px; }}
            .item-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
            .item-table th {{ border-bottom: 2px solid #000; border-top: 2px solid #000; }}
        </style>

        <div class="receipt-container">
            <h2 class="header-title">{l_name}</h2>
            <p class="header-sub">{l_addr}</p>
            <p class="header-sub">{l_phone}</p>
            
            <div style="text-align: center; border: 1px solid #000; margin: 10px 0; padding: 5px; font-size: 16px; font-weight: bold;">
                TOKEN NO: {token_no}
            </div>

            <hr style="border: 1px solid #000; margin: 5px 0;">
            
            <table class="info-table">
                <tr><td><b>Patient:</b> {patient_name}</td><td align="right"><b>Inv:</b> {inv_no}</td></tr>
                <tr><td><b>Age/Gen:</b> {age_gen}</td><td align="right"><b>Date:</b> {date_val}</td></tr>
                <tr><td><b>Mobile:</b> {mobile}</td><td align="right"><b>Ref:</b> {ref_by}</td></tr>
            </table>

            <table class="item-table">
                <thead>
                    <tr>
                        <th align="left">Description</th>
                        <th align="center">Qty</th>
                        <th align="right">Amt</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Tests/Meds Display Logic
        raw_items = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        for item in raw_items.split(", "):
            if item.strip():
                receipt_html += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        receipt_html += f"""
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
        
        st.markdown(receipt_html, unsafe_allow_html=True)
        st.button("Print Slip (Ctrl+P)", key=f"print_final_{inv_no}")
            
    except Exception as e:
        st.error(f"Receipt Error: {e}")