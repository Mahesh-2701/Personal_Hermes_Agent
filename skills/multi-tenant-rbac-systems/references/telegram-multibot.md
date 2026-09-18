# Multi-bot Telegram routing — practical notes

## Why a second bot never replies

A Hermes (or any) agent's live Telegram gateway listener is typically wired to
exactly ONE bot token (the one in the platform config). Creating additional
BotFather tokens for other roles (CTO bot, CMO bot, etc.) and adding them to
your RBAC config does NOT automatically give them a live listener — they're
just registered identities/tokens for role resolution and outbound sends.
Messaging a new bot with `/start` will get silence unless:
- the agent's gateway is reconfigured to also poll/webhook that token, or
- you manually poll (`getUpdates`) and push (`sendMessage`) through it, e.g.
  for one-off testing.

This is expected behavior, not a bug — don't tell the user "it's broken";
explain the listener-vs-token distinction directly.

## Manual test-message workflow (no live listener required)

1. Confirm the token is real: `GET https://api.telegram.org/bot<token>/getMe`
   — read-only, returns the bot's username/id, sends nothing.
2. Have the user DM the bot at least once (any text, e.g. "hi") — Telegram
   bots cannot initiate a conversation; they can only reply to a chat_id that
   has already messaged them.
3. Fetch that chat_id: `GET .../getUpdates` — look at
   `result[].message.chat.id` and `.from.id`. If empty, the message hasn't
   landed yet (or was already consumed by a webhook) — ask the user to
   resend and re-poll; don't assume failure from one empty check.
4. Send the real content: `POST .../sendMessage` with that chat_id.

## Markdown parse_mode bug with permission names

Telegram's default Markdown parser treats a single `_` as an unmatched italics
marker. Permission/action names with underscores (e.g. `ai_news.read`,
`change_hermes_config`) will make `sendMessage` fail with:
`Bad Request: can't parse entities: Can't find end of the entity...`
Fix: pass `parse_mode=''` (plain text) for any message whose body is built
from raw config/action strings, or escape underscores for MarkdownV2 if
formatting is required. Don't silently swallow the error — it will look like
the token/bot is broken when it's actually a formatting mismatch.

## Token handling

- Store bot tokens only as env vars (e.g. `HERMES_<ROLE>_TELEGRAM_TOKEN`) in
  the credential store (`.env`), never in YAML config, never echoed back to
  the user in chat once received, never printed in logs/audit records.
- Config validation should check `token_env` names are unique across bots
  (two roles accidentally pointing at the same token defeats the whole
  point of separate bots).
