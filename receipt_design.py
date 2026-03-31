import streamlit as st
import streamlit.components.v1 as components
import os

def show_receipt(v):
    try:
        # Template file read karein
        if not os.path.exists('receipt_template.html'):
            st.error("Error: receipt_template.html file nahi mili!")
            return

        with open('receipt_template.html', 'r') as f:
            html_template = f.read()

        # Items list tayyar karein
        tests = str(v[8]).replace("Tests: ", "").replace("Meds: ", "").replace(" | ", ", ").split(", ")
        items_html = ""
        for t in tests:
            if t.strip():
                items_html += f"<tr><td>{t}</td><td align='right'>-</td></tr>"

        # Data replace karein (Bina kisi % ya complex formatting ke)
        final_html = html_template.replace("{{ token }}", str(v[0])) \
                                   .replace("{{ patient }}", str(v[3])) \
                                   .replace("{{ inv }}", str(v[1])) \
                                   .replace("{{ age_gen }}", f"{v[5]} / {v[6]}") \
                                   .replace("{{ date }}", str(v[2])) \
                                   .replace("{{ mobile }}", str(v[4])) \
                                   .replace("{{ ref }}", str(v[7]) if v[7] else "SELF") \
                                   .replace('{% for item in items %}\n            <tr><td>{{ item }}</td><td align="right">-</td></tr>\n            {% endfor %}', items_html) \
                                   .replace("{{ total }}", str(v[9])) \
                                   .replace("{{ paid }}", str(v[10])) \
                                   .replace("{{ balance }}", str(v[11]))

        # Final Render
        components.html(final_html, height=550, scrolling=True)

    except Exception as e:
        st.error(f"Design Error: {e}")