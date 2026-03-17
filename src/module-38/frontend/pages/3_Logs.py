import streamlit as st
from pymongo import MongoClient
import pandas as pd

if "user" not in st.session_state:
    st.error("Login first")
    st.stop()

client = MongoClient("your_uri")
db = client["rbac_db"]

logs = db["access_logs"]

st.title("📜 Access Logs")

data = list(logs.find({}, {"_id": 0}))
df = pd.DataFrame(data)

st.dataframe(df)