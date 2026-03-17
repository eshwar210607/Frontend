import streamlit as st
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://eash210607_db_user:student123@cluster1.4aahrue.mongodb.net/rbac_db?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]
logs = db["access_logs"]

st.title("🏥 RBAC System")

# Access Check
st.header("Check User Access")

user_id = st.number_input("User ID", min_value=1, step=1)
permission_id = st.number_input("Permission ID", min_value=1, step=1)

if st.button("Check Access"):
    user = users.find_one({"_id": user_id})

    if not user:
        st.error("User not found")
    else:
        access = False

        for role_id in user["roles"]:
            role = roles.find_one({"_id": role_id})

            if role and permission_id in role.get("permissions", []):
                access = True
                break

        if access:
            st.success("✅ Access Granted")
            logs.insert_one({
                "user_id": user_id,
                "permission_id": permission_id,
                "status": "GRANTED"
            })
        else:
            st.error("❌ Access Denied")
            logs.insert_one({
                "user_id": user_id,
                "permission_id": permission_id,
                "status": "DENIED"
            })

# Logs
st.header("Access Logs")

if st.button("Show Logs"):
    data = list(logs.find({}, {"_id": 0}))
    st.write(data)