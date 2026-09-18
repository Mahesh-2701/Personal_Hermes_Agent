# Multi-Bot CRM Integration Pattern

## Summary

This document captures the pattern from Mahesh's session: deploying a shared CRM analytics skill across 3 independent Telegram bots (CMO, Manager, Employee) with unified Zoho CRM backend.

## Architecture

```
Zoho CRM (Live Data)
    |
    | (Single OAuth token in ~/.hermes/config.yaml)
    |
    v
~/.hermes/skills/crm-analytics-report/  (Shared skill code)
    |
    | (All 3 bots load this skill)
    |
    +----> CMO Bot     (cmo/)
    +----> Manager Bot (manager/)
    +----> Employee Bot (employee/)
```

## Key Learnings

### 1. Shared Skills, Isolated Pairing

- **Skills** are installed once in the main Hermes home (`~/.hermes/skills/crm-analytics-report/`)
- All bot instances load and execute the same skill code
- **Pairing state** is PER BOT HOME — user must be approved separately for each role bot

**Implication:** A user authorized with the CMO bot cannot use the Manager bot until their ID is explicitly approved in `~/.hermes/ops/bot_homes/manager/`.

### 2. Model Configuration Hierarchy

Bots inherit model settings in this order (first found wins):

1. `~/.hermes/ops/bot_homes/$ROLE/config/config.yaml` (bot-specific override)
2. `$HERMES_HOME/config/config.yaml` (if HERMES_HOME is set)
3. `~/.hermes/config.yaml` (main default)

**Best Practice:** Keep bot home configs MINIMAL (just onboarding/seen metadata). Put model config in the main `~/.hermes/config.yaml` and let all bots inherit.

### 3. Common Pitfall: "Token Limit Reached" False Signal

**Symptom:** Bots seem to fail with "token limit reached" errors.

**Actual Cause:** Misconfigured model provider with insufficient credits.

**Debug Path:**
1. Check logs: `grep -i "error\|insufficient" ~/.hermes/ops/bot_homes/$role/logs/gateway.log`
2. Search for credential/credit errors: `grep -i "credits\|unauthorized\|paid.*model"` 
3. Verify config: `hermes config get model`

### 4. Environment Variable Handling for Bot Fleet

When starting bots, use explicit environment variables:

```bash
export TELEGRAM_BOT_TOKEN="$HERMES_CMO_TELEGRAM_TOKEN"
export HERMES_HOME="~/.hermes/ops/bot_homes/cmo"
export _HERMES_GATEWAY=1
```

Do NOT use shell `${VAR^^}` (uppercase expansion) — not portable across sh/bash/zsh.
Instead, explicitly reference `$HERMES_CMO_TELEGRAM_TOKEN`, etc.

## CRM Skill Integration Points

### Test Commands

All bots expose the same commands (assume `crm-analytics-report` skill is installed):

```
/crm_report       → Full CRM report (contacts + accounts + leads)
/crm_contacts     → Contacts analysis
/crm_leads        → Leads/deals pipeline
/crm_projects     → Projects status
```

### Data Sources

The skill supports two modes:

1. **Mock Data** (fallback when token is invalid/expired)
   - 245 contacts, 50 accounts, 78 leads
   - Useful for testing the infrastructure

2. **Live Zoho Data** (when token is valid)
   - Must update `ZOHO_CRM_ACCESS_TOKEN` in `~/.hermes/config.yaml`
   - Scope required: `ZohoCRM.modules.READ`
   - Generate fresh tokens at https://api-console.zoho.com/

### Zoho Token Refresh Workflow

If token expires and bots stop returning CRM data:

1. Generate fresh token: `https://api-console.zoho.com/` → OAuth → scope `ZohoCRM.modules.READ`
2. Update main config:
   ```bash
   hermes config set mcp_servers.zoho_crm.env.ZOHO_CRM_ACCESS_TOKEN "1000.YOUR_NEW_TOKEN"
   ```
3. Restart all bots (they will pick up the new config automatically)

## Deployment Checklist

- [ ] 3 bot home directories created
- [ ] Minimal config.yaml in each (onboarding section only)
- [ ] Main ~/.hermes/config.yaml has model + Zoho token
- [ ] TELEGRAM_BOT_TOKEN env vars defined for each role
- [ ] All 3 bots started with correct HERMES_HOME + token
- [ ] All 3 bots connected (check logs for "Telegram.*Connected")
- [ ] CRM skill installed in main ~/.hermes/skills/
- [ ] User pairing approved in all 3 bot homes
- [ ] Test command `/crm_report` works on at least one bot
- [ ] Verified model is free tier (Claude Haiku, not paid Nous)

## Failure Modes & Recovery

### Mode 1: Bot Won't Connect

**Log Signal:** No "Telegram.*Connected" after 30 seconds

**Checks:**
- Token is real and not revoked: `echo $HERMES_CMO_TELEGRAM_TOKEN`
- Bot can reach Telegram API (network test)
- No stale cache: `rm -rf ~/.hermes/ops/bot_homes/$role/.hermes_cache`
- Restart bot with fresh environment

### Mode 2: Pairing Code Loop

**Log Signal:** User sends message, bot responds with pairing code repeatedly

**Cause:** Pairing state not persisted or bot cache is stale

**Fix:**
1. Clear cache: `rm -rf ~/.hermes/ops/bot_homes/$role/{.hermes_cache,cache,*db}`
2. Re-approve pairing: `export HERMES_HOME=...; hermes pairing approve telegram <REQUEST_ID>`
3. Restart bot

### Mode 3: CRM Skill Errors

**Log Signal:** "ModuleNotFoundError", "AttributeError" in logs

**Cause:** Skill not properly installed or Python environment mismatch

**Fix:**
- Verify skill exists: `ls -la ~/.hermes/skills/crm-analytics-report/scripts/crm_report.py`
- Test skill directly: `python3 ~/.hermes/skills/crm-analytics-report/scripts/crm_report.py text`
- Check Python venv: `which python3` (should be in ~/.hermes/hermes-agent/venv/bin/)

### Mode 4: "Insufficient Credits" on Paid Model

**Log Signal:** "insufficient_credits_for_paid_model", "usable $0.00"

**Cause:** Model provider still set to paid Nous model

**Fix:**
1. Update config: `hermes config set model.provider anthropic`
2. Update model: `hermes config set model.default claude-haiku-4-5-20251001`
3. Verify: `hermes config get model`
4. Restart all bots

## Observability Queries

### Find Bot Status Quickly

```bash
for role in cmo manager employee; do
  LOG=~/.hermes/ops/bot_homes/$role/logs/gateway.log
  connected=$(grep -c "Telegram.*Connected" $LOG)
  errors=$(grep -c "ERROR\|WARN" $LOG)
  unauthorized=$(grep -c "Unauthorized user" $LOG)
  echo "$role: connected=$connected errors=$errors unauthorized=$unauthorized"
done
```

### Find Last Error Per Bot

```bash
for role in cmo manager employee; do
  echo "=== $role ==="
  grep -i "error\|exception" ~/.hermes/ops/bot_homes/$role/logs/gateway.log | tail -1
done
```

### Test CRM Skill End-to-End

```bash
# Direct Python test (no Telegram)
python3 ~/.hermes/skills/crm-analytics-report/scripts/crm_report.py text | head -30

# Should output: CONTACTS, ACCOUNTS, LEADS sections with mock data
```

## References

- `hermes-role-bots-operations` skill: Full bot deployment guide
- `~/.hermes/QUICK_START_CRM.md`: User-friendly quick-start doc
- `~/.hermes/scripts/test_crm_skill.sh`: Comprehensive test script from the session
