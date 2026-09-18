# Hermes Model Provider Setup — Competitor Intelligence

Documented working model provider configuration for Hermes when used with the competitor intelligence system.

## The Problem

Hermes config.yaml specifies a model provider and model name. If the provider is set to
`gemini` but no Gemini API key is configured in the environment, **both CLI and Telegram
sessions fail** with an error like:

```
gemini api key failed
```

This is not a bug in Hermes — it's a missing credential for the specified provider. The
competitor intelligence system specifically depends on Hermes being able to respond to
queries and send Telegram messages, so an invalid model configuration blocks the entire
system.

## Symptom

Any message sent via Telegram or CLI results in:

```
gemini api key failed
```

The system is unusable for competitor intelligence because Hermes can't process queries
or generate alerts.

## Root Cause

`~/.hermes/config.yaml` lines 1-4 (before fix):

```yaml
model:
  default: gemini-3.1-flash-lite
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta
```

Two issues:
1. Model name `gemini-3.1-flash-lite` doesn't exist (correct name would be `gemini-2.5-flash-lite`)
2. Provider `gemini` requires `GOOGLE_API_KEY` in environment, which was not set

## Fix

Switch to a provider with working credentials. The working configuration for this user is:

```yaml
model:
  default: upstage/solar-pro4:free
  provider: nous
```

This uses Hermes' internal OAuth for the Nous provider, so no separate API key environment
variable is needed. This is the same model the user runs in the terminal.

## Provider Options

| Provider | Model | Credential Required | Working? |
|----------|-------|---------------------|----------|
| `gemini` | `gemini-2.5-flash-lite` | `GOOGLE_API_KEY` env var | Not configured |
| `nous` | `upstage/solar-pro4:free` | Hermes internal OAuth | Working |
| `openai` | `gpt-4o` | `OPENAI_API_KEY` env var | Not tested |
| `openrouter` | any model | `OPENROUTER_API_KEY` env var | Not tested |

## Verification

After changing config.yaml, verify by sending a message via Telegram or CLI. The model
should respond normally.

For Telegram specifically, test with a simple message like "hello" or "what competitors
are tracked?".

## Environment Variables

The `TELEGRAM_BOT_TOKEN` must also be set for Telegram to work:

```bash
export TELEGRAM_BOT_TOKEN="8914691230:AAGTm0tJtAg_IjNtYzodjy97UVrCn8rx2h4"
```

This is the token for `@Jarvis_ai_Hermesbot` — the user's main bot, NOT the Hermes
multi-bot tokens (HERMES_MANAGER_TELEGRAM_TOKEN, etc.).

## Files

- `~/.hermes/config.yaml` — Hermes main configuration (model provider section)
- `references/telegram-bot-identity.md` — Telegram bot identity documentation
