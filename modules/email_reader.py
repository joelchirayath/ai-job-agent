import imaplib
import email
from email.header import decode_header
import sqlite3

DB_PATH = "emails.db"  # your database file

def fetch_unread_replies():
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("your_email@gmail.com", "YOUR_APP_PASSWORD_OR_TOKEN")
    mail.select("inbox")

    # Search for unread emails
    status, messages = mail.search(None, '(UNSEEN)')
    unread_emails = messages[0].split()
    print(f"Fetched {len(unread_emails)} unread replies.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for e_id in unread_emails:
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                # Extract email address
                email_addr = from_.split("<")[-1].replace(">", "").strip()

                # Extract body
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                # Update database with reply content
                cursor.execute(
                    "UPDATE emails SET reply_content=?, status='replied' WHERE email=?",
                    (body, email_addr)
                )

    conn.commit()
    conn.close()
    mail.logout()