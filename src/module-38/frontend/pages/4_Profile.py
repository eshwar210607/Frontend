import streamlit as st
from pymongo import MongoClient

if "user" not in st.session_state:
    st.stop()

client = MongoClient("YOUR_URI")
db = client["rbac_db"]

roles = db["roles"]
user = st.session_state["user"]

col1, col2 = st.columns([8,1])
with col1:
    st.title("👤 Profile")
with col2:
    if st.button("Logout"):
        del st.session_state["user"]
        st.switch_page("app.py")

st.write("Name:", user["name"])
st.write("Email:", user["email"])

role_names = [roles.find_one({"_id": r})["role_name"] for r in user["roles"]]
st.write("Roles:", role_names)