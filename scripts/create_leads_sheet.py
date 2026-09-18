#!/usr/bin/env python3
"""Create the Lead Generation CRM Google Sheet."""

import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
except ImportError:
    print("ERROR: google-api-python-client not installed.")
    sys.exit(1)

IST = ZoneInfo("Asia/Kolkata")
NOW = datetime.now(IST)

LEADS_HEADERS = [
    "Lead ID", "Date Added", "Company Name", "Website", "Industry",
    "Size", "Location", "Contact Name", "Contact Role", "Email",
    "Phone", "LinkedIn", "Company LinkedIn", "Source", "Source URL",
    "Type", "Reason", "Signal", "Priority", "Status",
    "Assigned To", "Last Contacted", "Next Follow-up",
    "Follow-up Status", "Notes", "Last Updated",
]

SOURCE_HEADERS = [
    "Source", "Leads Discovered", "New Leads", "Duplicates",
    "Qualified", "High Priority", "Contactable", "Meetings",
    "Conversions", "Last Checked",
]

SEARCH_STATE_HEADERS = [
    "Source", "Last Search Time", "Last Query", "Last Page",
    "Last Result", "Candidates Found", "New Leads", "Duplicates",
]


def get_service():
    """Get Sheets API service."""
    token_path = os.path.expanduser("~/.hermes/google_token.json")
    with open(token_path) as f:
        td = json.load(f)
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    
    creds = Credentials(
        token=td.get("token"),
        refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=td.get("client_id"),
        client_secret=td.get("client_secret"),
        scopes=scopes,
    )
    
    try:
        creds.refresh(None)
    except Exception:
        pass
    
    return build("sheets", "v4", credentials=creds), build("drive", "v3", credentials=creds)


def create_spreadsheet_with_sheets(sheets_service, drive_service):
    """Create new spreadsheet with 3 sheets."""
    
    # Create spreadsheet
    spreadsheet = {
        "properties": {"title": "Lead Generation CRM"},
        "sheets": [
            {"properties": {"title": "LEADS", "index": 0, "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 2}}},
            {"properties": {"title": "SOURCE_PERFORMANCE", "index": 1, "gridProperties": {"frozenRowCount": 1}}},
            {"properties": {"title": "SEARCH_STATE", "index": 2, "gridProperties": {"frozenRowCount": 1}}},
        ],
    }
    
    try:
        result = sheets_service.spreadsheets().create(body=spreadsheet).execute()
        sheet_id = result.get("spreadsheetId")
        print(f"✅ Created spreadsheet: {sheet_id}")
        return sheet_id
    except Exception as e:
        print(f"ERROR creating spreadsheet: {e}")
        sys.exit(1)


def populate_sheets(sheets_service, sheet_id):
    """Add data and formatting to sheets."""
    
    # Define requests for each sheet
    requests_list = []
    
    # LEADS: headers + formatting
    requests_list.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"stringValue": h}} for h in LEADS_HEADERS]}],
            "fields": "userEnteredValue,userEnteredFormat",
            "start": {"sheetId": 0, "rowIndex": 0, "columnIndex": 0}
        }
    })
    
    # SOURCE_PERFORMANCE: headers + data
    requests_list.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"stringValue": h}} for h in SOURCE_HEADERS]}],
            "fields": "userEnteredValue",
            "start": {"sheetId": 1, "rowIndex": 0, "columnIndex": 0}
        }
    })
    
    # Add default source data
    default_sources = [
        ["Clutch", 0, 0, 0, 0, 0, 0, 0, 0, ""],
        ["ProductHunt", 0, 0, 0, 0, 0, 0, 0, 0, ""],
        ["GoodFirms", 0, 0, 0, 0, 0, 0, 0, 0, ""],
        ["AngelList", 0, 0, 0, 0, 0, 0, 0, 0, ""],
        ["GitHub", 0, 0, 0, 0, 0, 0, 0, 0, ""],
        ["LinkedIn", 0, 0, 0, 0, 0, 0, 0, 0, ""],
    ]
    source_rows = []
    for row in default_sources:
        source_rows.append({"values": [{"userEnteredValue": {"stringValue": str(c)}} for c in row]})
    requests_list.append({
        "updateCells": {
            "rows": source_rows,
            "fields": "userEnteredValue",
            "start": {"sheetId": 1, "rowIndex": 1, "columnIndex": 0}
        }
    })
    
    # SEARCH_STATE: headers
    requests_list.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"stringValue": h}} for h in SEARCH_STATE_HEADERS]}],
            "fields": "userEnteredValue",
            "start": {"sheetId": 2, "rowIndex": 0, "columnIndex": 0}
        }
    })
    
    body = {"requests": requests_list}
    
    try:
        sheets_service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
        print("✅ Populated all sheets")
    except Exception as e:
        print(f"ERROR populating sheets: {e}")


def share_spreadsheet(drive_service, sheet_id):
    """Share with owner if email is set."""
    email = os.environ.get("USER_EMAIL")
    if not email:
        print("ℹ️  Set USER_EMAIL env var to auto-share")
        return
    
    try:
        drive_service.permissions().create(
            fileId=sheet_id,
            body={"type": "user", "role": "writer", "emailAddress": email},
        ).execute()
        print(f"✅ Shared with {email}")
    except Exception as e:
        print(f"Warning: Could not share: {e}")


def add_sample_data(sheets_service, sheet_id):
    """Add a few sample leads to demonstrate the schema."""
    sample_leads = [
        ["LEAD-20260918-0001", NOW.strftime("%Y-%m-%d %H:%M"), "Example SaaS Co", "https://example.com", "SaaS", 
         "10-50", "Chennai", "John Doe", "CEO", "john@example.com", "+91-9876543210",
         "https://linkedin.com/in/johndoe", "https://linkedin.com/company/example", "Clutch",
         "https://clutch.co/profile/example", "Referral", "Hiring developers, expanding product team",
         "High hiring velocity", "High", "New", "", "", "", "", "Matched ICP + active hiring",
         NOW.strftime("%Y-%m-%d %H:%M")],
    ]
    
    try:
        sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="LEADS!A2",
            valueInputOption="USER_ENTERED",
            body={"values": sample_leads},
        ).execute()
        print("✅ Added sample lead")
    except Exception as e:
        print(f"Warning: Could not add sample: {e}")


def main():
    print("=" * 60)
    print("LEAD GENERATION CRM - Sheet Creation")
    print(f"Run Time: {NOW.strftime('%d %b %Y · %H:%M IST')}")
    print("=" * 60)
    
    sheets_service, drive_service = get_service()
    sheet_id = create_spreadsheet_with_sheets(sheets_service, drive_service)
    populate_sheets(sheets_service, sheet_id)
    share_spreadsheet(drive_service, sheet_id)
    add_sample_data(sheets_service, sheet_id)
    
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    
    print()
    print("=" * 60)
    print("DONE! Your Lead Generation CRM is ready:")
    print(f"Sheet ID: {sheet_id}")
    print(f"URL: {sheet_url}")
    print()
    print("Next steps:")
    print("1. Copy the Sheet ID above")
    print("2. Update lead_generation.py LEADS_SHEET_ID")
    print("3. Run: python3 /Users/apple/.hermes/scripts/lead_generation.py --dry-run")
    print("4. Set up cron: hermes cron add 'every day at 2pm' --skill lead-generation")
    print("=" * 60)
    
    # Save config
    config = {
        "LEADS_SHEET_ID": sheet_id,
        "SHEET_URL": sheet_url,
        "CRM_SPREADSHEET_ID": "1Zf0TrJVhzW6tnlKaG0MMCoe9kiKPHMg1A5l1DmFmNFc",
    }
    
    config_path = "/Users/apple/.hermes/scripts/.leads_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to: {config_path}")


if __name__ == "__main__":
    main()
