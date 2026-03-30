import streamlit as st
import streamlit.components.v1 as components

def show_receipt(v):
    try:
        # Data preparation (Citing user's data structure)
        patient_id = v[0]
        inv_no = v[1]
        date_str = v[2]
        p_name = v[3]
        mobile = v[4]
        age_gen = f"{v[5]} / {v[6]}"
        ref_by = v[7] if len(v) > 7 else "SELF"
        
        # Tests aur Meds ko clean dikhane ke liye
        raw_items = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")

        receipt_html = f"""
        <div id="receipt" style="width: 320px; border: 2px solid #000; padding: 10px; font-family: 'Courier New', Courier, monospace; background: white; color: black; margin: auto;">
            <h2 style="text-align: center; margin: 0; font-size: 20px; font-weight: 900; text-transform: uppercase;">JAWAD MEDICAL CENTER</h2>
            <p style="text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0;">MAJEED COLONY SEC 2, KARACHI</p>
            <p style="text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0;">0370-2906075</p>
            
            <div style="text-align: center; border: 2px solid #000; margin: 5px 0; padding: 5px; font-size: 18px; font-weight: bold;">
                TOKEN NO: {patient_id}
            </div>

            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 11px; line-height: 1.4;">
                <tr><td><b>Patient:</b> {p_name}</td><td align="right"><b>Inv:</b> {inv_no}</td></tr>
                <tr><td><b>Age/Gen:</b> {age_gen}</td><td align="right"><b>Date:</b> {date_str}</td></tr>
                <tr><td colspan="2"><b>Ref By:</b> {ref_by}</td></tr>
                <tr><td><b>Mobile:</b> {mobile}</td><td align="right"><b>Lab Box:</b> ____</td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 12px;">
                <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;">
                    <th align="left">Description</th>
                    <th align="center">Qty</th>
                    <th align="right">Amt</th>
                </tr>
        """

        # Description list setup
        items_list = raw_items.split(", ")
        for item in items_list:
            if item.strip():
                receipt_html += f"<tr><td>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        receipt_html += f"""
            </table>

            <div style="margin-top: 10px; border-top: 2px solid #000; padding-top: 5px; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;"><span>Total:</span> <span>Rs. {v[9]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Paid:</span> <span>Rs. {v[10]}</span></div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; background: #eee; padding: 2px; border: 1px solid #000;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 15px;">Developed by Zain - 03702906075</p>
        </div>
        """

        # Yeh line code ko hide karke sirf design dikhayegi
        components.html(receipt_html, height=500, scrolling=True)
        
        if st.button("Confirm & Print"):
             st.info("Please use browser print (Ctrl+P) after seeing the receipt above.")

    except Exception as e:
        st.error(f"Receipt Error: {e}")