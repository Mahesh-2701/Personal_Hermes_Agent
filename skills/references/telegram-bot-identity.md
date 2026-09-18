# Telegram Bot Identity for Competitor Intelligence

Documented bot identities in Hermes' multi-bot environment and which one is the user's main bot.

## Bot Identities

Hermes' Telegram environment has multiple bots. All were tested and confirmed to deliver to chat `5191016577`:

| Bot | Username | Bot ID | Purpose |
|-----|----------|--------|---------|
| Manager | `@Dci_managerbot` | 8879964163 | Manager-level operations |
| CMO | `@Dci_cmohermesbot` | 8770586389 | CMO-level operations |
| Employee | `@Dci_employeebot` | 8749653307 | Employee-level operations |
| **Main (User's)** | `@Jarvis_ai_Hermesbot` | 8914691230 | **Personal chat bot — this is the one to use** |

## User's Main Bot

The bot the user actually chats with is **@Jarvis_ai_Hermesbot** (ID: 8914691230).

Token: `8914691230:AAGTm0tJtAg_IjNtYzodjy97UVrCn8rx2h4`

This token should be stored in the `TELEGRAM_BOT_TOKEN` environment variable or used directly in alert scripts.

## Token Resolution (alert.py)

`alert.py` resolves the bot token in this order:

1. `TELEGRAM_BOT_TOKEN` environment variable (user's main bot — preferred)
2. Hardcoded fallback: `8914691230:AAGTm0tJtAg_IjNtYzodjy97UVrCn8rx2h4`

Do NOT use `HERMES_MANAGER_TELEGRAM_TOKEN`, `HERMES_CMO_TELEGRAM_TOKEN`, or `HERMES_EMPLOYEE_TELEGRAM_TOKEN` for user-facing alerts — those are for Hermes' internal multi-bot operations.

## Chat ID

Chat ID `5191016577` is hardcoded in alert scripts, sourced from Hermes config.yaml `home_channel`.

## Test

To verify the correct bot is being used:

```python
import urllib.request, json

token = "8914691230:AAGTm0tJtAg_IjNtYzodjy97UVrCn8rx2h4"
url = f"https://api.telegram.org/bot{token}/getMe"
with urllib.request.urlopen(url) as r:
    bot = json.loads(r.read())["result"]
    print(f"Bot: @{bot['username']} (ID: {bot['id']})")
```

Expected output: `Bot: @Jarvis_ai_Hermesbot (ID: 8914691230)`

## Files

- `scripts/alert.py` — Alert checking with Telegram delivery (uses main bot token)
- `scripts/telegram_summary.py` — Periodic summary (uses main bot token)
- `scripts/telegram_final.py` — One-time full summary (uses main bot token)
- `scripts/telegram_setup.py` — Token discovery script
- `scripts/find_main_bot.py` — Bot identification helper
