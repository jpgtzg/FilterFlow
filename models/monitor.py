from algorithms.mail_listener import *
from email.header import decode_header
from algorithms.mail_listener import mail_received
import algorithms.mail_filtering as mf
from dotenv import load_dotenv
from api.mail.imp_connection import connect
import os
import time

class EmailMonitor:
    def __init__(self, username, password, id, filters=None):
        """Initialize the email monitor with credentials and filters"""
        self.id = id
        self.username = username
        self.password = password
        self.filters = filters
        self.mail = None
        self.is_running = False

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
        
        self.is_running = True
        try:
            while self.is_running:
                self.process_new_emails()
                time.sleep(interval)
        finally:
            self.disconnect()

    def stop_monitoring(self):
        """Stop the email monitoring loop"""
        self.is_running = False


