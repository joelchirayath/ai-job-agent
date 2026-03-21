# main.py
import time
from modules.email_sender import send_email
from modules.ai_gemini import classify_text
from modules.email_reader_gmail import fetch_unread_emails_gmail
from modules.db_handler import init_db, insert_or_update, fetch_all
from modules.ai_classifier import classify_reply
import sqlite3

subject = "Test Email from AI Agent"
body = "Hello, this is an automated email from my AI job outreach agent."

# Initialize DB
init_db()

# Load companies from a CSV or manually for now
companies = [
    {"company": "testcompany1", "email": "mariagonzalez.oviedohospital@gmail.com"},
    {"company": "testcompany2", "email": "hospital.oviedo12@gmail.com"}
]

# ---------------- SEND EMAILS ----------------
for row in companies:
    print(f"Sending email to {row['company']} ({row['email']})")
    send_email(row["email"], subject, body)
    print(f"Email sent to {row['email']}")
    # Insert initial row with pending status
    insert_or_update(row['company'], row['email'], status="sent")

# ---------------- READ REPLIES ----------------
emails = fetch_unread_emails_gmail()
print(f"Fetched {len(emails)} unread replies.")

for e in emails:
    from_email = e["from"]
    subject_line = e["subject"]
    body_text = e["body"]
    # Match reply to company
    for row in companies:
        if row["email"].lower() in from_email.lower():
            classification = classify_text(body_text)
            print(f"AI classified reply from {from_email} as: {classification}")
            insert_or_update(
                row["company"],
                row["email"],
                status="replied",
                ai_classification=classification,
                reply_subject=subject_line,
                reply_body=body_text
            )

DB_PATH = "emails.db"

def classify_new_replies():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, reply_content FROM emails WHERE status='replied' AND ai_classification IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        id_, reply = row
        if reply:
            classification = classify_reply(reply)
            cursor.execute(
                "UPDATE emails SET ai_classification=? WHERE id=?",
                (classification, id_)
            )
            print(f"AI classified reply {id_} as: {classification}")

    conn.commit()
    conn.close()

# ---------------- SHOW DATABASE ----------------
print("All entries in database:")
for r in fetch_all():
    print(r)