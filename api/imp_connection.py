import email
import imaplib

def connect(username, password) -> imaplib.IMAP4_SSL:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    
    if mail is not None:    
        return mail
    else:
        raise Exception("Error connecting to the mail server")