from algorithms.mail_listener import *
from email.header import decode_header
from algorithms.mail_listener import mail_received
import algorithms.mail_filtering as mf
from dotenv import load_dotenv
import os

load_dotenv()

# Function to read the subjects of new emails
def main(username, password):
    # Connect to the email server
    mail = connect(username, password)

    new_uids = mail_received(mail, "inbox")
    
    if new_uids:
        print(f"New emails found: {len(new_uids)}")
        for email_uid in new_uids:
            num = mf.get_attached_documents(mail, email_uid)
            print(f"Attachments found for {email_uid}: {num}")
            keywords = ["OpenXilogGo"]
            filtered_docs = mf.filter_pdf_attachment(email_uid, num, keywords)
            print(f"Filtered documents: {filtered_docs}")
    else:
        print("No new emails found.")
    
    # Logout and close the connection
    mail.logout()
    
    return None

username = os.getenv("username")
password = os.getenv("password")
known_uids = main(username, password) 
