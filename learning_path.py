import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def get_learning_recommendations(topic: str) -> str:

    if not API_KEY:
        return "Error: GEMINI_API_KEY is not configured."

    if not topic.strip():
        return "Please enter a topic."

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
You are EduGenie, a personalized educational assistant.

Create a structured learning path for:

Topic: {topic}

Organize the learning path into:
1. Beginner Level
2. Intermediate Level
3. Advanced Level

For each level provide:
- Topics to learn
- Short explanation
- Suggested learning resources
- Approximate learning time

Also provide:
- Prerequisites
- Recommended learning order
- A short final project or practice activity

Use simple and student-friendly language.
"""
        )

        if response.text:
            return response.text.strip()

        return "No learning path was generated."

    except Exception as e:
        return f"Error in Learning Path: {str(e)}"