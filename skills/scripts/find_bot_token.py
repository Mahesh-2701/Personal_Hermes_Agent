#!/usr/bin/env python3
"""
Get the correct Telegram token for Mahesh's main bot.
Tries tokens and checks which one can send to chat 5191016577.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

CHAT_ID = "5191016577"


def get_all_tokens():
    """Get all Telegram tokens from environment."""
    tokens = {}
    
    for var in os.environ:
        if "TELEGRAM" in var.upper() and "TOKEN" in var.upper():
            val = os.environ.get(var, "")
            if val and len(val) > 20:
                tokens[var] = val
    
    return tokens


def test_token(token, chat_id):
    """Test if a token can send messages."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": "🔍 Token test",
        "disable_notification": True,  # Silent test
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                msg_id = result["result"].get("message_id")
                print(f"  ✅ {token[:20]}... -> Message ID: {msg_id}")
                return True
            else:
                print(f"  ❌ {token[:20]}... -> {result.get('description', 'Unknown')}")
                return False
    except Exception as e:
        print(f"  ❌ {token[:20]}... -> Error: {e}")
        return False


def main():
    print("=" * 50)
    print("TELEGRAM TOKEN DIAGNOSTICS")
    print("=" * 50)
    print(f"\nTarget: Chat {CHAT_ID} (Mahesh)")
    print()
    
    tokens = get_all_tokens()
    
    if not tokens:
        print("❌ No Telegram tokens found in environment!")
        print("\nAvailable env vars with 'TELEGRAM':")
        for var in os.environ:
            if "TELEGRAM" in var.upper():
                print(f"  {var} = {os.environ.get(var, '')[:30]}...")
        return 1
    
    print(f"Found {len(tokens)} token(s):\n")
    for name, token in tokens.items():
        print(f"  {name}")
        print(f"    Value: {token[:30]}...{token[-5:]}")
    print()
    
    print("Testing which token works for your chat...\n")
    
    working = []
    for name, token in tokens.items():
        if test_token(token, CHAT_ID):
            working.append(name)
    
    print()
    if working:
        print(f"✅ {len(working)} token(s) work:")
        for name in working:
            print(f"  - {name}")
        print(f"\n👉 Use {working[0]} for alerts to your main bot!")
        return 0
    else:
        print("❌ None of the tokens can send to your chat.")
        print("\nPossible issues:")
        print("  1. Tokens are for different bots/chats")
        print("  2. Bot is not added to your chat (5191016577)")
        print("  3. Bot was blocked or removed")
        print("\nTo get your main bot's token:")
        print("  - Check which bot you talk to in Telegram")
        print("  - That bot's token should be in config or auth")
        return 1


if __name__ == "__main__":
    sys.exit(main())
