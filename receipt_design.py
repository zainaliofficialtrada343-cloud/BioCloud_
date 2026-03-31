import streamlit as st

def show_receipt(v):
    try:
        # 1. CSS ko simple string mein rakha (f-string use nahi ki taake brackets ka masla na ho)
        css_code = """
        <style>
            @media print {
                @page { size: auto; margin: 0mm; }
                body { background: white !important; margin: 0 !important; padding: 0 !important; }
                header, footer, .sidebar, [data-testid="stSidebar"], [data-testid="stHeader"], .stButton {
                    display: none !important;
                }
                .receipt-container {
                    width: 350px !important; border: none !important; margin: 0 !important;
                    padding: 10px !important; visibility: visible !important;
                    position: absolute; left: 0; top: 0;
                }
                body * { visibility: hidden; }
                .receipt-container, .receipt-container * { visibility: visible !important; }
            }
            .receipt-container {
                width: 350px; border: 2px solid #000; padding: 15px;
                font-family: 'Courier New', Courier, monospace;
                margin: 20px auto; background: white; color: black;
            }
            .header-title { text-align: center; margin: 0; font-size: 22px; font-weight: 900; text-transform: uppercase; }
            .header-sub { text-align: center; font-size: 12px; font-weight: bold; margin: 2px 0; }
            .token-box { text-align: center; border: 1px solid #000; margin: 10px 0; padding: 5px; font-size: 18px; font-weight: bold; }
        </style>
        """

        # 2. Variable set karein (JAWAD MEDICAL CENTER fix kar diya)
        lab_name = "JAWAD MEDICAL CENTER"
        
        # 3. HTML structure (Sirf is hisse mein f-string use ki hai)
        html_body = f"""
        <div class="receipt-container">
            <h2 class="header-title">{lab_name}</h2>
            <p class="header-sub">MAJEED COLONY SEC 2, KARACHI</p>
            <p class="header-sub">0370-2906075</p>
            
            <div class="token-box">TOKEN NO: {v[0]}</div>
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

        # Tests loop
        tests_list = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ").split(", ")
        for t in tests_list:
            if t.strip():
                html_body += f"<tr><td>{t}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        html_body += f"""
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

        # 4. Final Output (CSS aur Body ko jod kar)
        st.markdown(css_code + html_body, unsafe_allow_html=True)
        
        # 5. Print Button
        st.button("Print Slip (Ctrl+P)", key=f"print_{v[1]}")

    except Exception as e:
        st.error(f"Receipt Design Error: {e}")