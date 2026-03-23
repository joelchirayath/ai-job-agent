import sqlite3
import os

DB_FILE = "emails.db"

# ---------------- PRIORITY LOGIC ----------------
def get_priority(classification):
    mapping = {
        "interview": 5,
        "positive": 4,
        "neutral": 2,
        "auto_reply": 1,
        "rejection": 0
    }
    return mapping.get(classification, 0)

# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS company_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        email TEXT,
        status TEXT,
        ai_classification TEXT,
        reply_subject TEXT,
        reply_body TEXT,
        auto_reply_sent INTEGER DEFAULT 0
    )
''')

    # Ensure priority column exists (for old DBs)
    try:
        c.execute("ALTER TABLE company_emails ADD COLUMN priority INTEGER DEFAULT 0")
    except:
        pass  # Column already exists

    conn.commit()
    conn.close()

# ---------------- INSERT OR UPDATE ----------------
def insert_or_update(company, email, status, ai_classification="", reply_subject="", reply_body=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    priority = get_priority(ai_classification) if ai_classification else 0

    # Check if entry exists
    c.execute("SELECT id FROM company_emails WHERE company=? AND email=?", (company, email))
    result = c.fetchone()

    if result:
        c.execute('''
            UPDATE company_emails
            SET status=?, ai_classification=?, reply_subject=?, reply_body=?, priority=?
            WHERE id=?
        ''', (status, ai_classification, reply_subject, reply_body, priority, result[0]))
    else:
        c.execute('''
            INSERT INTO company_emails
            (company, email, status, ai_classification, reply_subject, reply_body, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (company, email, status, ai_classification, reply_subject, reply_body, priority))

    conn.commit()
    conn.close()

# ---------------- FETCH ALL ----------------
def fetch_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM company_emails")
    rows = c.fetchall()
    conn.close()
    return rows

# ---------------- FETCH PRIORITIZED ----------------
def fetch_prioritized():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT company, email, ai_classification, priority
        FROM company_emails
        ORDER BY priority DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows