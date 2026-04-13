"""
Home Page: User registration and login.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_post, api_get

st.set_page_config(page_title="Login | Smart E-Commerce", page_icon="🏠", layout="wide")

st.markdown("## 🏠 Welcome")

tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

with tab1:
    st.markdown("### 🔑 Login")
    email = st.text_input("Email", placeholder="e.g., mahekmistry@gmail.com")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("🔑 Login", type="primary"):
        if email and password:
            result = api_post("/auth/login", {"email": email, "password": password})
            if "error" not in result and "detail" not in result:
                st.session_state["user"] = result.get("user", {})
                st.session_state["token"] = result.get("access_token", "")
                st.success(f"✅ Welcome back, {result['user']['name']}!")
                st.json(result["user"])
            else:
                st.error(f"Login failed: {result.get('detail', result.get('error', 'Invalid credentials'))}")
        else:
            st.warning("Please enter email and password")

    st.markdown("---")
    st.markdown("**Demo Accounts:**")
    st.markdown("""
<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef;">
    <strong>Admin:</strong><br>
    • mahekmistry@gmail.com / password123<br>
    • anushkanaik@gmail.com / password123<br>
    • sohamhande@gmail.com / password123<br>
    <br>
    <strong>User:</strong><br>
    • rahul@example.com / password123<br>
    • priya@example.com / password123
</div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📝 Register New Account")
    reg_name = st.text_input("Full Name", placeholder="e.g., John Doe")
    reg_email = st.text_input("Email Address", placeholder="e.g., john@example.com", key="reg_email")
    reg_phone = st.text_input("Phone", placeholder="e.g., 9876543210")
    reg_password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("📝 Register", type="primary"):
        if reg_name and reg_email and reg_password:
            result = api_post("/auth/register", {
                "name": reg_name,
                "email": reg_email,
                "phone": reg_phone,
                "password": reg_password,
            })
            if "error" not in result and "detail" not in result:
                st.success(f"✅ Account created for {result['user']['name']}!")
                st.json(result["user"])
            else:
                st.error(f"Registration failed: {result.get('detail', result.get('error', ''))}")
        else:
            st.warning("Please fill all required fields")
