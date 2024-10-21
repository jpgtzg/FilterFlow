# Written by Juan Pablo Gutiérrez

import imaplib
import api.uid_store as ustore

def fetch_email_uids(mail):
    status, messages = mail.uid('search', None, "ALL")
    email_uids = messages[0].split()
    return email_uids

def mail_received(mail : imaplib.IMAP4_SSL, mailbox : str) -> list:
    mail.select(mailbox)

    current_uids = fetch_email_uids(mail)
    known_uids = ustore.read_uid()
    
    new_uids = [uid for uid in current_uids if uid not in known_uids]
    return new_uids
    