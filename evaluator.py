import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY if API_KEY else None)
DEFAULT_MODEL = "models/gemini-2.5-flash"

def generate_question(role="general"):
    if not API_KEY:
        return "Error: GEMINI_API_KEY not set."
    prompt = f"Generate one interview question for the role: {role}. Return only the question."
    try:
        model = genai.GenerativeModel(DEFAULT_MODEL)
        response = model.generate_content(prompt)
        question = getattr(response, "text", str(response))
        return question.strip()
    except Exception as e:
        return f"Error generating question: {e}"

def evaluate_answer(question, user_answer):
    if not API_KEY:
        return "Error: GEMINI_API_KEY not set."
    if not question or not user_answer:
        return "Question or answer is empty."

    prompt = (
        "You are an Interview Agent.\n"
        "Evaluate the following answer in EXACTLY this format:\n"
        "Correct\nScore: 0/10\nExplanation sentence 1. Explanation sentence 2.\n"
        "Rules: no bullets, no asterisks, no hyphens, no markdown, plain text only.\n"
        f"Question: {question}\nAnswer: {user_answer}\nRespond exactly in the required format."
    )

    try:
        model = genai.GenerativeModel(DEFAULT_MODEL)
        response = model.generate_content(prompt)
        feedback = getattr(response, "text", str(response))
        return feedback.replace("*", "").replace("-", "").strip()
    except Exception as e:
        return f"Error evaluating answer: {e}"
