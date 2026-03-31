import streamlit as st
import streamlit.components.v1 as components
import os

def show_receipt(v):
    try:
        if not os.path.exists('receipt_template.html'):
            st.error("receipt_template.html file missing!")
            return

        with open('receipt_template.html', 'r') as f:
            html_template = f.read()

        # Items Formatting Logic
        raw_items = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_list = raw_items.split(", ")
        
        items_html = ""
        # Agar multiple items hain to total ko filhal divide kar rahe hain ya seedha show kar rahe hain
        for item in items_list:
            if item.strip():
                items_html += f"""
                <tr>
                    <td align='left'>{item.strip().upper()}</td>
                    <td align='center'>1</td>
                    <td align='right'>RS. {v[9]}</td>
                </tr>
                """

        # Final Data Replacement
        final_html = html_template.replace("{{ token }}", str(v[0])) \
                                   .replace("{{ patient }}", str(v[3]).upper()) \
                                   .replace("{{ inv }}", str(v[1])) \
                                   .replace("{{ age_gen }}", f"{v[5]} / {v[6]}".upper()) \
                                   .replace("{{ date }}", str(v[2])) \
                                   .replace("{{ mobile }}", str(v[4])) \
                                   .replace("{{ ref }}", str(v[7]).upper() if v[7] else "LAB BOX") \
                                   .replace("{{ items_rows }}", items_html) \
                                   .replace("{{ total }}", str(v[9])) \
                                   .replace("{{ paid }}", str(v[10])) \
                                   .replace("{{ balance }}", str(v[11]))

        # Display Receipt
        components.html(final_html, height=600, scrolling=True)

    except Exception as e:
        st.error(f"Design Error: {e}")