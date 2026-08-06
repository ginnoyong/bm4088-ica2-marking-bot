"""One-time setup: create the Google Sheet used by src/sheets_logger.py and
share it with the marker roster's admin. Requires the Google Sheets API and
Google Drive API to be enabled for the service account's GCP project first
(console.cloud.google.com -> APIs & Services -> Library).

Run manually with:
    python scripts/setup_google_sheet.py

Prints the created spreadsheet ID — put that in .streamlit/secrets.toml as
GOOGLE_SHEET_ID, and in the Streamlit Cloud app's Secrets when deploying.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gspread
from google.oauth2.service_account import Credentials

from src.sheets_logger import COLUMNS, WORKSHEET_TITLE

SERVICE_ACCOUNT_PATH = Path(__file__).resolve().parent.parent / "files" / "bm4088-ica2-marking-bot-08355738a126.json"
SHARE_WITH_EMAIL = "yongginno@gmail.com"
SHEET_NAME = "BM4088 ICA2 Marking Bot Log"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def main() -> None:
    service_account_info = json.loads(SERVICE_ACCOUNT_PATH.read_text(encoding="utf-8"))
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    client = gspread.authorize(creds)

    spreadsheet = client.create(SHEET_NAME)
    worksheet = spreadsheet.sheet1
    worksheet.update_title(WORKSHEET_TITLE)
    worksheet.append_row(COLUMNS)

    spreadsheet.share(SHARE_WITH_EMAIL, perm_type="user", role="writer")

    print(f"Created spreadsheet: {SHEET_NAME}")
    print(f"Spreadsheet ID: {spreadsheet.id}")
    print(f"Spreadsheet URL: {spreadsheet.url}")
    print(f"Shared with: {SHARE_WITH_EMAIL} (Editor)")
    print()
    print("Next: set GOOGLE_SHEET_ID in .streamlit/secrets.toml to the ID above.")


if __name__ == "__main__":
    main()
