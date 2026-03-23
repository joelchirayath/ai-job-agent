# modules/ai_classifier.py

def classify_reply(text: str) -> str:
    """
    Classify an email reply as positive, negative, or neutral.
    This is a placeholder function. You can replace it with
    an AI API call (Gemini/OpenAI) later.
    """
    text = text.lower()
    if any(word in text for word in ["yes", "accept", "interested", "available"]):
        return "positive"
    elif any(word in text for word in ["no", "reject", "not interested"]):
        return "negative"
    else:
        return "neutral"
