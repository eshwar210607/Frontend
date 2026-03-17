import streamlit as st
from pymongo import MongoClient
import pandas as pd

# 🔒 Login check
if "user" not in st.session_state:
    st.stop()

# 🔌 DB
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["rbac_db"]

logs = db["access_logs"]
users = db["users"]
permissions = db["permissions"]

# 🔷 HEADER + LOGOUT
col1, col2 = st.columns([8, 1])
with col1:
    st.title("📜 Access Logs")
with col2:
    if st.button("Logout"):
        del st.session_state["user"]
        st.switch_page("app.py")

# 🔷 FILTERS
st.markdown("### 🔍 Filters")

status_filter = st.selectbox("Filter by Status", ["All", "GRANTED", "DENIED"])

# 🔷 FETCH DATA
if status_filter == "All":
    data = list(logs.find({}, {"_id": 0}))
else:
    data = list(logs.find({"status": status_filter}, {"_id": 0}))

# 🔷 HANDLE EMPTY
if not data:
    st.warning("No logs found")
else:
    # 🔷 CONVERT IDS → NAMES
    for log in data:
        user = users.find_one({"_id": log["user_id"]})
        perm = permissions.find_one({"_id": log["permission_id"]})

        log["user"] = user["name"] if user else "Unknown"
        log["permission"] = perm["permission_name"] if perm else "Unknown"

        # optional cleanup
        log.pop("user_id", None)
        log.pop("permission_id", None)

    df = pd.DataFrame(data)

    # 🔷 SORT (latest first)
    if "time" in df.columns:
        df = df.sort_values(by="time", ascending=False)

    st.dataframe(df, use_container_width=True)