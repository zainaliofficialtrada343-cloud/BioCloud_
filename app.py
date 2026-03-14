# --- 4. STYLE & DESIGN (PREMIUM WEB LOOK) ---
st.markdown("""
    <style>
    /* Top Bar with blue background */
    .top-info-bar {
        background-color: #0d47a1;
        color: white;
        padding: 8px 60px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        margin: -75px -100px 0 -100px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Professional White Navbar */
    .web-nav {
        background-color: white;
        padding: 15px 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 0 -100px 30px -100px;
    }

    .nav-brand {
        font-size: 26px;
        font-weight: bold;
        color: #0d47a1;
        letter-spacing: 1px;
    }

    .nav-brand span { color: #42a5f5; }

    /* Hero Section */
    .hero-box {
        background: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), 
                    url("https://img.freepik.com/free-photo/scientist-working-with-microscope-lab_23-2148851015.jpg");
        background-size: cover;
        padding: 60px;
        border-radius: 15px;
        margin-bottom: 40px;
        border-left: 10px solid #0d47a1;
    }

    /* Stats & Action Cards */
    .modern-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        text-align: center;
        border-top: 5px solid #0d47a1;
        transition: 0.3s transform;
    }
    .modern-card:hover {
        transform: translateY(-5px);
    }

    /* Section Headings */
    .section-title {
        color: #1a237e;
        font-weight: 800;
        font-size: 28px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LANDING PAGE (HOME) ---
if menu == "🏠 Home":
    # 1. Top Mini Bar (Contact Info)
    st.markdown(f"""
        <div class="top-info-bar">
            <span>📞 Support: {st.session_state.lab_phone}</span>
            <span>📍 Location: {st.session_state.lab_name}</span>
            <span>🕒 Open: 24/7 Hours Available</span>
        </div>
    """, unsafe_allow_html=True)

    # 2. Web Navbar
    st.markdown(f"""
        <div class="web-nav">
            <div class="nav-brand">BIOCLOUD <span>LAB PRO</span></div>
            <div style="color: #555; font-weight: 500;">
                DASHBOARD &nbsp;&nbsp; | &nbsp;&nbsp; PATIENTS &nbsp;&nbsp; | &nbsp;&nbsp; REPORTS &nbsp;&nbsp; | &nbsp;&nbsp; SETTINGS
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. Hero Section
    st.markdown(f"""
        <div class="hero-box">
            <h4 style="color: #42a5f5; margin-bottom:0;">Trusted Diagnostic Excellence</h4>
            <h1 style="color: #0d47a1; font-size: 48px; margin-top:10px;">Safe & Accurate <br>Medical Reports</h1>
            <p style="color: #555; font-size: 18px; max-width: 500px;">
                Our cloud-based system ensures your lab data is secure, fast, and accessible anytime. Manage your patients with professional ease.
            </p>
            <br>
            <a href="#" style="background: #0d47a1; color: white; padding: 12px 35px; text-decoration: none; border-radius: 5px; font-weight: bold;">VIEW RECENT REPORTS</a>
        </div>
    """, unsafe_allow_html=True)

    # 4. System Statistics Section
    st.markdown('<div class="section-title">📊 Today\'s Lab Summary</div>', unsafe_allow_html=True)
    
    # Logic for metrics
    total_p = len(df[df['Date'] == today]) if not df.empty else 0
    total_cash = pd.to_numeric(df[df['Date'] == today]['Paid_Amount'], errors='coerce').sum() if not df.empty else 0
    pending_p = len(df[df['Status'] == 'Pending']) if not df.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="modern-card"><h2 style="color:#0d47a1;">{total_p}</h2><p>Patients Today</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="modern-card" style="border-top-color:#10B981;"><h2 style="color:#10B981;">Rs. {total_cash}</h2><p>Revenue Today</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="modern-card" style="border-top-color:#EF4444;"><h2 style="color:#EF4444;">{pending_p}</h2><p>Pending Reports</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="modern-card" style="border-top-color:#F59E0B;"><h2 style="color:#F59E0B;">Active</h2><p>Server Status</p></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 5. Services Shortcuts
    st.markdown('<div class="section-title">🚀 Core Management</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    
    with s1:
        if st.button("📝 Register New Patient", use_container_width=True):
             st.info("Sidebar se 'Registration' select karein.")
    with s2:
        if st.button("💰 Manage Cash/Dues", use_container_width=True):
             st.info("Sidebar se 'Dues & Reports' select karein.")
    with s3:
        if st.button("📈 View Detailed History", use_container_width=True):
             st.info("Sidebar se 'Excel History' select karein.")
