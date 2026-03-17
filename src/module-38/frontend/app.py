import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# MongoDB Connection
MONGO_URI = "mongodb+srv://eash210607_db_user:student123@cluster1.4aahrue.mongodb.net/rbac_db?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]
permissions = db["permissions"]
logs = db["access_logs"]

st.title("🏥 Advanced RBAC System")

# 🔷 Fetch Users
user_list = list(users.find())
user_dict = {u["name"]: u["_id"] for u in user_list}

selected_user = st.selectbox("Select User", list(user_dict.keys()))
user_id = user_dict[selected_user]

# 🔷 Fetch Permissions
perm_list = list(permissions.find())
perm_dict = {p["permission_name"]: p["_id"] for p in perm_list}

selected_perm = st.selectbox("Select Permission", list(perm_dict.keys()))
permission_id = perm_dict[selected_perm]

# 🔷 Show Roles
st.subheader("User Roles")

user = users.find_one({"_id": user_id})
role_names = []

for r_id in user["roles"]:
    role = roles.find_one({"_id": r_id})
    role_names.append(role["role_name"])

st.write(role_names)

# 🔷 Role Hierarchy Check
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

# 🔷 Access Button
if st.button("Check Access"):
    access = check_access(user_id, permission_id)

    if access:
        st.success("✅ Access Granted")
        logs.insert_one({
            "user_id": user_id,
            "permission_id": permission_id,
            "status": "GRANTED",
            "time": datetime.now()
        })
    else:
        st.error("❌ Access Denied")
        logs.insert_one({
            "user_id": user_id,
            "permission_id": permission_id,
            "status": "DENIED",
            "time": datetime.now()
        })

# 🔷 Emergency Access
if st.button("🚨 Emergency Access"):
    logs.insert_one({
        "user_id": user_id,
        "permission_id": permission_id,
        "status": "GRANTED",
        "emergency": True,
        "time": datetime.now()
    })
    st.warning("⚠ Emergency Access Granted")

# 🔷 Logs Table
st.subheader("Access Logs")

if st.button("Show Logs"):
    data = list(logs.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    st.dataframe(df)