from modules.ai_gemini import classify_text

sample_reply = "We are interested in hiring you for the summer internship."
result = classify_text(sample_reply)
print("Classification:", result)
