---
name: multi-tenant-rbac-systems
description: "Use when adding role permissions/approval gates to an agent."
version: 1.0.0
author: Hermes (curator)
category: software-development
metadata:
  tags: [rbac, authorization, identity, multi-tenant, multi-bot, telegram, fail-closed, audit-logging, risk-based-approval]
  related_skills: [backend, security-review, api-design]
---

# Multi-Tenant RBAC Systems (identity, roles, permissions, approval gates)

Use this when a user wants to turn a single-user agent/tool/ops system into one
that serves multiple people/roles safely — e.g. "add CEO/CTO/CMO/Manager access
to my Hermes ops system", "add role-based permissions to my bot", "support
multiple Telegram bots pointing at the same backend with different access
levels". This is backend/security work, not a from-scratch web app — do NOT
reach for `fullstack-builder`'s full design/Stitch/browser-QA pipeline for this
class of task; it is a permission-and-identity layer bolted onto an existing
system.

## Core methodology (apply in this order, every time)

1. **Audit before touching anything.** Search for existing identity/authz/
   audit code before writing new code — these systems often already have a
   partial scaffold (an identity resolver, a permission matrix, an audit
   logger) from an earlier session. Read it fully. Run the existing test
   suite for real (not from memory) and record the exact passing count
   before changing anything — that's your regression baseline.
2. **Extend additively, never replace.** Add new roles/fields alongside
   existing ones (e.g. keep legacy `OWNER/ADMIN/...` tiers AND add business
   roles `ceo/cto/cmo/...` in the same valid-roles set) so existing identities
   and tests keep working untouched. Prefer optional dataclass fields with
   defaults (`bot_id: str | None = None`) over changing existing signatures.
3. **One centralized authorization function, never scattered role checks.**
   `authorize_action(identity, action, approved=?)` should be the single
   gate: (a) permission check first — denial always wins regardless of any
   `approved` flag, (b) then risk-level check — HIGH/CRITICAL actions require
   an explicit `approved=True` even when permitted, (c) log every decision
   (allow, deny, pending-approval) via one audit function. Never let
   "approved" bypass "permitted" — test that ordering explicitly.
4. **Fail closed everywhere.** Unknown identity, unrecognized role, malformed
   YAML/config, missing permission entry → always deny, never grant. Write a
   `config_validation.py`-style startup check that catches: duplicate
   identities, invalid role names, duplicate bot tokens, and a permissive
   `default_role` (should be UNAUTHORIZED) — flag a non-default `default_role`
   as a warning even if not strictly invalid, so it never ships unnoticed.
5. **Role must never come from user-supplied text.** It resolves ONLY from a
   trusted server-side config keyed on the platform's own stable numeric user
   ID (never display name/username). For multi-bot setups, disambiguate
   further by a fixed `bot_id` attached server-side the moment a message
   arrives on that bot's token — never anything the remote user sends. Write
   an explicit test: same user_id, wrong bot_id → falls back to default deny.
6. **Test the escalation-resistance property directly**, don't just test the
   happy path: "unregistered user claiming role X" → still denied; "wrong bot
   for a bot-scoped identity" → still denied; "approved=True on a denied
   permission" → still denied.
7. **Run the full regression suite after every phase**, not just at the end.
   Report real before/after counts (e.g. "85/85 → 106/106"), never invented
   numbers, and always distinguish `IMPLEMENTED + TESTED` from `IMPLEMENTED
   BUT NOT LIVE-VERIFIED` (e.g. unit-tested permission logic vs. an actual
   live bot token that was never sent a real message) in your final report.

## Multi-bot Telegram routing specifics

See `references/telegram-multibot.md` for the concrete pitfalls: how bot
tokens map to roles, why a new bot token produces zero replies until wired
into a live gateway listener, how to manually poll/push messages through a
second bot for testing, and a real Markdown-parsing bug this class of task
hits (underscored permission action names like `ai_news.read` break Telegram's
default Markdown parse_mode).

## Config file shape (reusable pattern)

- `identities.yaml` — `(platform, user_id[, bot_id]) -> role` mapping, plus a
  `default_role: UNAUTHORIZED` fallback. An entry with no `bot_id` matches any
  bot (needed for backward compatibility when adding multi-bot support to a
  single-bot system).
- `roles.yaml` — descriptive metadata only; adding a role here alone grants
  nothing.
- `permissions.yaml` — the real `roles: {role: [action, ...]}` allow-list PLUS
  a `risk_levels: {action: LOW|MEDIUM|HIGH|CRITICAL}` section. Never invent
  permission names disconnected from what the system can actually do — derive
  the vocabulary from real capabilities found during the audit step.
- `telegram_bots.yaml` (or equivalent) — `bot_id -> token_env_var_NAME` only;
  the actual token lives in `.env`, never in a committed YAML file, never
  echoed back in chat when the user pastes one.

## Reporting to the user

Always produce, at minimum: architecture summary, files changed/added, before/
after test counts (real numbers from an actual run), and an explicit
IMPLEMENTED+TESTED vs IMPLEMENTED-BUT-NOT-LIVE-VERIFIED split. Don't claim a
live integration works until you've actually exercised it end to end with
real credentials — say so plainly when you haven't.
