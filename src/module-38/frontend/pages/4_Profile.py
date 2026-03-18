import streamlit as st
from pymongo import MongoClient

# 🔒 Login check
if "user" not in st.session_state:
    st.stop()

# 🔌 DB
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["rbac_db"]

users = db["users"]
roles = db["roles"]

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
    st.markdown("## 🏥 User Dashboard")

with col2:
    if st.button("🚪 Logout", key="logout_btn"):
        del st.session_state["user"]
        st.switch_page("app.py")

# 🔷 USER INFO CARD
st.markdown("### 📄 Basic Information")

st.info(f"""
**Name:** {user['name']}  
**Email:** {user['email']}
""")

# 🔷 ROLES DISPLAY
role_names = [
    roles.find_one({"_id": r})["role_name"]
    for r in user["roles"]
]

st.success(f"Roles: {', '.join(role_names)}")

# 🔷 PASSWORD UPDATE (OPTIONAL BUT GREAT FEATURE 🔥)
st.markdown("### 🔑 Change Password")

new_password = st.text_input("Enter New Password", type="password")

if st.button("Update Password"):
    if new_password.strip() == "":
        st.warning("Password cannot be empty")
    else:
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": new_password}}
        )
        st.success("Password updated successfully ✅")

# 🔷 NAVIGATION
st.markdown("### 🔗 Navigation")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏥 Dashboard"):
        st.switch_page("pages/1_User_Dashboard.py")

with col2:
    if st.button("📜 Logs"):
        st.switch_page("pages/3_Logs.py")