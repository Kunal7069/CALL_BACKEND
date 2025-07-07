import csv
from typing import Dict, List

import gspread
from fastapi import UploadFile
from oauth2client.service_account import ServiceAccountCredentials

from fastapi_orgs.app.settings import GOOGLE_CREDENTIALS, SHEET_NAME, SPREADSHEET_ID


async def parse_csv_files(files: List[UploadFile]) -> Dict[str, list]:
    result = {}
    for file in files:
        content = await file.read()
        decoded = content.decode("utf-8").splitlines()
        reader = csv.reader(decoded)
        result[file.filename] = list(reader)
    return result


def append_to_google_sheet(summary: dict):
    """
    Appends a summary dict to Google Sheet.
    Adds header if the sheet is empty.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    headers = list(summary.keys())
    values = list(summary.values())

    # Check if header row exists
    if sheet.row_count == 0 or not any(sheet.row_values(1)):
        sheet.append_row(headers)

    sheet.append_row(values)


async def save_summary_to_csv(summary: dict):
    """
    Unified function that sends summary data to Google Sheets.
    """
    try:
        append_to_google_sheet(summary)
    except Exception as e:
        raise RuntimeError("Failed to save summary to Google Sheets.") from e
