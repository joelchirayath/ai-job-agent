from modules.db_handler import fetch_all, insert_or_update
from modules.email_sender import send_email

def send_auto_responses():
    entries = fetch_all()
    for entry in entries:
        company, email, status, classification, reply_subject, reply_body, auto_sent = entry[1:8]
        
        if status == "replied" and auto_sent == 0:
            if classification == "interview":
                response = "Thank you for your email! I would be happy to schedule an interview."
            elif classification == "positive":
                response = "Thank you for your positive feedback. Looking forward to collaborating!"
            else:
                response = "Thank you for your message."
            
            send_email(email, "Re: " + (reply_subject or "Your Email"), response)
            
            insert_or_update(company, email, status, classification, reply_subject, reply_body, auto_reply_sent=1)
            print(f"Auto-replied to {email} ({classification})")
