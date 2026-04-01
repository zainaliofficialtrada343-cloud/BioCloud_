import streamlit as st
import pandas as pd

# --- 1. Doctors load karne ka function ---
def get_doctor_list(conn):
    try:
        df = conn.read(worksheet="doctors_db", ttl="0")
        return df["Doctor_Name"].tolist() if not df.empty else []
    except:
        return []

# --- 2. Medicines load karne ka function ---
def get_medicine_list(conn):
    try:
        df = conn.read(worksheet="meds_db", ttl="0")
        if not df.empty:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame(columns=["Medicine_Name", "Price"])

# --- Main UI Section ---
def show_medicine_section(conn):
    # Session state for medicines list
    if 'temp_meds' not in st.session_state:
        st.session_state.temp_meds = []
    
    # Doctor selection state
    if 'selected_dr_name' not in st.session_state:
        st.session_state.selected_dr_name = "Self"

    st.markdown("---")
    
    # --- DOCTOR SELECTION BOX ---
    st.subheader("👨‍⚕️ Select Doctor")
    dr_options = get_doctor_list(conn)
    
    # Ye wo box hai jahan se aap Doctor select karenge
    selected_dr = st.selectbox(
        "Referring Doctor", 
        ["Self"] + dr_options, 
        key="dr_selector"
    )
    st.session_state.selected_dr_name = selected_dr # Isko slip ke liye save kar liya

    st.subheader("💊 Pharmacy / Medicine Selection")
    
    mdf = get_medicine_list(conn)
    med_options = sorted(mdf["Medicine_Name"].unique().tolist()) if not mdf.empty else []
    med_price_dict = dict(zip(mdf["Medicine_Name"], mdf["Price"])) if not mdf.empty else {}

    col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1, 1, 1])
    
    selected_m = col_m1.selectbox("Select Medicine", ["--- Select ---"] + med_options)
    m_qty = col_m2.number_input("Qty", 1, 100, value=1, key="pharm_qty")
    
    current_p = float(med_price_dict.get(selected_m, 0)) if selected_m != "--- Select ---" else 0.0
    m_rate = col_m3.number_input("Price", value=current_p, key="pharm_price")

    if col_m4.button("➕ Add Medicine"):
        if selected_m != "--- Select ---":
            st.session_state.temp_meds.append({
                "Med": f"{selected_m} (x{m_qty})", 
                "Price": m_rate * m_qty
            })
            st.rerun()

    # Display added medicines
    if st.session_state.temp_meds:
        with st.container(border=True):
            st.write(f"**Selected Items (Dr. {st.session_state.selected_dr_name}):**")
            for i, m in enumerate(st.session_state.temp_meds):
                m_cols = st.columns([4, 1])
                m_cols[0].write(f"{i+1}. {m['Med']} — Rs. {m['Price']}")
                if m_cols[1].button("❌", key=f"del_m_{i}"):
                    st.session_state.temp_meds.pop(i)
                    st.rerun()