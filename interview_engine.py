import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY if API_KEY else None)
DEFAULT_MODEL = "models/gemini-2.5-flash"

def generate_question(role="general") -> str:
    if not API_KEY:
        return "Error: GEMINI_API_KEY not set."

    if not role:
        role = "general"

    prompt = (
        f"You are an Interview Agent. Generate ONE short and simple interview question "
        f"for the role: {role}. Keep it specific, clear, and beginner-friendly. "
        "Return only the question text."
    )

    try:
        model = genai.GenerativeModel(DEFAULT_MODEL)
        response = model.generate_content(prompt)
        question = getattr(response, "text", str(response))
        return question.strip()
    except Exception as e:
        return f"Error generating question: {e}"
