import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def summarize_text(text: str) -> str:

    if not API_KEY:
        return "Error: GEMINI_API_KEY is not configured."

    if not text.strip():
        return "Please provide some text to summarize."

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
Summarize the following educational text in simple language.

Requirements:
- Keep the important concepts.
- Remove unnecessary repetition.
- Make it easy for a student to understand.
- Keep the summary concise.

Text:
{text}
"""
        )

        if response.text:
            return response.text.strip()

        return "No summary was generated."

    except Exception as e:
        return f"Error in Summary: {str(e)}"