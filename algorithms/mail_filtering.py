# Written by Juan Pablo Gutiérrez
import imaplib
import os
import base64
import email
from email.header import decode_header

def get_attached_documents(mail : imaplib.IMAP4_SSL, email_uid : bytes):
    res, msg = mail.uid('fetch', email_uid, "(RFC822)")
    
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])

            if msg.is_multipart():

                part_number = 0
                for part in msg.walk():
                    if part.get_content_disposition() == 'attachment':
                        filename = part.get_filename()

                        if filename:
                            if not os.path.isdir("attachments"):
                                os.mkdir("attachments")

                            filename = decode_header(filename)[0][0]
                            

                            if isinstance(filename, bytes):
                                filename = filename.decode()

                            ext = filename.split(".")[-1] 
                            part_number += 1

                            filepath = os.path.join("attachments", f'{email_uid.decode()}_attach_{part_number}.{ext}')
                            open(filepath, "wb").write(part.get_payload(decode=True))
                            print(f"Attachment saved: {filename}")

