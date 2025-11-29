Interview Agent 

Interview Agent is a Streamlit-based application that uses Google Generative AI (Gemini) to generate interview questions, evaluate candidate answers, and optionally save the results to Google Sheets. It is designed to help users practice interviews effectively with clear feedback and scoring.

Features
* Generates short and relevant interview questions
* Evaluates candidate answers with score, strengths, weaknesses, and improvement suggestions
* Saves all responses and feedback to Google Sheets (optional)
* Simple and user-friendly Streamlit interface
* Secure API key and credential handling using environment variables

Project Structure

Interview-Agent-Gemini/
│
├── app.py                 # Streamlit application (UI)
├── interview_engine.py    # Gemini-based question generator
├── evaluator.py           # Gemini-based answer evaluator
├── sheets.py              # Google Sheets connection helper
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not included in repo)
└── README.md              # Documentation

Setup & Usage Instructions

1. Prerequisites

* Python 3.10 or higher
* Google account for Google Sheets
* Gemini API key from Google Generative AI
* Service account JSON file for Google Sheets API (Save it as `service.json` or update the `SERVICE_FILE` variable) 


2. Initial Setup and Install Dependencies
a. Open PowerShell in your project folder
Example:
C:\interview_agent1

b. Create a virtual environment
python -m venv venv

c. Activate the virtual environment
.\venv\Scripts\Activate.ps1

d. Install dependencies
pip install -r requirements.txt


3. Environment Variables

Create a `.env` file inside the project root with the following:
GEMINI_API_KEY=your_gemini_api_key_here


4. Google Sheets Setup

1. Create a Google Sheet named InterviewAgentDB
   (or use any other name and update it in `SPREADSHEET_NAME`)
2. Share this Google Sheet with your service account email
   * The email is found inside the `service.json` file
   * Provide Editor access
3. Place the service account JSON in the project root with the filename:
   service.json
   

5. Running the App

Start the Streamlit application:
streamlit run app.py

Once started:
1. Enter your Name and Job Role
2. Click Get Interview Question
3. Type your answer in the answer box
4. Click Evaluate Answer
5. Click Save Result to store the entry in Google Sheets

6. Notes

* Ensure your Gemini API key is active and has available quota
* The service account must have Editor access to the Google Sheet
* Only one questions generated at a time
* Each entry saved to Google Sheets includes:

  * Timestamp
  * Name
  * Job role
  * Question
  * Answer
  * Evaluation feedback
  * Score
  
7. Troubleshooting

Questions or evaluations not working:
* Check the `GEMINI_API_KEY`
* Ensure internet connection is stable

Google Sheets saving not working:
* Confirm `SERVICE_FILE` path is correct
* Verify the Google Sheet is shared with the service account email
* Make sure the spreadsheet name matches `SPREADSHEET_NAME`


