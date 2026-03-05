import streamlit as st
import streamlit.components.v1 as components

def show_receipt(v):
    try:
        # Data taiyar karna
        tests = str(v[8]).split(", ")
        total_bill = v[9]
        paid = v[10]
        balance = v[11]
        
        test_rows = ""
        for t in tests:
            test_rows += f"<tr><td style='padding:5px;'>{t}</td><td align='right'>-</td></tr>"

        # Mukammal HTML Slip
        receipt_html = f"""
        <html>
        <head>
            <style>
                @media print {{
                    @page {{ size: 80mm 200mm; margin: 0; }}
                    body {{ margin: 0; padding: 0; }}
                    .btn-print {{ display: none !important; }}
                }}
                body {{ font-family: 'Courier New', monospace; width: 300px; margin: auto; padding: 10px; }}
                .receipt-card {{ border: 1px solid #000; padding: 10px; }}
                .header {{ text-align: center; border-bottom: 2px solid #000; margin-bottom: 10px; }}
                .btn-print {{ 
                    background: #007bff; color: white; border: none; 
                    padding: 10px 20px; width: 100%; cursor: pointer; margin-bottom: 10px;
                    font-weight: bold; border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <button class="btn-print" onclick="window.print()">PRINT RECEIPT (SLIP)</button>
            <div class="receipt-card">
                <div class="header">
                    <h2 style="margin:0;">THE LIFE CARE</h2>
                    <small>MAJEED COLONY SEC 2, KARACHI</small><br>
                    <small>0370-2926075</small>
                </div>
                
                <table style="width:100%; font-size:12px;">
                    <tr><td><b>Inv:</b> {v[1]}</td><td align="right">{v[2]}</td></tr>
                    <tr><td colspan="2"><b>Name:</b> {v[3]}</td></tr>
                    <tr><td><b>Age/Sex:</b> {v[5]}/{v[6]}</td><td align="right">{v[4]}</td></tr>
                </table>
                <hr>
                <table style="width:100%; font-size:13px; border-collapse: collapse;">
                    <thead><tr style="border-bottom:1px solid #000;"><th align="left">Test</th><th align="right">Amt</th></tr></thead>
                    {test_rows}
                </table>
                <hr>
                <table style="width:100%; font-size:14px; font-weight:bold;">
                    <tr><td>TOTAL:</td><td align="right">Rs. {total_bill}</td></tr>
                    <tr><td>PAID:</td><td align="right">Rs. {paid}</td></tr>
                    <tr style="background:#eee;"><td>BAL:</td><td align="right">Rs. {balance}</td></tr>
                </table>
                <p style="text-align:center; font-size:10px; margin-top:20px;">Developed by Zain</p>
            </div>
        </body>
        </html>
        """
        # Ye line HTML ko sahi se dikhayegi
        components.html(receipt_html, height=600, scrolling=True)

    except Exception as e:
        st.error(f"Design Error: {e}")
