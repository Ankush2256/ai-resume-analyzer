import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompt import get_resume_prompt

# ---------------- Load Environment Variables ---------------- #

load_dotenv()

def get_api_key():
    # Local .env
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    # Streamlit Cloud Secrets
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


API_KEY = get_api_key()

if API_KEY is None:
    st.error(
        "❌ Gemini API Key not found.\n\n"
        "Local: create a .env file with GEMINI_API_KEY\n"
        "Cloud: add GEMINI_API_KEY to Streamlit Secrets."
    )
    st.stop()

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