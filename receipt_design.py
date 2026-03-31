import streamlit as st
import streamlit.components.v1 as components

def show_receipt(v):
    try:
        # 1. Variables ko setup karain
        lab_name = "JAWAD MEDICAL CENTER"
        p_name = v[3]
        inv_no = v[1]
        token_no = v[0]
        
        # 2. Poora HTML aur CSS ek saath (Bina kisi Python bracket tension ke)
        # Maine CSS ko seedha yahan daal diya hai
        receipt_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Courier New', monospace; margin: 0; padding: 10px; color: black; background: white; }}
                .receipt-container {{ width: 320px; border: 2px solid black; padding: 10px; margin: auto; }}
                .header-title {{ text-align: center; margin: 0; font-size: 20px; font-weight: bold; text-transform: uppercase; }}
                .header-sub {{ text-align: center; font-size: 11px; margin: 2px 0; font-weight: bold; }}
                .token-box {{ text-align: center; border: 1px solid black; margin: 10px 0; padding: 5px; font-size: 16px; font-weight: bold; }}
                table {{ width: 100%; font-size: 12px; border-collapse: collapse; }}
                .items-table {{ border-top: 2px solid black; border-bottom: 2px solid black; margin-top: 10px; }}
                .total-section {{ margin-top: 10px; border-top: 1px solid black; font-weight: bold; }}
                @media print {{
                    .print-btn {{ display: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="receipt-container">
                <div class="header-title">{lab_name}</div>
                <div class="header-sub">MAJEED COLONY SEC 2, KARACHI</div>
                <div class="header-sub">0370-2906075</div>
                
                <div class="token-box">TOKEN NO: {token_no}</div>
                
                <table>
                    <tr><td><b>Patient:</b> {p_name}</td><td align="right"><b>Inv:</b> {inv_no}</td></tr>
                    <tr><td><b>Age/Gen:</b> {v[5]} / {v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                    <tr><td><b>Mobile:</b> {v[4]}</td><td align="right"><b>Ref:</b> {v[7] if v[7] else 'SELF'}</td></tr>
                </table>

                <table class="items-table">
                    <tr style="border-bottom: 1px solid black;">
                        <th align="left">Description</th>
                        <th align="center">Qty</th>
                        <th align="right">Amt</th>
                    </tr>
                    <tr>
                        <td>{v[8]}</td>
                        <td align="center">1</td>
                        <td align="right">{v[9]}</td>
                    </tr>
                </table>

                <div class="total-section">
                    <div style="display: flex; justify-content: space-between;"><span>Total:</span> <span>Rs. {v[9]}</span></div>
                    <div style="display: flex; justify-content: space-between;"><span>Paid:</span> <span>Rs. {v[10]}</span></div>
                    <div style="display: flex; justify-content: space-between; background: #eee;"><span>Balance:</span> <span>Rs. {v[11]}</span></div>
                </div>
                
                <p style="text-align: center; font-size: 9px; margin-top: 15px;">Developed by Zain - 03702906075</p>
                
                <button class="print-btn" onclick="window.print()" style="width: 100%; margin-top: 10px; padding: 5px; cursor: pointer;">
                    Print Receipt
                </button>
            </div>
        </body>
        </html>
        """

        # Yeh wo magic line hai jo aapka masla hal karegi
        # Height 600px rakhi hai taake slip poori nazar aaye
        components.html(receipt_html, height=600, scrolling=True)

    except Exception as e:
        st.error(f"Design Error: {e}")