#!/usr/bin/env python3
import subprocess
import urllib.request
import urllib.parse
import json
import os

# Get report text
result = subprocess.run(
    ['python3', '/Users/apple/.hermes/scripts/crm_real_report.py'],
    capture_output=True, text=True
)
text = result.stdout.strip()

# Use HERMES_MANAGER_TELEGRAM_TOKEN from environment (set by cron job)
token = os.environ.get('HERMES_MANAGER_TELEGRAM_TOKEN')
if not token:
    print("ERROR: No TELEGRAM token found in environment")
    exit(1)

chat_id = '5191016577'
url = f'https://api.telegram.org/bot{token}/sendMessage'
data = urllib.parse.urlencode({'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}).encode()

req = urllib.request.Request(url, data=data)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read().decode())
    print(f"ok={result.get('ok')}, description={result.get('description', '')}")
except Exception as e:
    print(f"ERROR: {e}")
