import streamlit as st
from pymongo import MongoClient

# 🔒 Login Check
if "user" not in st.session_state:
    st.stop()

# 🔌 DB
client = MongoClient("mongodb+srv://eash210607_db_user:student123@cluster1.4aahrue.mongodb.net/rbac_db?retryWrites=true&w=majority")
db = client["rbac_db"]

roles = db["roles"]
permissions = db["permissions"]
users = db["users"]

user = st.session_state["user"]

# 🔷 CHECK ADMIN
role_names = [roles.find_one({"_id": r})["role_name"] for r in user["roles"]]

if "Admin" not in role_names:
    st.error("❌ Access Denied - Admin Only")
    st.stop()

# 🔷 HEADER
col1, col2 = st.columns([8,1])
with col1:
    st.title("🛠 Admin Dashboard")
with col2:
    if st.button("Logout"):
        del st.session_state["user"]
        st.switch_page("app.py")

# ================= ROLE MANAGEMENT =================
st.subheader("➕ Add New Role")

role_name = st.text_input("Role Name")

if st.button("Add Role"):
    roles.insert_one({
        "role_name": role_name,
        "permissions": [],
        "parent_role": None
    })
    st.success("Role Added ✅")

# ================= PERMISSION ASSIGN =================
st.subheader("🔐 Assign Permissions")

role_list = list(roles.find())
role_dict = {r["role_name"]: r["_id"] for r in role_list}

selected_role = st.selectbox("Select Role", list(role_dict.keys()))
role_id = role_dict[selected_role]

perm_list = list(permissions.find())
perm_dict = {p["permission_name"]: p["_id"] for p in perm_list}

selected_perms = st.multiselect("Select Permissions", list(perm_dict.keys()))

if st.button("Update Permissions"):
    perm_ids = [perm_dict[p] for p in selected_perms]

    roles.update_one(
        {"_id": role_id},
        {"$set": {"permissions": perm_ids}}
    )

    st.success("Permissions Updated ✅")

# ================= VIEW USERS =================
st.subheader("👥 All Users")

user_data = list(users.find({}, {"_id": 0}))
st.dataframe(user_data)