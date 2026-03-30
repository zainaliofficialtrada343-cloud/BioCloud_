import streamlit as st
import streamlit.components.v1 as components

def show_receipt(v):
    try:
        # 1. Lab Settings se data uthana
        l_name = st.session_state.get('lab_name', 'JAWAD MEDICAL CENTER')
        l_addr = st.session_state.get('lab_addr', 'MAJEED COLONY SEC 2, KARACHI')
        l_phone = st.session_state.get('lab_phone', '0370-2906075')

        # 2. Details (Tests + Meds) ki list taiyar karna
        details_raw = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_list = details_raw.split(", ")
        
        items_tr = ""
        for item in items_list:
            if item.strip():
                items_tr += f"<tr><td style='padding:2px;'>{item}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        # 3. Design String (Bilkul purana style aur pixels)
        html_content = f"""
        <div style="width: 310px; border: 2px solid #000; padding: 10px; font-family: 'Courier New', Courier, monospace; background: white; color: black; margin: auto;">
            <h2 style="text-align: center; margin: 0; font-size: 18px; font-weight: 900; text-transform: uppercase;">{l_name}</h2>
            <p style="text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0;">{l_addr}</p>
            <p style="text-align: center; font-size: 11px; font-weight: bold; margin: 2px 0;">{l_phone}</p>
            
            <div style="text-align: center; border: 2px solid #000; margin: 10px 0; padding: 5px; font-size: 16px; font-weight: bold;">
                TOKEN NO: {v[0]}
            </div>

            <hr style="border: 1px solid #000;">
            
            <table style="width: 100%; font-size: 11px; line-height: 1.4;">
                <tr><td><b>Patient:</b> {v[3]}</td><td align="right"><b>Inv:</b> {v[1]}</td></tr>
                <tr><td><b>Age/Gen:</b> {v[5]}/{v[6]}</td><td align="right"><b>Date:</b> {v[2]}</td></tr>
                <tr><td><b>Ref By:</b> {v[7] if len(v)>7 else 'SELF'}</td><td align="right"><b>Lab Box:</b> ____</td></tr>
                <tr><td><b>Mobile:</b> {v[4]}</td><td></td></tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px;">
                <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;">
                    <th align="left">Description</th>
                    <th align="center">Qty</th>
                    <th align="right">Amt</th>
                </tr>
                {items_tr}
            </table>

            <div style="margin-top: 15px; border-top: 2px solid #000; padding-top: 5px; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;"><span>Total:</span> <span>Rs. {v[9]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Paid:</span> <span>Rs. {v[10]}</span></div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; background: #eee; padding: 2px; border: 1px solid #000;">
                    <span>Balance:</span> <span>Rs. {v[11]}</span>
                </div>
            </div>
            <p style="text-align: center; font-size: 9px; margin-top: 20px;">Developed by Zain - 03702906075</p>
        </div>
        """

        # 4. YEH HAI ASLI SOLUTION:
        # st.markdown use nahi karna, components use karna hai
        components.html(html_content, height=550, scrolling=True)
        
    except Exception as e:
        st.error(f"Design Error: {e}")