# AI Interview Agent (Gemini)

A Streamlit-based Interview Agent that:
- Generates short interview questions using Gemini (Google Generative AI)
- Evaluates candidate answers (score, strengths, weaknesses, feedback)
- Optionally saves results to Google Sheets

## Files
- `app.py` - Streamlit UI
- `interview_engine.py` - Gemini question generator
- `evaluator.py` - Gemini-based answer evaluator
- `sheets.py` - Google Sheets saving helper
- `requirements.txt` - Python dependencies

## Setup (Local)
1. Clone repository.
2. Create and activate a Python venv (recommended).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
