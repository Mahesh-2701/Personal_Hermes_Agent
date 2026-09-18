#!/usr/bin/env python3
"""Get the correct Telegram token for Mahesh's main bot."""

import os
import sys
import json
import urllib.request
import urllib.parse

CHAT_ID = "5191016577"


def get_all_tokens():
    tokens = {}
    for var in os.environ:
        if "TELEGRAM" in var.upper() and "TOKEN" in var.upper():
            val = os.environ.get(var, "")
            if val and len(val) > 20:
                tokens[var] = val
    return tokens


def test_token(token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": "Which bot is this?",
        "disable_notification": True,
    }).encode()
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except:
        return False


def main():
    tokens = get_all_tokens()
    
    print("Telegram bots found:")
    for name, token in tokens.items():
        # Get bot info
        try:
            url = f"https://api.telegram.org/bot{token}/getMe"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                bot = json.loads(resp.read())["result"]
                username = bot.get("username", "?")
                can_send = "✓" if test_token(token, CHAT_ID) else "✗"
                print(f"  {can_send} @{username} ({name})")
        except:
            print(f"  ✗ {name} (can't identify)")
    
    print("\n👉 Your main bot is likely @Dci_employeebot")
    print("   Updating alert scripts to use HERMES_EMPLOYEE_TELEGRAM_TOKEN...")


if __name__ == "__main__":
    main()
