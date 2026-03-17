import streamlit as st
import requests

st.title("🏥 RBAC System - Hospital Access Control")

st.header("Check User Access")

user_id = st.number_input("Enter User ID", min_value=1, step=1)
permission_id = st.number_input("Enter Permission ID", min_value=1, step=1)

if st.button("Check Access"):
    response = requests.post(
        "http://127.0.0.1:5000/check-access",
        json={"user_id": user_id, "permission_id": permission_id}
    )

    if response.status_code == 200:
        result = response.json()
        if result["access"]:
            st.success("✅ Access Granted")
        else:
            st.error("❌ Access Denied")
    else:
        st.error("Server Error")

st.header("Access Logs")

if st.button("View Logs"):
    response = requests.get("http://127.0.0.1:5000/logs")
    if response.status_code == 200:
        logs = response.json()
        st.write(logs)
    else:
        st.error("Error fetching logs")