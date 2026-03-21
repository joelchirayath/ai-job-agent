import imaplib
import email
from dotenv import load_dotenv
import os
import socket

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def fetch_unread_emails():
    emails = []
    try:
        # Set a socket timeout so it doesn't hang
        socket.setdefaulttimeout(10)

        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search unread emails
        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK":
            print("No messages found or search failed.")
            return emails

        email_ids = messages[0].split()
        if not email_ids:
            print("No unread emails.")
            return emails

        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    from_ = msg["from"]
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                    emails.append({"from": from_, "subject": subject, "body": body})

        mail.logout()
    except Exception as e:
        print(f"Error fetching emails: {e}")

    return emails