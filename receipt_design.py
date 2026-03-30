import streamlit as st

def show_receipt(v):
    """
    v is the list of patient data.
    v[12] ko hum Token No ke liye use kar sakte hain agar sheet mein hai, 
    warna yahan manually handle kiya hai.
    """
    try:
        receipt_html = f"""
        <style>
            @media print {{
                @page {{ size: 80mm auto; margin: 0mm; }}
                body {{ background: white !important; margin: 0 !important; padding: 0 !important; }}
                header, footer, .sidebar, [data-testid="stSidebar"], [data-testid="stHeader"], .stButton {{ 
                    display: none !important; 
                }}
                .receipt-container {{
                    width: 300px !important; /* Standard Thermal Size */
                    border: none !important;
                    margin: 0 !important;
                    padding: 5px !important;
                    visibility: visible !important;
                    position: absolute;
                    left: 0;
                    top: 0;
                }}
                body * {{ visibility: hidden; }}
                .receipt-container, .receipt-container * {{ visibility: visible !important; }}
            }}
            .receipt-container {{
                width: 320px;
                border: 1px solid #000;
                padding: 10px;
                font-family: 'Courier New', Courier, monospace;
                margin: 10px auto;
                background: white;
                color: black;
            }}
            .header-title {{ text-align: center; margin: 0; font-size: 18px; font-weight: 900; text-transform: uppercase; }}
            .header-sub {{ text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0; }}
            .token-box {{ 
                text-align: center; 
                border: 2px solid #000; 
                margin: 5px 0; 
                padding: 5px; 
                font-size: 20px; 
                font-weight: bold; 
            }}
        </style>

        <div class="receipt-container">
            <h2 class="header-title">JAWAD MEDICAL CENTER</h2>
            <p class="header-sub">MAJEED COLONY SEC 2, KARACHI</p>
            <p class="header-sub">0370-2906075</p>
            
            <div class="token-box">TOKEN NO: {v[0]}</div> <hr style="border: 1px solid #000; margin: 5px 0;">
            
            <table style="width: 100%; font-size: 11px; line-height: 1.4;">
                <tr><td><b>Patient:</b> {v[3]}</td><td align="right"><b>Inv:</b> {v[1]}</td></tr>
                <tr><td><b>Age/Gen:</b> {v[5]} / {v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td colspan="2"><b>Ref By / Doctor:</b> {v[7] if len(v)>7 else 'Self'}</td></tr>
                <tr><td><b>Mobile:</b> {v[4]}</td><td align="right"><b>Lab Box:</b> _______</td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px;">
                <tr style="border-bottom: 1px solid #000; border-top: 1px solid #000;">
                    <th align="left">Description</th>
                    <th align="right">Amt</th>
                </tr>
        """
        
        # Tests aur Medicines ki list dikhane ke liye
        details = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").split(" | ")
        for item_group in details:
            items = item_group.split(", ")
            for item in items:
                receipt_html += f"<tr><td style='padding: 2px 0;'>{item}</td><td align='right'>-</td></tr>"

        receipt_html += f"""
            </table>

            <div style="margin-top: 10px; border-top: 1px solid #000; padding-top: 5px; font-size: 13px; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;"><span>Total Bill:</span> <span>Rs. {v[9]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Paid Amount:</span> <span>Rs. {v[10]}</span></div>
                <div style="display: flex; justify-content: space-between; border: 1px solid #000; padding: 2px; margin-top: 2px;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 10px; margin-top: 15px; font-weight: bold;">*** Wish You A Speedy Recovery ***</p>
            <p style="text-align: center; font-size: 8px; margin-top: 5px;">Developed by Zain - 03702906075</p>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)
        if st.button("Print Receipt", key="print_btn"):
            st.write("Press **Ctrl + P** to print")
            
    except Exception as e:
        st.error(f"Receipt Design Error: {e}")