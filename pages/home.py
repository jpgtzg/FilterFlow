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
    else:
        st.error(f"Error {action}ing monitor: {response.text}")

# UI Components
st.title("Email Monitor Dashboard")

# Login Section
with st.container():
    st.subheader("Monitor Configuration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    filters = st.text_input("Filters (comma-separated)")

    if st.button("Create Monitor"):
        if filters:
            filters = [f.strip() for f in filters.split(",")]
            create_monitor(username, password, filters)
        else:
            st.warning("Please enter at least one filter")

# Existing Monitors Section
st.subheader("Existing Monitors")
monitors = get_monitors()

if monitors:
    for monitor in monitors:
        with st.expander(f"Monitor: {monitor['username']}"):
            st.write(f"Filters: {', '.join(monitor['filters'])}")
            st.write(f"Status: {'Running' if monitor['is_running'] else 'Stopped'}")
            
            col1, col2 = st.columns(2)
            with col1:
                if not monitor['is_running']:
                    if st.button("Start", key=f"start_{monitor['id']}"):
                        toggle_monitor(monitor['id'], "start")
            with col2:
                if monitor['is_running']:
                    if st.button("Stop", key=f"stop_{monitor['id']}"):
                        toggle_monitor(monitor['id'], "stop")
else:
    st.info("No monitors configured yet")



