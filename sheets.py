import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "InterviewAgentDB")
SERVICE_FILE = os.getenv("SERVICE_FILE", "service.json")

def _get_sheet():
    if not os.path.exists(SERVICE_FILE):
        raise FileNotFoundError(f"Service account JSON not found at '{SERVICE_FILE}'.")

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_FILE, scope)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).sheet1

def save_to_sheets(name, role, question, answer, feedback, score=None):
    try:
        sheet = _get_sheet()
    except Exception as e:
        raise RuntimeError(f"Unable to access Google Sheet: {e}")

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    row = [timestamp, name or "", role or "", question or "", answer or "", feedback or ""]
    
    if score is not None:
        row.append(score)

    sheet.append_row(row)
