import os
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "InterviewAgentDB")

SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")


def _get_sheet():
    if not SERVICE_ACCOUNT_JSON:
        raise RuntimeError("SERVICE_ACCOUNT_JSON env variable missing in secrets!")

    try:
        service_info = json.loads(SERVICE_ACCOUNT_JSON)
    except Exception as e:
        raise RuntimeError(f"Invalid JSON in SERVICE_ACCOUNT_JSON: {e}")

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
    client = gspread.authorize(creds)

    return client.open(SPREADSHEET_NAME).sheet1


def save_to_sheets(name, role, question, answer, feedback, score=None):
    try:
        sheet = _get_sheet()
    except Exception as e:
        raise RuntimeError(f"Unable to access Google Sheet: {e}")

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    row = [
        timestamp,
        name or "",
        role or "",
        question or "",
        answer or "",
        feedback or ""
    ]

    if score is not None:
        row.append(score)

    sheet.append_row(row)
