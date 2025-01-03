# Written by Juan Pablo Gutiérrez
import imaplib
import os
import base64
import email
from email.header import decode_header
import PyPDF2

def get_attached_documents(mail : imaplib.IMAP4_SSL, email_uid : bytes) -> int:
    mail.select("inbox")
    res, msg = mail.uid('fetch', email_uid, "(RFC822)")
    part_number = 0
    
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])

            if msg.is_multipart():

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

                            filename = f"{email_uid.decode()}_attach_{part_number}.{ext}"

                            filepath = os.path.join("attachments", filename)
                            if ext.lower() == 'pdf':
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                print(f"PDF attachment saved: {filename}")
                            else:
                                part_number -= 1  # Don't count non-PDF attachments
    
    return part_number


def filter_pdf_attachment(email_uid: bytes, part_number:int, keywords : list) -> list:
    if isinstance(keywords, str):
        keywords = [keywords]

    coincidences = []
    for i in range(1, part_number+1):
        filename = f"{email_uid.decode()}_attach_{i}.pdf"
        filepath = os.path.join("attachments", filename)

        with open(filepath, "rb") as f: 
            reader = PyPDF2.PdfReader(f)
            
            content = ""
            for page_num in range(len(reader.pages)):
                content += reader.pages[page_num].extract_text()
            
            keyword_found = False    
            for keyword in keywords:
                if keyword in content:
                    coincidences.append(filename)
                    print(f"Keyword found in {filename}: {keyword}")
                    keyword_found = True
                    break
            
            if not keyword_found:
                f.close()
                os.remove(filepath)
                print(f"No keywords found - deleted {filename}")
                    
    return coincidences
