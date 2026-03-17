import streamlit as st
from pymongo import MongoClient

# UI STYLE
st.set_page_config(page_title="RBAC System", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(to right, #eef2f3, #dfe9f3); }
.stButton>button { width: 100%; border-radius: 10px; height: 3em; }
</style>
""", unsafe_allow_html=True)

# DB
MONGO_URI = "mongodb+srv://eash210607_db_user:student123@cluster1.4aahrue.mongodb.net/rbac_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]

st.title("🔐 RBAC System")

menu = st.radio("Choose", ["Login", "Signup"], horizontal=True)

# LOGIN
if menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users.find_one({"email": email, "password": password})

        if user:
            st.session_state["user"] = user

            # ROLE BASED REDIRECT
            role_ids = user["roles"]
            role_names = [roles.find_one({"_id": r})["role_name"] for r in role_ids]

            if "Admin" in role_names:
                st.switch_page("pages/2_Admin_Dashboard.py")
            else:
                st.switch_page("pages/1_User_Dashboard.py")
        else:
            st.error("Invalid Credentials ❌")

# SIGNUP
else:
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role_option = st.selectbox("Role", ["User", "Admin", "Patient"])

    if st.button("Signup"):
        if users.find_one({"email": email}):
            st.warning("User already exists")
        else:
            role = roles.find_one({"role_name": role_option})

            users.insert_one({
                "name": name,
                "email": email,
                "password": password,
                "roles": [role["_id"]]
            })

            st.success("Account Created ✅")