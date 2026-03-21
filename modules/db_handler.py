import sqlite3
import os

DB_FILE = "emails.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS company_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            email TEXT,
            status TEXT,
            ai_classification TEXT,
            reply_subject TEXT,
            reply_body TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_or_update(company, email, status, ai_classification="", reply_subject="", reply_body=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Check if entry exists
    c.execute("SELECT id FROM company_emails WHERE company=? AND email=?", (company, email))
    result = c.fetchone()
    if result:
        c.execute('''
            UPDATE company_emails
            SET status=?, ai_classification=?, reply_subject=?, reply_body=?
            WHERE id=?
        ''', (status, ai_classification, reply_subject, reply_body, result[0]))
    else:
        c.execute('''
            INSERT INTO company_emails
            (company, email, status, ai_classification, reply_subject, reply_body)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (company, email, status, ai_classification, reply_subject, reply_body))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM company_emails")
    rows = c.fetchall()
    conn.close()
    return rows
