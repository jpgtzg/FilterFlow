import streamlit as st
import requests
import json
from typing import List

# Constants
API_BASE_URL = "http://127.0.0.1:8000"

def create_monitor(username, password, filters):
    if not username or not password:
        st.error("Please enter username and password")
        return
        
    data = {
        "username": username,
        "password": password,
        "filters": filters
    }
    
    response = requests.post(f"{API_BASE_URL}/monitors", json=data)
    if response.status_code == 200:
        st.success("Monitor created successfully!")
        return response.json()["monitor_id"]
    else:
        st.error(f"Error creating monitor: {response.text}")

def get_monitors():
    response = requests.get(f"{API_BASE_URL}/monitors")
    if response.status_code == 200:
        return response.json()
    return []

def toggle_monitor(monitor_id, action):
    response = requests.post(f"{API_BASE_URL}/monitors/{monitor_id}/{action}")
    if response.status_code == 200:
        st.success(f"Monitor {action}ed successfully!")
        st.rerun()
    else:
        st.error(f"Error {action}ing monitor: {response.text}")

# UI Components
st.set_page_config(page_title="Email Monitor Dashboard", layout="wide")

# Login Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Monitor Configuration")
    with st.form(key="monitor_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        filters = st.text_area("Filters (one per line)")
        submit_button = st.form_submit_button("Create Monitor")
        
        if submit_button:
            if filters:
                filters = [f.strip() for f in filters.split("\n") if f.strip()]
                create_monitor(username, password, filters)
            else:
                st.warning("Please enter at least one filter")

with col2:
    st.subheader("Existing Monitors")
    if st.button("🔄 Refresh Monitors"):
        st.rerun()

# Existing Monitors Section
monitors = get_monitors()

if monitors:
    for monitor in monitors:
        with st.expander(f"Monitor: {monitor['username']}", expanded=True):
            st.markdown(f"**Filters:** {', '.join(monitor['filters'])}")
            status_color = "🟢" if monitor['is_running'] else "🔴"
            st.markdown(f"**Status:** {status_color} {'Running' if monitor['is_running'] else 'Stopped'}")
            
            cols = st.columns([1, 1, 2])
            with cols[0]:
                if st.button("▶️ Start", key=f"start_{monitor['id']}", disabled=monitor['is_running']):
                    toggle_monitor(monitor['id'], "start")
                    
            
            with cols[1]:
                if st.button("⏹️ Stop", key=f"stop_{monitor['id']}", disabled=not monitor['is_running']):
                    toggle_monitor(monitor['id'], "stop")
else:
    st.info("💡 No monitors configured yet")



