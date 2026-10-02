import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def answer_question(question: str) -> str:

    if not API_KEY:
        return "Error: GEMINI_API_KEY is not configured."

    if not question.strip():
        return "Please enter a question."

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
You are EduGenie, an AI-powered educational assistant.

Answer the following question clearly and accurately.

Question:
{question}

Instructions:
- Use simple language.
- Give a concise but useful answer.
- Explain important terms when necessary.
- Use examples if they help understanding.
"""
        )

        if response.text:
            return response.text.strip()

        return "No answer was generated."

    except Exception as e:
        return f"Error in Q&A: {str(e)}"