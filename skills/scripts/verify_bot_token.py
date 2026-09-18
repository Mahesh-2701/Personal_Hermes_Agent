#!/usr/bin/env python3
"""Verify a Telegram bot token by hitting getMe.

Usage: python3 verify_bot_token.py <role>
       python3 verify_bot_token.py cmo
       python3 verify_bot_token.py manager
       python3 verify_bot_token.py employee
       python3 verify_bot_token.py cto

Role → env var mapping:
  cmo      → HERMES_CMO_TELEGRAM_TOKEN
  manager  → HERMES_MANAGER_TELEGRAM_TOKEN
  employee → HERMES_EMPLOYEE_TELEGRAM_TOKEN
  cto      → HERMES_CTO_TELEGRAM_TOKEN
"""
import os
import sys
import json
import urllib.request

ROLE_TO_TOKEN_ENV = {
    "cmo": "HERMES_CMO_TELEGRAM_TOKEN",
    "manager": "HERMES_MANAGER_TELEGRAM_TOKEN",
    "employee": "HERMES_EMPLOYEE_TELEGRAM_TOKEN",
    "cto": "HERMES_CTO_TELEGRAM_TOKEN",
}

def verify(role: str):
    env_name = ROLE_TO_TOKEN_ENV.get(role)
    if not env_name:
        print(f"Unknown role: {role}. Choose from: {list(ROLE_TO_TOKEN_ENV.keys())}")
        sys.exit(1)
    token = os.environ.get(env_name)
    if not token:
        print(f"FAIL: {env_name} is not set in the environment")
        sys.exit(1)
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if data.get("ok"):
                username = data["result"].get("username", "?")
                print(f"OK: @{username}  (token valid)")
            else:
                print(f"FAIL: {data.get('description', 'unknown error')}")
                sys.exit(1)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"FAIL: HTTP {e.code} — {body[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    role = sys.argv[1] if len(sys.argv) > 1 else "cmo"
    verify(role)
