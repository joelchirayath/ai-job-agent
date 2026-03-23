from modules.db_handler import fetch_all, insert_or_update
from modules.email_sender import send_email

def send_auto_responses():
    """
    Sends automatic replies based on AI classification.
    Marks auto_reply_sent=1 to avoid duplicate responses.
    """
    entries = fetch_all()
    for entry in entries:
        # Unpack database row
        company = entry[1]
        email = entry[2]
        status = entry[3]
        classification = entry[4]
        reply_subject = entry[5] or "Your Email"
        reply_body = entry[6] or ""
        # Use 0 if auto_reply_sent column does not exist yet
        auto_sent = entry[7] if len(entry) > 7 else 0

        if status == "replied" and auto_sent == 0:
            # Compose response based on classification
            if classification == "interview":
                response = "Thank you for your email! I would be happy to schedule an interview."
            elif classification == "positive":
                response = "Thank you for your positive feedback. Looking forward to collaborating!"
            elif classification == "neutral":
                response = "Thank you for your message. I will follow up if needed."
            elif classification == "auto_reply":
                response = "Thanks for your automated response."
            else:  # rejection or unknown
                response = "Thank you for letting me know. I appreciate your consideration."

            # Send the email
            send_email(email, f"Re: {reply_subject}", response)
            print(f"Auto-replied to {email} ({classification})")

            # Update DB to mark auto_reply_sent
            insert_or_update(
                company,
                email,
                status=status,
                ai_classification=classification,
                reply_subject=reply_subject,
                reply_body=reply_body,
                auto_reply_sent=1  # mark as sent
            )