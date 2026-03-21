import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def classify_text(text):
    """
    Classify a job reply as positive, negative, or neutral.
    Returns the classification as a lowercase string.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Classify the following job reply as positive, negative, or neutral:\n\n{text}\n\nAnswer with only one word:"
    )
    return response.text.strip().lower()
