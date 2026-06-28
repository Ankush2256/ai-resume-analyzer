import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompt import get_resume_prompt

# ---------------- Load Environment Variables ---------------- #
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# ---------------- Configure Gemini ---------------- #
genai.configure(api_key=API_KEY)

# ---------------- Create Model ---------------- #
model = genai.GenerativeModel("gemini-2.5-flash")


def test_connection():
    """
    Test Gemini API Connection
    """

    try:
        response = model.generate_content(
            "Reply with only one word: Connected"
        )

        return response.text.strip()

    except Exception as e:
        return f"❌ {str(e)}"


def analyze_resume(resume_text):
    """
    Analyze Resume and return JSON.
    """

    try:

        prompt = get_resume_prompt(resume_text)

        response = model.generate_content(prompt)

        response_text = response.text.strip()

        # Remove markdown if Gemini returns it
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        data = json.loads(response_text)

        return data

    except json.JSONDecodeError:

        return {
            "error": "Gemini returned an invalid JSON response."
        }

    except Exception as e:

        return {
            "error": str(e)
        }