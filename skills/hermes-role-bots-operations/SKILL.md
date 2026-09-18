---
name: hermes-role-bots-operations
description: "Deploy and manage Hermes multi-bot telegram infrastructure."
version: 1.0.0
author: Hermes Operations
metadata:
  category: autonomous-ai-agents
  tags: [hermes, bots, multi-agent, telegram, infrastructure, operations, pairing, deployment]
---

# Hermes Role-Based Bots Operations

Guide for setting up, configuring, troubleshooting, and operating multiple independent Hermes gateway bots (e.g., CMO, Manager, Employee) as a coordinated telegram infrastructure.

## When to Use This Skill

- Setting up or restarting multiple Hermes role bots
- Troubleshooting model configuration in bot homes
- Handling bot pairing codes and user authorization
- Migrating model providers across bot fleet (e.g., Nous → Anthropic)
- Testing CRM or multi-role workflows via telegram
- Resolving "unauthorized user", "pairing code", or "no response" errors

## Quick Start: Multi-Bot Deployment

### 1. Create Bot Home Directories

```bash
mkdir -p ~/.hermes/ops/bot_homes/{cmo,manager,employee}
cd ~/.hermes/ops/bot_homes
```

### 2. Create Minimal Config for Each Role

Each bot home needs a `config/config.yaml` that inherits from the main Hermes config:

```yaml
# ~/.hermes/ops/bot_homes/cmo/config/config.yaml
onboarding:
  seen:
    profile_build_offered: true
```

Repeat for `manager/` and `employee/`.

### 3. Start Each Bot with Environment Variables

```bash
# CMO bot
export TELEGRAM_BOT_TOKEN="$HERMES_CMO_TELEGRAM_TOKEN"
export HERMES_HOME="~/.hermes/ops/bot_homes/cmo"
export _HERMES_GATEWAY=1
mkdir -p "$HERMES_HOME/logs"
hermes gateway run --external-supervisor > "$HERMES_HOME/logs/gateway.log" 2>&1 &
echo $! > "$HERMES_HOME/gateway.pid"
```

Repeat for MANAGER and EMPLOYEE tokens/homes.

### 4. Verify All Bots Are Running

```bash
for role in cmo manager employee; do
  LOG="~/.hermes/ops/bot_homes/$role/logs/gateway.log"
  grep -q "Telegram.*Connected" "$LOG" && echo "✅ $role: CONNECTED" || echo "❌ $role: NOT READY"
done
```

## Model Configuration Across Bot Fleet

### The Pitfall: Model Mismatch

**Problem:** Bots configured to use free model (`upstage/solar-pro4:free`), but at runtime they try a paid Nous model (`z-ai/glm-5.2`), run out of credits, and show "token limit reached" errors.

**Root Cause:** 
- Bot home config has old/stale model override
- OR main `~/.hermes/config.yaml` has provider set to paid model
- OR both files exist and the wrong precedence is used

**Fix:**

1. **Update main config ONLY** — set `~/.hermes/config.yaml`:

```yaml
model:
  default: claude-haiku-4-5-20251001
  provider: anthropic
```

2. **Keep bot homes minimal** — each bot's `config/config.yaml` should have NO model section:

```yaml
onboarding:
  seen:
    profile_build_offered: true
```

Bots inherit model from main config automatically.

3. **Clear stale caches**:

```bash
for role in cmo manager employee; do
  rm -rf ~/.hermes/ops/bot_homes/$role/.hermes_cache 2>/dev/null
done
```

4. **Restart all bots** with fresh environment:

```bash
# Kill old processes first
killall hermes 2>/dev/null || true
sleep 2

# Start fresh
# (follow Quick Start: Multi-Bot Deployment section above)
```

## Pairing: Authorization Workflow

### When Pairing Codes Appear

Bots show pairing codes when you send a message and they don't recognize your user ID yet:

```
"Pairing code: UUHAET2K"
```

### Approve Pairing (Server-Side)

**This workflow is the KEY DIFFERENCE from single-bot setup.**

1. **List pending pairing requests**:

```bash
export HERMES_HOME="~/.hermes/ops/bot_homes/cmo"
hermes pairing list
```

Output:
```
Pending Pairing Requests (1):
Platform     Request ID             User ID              Name                 Age
--------     ----------             -------              ----                 ---
telegram     56477086a7fd8d76       5191016577           Mahesh               5m ago
```

2. **Approve the request**:

```bash
hermes pairing approve telegram 56477086a7fd8d76
```

3. **Verify approval**:

```bash
hermes pairing list
# Should now show under "Approved Users (1)"
```

### Pairing Each Role Bot

**CRITICAL:** Each bot home has its own pairing state. You must approve for each role:

```bash
# CMO bot
export HERMES_HOME="~/.hermes/ops/bot_homes/cmo"
REQID=$(hermes pairing list | grep "telegram" | awk '{print $3}')
hermes pairing approve telegram "$REQID"

# Manager bot
export HERMES_HOME="~/.hermes/ops/bot_homes/manager"
REQID=$(hermes pairing list | grep "telegram" | awk '{print $3}')
hermes pairing approve telegram "$REQID"

# Employee bot
export HERMES_HOME="~/.hermes/ops/bot_homes/employee"
REQID=$(hermes pairing list | grep "telegram" | awk '{print $3}')
hermes pairing approve telegram "$REQID"
```

**After approval:** Bots recognize your user ID and respond without showing pairing codes.

## Testing Multi-Bot Setup

### Create a Test Script

```bash
#!/bin/bash
# test_bots.sh

echo "Testing CRM skill across all 3 bots..."
echo ""

for role in cmo manager employee; do
  LOG="~/.hermes/ops/bot_homes/$role/logs/gateway.log"
  
  echo "--- $role bot ---"
  if grep -q "Telegram.*Connected" "$LOG"; then
    echo "✅ Connected"
  else
    echo "❌ Not connected"
    tail -10 "$LOG"
    continue
  fi
  
  if grep -q "Unauthorized user" "$LOG"; then
    echo "⚠️  User NOT authorized (needs pairing approval)"
  else
    echo "✅ User authorized"
  fi
  echo ""
done

echo "To test commands, send to Telegram:"
echo "  /crm_report"
echo "  /crm_contacts"
echo "  /crm_leads"
```

### Verify Logs

```bash
# Check for successful startup
grep -i "application startup\|telegram connected\|hermes.*running" \
  ~/.hermes/ops/bot_homes/*/logs/gateway.log

# Check for errors
grep -i "error\|warning\|failed\|denied" \
  ~/.hermes/ops/bot_homes/*/logs/gateway.log | tail -20
```

## Troubleshooting

### Bot Shows Pairing Code But User Is Already Authorized

**Symptom:** User sends message, bot responds with pairing code even though they were just approved.

**Cause:** Bot home config or cache is out of sync.

**Fix:**

1. Clear cache:
```bash
rm -rf ~/.hermes/ops/bot_homes/$role/{.hermes_cache,cache}
```

2. Check the specific bot home's pairing state:
```bash
export HERMES_HOME="~/.hermes/ops/bot_homes/$role"
hermes pairing list | grep "Approved Users" -A 5
```

3. If user is NOT in approved list, re-approve:
```bash
REQID=$(hermes pairing list | grep "telegram" | awk '{print $3}')
hermes pairing approve telegram "$REQID"
```

4. Restart the bot:
```bash
kill $(cat ~/.hermes/ops/bot_homes/$role/gateway.pid)
sleep 2
# Restart (follow Quick Start)
```

### Bot Returns "Unauthorized User"

**Symptom:** Logs show `WARNING gateway.run: Unauthorized user: <ID> on telegram`

**Cause:** User hasn't completed the pairing workflow for this specific bot.

**Fix:** Follow the pairing approval section above for that role.

### All Bots Use Wrong Model (Paid Instead of Free)

**Symptom:** Bots work, but charge $$ or report "insufficient_credits_for_paid_model".

**Root Cause:** Bot or main config still points to paid provider/model.

**Fix:**

1. Check main config:
```bash
grep -A 3 "^model:" ~/.hermes/config.yaml
# Should show: provider: anthropic
```

2. Update if needed:
```bash
hermes config set model.default claude-haiku-4-5-20251001
hermes config set model.provider anthropic
```

3. Restart all bots

### Bot Doesn't Respond to Commands

**Symptoms:** Send `/crm_report` or other command, no response.

**Checklist:**

1. Bot is running:
```bash
ps aux | grep hermes | grep gateway
```

2. Bot is connected:
```bash
grep -i "telegram.*connected" ~/.hermes/ops/bot_homes/$role/logs/gateway.log
```

3. User is authorized:
```bash
export HERMES_HOME="~/.hermes/ops/bot_homes/$role"
hermes pairing list | grep "Approved Users" -A 5
```

4. Skill/command is loaded:
```bash
grep -i "crm_report\|slash.*command" ~/.hermes/ops/bot_homes/$role/logs/gateway.log
```

5. Recent errors in log:
```bash
tail -50 ~/.hermes/ops/bot_homes/$role/logs/gateway.log | grep -i "error\|exception\|failed"
```

## Multi-Bot Integration: CRM Example

Once all bots are paired and connected, they can run shared skills across different user personas.

### Install CRM Skill Once (Main Hermes)

The skill loads from `~/.hermes/skills/crm-analytics-report/` automatically for all bots.

### Each Bot Responds to Same Commands

All three bots understand:

```
/crm_report       → Full CRM analysis
/crm_contacts     → Contacts only
/crm_leads        → Leads only
```

Response formatting adapts to Telegram inline.

### Test Across Roles

```bash
# Send to CMO bot: /crm_report
# Send to Manager bot: /crm_contacts
# Send to Employee bot: /crm_leads

# Each should respond within 3-5 seconds with role-appropriate data
```

## Monitoring & Observability

### Live Bot Status

```bash
for role in cmo manager employee; do
  PID=$(cat ~/.hermes/ops/bot_homes/$role/gateway.pid 2>/dev/null)
  if ps -p $PID > /dev/null 2>&1; then
    echo "✅ $role: RUNNING (PID $PID)"
  else
    echo "❌ $role: STOPPED"
  fi
done
```

### Recent Activity

```bash
# Last 10 events per bot
for role in cmo manager employee; do
  echo "--- $role ---"
  tail -10 ~/.hermes/ops/bot_homes/$role/logs/gateway.log
  echo ""
done
```

### Error Rate

```bash
for role in cmo manager employee; do
  count=$(grep -c "ERROR\|WARNING" ~/.hermes/ops/bot_homes/$role/logs/gateway.log)
  echo "$role: $count errors/warnings"
done
```

## Files & Paths

```
~/.hermes/ops/bot_homes/
├── cmo/
│   ├── config/config.yaml          (minimal; inherits from main)
│   ├── logs/gateway.log            (append-only event log)
│   └── gateway.pid                 (process ID)
├── manager/
│   ├── config/config.yaml
│   ├── logs/gateway.log
│   └── gateway.pid
└── employee/
    ├── config/config.yaml
    ├── logs/gateway.log
    └── gateway.pid

~/.hermes/config.yaml               (main; model + shared settings)
~/.hermes/skills/crm-analytics-report/  (shared skill for all bots)
```

## Reference: Pairing Code Lifecycle

1. **Bot starts** → waits for first message from user
2. **User sends message** → bot doesn't recognize the user ID
3. **Bot generates pairing code** → shows in bot's response or log
4. **User/Admin sees code** → can choose to approve or reject
5. **Admin runs `hermes pairing approve telegram <REQUEST_ID>`**
6. **Next message from user** → bot recognizes them; no more pairing codes

**Key:** Pairing state lives in EACH bot home's isolated database. A user approved in `cmo/` is NOT automatically approved in `manager/` — you must approve each bot separately.

## See Also

- `hermes-agent` skill: Overall Hermes setup and CLI
- `references/cli-reference.md` in hermes-agent skill: `hermes pairing` commands
- Telegram bot docs: https://hermes-agent.nousresearch.com/docs/
