---
name: multi-bot-gateway
description: "Launch multiple per-bot Telegram gateway instances."
tags: [multi-bot, telegram, gateway, ops]
category: ops
---

# Multi-Bot Telegram Gateway

Hermes ships with ONE gateway polling ONE token (`TELEGRAM_BOT_TOKEN` = CEO bot). Other bot tokens that exist as env vars (`HERMES_CMO_TELEGRAM_TOKEN`, etc.) are silent until a second gateway polls them.

This skill covers launching and managing per-bot gateway instances so every role bot receives messages.

## When to Use

- Multiple Telegram bot tokens exist but only one receives messages.
- User asks "why isn't my other bot receiving" or "make all bots working".
- User wants to verify which bots are live.

## When NOT to Use

- Only one bot exists and it's not receiving — single-token debugging, not multi-bot.
- Token is invalid/expired — verify with `scripts/verify_bot_token.py` first.

## Core Pattern

Each bot needs:
1. Its own `HERMES_HOME` (isolated sessions/sockets/logs).
2. `TELEGRAM_BOT_TOKEN` set to THAT bot's token at launch.
3. A copy of ops RBAC config (`identities.yaml`, `permissions.yaml`, `roles.yaml`, `telegram_bots.yaml`) in its `config/`.

## Prerequisites

- Each token must be a valid 46-char BotFather token.
- Each token exported as env var before launch.
- Hermes agent at `~/.hermes/hermes-agent` with working venv.
- Ops RBAC config at `~/.hermes/ops/config/` with bot-scoped identity rows.

## Launch

```bash
HERMES_HOME=$HOME/.hermes/ops/bot_homes/cmo \
TELEGRAM_BOT_TOKEN=$HERMES_CMO_TELEGRAM_TOKEN \
python3 $HOME/.hermes/hermes-agent/hermes_cli/main.py gateway run --external-supervisor &
```

Key env vars: `HERMES_HOME` (isolated home), `TELEGRAM_BOT_TOKEN` (the bot's token, NOT the role-env-var name), `_HERMES_GATEWAY=1`, `HERMES_QUIET=1` (optional).

## Verify

Check bot log for:
```
Telegram polling confirmed healthy: getUpdates progressing
Connected to Telegram (polling mode)
✓ telegram connected
```

Check `<bot_home>/gateway.sock` exists.

Message each bot from Telegram and confirm reply. Identity resolves via `bot_id` in `identities.yaml`.

## Pitfalls

- **Not isolating HERMES_HOME**: gateways sharing a home fight over session store, socket, kanban lock.
- **Forgetting `TELEGRAM_BOT_TOKEN`**: gateway reads `TELEGRAM_BOT_TOKEN`, not `HERMES_CMO_TELEGRAM_TOKEN`. Export both.
- **Kanban lock**: first gateway holds `/Users/apple/.hermes/kanban/.dispatcher.lock`; siblings log "will NOT dispatch" — fine for inbound-only bots.
- **Missing config in bot home**: without `identities.yaml`, `resolve_identity()` fails closed to UNAUTHORIZED.
- **Token env not exported**: launching from a script that doesn't inherit shell env loses the token.
- **`TELEGRAM_ALLOWED_USERS` not set**: gateway rejects messages as "Unauthorized user" even when the token is valid. Each isolated gateway needs its own allowlist env var (e.g. `TELEGRAM_ALLOWED_USERS=5191016577` in the launch env).
- **Provider auth failure ("No inference provider configured")**: isolated bot homes lack `auth.json` (the file the gateway reads for `active_provider`, NOT `shared/nous_auth.json` alone). Without it the gateway can't resolve the model provider and falls back to a canned stub reply. Sync `~/.hermes/auth.json` into each bot home before launch, and ensure `active_provider` is set to the intended provider (e.g. `nous`). If the OAuth token is expired, the provider will still fail — refresh the token via the provider's OAuth flow before relaunching.
- **Stale PID file blocking relaunch**: after killing a gateway, the `gateway.pid` file may persist and the process may respawn via the external supervisor, causing "Gateway already running" errors on the next launch. Always `kill -9` the PID, verify the process is gone via `ps`/`kill -0`, remove the pid file, AND pkill by pattern (`pkill -9 -f "gateway.<role>"`) before launching. Prefer a launcher script that does all three cleanup steps atomically.

## References

- `references/telegram-bot-tokens.md` — token env var names, bot usernames, verification.
- `references/hermes-gateway-isolation.md` — HERMES_HOME isolation pattern.

## Scripts

- `scripts/verify_bot_token.py` — hit `getMe` for a token, print username.
- `scripts/manage_bots.py` — launch/stop/restart/status/test for all role bots. MUST include: (1) `kill_existing()` that SIGKILLs by pid file + pkill by pattern before launch, (2) sync of `auth.json` from main Hermes home into each bot home, (3) sync of provider model caches (`provider_models_cache.json`, `models_dev_cache.json`, `cache/`), (4) `TELEGRAM_ALLOWED_USERS` in the launch env, (5) `active_provider` set in synced `auth.json` if needed.

## Related

- `omh-gateway-intent-card` — delivery policy (different concern).
- `~/.hermes/ops/config/telegram_bots.yaml` — bot_id → token_env mapping.
- `~/.hermes/ops/config/identities.yaml` — (platform, user_id, bot_id) → role.
- `~/.hermes/ops/config/permissions.yaml` — per-role permission matrices.
