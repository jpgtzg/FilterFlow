from algorithms.mail_listener import *
from email.header import decode_header
from algorithms.mail_listener import mail_received
import algorithms.mail_filtering as mf
from dotenv import load_dotenv
from api.mail.imp_connection import connect
import os
import time
import streamlit as st
from models.monitor import EmailMonitor

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("username")
    password = os.getenv("password")
    
    monitor = EmailMonitor(username, password)
    monitor.start_monitoring()
