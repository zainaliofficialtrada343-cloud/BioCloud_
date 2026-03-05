import streamlit as st

def show_receipt(v):
    try:
        # Tests aur Amount ki setting
        tests = str(v[8]).split(", ")
        total_bill = float(v[9])
        per_test_amt = total_bill / len(tests) if len(tests) > 0 else 0
        
        test_rows = ""
        for t in tests:
            test_rows += f"""
            <tr style="border-bottom: 1px dashed #ddd;">
                <td style="padding: 5px 0;">{t}</td>
                <td align="right">Rs. {per_test_amt:.0f}</td>
            </tr>"""

        receipt_html = f"""
        <style>
            @media print {{
                body * {{ visibility: hidden; }}
                .main-receipt, .main-receipt * {{ visibility: visible; }}
                .main-receipt {{ position: absolute; left: 0; top: 0; width: 350px !important; }}
                header, footer, [data-testid="stSidebar"], .stButton {{ display: none !important; }}
            }}
            .main-receipt {{
                width: 320px;
                border: 2px solid black;
                padding: 15px;
                font-family: 'Courier New', Courier, monospace;
                background: white;
                color: black;
                margin: 10px auto;
            }}
            .line-dash {{ border-top: 1px dashed black; margin: 10px 0; }}
        </style>

        <div class="main-receipt">
            <div style="text-align: center;">
                <h2 style="margin:0;">( THE LIFE CARE )</h2>
                <p style="font-size:12px; margin:5px 0;">MAJEED COLONY SEC 2, KARACHI<br>0370-2926075</p>
                <div style="border:1px solid black; font-weight:bold; margin:5px 0;">PATIENT SLIP</div>
            </div>

            <table style="width: 100%; font-size: 13px;">
                <tr><td><b>Inv #:</b> {v[1]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td colspan="2"><b>Name:</b> {v[3]}</td></tr>
                <tr><td><b>Age/Sex:</b> {v[5]}/{v[6]}</td><td align="right"><b>Mob:</b> {v[4]}</td></tr>
            </table>

            <div class="line-dash"></div>
            <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid black;">
                    <th align="left">Test Name</th>
                    <th align="right">Amt</th>
                </tr>
                {test_rows}
            </table>
            <div class="line-dash"></div>

            <table style="width: 100%; font-size: 14px; font-weight: bold;">
                <tr><td>TOTAL BILL:</td><td align="right">Rs. {v[9]}</td></tr>
                <tr><td>PAID:</td><td align="right">Rs. {v[10]}</td></tr>
                <tr style="background:#eee;"><td>BALANCE:</td><td align="right">Rs. {v[11]}</td></tr>
            </table>

            <div class="line-dash"></div>
            <p style="text-align: center; font-size: 10px;">Developed by Zain - 03702926075</p>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Design Error: {e}")
