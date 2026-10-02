import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def clean_json_block(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(text: str):

    if not API_KEY:
        return {
            "error": "GEMINI_API_KEY is not configured."
        }

    if not text.strip():
        return {
            "error": "Please provide a topic or passage."
        }

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
Create exactly 3 multiple-choice questions from the following
educational topic or passage.

Topic/Passage:
{text}

Return ONLY valid JSON.

The JSON must have this exact structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option"
  }}
]

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- Only one correct answer.
- Questions must be relevant to the given content.
- Do not include Markdown.
- Do not include explanations outside the JSON.
"""
        )

        if not response.text:
            return {
                "error": "No quiz was generated."
            }

        cleaned = clean_json_block(response.text)

        quiz = json.loads(cleaned)

        if not isinstance(quiz, list):
            return {
                "error": "Invalid quiz format."
            }

        return quiz

    except json.JSONDecodeError:
        return {
            "error": "Gemini returned an invalid quiz format."
        }

    except Exception as e:
        return {
            "error": f"Error in Quiz: {str(e)}"
        }