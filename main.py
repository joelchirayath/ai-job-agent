# main.py
import time
from modules.email_sender import send_email
from modules.ai_gemini import classify_text
from modules.email_reader_gmail import fetch_unread_emails_gmail
from modules.db_handler import init_db, insert_or_update, fetch_all, fetch_prioritized
from modules.ai_classifier import classify_reply
from modules.auto_responder import send_auto_responses

subject = "Test Email from AI Agent"
body = "Hello, this is an automated email from my AI job outreach agent."

# ---------------- INIT ----------------
init_db()

# ---------------- TEST COMPANIES ----------------
companies = [
    {"company": "testcompany1", "email": "mariagonzalez.oviedohospital@gmail.com"},
    {"company": "testcompany2", "email": "hospital.oviedo12@gmail.com"}
]

# ---------------- SEND EMAILS ----------------
print("\n📤 SENDING EMAILS...\n")
for row in companies:
    print(f"Sending email to {row['company']} ({row['email']})")
    send_email(row["email"], subject, body)
    print(f"✅ Email sent to {row['email']}")
    
    insert_or_update(row['company'], row['email'], status="sent")

# ---------------- FETCH REPLIES ----------------
print("\n📥 FETCHING REPLIES...\n")
emails = fetch_unread_emails_gmail()
print(f"Fetched {len(emails)} unread replies.\n")

for e in emails:
    from_email = e["from"]
    subject_line = e["subject"]
    body_text = e["body"]

    print(f"📩 Processing email from: {from_email}")

    for row in companies:
        if row["email"].lower() in from_email.lower():
            classification = classify_text(body_text)

            print(f"🧠 AI classified as: {classification}")
            print(f"📝 Preview: {body_text[:60]}...\n")

            insert_or_update(
                row["company"],
                row["email"],
                status="replied",
                ai_classification=classification,
                reply_subject=subject_line,
                reply_body=body_text
            )

# ---------------- FALLBACK CLASSIFICATION ----------------
def classify_new_replies():
    from modules.db_handler import get_priority
    import sqlite3

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, reply_body 
        FROM company_emails 
        WHERE status='replied' AND (ai_classification IS NULL OR ai_classification='')
    """)

    rows = cursor.fetchall()

    for row in rows:
        id_, reply = row
        if reply:
            classification = classify_reply(reply)

            cursor.execute(
                "UPDATE company_emails SET ai_classification=?, priority=? WHERE id=?",
                (classification, get_priority(classification), id_)
            )

            print(f"⚠️ Fallback classified reply {id_} as: {classification}")

    conn.commit()
    conn.close()

classify_new_replies()

print("\n🤖 SENDING AUTO-RESPONSES...\n")
send_auto_responses()

# ---------------- QUICK TEST (SIMULATION) ----------------
print("\n🧪 RUNNING TEST CLASSIFICATIONS...\n")

test_replies = [
    {"company": "testcompany1", "email": "mariagonzalez.oviedohospital@gmail.com",
     "body": "We would like to schedule an interview with you."},

    {"company": "testcompany2", "email": "hospital.oviedo12@gmail.com",
     "body": "Unfortunately, we are not moving forward with your application."},

    {"company": "testcompany3", "email": "auto@company.com",
     "body": "This is an automated message. We received your email."}
]

for reply in test_replies:
    classification = classify_text(reply["body"])

    insert_or_update(
        reply["company"],
        reply["email"],
        status="replied",
        ai_classification=classification,
        reply_subject="Test Subject",
        reply_body=reply["body"]
    )

    print(f"🧠 Test classified {reply['company']} as: {classification}")

# ---------------- SHOW ALL DATA ----------------
print("\n📊 ALL DATABASE ENTRIES:\n")
for r in fetch_all():
    print(r)

# ---------------- PRIORITIZED OUTPUT ----------------
print("\n🔥 PRIORITIZED RESULTS (MOST IMPORTANT FIRST):\n")
for row in fetch_prioritized():
    print(row)