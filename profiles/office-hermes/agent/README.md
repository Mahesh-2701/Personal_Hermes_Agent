# Hermes Agent Export — Office Edition

**Source:** Mahesh's Personal Hermes Agent (Sept 2026)  
**Purpose:** Portable templates and configuration to initialize an equivalent Hermes agent in office environment  
**Scope:** Agent identity, personality, behavioral rules, and integration protocols

---

## 📋 Contents

### Core Identity
- **AGENT_IDENTITY.md** — Full personality profile, working principles, behavioral traits

### Rules & Standards (Behavioral Guidelines)
- **rules/tool_selection_rules.md** — When/how to ask user for tool choice
- **rules/approval_and_execution_policies.md** — Approval gates, approval format
- **rules/output_and_reporting_standards.md** — Response format, brevity standards

### Protocols (Integration & Operations)
- **protocols/config_baseline.yaml** — Portable Hermes configuration template
- **protocols/crm_integration_zoho.md** — Optional CRM automation setup
- **protocols/multi_role_hermes.md** — Optional multi-bot (CMO/Manager/Employee) deployment

### Templates (Direct Copy to Office Profile)
- **templates/USER_PROFILE_TEMPLATE.md** → Copy to `~/.hermes/memories/USER.md`
- **templates/WORKFLOW_MEMORY_TEMPLATE.md** → Copy to `~/.hermes/memories/MEMORY.md`

### Quick Start
- **INITIALIZATION_GUIDE.md** — Step-by-step setup (10–30 min)

---

## 🚀 Quick Start

### 1. Copy Templates (5 min)

```bash
# Copy to office Hermes profile
cp templates/USER_PROFILE_TEMPLATE.md ~/.hermes/memories/USER.md
cp templates/WORKFLOW_MEMORY_TEMPLATE.md ~/.hermes/memories/MEMORY.md

# Customize (fill in placeholders)
nano ~/.hermes/memories/USER.md
```

### 2. Configure (5 min)

```bash
# Copy and customize config
cp protocols/config_baseline.yaml ~/.hermes/config.yaml
nano ~/.hermes/config.yaml

# Required: Update Telegram chat IDs, model provider
```

### 3. Restart & Test (2 min)

```bash
hermes daemon restart
hermes ask "Hi, who are you?"
```

**Done!** Agent is ready. See **INITIALIZATION_GUIDE.md** for full setup.

---

## 🎯 What You Get

### Personality
- **Archetype:** "Jarvis" — friendly, encouraging friend/buddy
- **Tone:** Casual ("Hey buddy"), but technically accurate
- **Approach:** Understand complexity → propose → execute → verify → explain three ways

### Behavioral Standards
- **Tool selection:** Always ask user before picking Codex/Antigravity/etc.
- **Approvals:** Clear, itemized approval gates for destructive/system actions
- **Output:** Brief, outcome-focused summaries (no process replay)
- **Honesty:** Never fabricate results; report blockers directly

### Operational Features
- **Multi-role support:** Optional CMO/Manager/Employee bot coordination
- **CRM integration:** Ready-to-deploy Zoho CRM automation
- **Memory system:** Shared institutional knowledge + user profile
- **Cost optimized:** Default to claude-haiku (free tier at Nous)

---

## 📖 Customization Guide

### For User Profile (USER.md)

Replace placeholders:
- `[OFFICE_USER_NAME]` — Name of office user
- `[SKILL_LEVEL]` — "Intermediate JavaScript", "Beginner Python", etc.
- `[LEARNING_GOALS]` — What they want to learn
- `[OS_PLATFORM]` — macOS / Windows / Linux
- `[SKILL_COUNT]` — Number of skills available (usually 72+)

### For Workflow Memory (MEMORY.md)

Add office-specific:
- Approval policies for your team
- Cron job schedules for automation
- Custom tool preferences
- Team-wide workflow rules

### For Configuration (config.yaml)

Critical updates:
- `model.provider` — Use `anthropic` (default) or your provider
- `platforms.telegram.home_channel.chat_id` — Office Telegram chat ID
- `platforms.telegram.home_channel.user_id` — Office user ID
- `mcp_servers.zoho_crm` — If using CRM (optional)

---

## 📚 Rule Documents Explained

### tool_selection_rules.md
**When:** User says "write code" or "build feature"  
**What agent does:** Asks "Use Codex CLI or Antigravity CLI?"  
**Why:** User gets to choose their preferred tool; agent sticks with it

### approval_and_execution_policies.md
**Core principle:** User owns all approvals  
**Examples:**
- Terminal: Needs approval for `sudo`, package installs, destructive `rm`
- Files: Needs approval for deletes, overwrites of large files
- Secrets: Needs approval for any credential operation
- Deployment: Needs approval for `git push`, deployments

**Format:** Clear `⚠️ Need approval to [ACTION]` messages

### output_and_reporting_standards.md
**Philosophy:** "Match response length to task weight"  
- One-line question → one-line answer
- Finished work → short, structured summary
- No filler ("Great question!"), no replay
- Lead with outcomes; prefer bullets over prose

---

## 🔗 Integration Protocols

### CRM Integration (Optional)

If office uses Zoho CRM:
1. Follow **protocols/crm_integration_zoho.md**
2. Get Personal Access Token from Zoho
3. Update `config.yaml` with token
4. Restart Hermes
5. Test: `hermes cronjob run daily_report`

Available cron jobs:
- Daily 9am: Contact/lead summary
- 11am weekdays: High-value leads alert
- Monday 10am: Weekly engagement trends
- Friday 5pm: Weekly revenue report
- 1st of month, 8am: Monthly revenue analysis

### Multi-Bot Deployment (Optional)

If office needs multiple roles:
1. Follow **protocols/multi_role_hermes.md**
2. Install: `hermes init --multi-role --enable cmo,manager,employee`
3. Configure per role (CMO = strategy, Manager = delegation, Employee = execution)
4. Start: `hermes ops bots start`
5. Interact: `hermes ask:cmo "Market analysis"`, etc.

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Agent responds to "Who are you?" (should say "Jarvis" or similar)
- [ ] Memory loads: `hermes memory show`
- [ ] Skills available: `hermes skills list` shows 72+
- [ ] Terminal works: `hermes run "ls ~"`
- [ ] Approvals work: Agent asks before destructive actions
- [ ] Telegram connected (if configured): `hermes platforms test telegram`

---

## 🆘 Troubleshooting

| Issue | Check |
|-------|-------|
| Agent doesn't respond | `hermes status`, `hermes daemon restart` |
| "Unknown personality" | USER.md exists at `~/.hermes/memories/USER.md` |
| Config error | YAML syntax; run `yamllint ~/.hermes/config.yaml` |
| CRM not working | Check Zoho token; test `hermes mcp test zoho_crm` |
| Telegram failing | Verify chat IDs in config; test `hermes platforms test telegram` |

See **INITIALIZATION_GUIDE.md** for detailed troubleshooting.

---

## 📝 File Reference

```
~/office-hermes-export/agent/
├── AGENT_IDENTITY.md                              [Read first]
├── INITIALIZATION_GUIDE.md                        [Setup steps]
├── README.md                                      [This file]
│
├── rules/                                         [Behavioral standards]
│   ├── tool_selection_rules.md
│   ├── approval_and_execution_policies.md
│   └── output_and_reporting_standards.md
│
├── protocols/                                     [Integration guides]
│   ├── config_baseline.yaml                       [→ ~/.hermes/config.yaml]
│   ├── crm_integration_zoho.md                    [Optional CRM setup]
│   └── multi_role_hermes.md                       [Optional multi-bot setup]
│
└── templates/                                     [Direct copy to office]
    ├── USER_PROFILE_TEMPLATE.md                  [→ USER.md]
    └── WORKFLOW_MEMORY_TEMPLATE.md               [→ MEMORY.md]
```

---

## 🔐 Security Notes

1. **Never commit credentials to git**
   - Tokens, API keys, passwords → environment variables only
   - Hermes auto-redacts secrets in logs

2. **Rotate tokens regularly**
   - Zoho CRM PAT: Refresh via Zoho UI quarterly
   - SSH keys: Audit access logs regularly

3. **Audit & monitor**
   - Check `~/.hermes/logs/` for suspicious activity
   - Monitor tool execution approvals

4. **Redaction policy**
   - Enabled by default
   - Masks: AWS keys, API tokens, OAuth creds, SSH keys, passwords
   - Visible only to: Local execution, user's local logs (not cloud)

---

## 💡 Philosophy

This export captures:
- **What Jarvis is:** Friendly, helpful, honest collaborator
- **How Jarvis works:** Understand → propose → execute → verify → explain
- **What Jarvis values:** Production quality, maintainability, security, testing
- **How Jarvis behaves:** Explicit tools, clear approvals, outcome-focused output

**Not included:** Personal memories, conversation history, or specific project context. Those are unique to Mahesh's instance.

---

## 🎓 Learning Path

1. **Start here:** Read **AGENT_IDENTITY.md** (5 min)
2. **Then:** Follow **INITIALIZATION_GUIDE.md** for setup (30 min)
3. **Rules:** Read all three `rules/*.md` files (20 min)
4. **Optional integrations:** CRM protocol or multi-bot protocol (as needed)
5. **Team training:** Share relevant docs with your team

---

## 📞 Support

For issues:
1. Check **INITIALIZATION_GUIDE.md** troubleshooting section
2. Review logs: `tail -f ~/.hermes/logs/gateway.log`
3. Test specific component: `hermes platforms test [platform]`
4. Verify config: `hermes config validate`

---

## 📄 Version & Attribution

| Attribute | Value |
|-----------|-------|
| Export Version | 1.0 |
| Source Agent | Mahesh's Personal Hermes Instance |
| Export Date | 2026-09-11 |
| Base Model | claude-haiku-4-5-20251001 (Anthropic) |
| Provider | Nous Research |
| Platform | Hermes Agent v1.x |

---

## 🔄 Feedback & Iteration

This is a **snapshot** of Mahesh's Hermes configuration. As you customize for your office:

1. **Iterate on USER.md:** Update as team learns
2. **Enhance MEMORY.md:** Add office-specific workflows
3. **Tune rules:** Adjust approval policies to fit your team
4. **Document changes:** Keep a changelog of customizations

---

*Export created: 2026-09-11*  
*Ready for office deployment*  
*Start with INITIALIZATION_GUIDE.md →*
