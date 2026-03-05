import streamlit as st

def show_receipt(v):
    try:
        # Amount calculation fix
        tests = str(v[8]).split(", ")
        test_rows = ""
        # Farz karen total amount ko tests par divide kar rahe hain ya list handle kar rahe hain
        per_test_amt = int(v[9]) // len(tests) if len(tests) > 0 else 0
        
        for t in tests:
            test_rows += f"""
            <tr style="border-bottom: 0.5px solid #eee;">
                <td style="padding: 5px 0;">{t}</td>
                <td align="right">Rs. {per_test_amt}</td>
            </tr>"""

        receipt_html = f"""
        <style>
            /* Ye hissa Ctrl+P par baki sab hide kar dega */
            @media print {{
                body * {{ visibility: hidden; }}
                .print-container, .print-container * {{ visibility: visible; }}
                .print-container {{ position: absolute; left: 0; top: 0; width: 300px !important; }}
                header, footer, .stSidebar, .stActionButton {{ display: none !important; }}
            }}
            
            .receipt-box {{
                width: 320px;
                border: 1px solid #000;
                padding: 20px;
                font-family: 'Courier New', Courier, monospace;
                background-color: white;
                color: black;
                margin: 10px auto;
            }}
            .header-text {{ text-align: center; font-weight: bold; }}
            .line {{ border-top: 1px dashed black; margin: 10px 0; }}
        </style>

        <div class="print-container">
            <div class="receipt-box">
                <div class="header-text">
                    <h3 style="margin: 0;">( THE LIFE CARE )</h3>
                    <p style="font-size: 12px; margin: 5px 0;">MAJEED COLONY SEC 2, KARACHI<br>0370-2926075</p>
                </div>
                
                <div style="text-align: center; border: 1px solid black; margin: 10px 0; font-weight: bold;">PATIENT SLIP</div>

                <table style="width: 100%; font-size: 13px;">
                    <tr><td><b>Inv #:</b> {v[1]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                    <tr><td colspan="2"><b>Patient:</b> {v[3]}</td></tr>
                    <tr><td><b>Age/Gen:</b> {v[5]} / {v[6]}</td><td align="right"><b>Mobile:</b> {v[4]}</td></tr>
                </table>

                <div class="line"></div>
                
                <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid black;">
                        <th align="left">Description</th>
                        <th align="right">Amt</th>
                    </tr>
                    {test_rows}
                </table>

                <div class="line"></div>

                <table style="width: 100%; font-size: 14px; font-weight: bold;">
                    <tr><td>TOTAL BILL:</td><td align="right">Rs. {v[9]}</td></tr>
                    <tr style="color: green;"><td>PAID AMOUNT:</td><td align="right">Rs. {v[10]}</td></tr>
                    <tr style="background: #eee;"><td>BALANCE:</td><td align="right">Rs. {v[11]}</td></tr>
                </table>

                <div class="line"></div>
                <p style="text-align: center; font-size: 11px; margin-top: 10px;">
                    *** Software System ***<br>Developed by Zain - 03702926075
                </p>
            </div>
        </div>
        """
        
        st.markdown(receipt_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Design Error: {e}")
