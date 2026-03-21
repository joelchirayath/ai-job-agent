import csv
from modules.email_sender import send_email

subject = "Test Email from AI Agent"
body = "Hello, this is an automated email from my AI job outreach agent."

rows = []

# Read CSV and send emails
with open("data.csv", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["status"] == "pending":
            print(f"Sending email to {row['company']} ({row['email']})")
            send_email(row["email"], subject, body)
            row["status"] = "sent"
        rows.append(row)

# Write updated statuses back to CSV
with open("data.csv", "w", newline="") as file:
    fieldnames = ["company", "email", "status"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
