import streamlit as st

def local_css(file_name):
    pass 

def show_login_page(authenticate_function):
    # CSS for layout and image fix
    st.markdown("""
        <style>
            /* Image height fix taake 'lamba' nazar aaye */
            .stImage img {
                height: 580px !important; 
                object-fit: cover; 
                border-radius: 25px;
                border: 2px solid #f0f2f6;
            }
            /* White space aur alignment fix karne ke liye */
            [data-testid="column"] {
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Top margin
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    # 50-50 Split
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        # ✅ High-Speed CDN Link (Yeh hamesha chalta hai)
        # Professional Lab Research Image
        img_url = "https://cdn.pixabay.com/photo/2017/02/01/13/52/analysis-2030261_1280.jpg"
        
        st.image(img_url, use_container_width=True)

    with col_right:
        # Branding
        st.markdown("<h1 style='color:#1e3a8a; font-size: 48px; margin-bottom: 0;'>🧪 BioCloud Lab</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:gray; font-size: 20px;'>Laboratory Management System</p>", unsafe_allow_html=True)
        st.write("---")
        
        # Inputs
        user = st.text_input("Username", key="login_user", placeholder="admin")
        pas = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sign In Button
        if st.button("SIGN IN TO LAB", use_container_width=True):
            if user and pas:
                authenticate_function(user, pas)
            else:
                st.error("Fields cannot be empty!")
                
        st.markdown("<p style='text-align:center; font-size:12px; color:#aaa; margin-top:80px;'>Authorized Access Only V1.0</p>", unsafe_allow_html=True)