import streamlit as st
import streamlit.components.v1 as components
import os

def show_receipt(v):
    try:
        # Check if template exists
        if not os.path.exists('receipt_template.html'):
            st.error("Template file nahi mili! Please 'receipt_template.html' banayein.")
            return

        with open('receipt_template.html', 'r') as f:
            html_template = f.read()

        # Items handle karein
        raw_data = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ")
        items_list = raw_data.split(", ")
        items_html = ""
        for item in items_list:
            if item.strip():
                items_html += f"<tr><td>{item.strip()}</td><td align='center'>1</td><td align='right'>-</td></tr>"

        # Data Replace Logic
        final_html = html_template.replace("{{ token }}", str(v[0])) \
                                   .replace("{{ patient }}", str(v[3])) \
                                   .replace("{{ inv }}", str(v[1])) \
                                   .replace("{{ age_gen }}", f"{v[5]} / {v[6]}") \
                                   .replace("{{ date }}", str(v[2])) \
                                   .replace("{{ mobile }}", str(v[4])) \
                                   .replace("{{ ref }}", str(v[7]) if v[7] else "SELF") \
                                   .replace("{{ items_rows }}", items_html) \
                                   .replace("{{ total }}", str(v[9])) \
                                   .replace("{{ paid }}", str(v[10])) \
                                   .replace("{{ balance }}", str(v[11]))

        # Render the receipt
        # Height 650px rakhi hai taake slip poori nazar aaye
        components.html(final_html, height=650, scrolling=True)

    except Exception as e:
        st.error(f"Design Error: {e}")