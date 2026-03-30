import streamlit as st
import pandas as pd

# --- 1. Dawaiyon ki list uthany ka function ---
def get_medicine_list(conn):
    try:
        df = conn.read(worksheet="medicine_db", ttl="0")
        if not df.empty:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
        return df
    except:
        # Agar sheet nahi milti toh khali table
        return pd.DataFrame(columns=["Med_Name", "Price"])

# --- 2. Main Medicine UI (Jo app.py mein dikhayega) ---
def show_medicine_section(conn):
    # AUTOMATIC CHECK: Agar session state nahi bani, toh yahan khud ban jaye gi
    if 'temp_meds' not in st.session_state:
        st.session_state.temp_meds = []

    st.markdown("---")
    st.subheader("💊 Pharmacy / Medicine Selection")
    
    mdf = get_medicine_list(conn)
    med_options = sorted(mdf["Med_Name"].unique().tolist()) if not mdf.empty else []
    med_price_dict = dict(zip(mdf["Med_Name"], mdf["Price"])) if not mdf.empty else {}

    col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1, 1, 1])
    
    selected_m = col_m1.selectbox("Select Medicine", ["--- Select ---"] + med_options)
    m_qty = col_m2.number_input("Qty", 1, 100, value=1, key="pharm_qty")
    
    # Price khud ba khud uthayega
    current_p = float(med_price_dict.get(selected_m, 0)) if selected_m != "--- Select ---" else 0.0
    m_rate = col_m3.number_input("Price", value=current_p, key="pharm_price")

    if col_m4.button("➕ Add Medicine"):
        if selected_m != "--- Select ---":
            st.session_state.temp_meds.append({
                "Med": f"{selected_m} (x{m_qty})", 
                "Price": m_rate * m_qty
            })
            st.rerun()

    # Jo dawaiyan add ho chuki hain unki list
    if st.session_state.temp_meds:
        with st.container(border=True):
            st.write("**Selected Medicines List:**")
            for i, m in enumerate(st.session_state.temp_meds):
                m_cols = st.columns([4, 1])
                m_cols[0].write(f"{i+1}. {m['Med']} — Rs. {m['Price']}")
                if m_cols[1].button("❌", key=f"del_m_{i}"):
                    st.session_state.temp_meds.pop(i)
                    st.rerun()