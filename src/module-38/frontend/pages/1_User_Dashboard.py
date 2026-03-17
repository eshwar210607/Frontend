import streamlit as st
from pymongo import MongoClient
from datetime import datetime

if "user" not in st.session_state:
    st.stop()

client = MongoClient("YOUR_URI")
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]
permissions = db["permissions"]
logs = db["access_logs"]

user = st.session_state["user"]

# HEADER + LOGOUT
col1, col2 = st.columns([8,1])
with col1:
    st.title("🏥 User Dashboard")
with col2:
    if st.button("Logout"):
        del st.session_state["user"]
        st.switch_page("app.py")

st.write(f"Welcome {user['name']}")

# PERMISSIONS
perm_list = list(permissions.find())
perm_dict = {p["permission_name"]: p["_id"] for p in perm_list}

selected_perm = st.selectbox("Permission", list(perm_dict.keys()))
permission_id = perm_dict[selected_perm]

# ROLE DISPLAY
role_names = [roles.find_one({"_id": r})["role_name"] for r in user["roles"]]
st.write("Roles:", role_names)

# ACCESS CHECK
def check_access(user_id, permission_id):
    user = users.find_one({"_id": user_id})

    for role_id in user["roles"]:
        role = roles.find_one({"_id": role_id})

        while role:
            if permission_id in role.get("permissions", []):
                return True
            role = roles.find_one({"_id": role.get("parent_role")}) if role.get("parent_role") else None
    return False

if st.button("Check Access"):
    if check_access(user["_id"], permission_id):
        st.success("Access Granted")
    else:
        st.error("Access Denied")

if st.button("🚨 Emergency"):
    logs.insert_one({"user_id": user["_id"], "permission_id": permission_id, "status": "GRANTED"})
    st.warning("Emergency Access")

# NAVIGATION
if st.button("Profile"):
    st.switch_page("pages/4_Profile.py")