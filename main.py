from algorithms.mail_listener import *
import imaplib
import email
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
    
    # Return the updated UID list (including the new ones)
    return None
# Initial setup (fetch all UIDs and start with an empty known_uids list)
known_uids = []


from api.imp_connection import connect

#print(mail_received(connect(username, password), "inbox"))
# Call this function periodically to check for new emails
known_uids = main(os.getenv("username"), os.getenv("password")) 
from models.flow import Flow
from models.action import Action

