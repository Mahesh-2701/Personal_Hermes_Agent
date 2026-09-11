# CRM Integration Protocol (Zoho CRM)
# Optional: Use if office needs CRM automation
# Version: 1.0

name: "crm-integration-zoho"
description: "Automated CRM workflows via Zoho CRM integration"

---

## Overview

Zoho CRM integration provides:
- Daily contact/lead/project reports
- Automated lead scoring alerts
- Weekly engagement summaries
- Revenue tracking
- Custom automation via cron jobs

**Status:** Tested with mock data. Ready for live data swap.

---

## Prerequisites

1. **Zoho Account:** Existing Zoho CRM subscription
2. **Authentication Token:** Personal Access Token or OAuth credentials
3. **MCP Server:** Python environment with Zoho MCP server
4. **Skill:** CRM analytics skill (`~/.hermes/skills/crm-analytics-report/`)

---

## Setup Steps

### Step 1: Obtain Zoho Credentials

**Option A: Personal Access Token (Recommended)**
1. Log in to Zoho CRM
2. Navigate: Settings > API > Personal Access Tokens
3. Create new token with scope: `Read, Create`
4. Copy token (you'll need it in Step 2)

**Option B: OAuth (Automatic)**
1. Use Hermes built-in OAuth flow
2. Hermes will prompt for Zoho account access
3. Grant permissions automatically

### Step 2: Configure config.yaml

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  zoho_crm:
    command: /path/to/python3
    args:
      - /path/to/scripts/zoho_crm_mcp_server.py
    env:
      ZOHO_CRM_ACCESS_TOKEN: "1000.YOUR_TOKEN_HERE"
    timeout: 60
    connect_timeout: 30
    sampling:
      enabled: false
```

Replace:
- `/path/to/python3` with actual Python path (e.g., `/usr/bin/python3`)
- `/path/to/scripts/zoho_crm_mcp_server.py` with actual path
- `1000.YOUR_TOKEN_HERE` with actual token from Step 1

### Step 3: Restart Hermes

```bash
hermes daemon restart
```

Verify connection:
```bash
hermes mcp test zoho_crm
```

---

## Available Cron Jobs

Pre-configured cron jobs (customize schedule as needed):

| Job | Schedule | Purpose | Status |
|-----|----------|---------|--------|
| daily_report | 9am daily | Contact/lead summary | Active |
| leads_alert | 11am weekdays | New high-value leads | Active |
| engagement_weekly | 10am Monday | Weekly engagement trends | Active |
| revenue_summary | 5pm Friday | Weekly revenue report | Active |
| revenue_monthly | 8am 1st | Monthly revenue analysis | Active |

**To customize schedules:**
Edit `~/.hermes/cron/[job_id]/config.yaml`

**To disable a job:**
Set `enabled: false` in job config

**To test a job immediately:**
```bash
hermes cronjob run [job_id]
```

---

## Data Mapping

### Contact Reports
- Name, Email, Phone
- Company, Industry
- Last activity
- Contact score

### Lead Reports
- Lead name, Email
- Company, Industry
- Lead score
- Status, Stage
- Next action

### Engagement Summary
- Total interactions (past week)
- Most active leads
- Conversion trends
- Response times

### Revenue Tracking
- Total pipeline value
- Closed deals (week/month)
- Average deal size
- Sales velocity

---

## Switching from Mock to Live Data

### Current State
All jobs run against mock data (doesn't affect real Zoho).

### To Enable Live Data

1. **Verify credentials in Step 2 above**
2. **Restart Hermes:**
   ```bash
   hermes daemon restart
   ```
3. **Test with one job:**
   ```bash
   hermes cronjob run daily_report
   ```
4. **Review output** — should show real data
5. **Enable remaining jobs** via cron config

### Rollback to Mock Data
1. Revert `ZOHO_CRM_ACCESS_TOKEN` to mock value (or remove it)
2. Restart Hermes
3. Jobs automatically use mock data

---

## Troubleshooting

### "Connection refused" error
- **Cause:** MCP server not running
- **Fix:** `hermes mcp test zoho_crm` and restart daemon

### "Invalid token" error
- **Cause:** Token expired or incorrect
- **Fix:** Generate new Personal Access Token in Zoho, update config

### Jobs not running at scheduled time
- **Cause:** Cron service disabled or machine off
- **Fix:** Ensure Hermes daemon is running: `hermes daemon status`

### No data returned
- **Cause:** Permission issues or empty Zoho database
- **Fix:** Test with `hermes cronjob run daily_report`, check Zoho permissions

---

## Security Notes

- **Never commit credentials to git** — use environment variables
- **Rotate tokens regularly** — Zoho UI or API
- **Audit access logs** in Zoho — Settings > Audit Logs
- **Use scope minimization** — Request only needed CRM scopes
- **Redaction enabled** — Hermes masks tokens in logs/chat

---

## Advanced: Custom CRM Automations

To create new CRM-driven workflows:

1. **Create new cron job:**
   ```bash
   hermes cronjob create my_workflow --schedule "0 10 * * *"
   ```

2. **Define action in Hermes memory:**
   ```
   Cron trigger: daily 10am
   Action: Query Zoho for deals close to expiration, create Slack alert
   Payload: [custom logic]
   ```

3. **Test:** `hermes cronjob run my_workflow`

4. **Monitor:** `hermes cronjob logs my_workflow`

See `~/.hermes/cron/` for examples.

---

## Maintenance Checklist

- [ ] Token expires? Refresh token in Zoho
- [ ] Test jobs monthly: `hermes cronjob run daily_report`
- [ ] Review missed jobs: `hermes cronjob logs`
- [ ] Update skill if Zoho API changes
- [ ] Archive old cron logs quarterly

---

*Protocol Version: 1.0*
*Source: Mahesh's Personal Hermes Agent*
*Updated: 2026-09-11*
