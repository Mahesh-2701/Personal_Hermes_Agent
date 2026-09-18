#!/usr/bin/env python3
"""
Telegram setup and test for competitor intelligence alerts.
Finds Telegram bot token and sends a test message.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

HERMES_HOME = Path.home() / ".hermes"
CONFIG_FILE = HERMES_HOME / "config.yaml"
AUTH_FILE = HERMES_HOME / "auth.json"
CHAT_ID = "5191016577"  # From config.yaml


def find_telegram_token():
    """Find Telegram bot token from various sources."""
    
    # 1. Check environment variables
    env_vars = [
        "TELEGRAM_BOT_TOKEN",
        "HERMES_TELEGRAM_TOKEN",
        "TELEGRAM_TOKEN",
        "BOT_TOKEN",
        "HERMES_MANAGER_TELEGRAM_TOKEN",
    ]
    
    for var in env_vars:
        val = os.environ.get(var, "")
        if val and len(val) > 20 and ":" in val:
            print(f"Found token in env: {var}")
            return val
    
    # 2. Read config.yaml for token reference
    try:
        import yaml
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                config = yaml.safe_load(f) or {}
            
            # Check plugins section for Telegram
            plugins = config.get("plugins", {})
            for plugin_name, plugin_config in plugins.items():
                if "telegram" in plugin_name.lower():
                    token = plugin_config.get("token", "")
                    if token and len(token) > 20:
                        print(f"Found token in config.yaml plugins.{plugin_name}")
                        return token
                    
                    # Check nested token
                    if isinstance(plugin_config, dict):
                        for key in ["bot_token", "api_token", "credentials"]:
                            val = plugin_config.get(key, "")
                            if val and len(str(val)) > 20:
                                print(f"Found token in config.yaml plugins.{plugin_name}.{key}")
                                return str(val)
    except Exception as e:
        print(f"Error reading config.yaml: {e}")
    
    # 3. Try to find token in auth files (may require special access)
    # Check common locations
    auth_paths = [
        HERMES_HOME / "auth.json",
        HERMES_HOME / "config" / "auth.json",
        Path("/Users/apple/.hermes/config/auth.json"),
    ]
    
    for auth_path in auth_paths:
        if auth_path.exists():
            try:
                with open(auth_path) as f:
                    auth_data = json.load(f)
                
                # Search recursively for Telegram tokens
                def search_tokens(obj, path=""):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if "telegram" in k.lower():
                                if isinstance(v, str) and len(v) > 20 and ":" in v:
                                    print(f"Found token at {path}.{k}")
                                    return v
                                elif isinstance(v, dict):
                                    result = search_tokens(v, f"{path}.{k}")
                                    if result:
                                        return result
                    return None
                
                token = search_tokens(auth_data)
                if token:
                    print(f"Found token in {auth_path}")
                    return token
            except Exception as e:
                print(f"Error reading {auth_path}: {e}")
    
    return None


def send_telegram_message(token, chat_id, message):
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read())
            if result.get("ok"):
                print(f"Message sent successfully!")
                print(f"Message ID: {result['result']['message_id']}")
                return True
            else:
                print(f"Telegram API error: {result.get('description', 'Unknown error')}")
                return False
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False


def main():
    print("=" * 50)
    print("COMPETITOR INTELLIGENCE - TELEGRAM SETUP")
    print("=" * 50)
    print()
    
    print(f"Target chat: {CHAT_ID} (Mahesh)")
    print()
    
    token = find_telegram_token()
    
    if not token:
        print("ERROR: Could not find Telegram bot token!")
        print()
        print("Please set TELEGRAM_BOT_TOKEN environment variable:")
        print("  export TELEGRAM_BOT_TOKEN='your-bot-token-here'")
        print()
        print("Or add it to ~/.hermes/.env file:")
        print("  TELEGRAM_BOT_TOKEN=your-bot-token-here")
        print()
        print("You can get a bot token from @BotFather on Telegram.")
        return 1
    
    # Test message
    test_message = """
<b>🤖 Hermes Competitor Intelligence</b>

Your competitor intelligence system is now active!

<b>Tracked Competitors (11):</b>
• OpenAI (High)
• Anthropic (High)
• Google DeepMind (High)
• Meta AI (High)
• Mistral AI (High)
• DeepSeek (High)
• xAI (High)
• Cohere (Medium)
• Hugging Face (Medium)
• Stability AI (Medium)
• EleutherAI (Low)

<b>Tracked People (24):</b>
Including Sam Altman, Dario Amodei, Sundar Pichai, Demis Hassabis,
Elon Musk, Jensen Huang, and more.

<b>Collection Schedule:</b>
• Every 6h: Collect & diff high-priority competitors
• Daily 9am: Daily report
• Weekly Monday 9am: Weekly report

Use commands like:
• Track Company X
• What changed today?
• Competitor report
• Check OpenAI
"""
    
    print(f"Sending test message to Telegram...")
    success = send_telegram_message(token, CHAT_ID, test_message)
    
    if success:
        print("\nTelegram integration is WORKING!")
        print("Alerts will now be sent to your Telegram.")
        return 0
    else:
        print("\nTelegram send FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
