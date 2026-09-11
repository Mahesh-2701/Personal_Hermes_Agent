# Multi-Role Hermes Protocol
# Deploy multiple agent roles for team coordination
# Version: 1.0

name: "multi-role-hermes"
description: "Coordinate multiple Hermes agents by role (CMO, Manager, Employee)"

---

## Overview

Multi-role Hermes enables:
- **CMO Bot:** Strategic planning, market analysis, high-level decisions
- **Manager Bot:** Workflow coordination, team oversight, delegation
- **Employee Bot:** Execution, detailed work, feedback loops

All roles share:
- Same underlying model (inherit from main config)
- Same skill library
- Coordinated memory
- Centralized approvals

---

## Architecture

```
Main Hermes (Control)
    ├── CMO Bot (Port 8001)
    ├── Manager Bot (Port 8002)
    └── Employee Bot (Port 8003)

Shared:
    ├── config.yaml (main)
    ├── skills/ (all 72+ skills)
    ├── memories/ (coordinated)
    └── cron/ (shared jobs)
```

---

## Setup

### Prerequisite: Multi-Bot Installation

If not already installed:
```bash
hermes init --multi-role --enable cmo,manager,employee
```

### Directory Structure

After install:
```
~/.hermes/
├── config.yaml (main config)
├── ops/
│   ├── bot_homes/
│   │   ├── cmo/
│   │   │   ├── config.yaml (inherits from main)
│   │   │   ├── logs/
│   │   │   └── state/
│   │   ├── manager/
│   │   └── employee/
│   ├── coordination/
│   │   └── roles.yaml
│   └── gateway.log
└── [other directories shared]
```

---

## Configuration

### Main config.yaml
No changes needed — all roles inherit.

### Per-Role Config Override (Optional)

To customize a role's behavior, edit `~/.hermes/ops/bot_homes/[role]/config.yaml`:

```yaml
# For CMO (strategic focus)
agent:
  reasoning_effort: high
  max_turns: 200

# For Employee (execution focus)
agent:
  reasoning_effort: medium
  max_turns: 100
```

**Important:** Don't override model provider — roles inherit from main config.

---

## Role Definitions

### CMO Bot
**Focus:** Strategic direction, market trends, high-level decisions
**Characteristics:**
- Longer context window (if budget allows)
- Higher reasoning effort
- Access to all strategic skills
- Generates reports, analyses, recommendations

**Example Prompt:**
```
CMO Bot: Analyze market trends for Q4. What are the top 3 opportunities 
for the company to pursue? What should we prioritize?
```

### Manager Bot
**Focus:** Workflow coordination, team management, delegation
**Characteristics:**
- Moderate reasoning
- Delegator role
- Oversees Employee Bot tasks
- Tracks progress, escalates blockers

**Example Prompt:**
```
Manager Bot: Delegate the Q4 project to Employee Bot. 
Oversee progress and alert me if blockers arise.
```

### Employee Bot
**Focus:** Execution, detailed work, hands-on tasks
**Characteristics:**
- Lower reasoning (cost control)
- Hands-on tool usage
- Detailed execution
- Reports to Manager

**Example Prompt:**
```
Employee Bot: Implement the feature described in the project brief.
Report progress every 2 hours.
```

---

## Starting the Multi-Bot System

### Start All Bots
```bash
hermes ops bots start
```

### Start Single Bot
```bash
hermes ops bots start --role cmo
hermes ops bots start --role manager
hermes ops bots start --role employee
```

### Check Status
```bash
hermes ops bots status
```

Expected output:
```
CMO Bot:      Running (PID 24087) — claude-haiku-4-5-20251001
Manager Bot:  Running (PID 24106) — claude-haiku-4-5-20251001
Employee Bot: Running (PID 24124) — claude-haiku-4-5-20251001
```

### Stop Bots
```bash
hermes ops bots stop
```

---

## Interacting with Roles

### Via CLI
```bash
# Direct to CMO
hermes ask:cmo "What's our market position?"

# Direct to Manager
hermes ask:manager "Delegate Q4 project to employee"

# Direct to Employee
hermes ask:employee "Implement feature X"
```

### Via Telegram

Create separate Telegram groups or channels:
- `#hermes-cmo` → Routes to CMO Bot
- `#hermes-manager` → Routes to Manager Bot
- `#hermes-employee` → Routes to Employee Bot

**Setup in config.yaml:**
```yaml
platforms:
  telegram:
    enabled: true
  home_channel:
    platform: telegram
    chat_id: "[CMO_GROUP_ID]"  # Main channel for CMO
    name: "Hermes CMO"

# Per-role channels configured in ops/ automatically
```

---

## Coordination & Memory

### Shared Memory
All bots access same:
- `MEMORY.md` — Institutional knowledge
- `USER.md` — User profile
- Skills library
- Cron jobs

### Role-Specific Notes (Optional)
Create role-specific sections in MEMORY.md:
```markdown
## CMO Bot Tasks
[Strategic items]

## Manager Bot Tasks  
[Coordination items]

## Employee Bot Tasks
[Execution items]
```

### Cross-Bot Communication
Manager Bot can delegate to Employee Bot:
```
Manager: "Employee Bot, please execute this task. 
Report progress in real-time."

[Employee Bot runs task, updates Manager]

Manager: "Summary for CMO: Task completed. Metrics: [data]"
```

---

## Cron Jobs with Multi-Role

### Job Ownership
Define which role runs which job:

```yaml
# In cron job config
owner_role: manager  # or: cmo, employee
schedule: "0 9 * * *"
task: "Generate daily report"
report_to: cmo  # Which role gets notified
```

### Example: Daily Workflow

1. **8am:** CMO Bot reviews market data
2. **9am:** Manager Bot fetches tasks from Zoho CRM
3. **9:30am:** Manager Bot delegates to Employee Bot
4. **Throughout day:** Employee Bot executes, updates Manager
5. **5pm:** Manager Bot summarizes for CMO

---

## Cost Optimization

### Model Selection
All roles use same model (inherited). To optimize costs:

1. **During working hours:** Use default model (Haiku)
2. **Off-hours automation:** Configure `fallback_model` for cheaper option
3. **High-reasoning tasks:** Route to CMO only (higher reasoning effort)

### Reasoning Effort per Role
```yaml
# CMO: Strategic
reasoning_effort: high

# Manager: Moderate
reasoning_effort: medium

# Employee: Execution-focused
reasoning_effort: low
```

### Token Budgets (Optional)
Implement per-role token caps:
```yaml
agent:
  token_budget:
    cmo: 200000       # Full budget for strategy
    manager: 150000   # Coordination
    employee: 100000  # Execution focus
```

---

## Troubleshooting

### Bot Not Starting
```bash
# Check logs
tail -f ~/.hermes/ops/bot_homes/[role]/logs/gateway.log

# Restart daemon
hermes daemon restart
```

### Communication Issues
```bash
# Test inter-bot messaging
hermes ops bots test --from manager --to employee

# Check Telegram connectivity
hermes platforms test telegram
```

### Memory Sync Issues
```bash
# Force sync
hermes memory sync --all-roles

# Verify consistency
hermes memory check --consistency
```

---

## Best Practices

1. **Clear Role Boundaries:** Each role has clear responsibilities
2. **Explicit Delegation:** Manager explicitly asks Employee for tasks
3. **Regular Reporting:** Employee reports to Manager; Manager to CMO
4. **Shared Context:** Keep MEMORY.md current for all roles
5. **Backup Strategy:** Archive old session logs regularly
6. **Cost Monitoring:** Track token usage per role monthly

---

## Shutdown Procedure

When shutting down for maintenance:

```bash
# Graceful stop
hermes ops bots stop

# Verify all stopped
hermes ops bots status

# Backup state (optional)
hermes backup --roles cmo,manager,employee
```

---

## Maintenance Checklist

- [ ] All bots started successfully?
- [ ] Telegram channels connected?
- [ ] MEMORY.md synchronized?
- [ ] Cron jobs assigned to correct role?
- [ ] Token usage within budget?
- [ ] Logs reviewed for errors?
- [ ] Weekly: Verify CMO→Manager→Employee flow works

---

*Protocol Version: 1.0*
*Source: Mahesh's Personal Hermes Agent*
*Status: Tested & verified (Sept 2026)*
*Updated: 2026-09-11*
