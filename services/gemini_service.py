import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompt import get_resume_prompt

# ---------------- Load Environment Variables ---------------- #

load_dotenv()

# First try .env (Local)
API_KEY = os.getenv("GEMINI_API_KEY")

# If not found, try Streamlit Secrets (Cloud)
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# If still not found
if not API_KEY:
    raise ValueError(
        "Gemini API Key not found. Add it to your local .env file or Streamlit Secrets."
    )

# ---------------- Configure Gemini ---------------- #

genai.configure(api_key=API_KEY)

# ---------------- Create Model ---------------- #

model = genai.GenerativeModel("gemini-2.5-flash")


def test_connection():
    """Test Gemini API"""

    try:
        response = model.generate_content(
            "Reply with only one word: Connected"
        )
        return response.text.strip()

    except Exception as e:
        return f"❌ {str(e)}"


def analyze_resume(resume_text):
    """Analyze Resume"""

    try:

        prompt = get_resume_prompt(resume_text)

        response = model.generate_content(prompt)

        response_text = response.text.strip()

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        return json.loads(response_text)

    except json.JSONDecodeError:

        return {
            "error": "Gemini returned invalid JSON."
        }

    except Exception as e:

        return {
            "error": str(e)
        }