# modules/ai_classifier.py

def classify_reply(text: str) -> str:
    text = text.lower()

    #strong positive
    if any(word in text for word in [
        "interview", "schedule a call", "let's talk",
        "available for a call", "meet with you"
    ]):
        return "interview"

    #Positive
    elif any(word in text for word in [
        "interested", "sounds good", "we like your profile"
    ]):
        return "positive"

    #Rejection
    elif any(word in text for word in [
        "not interested", "unfortunately", "we regret",
        "position filled", "not moving forward"
    ]):
        return "rejection"

    #Auto reply
    elif any(word in text for word in [
        "this is an automated message",
        "do not reply",
        "out of office",
        "auto response"
    ]):
        return "auto_reply"

    #Default
    else:
        return "neutral"