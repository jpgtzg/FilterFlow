from algorithms.mail_listener import *
from email.header import decode_header
from algorithms.mail_listener import mail_received
import algorithms.mail_filtering as mf
from dotenv import load_dotenv
from api.imp_connection import connect
import os

load_dotenv()

# Function to read the subjects of new emails
def main(username, password):
    # Connect to the email server
    mail = connect(username, password)

    new_uids = mail_received(mail, "inbox")
    
    if new_uids:
        print(f"New emails found: {len(new_uids)}")
        filtered_docs = []
        for email_uid in new_uids:
            num = mf.get_attached_documents(mail, email_uid)
            keywords = ["OpenXilogGo"]
            docs = mf.filter_pdf_attachment(email_uid, num, keywords)
            if docs:
                filtered_docs.extend(docs)
        print(f"Filtered documents: {filtered_docs}")
    else:
        print("No new emails found.")
    
    # Logout and close the connection
    mail.logout()
    
    return None

username = os.getenv("username")
password = os.getenv("password")
main(username, password)