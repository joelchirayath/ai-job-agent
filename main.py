from modules.email_sender import send_email

receiver_email = "hospital.oviedo12@gmail.com"

subject = "Test Email from AI Agent"
body = "Hello, this is a secure test email from my AI job outreach agent."

send_email(receiver_email, subject, body)
