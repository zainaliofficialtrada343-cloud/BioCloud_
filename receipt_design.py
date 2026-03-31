import streamlit as st
import streamlit.components.v1 as components

def show_receipt(v):
    try:
        # Variables ko pehle hi nikal lein taake niche koi gadbad na ho
        lab_name = "JAWAD MEDICAL CENTER"
        p_name = str(v[3])
        inv_no = str(v[1])
        token_no = str(v[0])
        age_gen = f"{v[5]} / {v[6]}"
        date_val = str(v[2])
        mobile = str(v[4])
        ref_by = str(v[7]) if v[7] else "SELF"
        total = str(v[9])
        paid = str(v[10])
        balance = str(v[11])
        
        # Items ki list tayaar karein
        items_list = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ").split(", ")
        items_rows = ""
        for item in items_list:
            if item.strip():
                items_rows += f"<tr><td>{item}</td><td align='right'>-</td></tr>"

        # Poora HTML code ek string mein
        # Ismein hum f-string ke bajaye % use kar rahe hain taake CSS ke { } se clash na ho
        html_code = """
        <html>
        <head>
            <style>
                body { font-family: 'Courier New', monospace; background: white; color: black; margin: 0; padding: 10px; }
                .receipt-container { width: 300px; border: 2px solid black; padding: 10px; margin: auto; }
                .header-title { text-align: center; margin: 0; font-size: 20px; font-weight: bold; }
                .header-sub { text-align: center; font-size: 11px; margin: 2px 0; }
                .token-box { text-align: center; border: 1px solid black; margin: 10px 0; padding: 5px; font-size: 18px; font-weight: bold; }
                table { width: 100%; font-size: 12px; margin-top: 5px; }
                .items-table { border-top: 2px solid black; border-bottom: 2px solid black; margin-top: 10px; padding: 5px 0; }
                .total-section { margin-top: 10px; font-weight: bold; border-top: 1px solid black; padding-top: 5px; }
                @media print { .no-print { display: none; } }
            </style>
        </head>
        <body>
            <div class="receipt-container">
                <div class="header-title">%(lab)s</div>
                <div class="header-sub">MAJEED COLONY SEC 2, KARACHI</div>
                <div class="header-sub">0370-2906075</div>
                
                <div class="token-box">TOKEN NO: %(token)s</div>
                
                <table>
                    <tr><td><b>Patient:</b> %(patient)s</td><td align="right"><b>Inv:</b> %(inv)s</td></tr>
                    <tr><td><b>Age/Gen:</b> %(age)s</td><td align="right"><b>Date:</b> %(date)s</td></tr>
                    <tr><td><b>Mobile:</b> %(mob)s</td><td align="right"><b>Ref:</b> %(ref)s</td></tr>
                </table>

                <table class="items-table">
                    <tr><th align="left">Description</th><th align="right">Amt</th></tr>
                    %(rows)s
                </table>

                <div class="total-section">
                    <div style="display:flex; justify-content:space-between"><span>Total:</span><span>Rs. %(total)s</span></div>
                    <div style="display:flex; justify-content:space-between"><span>Paid:</span><span>Rs. %(paid)s</span></div>
                    <div style="display:flex; justify-content:space-between; background:#eee; padding:2px; border:1px solid #000; margin-top:3px;">
                        <span>Balance:</span><span>Rs. %(bal)s</span>
                    </div>
                </div>
                
                <p style="text-align:center; font-size:9px; margin-top:10px;">Developed by Zain - 03702906075</p>
                
                <button class="no-print" onclick="window.print()" style="width:100%%; margin-top:10px; cursor:pointer; padding:5px;">
                    Print Receipt
                </button>
            </div>
        </body>
        </html>
        """ % {
            "lab": lab_name, "token": token_no, "patient": p_name, "inv": inv_no,
            "age": age_gen, "date": date_val, "mob": mobile, "ref": ref_by,
            "rows": items_rows, "total": total, "paid": paid, "bal": balance
        }

        # Components use karne se code nazar nahi aayega, sirf receipt dikhegi
        components.html(html_code, height=550, scrolling=True)

    except Exception as e:
        st.error(f"Design Error: {e}")