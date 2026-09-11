# Office Hermes Initialization Guide

## Quick Start (10 minutes)

### 1. Copy Templates to Office Hermes Profile

```bash
# Assuming office Hermes is at ~/.hermes (or customize path)

# Copy user profile
cp ~/office-hermes-export/agent/templates/USER_PROFILE_TEMPLATE.md \
   ~/.hermes/memories/USER.md

# Copy workflow memory
cp ~/office-hermes-export/agent/templates/WORKFLOW_MEMORY_TEMPLATE.md \
   ~/.hermes/memories/MEMORY.md

# Customize USER.md (open and fill in placeholders)
nano ~/.hermes/memories/USER.md
```

### 2. Configure config.yaml

```bash
# Copy baseline config
cp ~/office-hermes-export/agent/protocols/config_baseline.yaml \
   ~/.hermes/config.yaml

# Customize (fill in office-specific values)
nano ~/.hermes/config.yaml

# Required changes:
# - Update platforms.telegram.home_channel.chat_id
# - Update platforms.telegram.home_channel.user_id
# - Update model.provider if not using Anthropic
```

### 3. Restart Hermes

```bash
hermes daemon restart

# Verify running
hermes status
```

### 4. Test Basic Functionality

```bash
# Say hello
hermes ask "Hi, who are you?"

# Check memory
hermes memory show

# List skills
hermes skills list
```

---

## Full Setup (30 minutes)

### Additional: Apply Behavioral Rules

All rules are documented in `~/office-hermes-export/agent/rules/`:
- `tool_selection_rules.md` — Ask before tool use
- `approval_and_execution_policies.md` — Approval gates
- `output_and_reporting_standards.md` — Response format

**These are behavioral expectations (not auto-enforced).** Educate team on these standards:

```bash
# Share with team
cat ~/office-hermes-export/agent/rules/output_and_reporting_standards.md
```

### Optional: Configure CRM Integration

If office uses Zoho CRM:

```bash
# Follow protocol in protocols/crm_integration_zoho.md
# Step 1: Get Zoho token (see protocol)
# Step 2: Update config.yaml mcp_servers section
# Step 3: Restart daemon
# Step 4: Test: hermes cronjob run daily_report
```

### Optional: Deploy Multi-Role Bots

If office needs CMO/Manager/Employee bots:

```bash
# Install multi-role
hermes init --multi-role --enable cmo,manager,employee

# Configure per protocol: protocols/multi_role_hermes.md
# Start: hermes ops bots start
# Test: hermes ask:manager "Status check"
```

---

## Customization Checklist

### User Profile (USER.md)
- [ ] Fill in `[OFFICE_USER_NAME]`
- [ ] Update `[SKILL_LEVEL]` with user's coding background
- [ ] Set `[LEARNING_GOALS]`
- [ ] Set `[OS_PLATFORM]` (macOS/Windows/Linux)
- [ ] Update `[SKILL_COUNT]` (usually 72+ available)
- [ ] Adjust communication style if needed

### Workflow Memory (MEMORY.md)
- [ ] Review skill creation rule
- [ ] Review tool selection rule
- [ ] Add office-specific cron jobs
- [ ] Document office approval policies
- [ ] Add any custom workflow rules

### Configuration (config.yaml)
- [ ] Update model provider if needed
- [ ] Set Telegram chat IDs
- [ ] Enable/disable platforms as needed
- [ ] Configure MCP servers (if using CRM, design tools, etc.)
- [ ] Set memory limits appropriate for office

### Rules (behavioral expectations)
- [ ] Review and print `output_and_reporting_standards.md`
- [ ] Review `approval_and_execution_policies.md`
- [ ] Review `tool_selection_rules.md`
- [ ] Train team on these standards

---

## File Structure Reference

```
~/office-hermes-export/agent/
├── AGENT_IDENTITY.md                           # Core personality & identity
├── rules/
│   ├── tool_selection_rules.md                 # Tool choice policy
│   ├── approval_and_execution_policies.md      # Approval gates
│   └── output_and_reporting_standards.md       # Response format
├── protocols/
│   ├── config_baseline.yaml                    # config.yaml template
│   ├── crm_integration_zoho.md                 # CRM setup (optional)
│   └── multi_role_hermes.md                    # Multi-bot setup (optional)
└── templates/
    ├── USER_PROFILE_TEMPLATE.md                # → ~/.hermes/memories/USER.md
    └── WORKFLOW_MEMORY_TEMPLATE.md             # → ~/.hermes/memories/MEMORY.md
```

---

## Verification Checklist

After setup, verify these work:

```bash
# 1. Agent responds
hermes ask "Hello, who are you?"
# Expected: Friendly response about being Jarvis, office helper

# 2. Memory works
hermes memory show
# Expected: Shows USER.md and MEMORY.md content

# 3. Skills load
hermes skills list | wc -l
# Expected: 72+ skills available

# 4. Terminal execution works
hermes run "ls ~"
# Expected: Lists home directory

# 5. Approval policy works
hermes run "rm /etc/passwd"  # (don't actually run this)
# Expected: Agent asks for approval first

# 6. Telegram connected (if configured)
hermes platforms test telegram
# Expected: Connection verified
```

---

## Common Issues & Fixes

### Issue: Agent doesn't respond
**Fix:**
```bash
hermes daemon restart
hermes status
```

### Issue: "Unknown personality"
**Fix:** USER.md or MEMORY.md not found
```bash
ls -la ~/.hermes/memories/
# Should show USER.md and MEMORY.md (not .lock files)
```

### Issue: Config.yaml validation error
**Fix:** YAML syntax error (check indentation)
```bash
yamllint ~/.hermes/config.yaml
# Or: hermes config validate
```

### Issue: Telegram not working
**Fix:** Chat IDs incorrect
```bash
# Get correct IDs from Telegram
# Message ID: Right-click on chat > Copy link
# Extract numbers: t.me/c/[CHAT_ID]
```

### Issue: "CRM connection refused"
**Fix:** Zoho MCP not running or token invalid
```bash
# Test connection
hermes mcp test zoho_crm

# If fails, check token in config
cat ~/.hermes/config.yaml | grep ZOHO
```

---

## Next Steps

1. **Team Training:** Share rules docs with team
2. **Skill Discovery:** Explore skills catalog at ~/.hermes/skills/
3. **Set Cron Jobs:** Configure recurring automation (if needed)
4. **Monitor:** Check logs regularly: ~/.hermes/logs/
5. **Iterate:** Customize as team learns system

---

## Support & Questions

**Troubleshooting:** Check `~/.hermes/logs/` for detailed error messages

**Configuration:** Reference `config_baseline.yaml` comments

**Behavioral Rules:** See `rules/` directory for detailed policies

**Integration:** Follow `protocols/` for CRM, multi-bot, etc.

---

*Initialization Guide Version: 1.0*
*Source: Mahesh's Personal Hermes Agent*
*Generated: 2026-09-11*
