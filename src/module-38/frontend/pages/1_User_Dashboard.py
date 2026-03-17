import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# 🔒 Login check
if "user" not in st.session_state:
    st.error("Please login first")
    st.stop()

MONGO_URI = "mongodb+srv://eash210607_db_user:student123@cluster1.4aahrue.mongodb.net/rbac_db?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]
permissions = db["permissions"]
logs = db["access_logs"]

user = st.session_state["user"]
user_id = user["_id"]

st.title("🏥 User Dashboard")
st.write(f"Welcome {user['name']}")

# Permissions dropdown
perm_list = list(permissions.find())
perm_dict = {p["permission_name"]: p["_id"] for p in perm_list}

selected_perm = st.selectbox("Select Permission", list(perm_dict.keys()))
permission_id = perm_dict[selected_perm]

# Show roles
st.subheader("Your Roles")

role_names = []
for r_id in user["roles"]:
    role = roles.find_one({"_id": r_id})
    role_names.append(role["role_name"])

st.write(role_names)

# Access logic (same as before)
def check_access(user_id, permission_id):
    user = users.find_one({"_id": user_id})

    for role_id in user["roles"]:
        current_role = roles.find_one({"_id": role_id})

        while current_role:
            if permission_id in current_role.get("permissions", []):
                return True

            parent_id = current_role.get("parent_role")
            if parent_id:
                current_role = roles.find_one({"_id": parent_id})
            else:
                break
    return False

# Buttons
if st.button("Check Access"):
    access = check_access(user_id, permission_id)

    if access:
        st.success("✅ Access Granted")
    else:
        st.error("❌ Access Denied")

if st.button("🚨 Emergency Access"):
    logs.insert_one({
        "user_id": user_id,
        "permission_id": permission_id,
        "status": "GRANTED",
        "emergency": True,
        "time": datetime.now()
    })
    st.warning("⚠ Emergency Access Granted")