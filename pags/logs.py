import streamlit as st 
from db_connection import connect_to_db
from pymongo import DESCENDING  # Import DESCENDING from pymongo

def fetch_logs():
    db = connect_to_db("DiscoData")
    if db is not None:
        botLogs = db.botpetoLogs
        logs = botLogs.find({}, {"timestamp": 1, "level": 1, "message": 1}).sort("timestamp", DESCENDING).limit(30)
        return logs

def app():
    if st.button('Get Data / Refresh Data'):
        logs = fetch_logs()

        if logs:
            for log in logs:
                st.write(f"{log['timestamp']}  -  {log['level']}  -  {log['message']}")
        else:
            st.write("Failed to retrieve data from the database.")
