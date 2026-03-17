import streamlit as st
from pymongo import MongoClient

if "user" not in st.session_state:
    st.stop()

client = MongoClient("YOUR_URI")
db = client["rbac_db"]

roles = db["roles"]

user = st.session_state["user"]

# CHECK ADMIN
role_names = [roles.find_one({"_id": r})["role_name"] for r in user["roles"]]

if "Admin" not in role_names:
    st.error("Access Denied - Admin Only")
    st.stop()

# HEADER
col1, col2 = st.columns([8,1])
with col1:
    st.title("🛠 Admin Dashboard")
with col2:
    if st.button("Logout"):
        del st.session_state["user"]
        st.switch_page("app.py")

# ADD ROLE
role_name = st.text_input("New Role")

if st.button("Add Role"):
    roles.insert_one({"role_name": role_name, "permissions": []})
    st.success("Role Added")