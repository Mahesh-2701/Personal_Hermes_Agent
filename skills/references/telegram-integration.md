# Telegram Integration for Competitor Intelligence Alerts

Documented working approach for sending competitor intelligence alerts via Telegram.

## Setup

The Telegram integration was configured to send alerts to Mahesh's chat (ID: 5191016577).

### Token Resolution Order

The alert system (`alert.py`) resolves the bot token in this order:

1. `TELEGRAM_BOT_TOKEN` environment variable
2. `HERMES_MANAGER_TELEGRAM_TOKEN` (Hermes multi-bot environment)
3. `HERMES_TELEGRAM_TOKEN`
4. `HERMES_CMO_TELEGRAM_TOKEN`
5. `HERMES_EMPLOYEE_TELEGRAM_TOKEN`

A token is considered valid if it's a non-empty string longer than 20 characters (basic sanity check for a bot token format).

### Chat ID

The chat ID `5191016577` is hardcoded in `alert.py` and `telegram_summary.py`, sourced from the Hermes config.yaml home_channel configuration. To send to a different chat, update the `CHAT_ID` constant in both scripts.

### Test Message

A test message was successfully sent during setup (Message ID: 32). The message included:

```html
<b>🤖 Hermes Competitor Intelligence</b>
<i>Your competitor intelligence system is now active!</i>
...
```

### Sending Messages

Both `alert.py` and `telegram_summary.py` use the same pattern:

```python
import urllib.request, urllib.parse, json

url = f"https://api.telegram.org/bot{token}/sendMessage"
data = urllib.parse.urlencode({
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "HTML",
}).encode()

req = urllib.request.Request(url, data=data)
with urllib.request.urlopen(req, timeout=10) as resp:
    result = json.loads(resp.read())
    if result.get("ok"):
        print(f"Message sent! ID: {result['result']['message_id']}")
```

### Alert Deduplication

The alert system implements a 24-hour cooldown to prevent spam. The cooldown key is `{entity_id}:{event_type}`. Once an alert is sent for a given entity+event_type pair, no further alerts for that pair will be sent within 24 hours.

The state is persisted in `~/.hermes/data/competitor-intelligence/alerts/alert_state.json`.

### Known Issue

The `alert.py` `send_telegram()` function had its token resolution updated mid-session. Ensure that any future modifications to `alert.py` preserve the environment variable fallback chain and the hardcoded chat_id.

## Files

- `scripts/alert.py` — Alert checking with Telegram delivery
- `scripts/telegram_summary.py` — Comprehensive periodic summary
- `scripts/telegram_final.py` — One-time full system summary
- `scripts/telegram_setup.py` — Token discovery and test (reference only)
