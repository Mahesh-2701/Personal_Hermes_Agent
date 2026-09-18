# Hermes Gateway Isolation Pattern

## Why isolation is needed

The Hermes gateway stores per-session state, the control socket (`gateway.sock`), the loop-tick socket, and the kanban dispatcher lock under `HERMES_HOME`. If two gateways share the same home:

- They fight over the session database.
- They collide on the control socket path.
- The second gateway logs "another gateway already holds the dispatcher lock; this gateway will NOT dispatch."

## The pattern

Give each bot its own `HERMES_HOME`:

```
~/.hermes/ops/bot_homes/<role>/
  config/     # RBAC config copy
  sessions/
  logs/
  state/
```

Then launch with:

```bash
HERMES_HOME=$HOME/.hermes/ops/bot_homes/cmo \
TELEGRAM_BOT_TOKEN=$HERMES_CMO_TELEGRAM_TOKEN \
python3 .../hermes_cli/main.py gateway run --external-supervisor &
```

## What goes in each bot home's config/

- `identities.yaml` — bot-scoped identity rows so `resolve_identity()` returns the right role.
- `permissions.yaml` — per-role permission matrices.
- `roles.yaml` — role metadata.
- `telegram_bots.yaml` — bot_id → token_env mapping (used by `telegram_client.send_message`).
- `config.yaml` — minimal gateway config (model, platform toolsets, etc.).

## Kanban dispatcher lock note

The first gateway to start holds `/Users/apple/.hermes/kanban/.dispatcher.lock`. Subsequent gateways skip kanban dispatch. This is fine for inbound-only bots — receiving and replying to Telegram messages does not require kanban dispatch.

## Session storage

Each gateway stores sessions under `<HERMES_HOME>/sessions/`. With isolated homes, each bot's sessions are independent and never collide.
