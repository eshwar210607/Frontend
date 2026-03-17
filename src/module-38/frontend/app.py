import streamlit as st
from pymongo import MongoClient

# 🔷 PAGE CONFIG
st.set_page_config(page_title="RBAC System", layout="centered")

# 🔷 UI STYLE
st.markdown("""
<style>
.stApp { background: linear-gradient(to right, #eef2f3, #dfe9f3); }
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 🔷 SECURE DATABASE CONNECTION (IMPORTANT 🔐)
MONGO_URI = st.secrets["MONGO_URI"]   # <-- CHANGED HERE
client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]

# 🔷 TITLE
st.title("🔐 RBAC System")

menu = st.radio("Choose", ["Login", "Signup"], horizontal=True)

# ================= LOGIN =================
if menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users.find_one({"email": email, "password": password})

        if user:
            st.session_state["user"] = user

            # 🔷 GET ROLE NAMES
            role_ids = user.get("roles", [])
            role_names = [
                roles.find_one({"_id": r})["role_name"]
                for r in role_ids if roles.find_one({"_id": r})
            ]

            # 🔷 ROLE BASED REDIRECT
            if "Admin" in role_names:
                st.switch_page("pages/2_Admin_Dashboard.py")
            else:
                st.switch_page("pages/1_Doctor_Dashboard.py")

        else:
            st.error("Invalid Credentials ❌")

# ================= SIGNUP =================
else:
    st.subheader("Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # 🔷 FETCH ROLES DYNAMICALLY
    role_list = list(roles.find())
    role_names = [r["role_name"] for r in role_list if r["role_name"] != "Admin"]

    role_option = st.selectbox("Select Role", role_names)

    if st.button("Signup"):
        if not name or not email or not password:
            st.warning("Please fill all fields")
        elif users.find_one({"email": email}):
            st.warning("User already exists")
        else:
            role = roles.find_one({"role_name": role_option})

            users.insert_one({
                "name": name,
                "email": email,
                "password": password,
                "roles": [role["_id"]] if role else []
            })

            st.success("Account Created ✅")