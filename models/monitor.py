# Written by Juan Pablo Gutiérrez

from algorithms.mail_listener import *
from email.header import decode_header
from algorithms.mail_listener import mail_received
import algorithms.mail_filtering as mf
from dotenv import load_dotenv
from api.mail.imp_connection import connect
import os
import time
from threading import Lock

class EmailMonitor:
    def __init__(self, username, password, monitor_id, filters=None):
        """Initialize the email monitor with credentials and filters"""
        self.id = monitor_id
        self.username = username
        self.password = password
        self.filters = filters
        self.mail = None
        self._is_running = False
        self._lock = Lock()

    @property
    def is_running(self):
        """Property to safely access the running state"""
        return self.get_is_running()

    def connect(self):
        """Establish connection to the email server"""
        self.mail = connect(self.username, self.password)
        return self.mail is not None

    def disconnect(self):
        """Close the email server connection"""
        if self.mail:
            self.mail.logout()
            self.mail = None

    def process_new_emails(self):
        """Process new emails and return filtered documents"""
        new_uids = mail_received(self.mail, "inbox")
        filtered_docs = []
        
        if new_uids:
            print(f"New emails found: {len(new_uids)}")
            for email_uid in new_uids:
                num = mf.get_attached_documents(self.mail, email_uid)
                docs = mf.filter_pdf_attachment(email_uid, num, self.filters)
                if docs:
                    filtered_docs.extend(docs)
            print(f"Filtered documents: {filtered_docs}")
        else:
            print("No new emails found.")
            
        return filtered_docs

    def start_monitoring(self, interval=10):
        """Start the email monitoring loop"""
        if not self.connect():
            raise ConnectionError("Failed to connect to email server")
        
        with self._lock:
            self._is_running = True
        print(f"Monitor {self.id} started with is_running = {self._is_running}")
        try:
            while self.get_is_running():
                self.process_new_emails()
                time.sleep(interval)
        finally:
            with self._lock:
                self._is_running = False
            self.disconnect()

    def stop_monitoring(self):
        """Stop the email monitoring loop in a thread-safe way"""
        with self._lock:
            self._is_running = False
        print(f"Monitor {self.id} stopped with is_running = {self._is_running}")
        
    def get_is_running(self):
        """Get the is_running status in a thread-safe way"""
        with self._lock:
            return self._is_running
