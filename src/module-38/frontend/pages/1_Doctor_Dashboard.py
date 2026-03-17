import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# 🔒 Check Login
if "user" not in st.session_state:
    st.stop()

# 🔌 DB
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]
permissions = db["permissions"]
logs = db["access_logs"]

user = st.session_state["user"]

# 🔷 HEADER + LOGOUT
# 🔷 HEADER + STYLED LOGOUT
st.markdown("""
<style>
.logout-btn button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 40px;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([8,2])

with col1:
    st.markdown("## 🏥 Doctor Dashboard")

with col2:
    if st.button("🚪 Logout", key="logout_btn"):
        del st.session_state["user"]
        st.switch_page("app.py")

st.write(f"👋 Welcome **{user['name']}**")

# 🔷 ROLES DISPLAY
role_names = [roles.find_one({"_id": r})["role_name"] for r in user["roles"]]
st.success(f"Roles: {', '.join(role_names)}")

# 🔷 STATS
st.markdown("### 📊 Quick Stats")

col1, col2, col3 = st.columns(3)
col1.metric("Total Logs", logs.count_documents({}))
col2.metric("Granted", logs.count_documents({"status": "GRANTED"}))
col3.metric("Denied", logs.count_documents({"status": "DENIED"}))

# 🔷 PERMISSIONS DROPDOWN
perm_list = list(permissions.find())
perm_dict = {p["permission_name"]: p["_id"] for p in perm_list}

selected_perm = st.selectbox("Select Permission", list(perm_dict.keys()))
permission_id = perm_dict[selected_perm]

st.info(f"Selected Permission: {selected_perm}")

# 🔷 ACCESS CHECK FUNCTION
def check_access(user_id, permission_id):
    user_data = users.find_one({"_id": user_id})

    for role_id in user_data["roles"]:
        role = roles.find_one({"_id": role_id})

        while role:
            if permission_id in role.get("permissions", []):
                return True

            parent = role.get("parent_role")
            role = roles.find_one({"_id": parent}) if parent else None

    return False

# 🔷 CHECK ACCESS
if st.button("Check Access"):
    access = check_access(user["_id"], permission_id)

    if access:
        st.success("✅ Access Granted")
        logs.insert_one({
            "user_id": user["_id"],
            "permission_id": permission_id,
            "status": "GRANTED",
            "time": datetime.now()
        })
    else:
        st.error("❌ Access Denied")
        logs.insert_one({
            "user_id": user["_id"],
            "permission_id": permission_id,
            "status": "DENIED",
            "time": datetime.now()
        })

# 🔷 EMERGENCY ACCESS
if st.button("🚨 Emergency Access"):
    logs.insert_one({
        "user_id": user["_id"],
        "permission_id": permission_id,
        "status": "GRANTED",
        "emergency": True,
        "time": datetime.now()
    })
    st.warning("⚠ Emergency Access Granted")

# 🔷 NAVIGATION
if st.button("👤 Go to Profile"):
    st.switch_page("pages/4_Profile.py")