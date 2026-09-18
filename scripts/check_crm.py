#!/usr/bin/env python3
"""Check CRM sheet structure and existing data."""
import sys
sys.path.insert(0, '/Users/apple/.hermes/scripts')

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    print("gspread not available — attempting install via pip...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'gspread', 'google-auth', '-q'], check=False)
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("FATAL: Cannot import gspread even after install attempt")
        sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CRED_PATH = '/Users/apple/.hermes/scripts/crm-service-account.json'
SHEET_KEY = '1guNSf6QdXZ7rQ5zshGVSNcWpkz94Jzgbhk0LjBC7KIU'

creds = Credentials.from_service_account_file(CRED_PATH, scopes=SCOPES)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_KEY)

print(f"Sheet title: {sheet.title}")
print(f"Worksheet count: {len(sheet.worksheets)}")

for i, ws in enumerate(sheet.worksheets):
    print(f"\n--- Sheet {i}: '{ws.title}' ---")
    print(f"  Rows: {ws.row_count}, Cols: {ws.col_count}")
    values = ws.get_all_values()
    print(f"  Actual rows with data: {len(values)}")
    if values:
        print(f"  Header: {values[0]}")
        for j, row in enumerate(values[1:], 1):
            print(f"  Row {j}: {row}")
    else:
        print("  (empty)")
