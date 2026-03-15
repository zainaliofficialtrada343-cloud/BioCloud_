import streamlit as st
import pandas as pd

def test_settings_page(conn):
    st.header("🧪 Test Master Management")
    
    # Google Sheet se data load karna
    try:
        master_df = conn.read(worksheet="master_tests_db", ttl="0")
    except:
        master_df = pd.DataFrame(columns=["Test_Name", "Normal_Range", "Unit", "Category"])

    tab1, tab2, tab3 = st.tabs(["🔍 Search Tests", "➕ Manual Add", "⬆️ Bulk Tools"])

    with tab1:
        search_term = st.text_input("Search Test (e.g. HbA1C, Glucose)...")
        if search_term:
            filtered_df = master_df[master_df['Test_Name'].str.contains(search_term, case=False, na=False)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.write("Top 10 Tests:")
            st.dataframe(master_df.head(10), use_container_width=True)
            st.info(f"Total Tests in Database: {len(master_df)}")

    with tab2:
        # Naya test ya purane ko update karne ka form
        with st.form("edit_test_form"):
            t_name = st.selectbox("Select Test to Edit/Add", ["New Test"] + list(master_df['Test_Name'].unique()))
            input_name = st.text_input("Test Name", value="" if t_name == "New Test" else t_name)
            t_range = st.text_input("Normal Range (e.g. 70-110)")
            t_unit = st.text_input("Unit (e.g. mg/dL)")
            
            if st.form_submit_button("Save Changes"):
                # Logic to update Google Sheet
                new_row = pd.DataFrame([[input_name, t_range, t_unit]], columns=["Test_Name", "Normal_Range", "Unit"])
                # Agar pehle se hai toh purana delete karke naya add karein
                updated_df = master_df[master_df['Test_Name'] != input_name]
                updated_df = pd.concat([updated_df, new_row], ignore_index=True)
                conn.update(worksheet="master_tests_db", data=updated_df)
                st.success(f"Data for {input_name} updated!")
                st.rerun()

    with tab3:
        st.subheader("Bulk Import")
        st.write("Aapke pas 1500 tests ki list hai. Kya aap unhein database mein dalna chahte hain?")
        
        if st.button("🚀 Load 1500+ Test Names into Database"):
            # Jo list aap ne mujhe di, usko array mein convert karke yahan dala ja sakta hai
            # Filhal main sample code de raha hoon
            raw_list = ["DLC", "RBCCount", "Eosinophil Count", "Platelet Count"] # Ismein poori list dal jaye gi
            existing_names = master_df['Test_Name'].tolist()
            new_names = [x for x in raw_list if x not in existing_names]
            
            if new_names:
                bulk_df = pd.DataFrame({'Test_Name': new_names})
                final_df = pd.concat([master_df, bulk_df], ignore_index=True)
                conn.update(worksheet="master_tests_db", data=final_df)
                st.success(f"{len(new_names)} naye tests add ho gaye!")
            else:
                st.warning("Koi naya test nahi mila.")