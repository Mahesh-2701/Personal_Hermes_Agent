---
name: crm-analytics-report
description: "Use when analyzing CRM data. Generate reports."
version: 1.0.0
---

# CRM Analytics & Reporting Skill

Generates comprehensive reports on contacts, leads, and projects from Zoho CRM. Works with both real Zoho data and mock test data for testing.

## Quick Usage

### Chat Request

```
Analyze my CRM and give me a report of contacts, leads, and projects
```

### Telegram Commands

```
/crm_report         - Full CRM report
/crm_contacts       - Contacts analysis
/crm_leads          - Leads pipeline
/crm_projects       - Projects status
```

## What It Reports

### Contacts Report
- Total contacts count
- Contacts by status (Active, Inactive, etc.)
- Contact list with email, phone, company
- Key metrics

### Leads Report
- Total leads in pipeline
- Leads by status (New, Qualified, Lost, Won)
- Lead value by status
- Conversion metrics
- Lead sources breakdown

### Projects Report
- Active and completed projects
- Project status breakdown
- Project value / budget tracking
- Timeline summary (overdue, on-track, upcoming)

## Report Output Format

### Text Report (Chat)

```
╔════════════════════════════════════════════════════════════════╗
║            CRM ANALYTICS REPORT                               ║
║           As of 2025-09-10 14:32 IST                          ║
╚════════════════════════════════════════════════════════════════╝

📊 CONTACTS
  Total: 245
  Active: 198 (80.8%)
  Inactive: 47 (19.2%)

💼 LEADS
  Total: 78
  New: 12
  Qualified: 34
  Won: 22
  Lost: 10
  Pipeline Value: ₹4,250,000

🏗️  PROJECTS
  Active: 15
  Completed: 42
  On-Time: 14 (93.3%)
  Overdue: 1 (6.7%)
```

### JSON Report (API)

```json
{
  "timestamp": "2025-09-10T14:32:00+05:30",
  "contacts": {
    "total": 245,
    "by_status": {"Active": 198, "Inactive": 47}
  },
  "leads": {
    "total": 78,
    "by_status": {"New": 12, "Qualified": 34, "Won": 22},
    "pipeline_value": 4250000
  },
  "projects": {
    "active": 15,
    "completed": 42,
    "on_time_pct": 93.3
  }
}
```

## Configuration

### Step 1: Update Zoho Token

Edit `~/.hermes/config.yaml` and update this section:

```yaml
mcp_servers:
  zoho_crm:
    command: /Users/apple/.hermes/hermes-agent/venv/bin/python
    args:
      - /Users/apple/.hermes/scripts/zoho_crm_mcp_server.py
    env:
      ZOHO_CRM_ACCESS_TOKEN: "1000.SG6XWYG2ASX1RGJ4B38DM6L4FVKN8D"
    timeout: 60
    connect_timeout: 30
    sampling:
      enabled: false
```

### Step 2: Restart Hermes

```bash
hermes shutdown
hermes
```

## Testing Mode

If token is expired/invalid, the skill automatically returns **mock data** for testing. This lets you verify everything works before connecting real CRM data.

## Troubleshooting

### Token Invalid

**Problem:** "invalid oauth token" error

**Solution:**
1. Visit https://api-console.zoho.com/
2. Generate new access token with scope: `ZohoCRM.modules.READ`
3. Update token in `~/.hermes/config.yaml`
4. Restart Hermes

### No Data Showing

**Problem:** "0 contacts" even though CRM has data

**Solution:**
- Verify token scopes include `ZohoCRM.modules.READ`
- Check Zoho account is accessible
- Verify API quota

### Telegram Not Working

**Problem:** `/crm_report` command no response

**Solution:**
- Confirm bot token is valid in config
- Verify Telegram bot is running
- Test command in main Hermes chat first

## Zoho CRM Tools Available

All tools work via MCP (Model Context Protocol):

| Tool | Description |
|------|-------------|
| `mcp_zoho_crm_list_contacts` | Get all contacts (paginated) |
| `mcp_zoho_crm_list_deals` | Get all deals/leads in pipeline |
| `mcp_zoho_crm_list_accounts` | Get all companies/accounts |
| `mcp_zoho_crm_list_tasks` | Get all tasks |
| `mcp_zoho_crm_search` | Search any module by keyword |
| `mcp_zoho_crm_get_contact` | Get one contact by ID |
| `mcp_zoho_crm_get_deal` | Get one deal by ID |
| `mcp_zoho_crm_list_users` | Get CRM users |
| `mcp_zoho_crm_get_account` | Get one account by ID |

## Testing the Skill NOW ✅

### 1. Test in Hermes Chat

Simply ask in any Hermes chat:

```
Generate CRM analytics report
```

Or:

```
Analyze my Zoho CRM - show contacts, leads, and projects
```

The skill will automatically:
- Load the `crm-analytics-report` skill ✅
- Call `crm_report.py` to generate report ✅
- Display formatted output with all metrics ✅

### 2. Test Telegram Commands (Once Connected)

In your Telegram chat with Hermes:

```
/crm_report          # Full CRM report
/crm_contacts        # Just contacts analysis
/crm_leads           # Just leads pipeline
/crm_projects        # Just projects status
```

The bot will respond with formatted Telegram-friendly message.

### 3. Verify Mock Data is Working

Run the test script:

```bash
python3 ~/.hermes/skills/crm-analytics-report/scripts/crm_report.py text
```

Should return full report with sample data.

## Next Steps (After Getting Fresh Token)

### Step 1: Generate Fresh Zoho Token

1. Go to https://api-console.zoho.com/
2. Create/select OAuth client
3. Generate access token with scopes:
   - `ZohoCRM.modules.READ` (all modules)
   - OR specific scopes: `ZohoCRM.Contacts.READ`, `ZohoCRM.Deals.READ`

### Step 2: Update Hermes Config

```bash
# Edit your config
nano ~/.hermes/config.yaml

# Find this section:
mcp_servers:
  zoho_crm:
    env:
      ZOHO_CRM_ACCESS_TOKEN: "<your-new-token-here>"

# Update the token and save
```

### Step 3: Restart Hermes

```bash
hermes shutdown
hermes
```

### Step 4: Test with Real Data

```bash
# Test the connection
python3 ~/.hermes/skills/crm-analytics-report/scripts/crm_report.py text

# Should now show REAL Zoho CRM data instead of mock
```

## Advanced Usage

### Daily Scheduled Report

Send CRM report to Telegram every day at 9am:

```bash
hermes cronjob create \
  --schedule "every day at 9am" \
  --prompt "Generate CRM analytics and send to Telegram" \
  --deliver telegram
```

### Export to CSV

```python
report = fetch_crm_report('full')
export_to_csv(report, 'crm_report.csv')
```

### Filter by Status

```python
# Only qualified leads
leads = get_crm_data('leads', status='Qualified')

# Only active contacts
contacts = get_crm_data('contacts', status='Active')
```
