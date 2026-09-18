---
name: test-crm-skill
description: "Test CRM analytics skill. Use to verify reports work."
version: 1.0.0
---

# CRM Skill Test Suite

Quick testing workflow for CRM analytics skill across chat and Telegram.

## Test Commands

### Test 1: Full Report

```
Test CRM analytics - generate full report
```

Expected output:
- Contact count: 245
- Account companies: 50
- Lead deals: 78
- Pipeline value: ₹21.45M

### Test 2: Telegram /crm_report

Send to your Manager, CMO, or Employee bot:

```
/crm_report
```

Expected: Formatted CRM report in Telegram

### Test 3: Telegram /crm_contacts

```
/crm_contacts
```

Expected: Contact analysis only

### Test 4: JSON Format

```
Generate CRM report in JSON format
```

Expected: Machine-readable JSON with all metrics

## Quick Verification

**Data Source:** Mock data (245 contacts, 50 accounts, 78 leads)

**Format Options:**
- Text (human-readable)
- JSON (API/integration)
- Telegram (mobile-formatted)

**Commands Available:**
- `/crm_report` - Full report
- `/crm_contacts` - Contacts only
- `/crm_leads` - Leads/deals pipeline
- `/crm_projects` - Projects status

## Status

✅ **Skill Ready** - crm-analytics-report installed
✅ **Mock Data** - 245 contacts, 50 accounts, 78 leads
✅ **Bots Running** - CMO, Manager, Employee bots online
⏳ **Telegram** - Ready to test commands

## What's Tested

1. **Report Generation** - crm_report.py works
2. **Data Formatting** - Text and JSON formats
3. **Mock Data** - Complete test dataset loaded
4. **Bot Integration** - Telegram handlers configured
5. **Skill Loading** - crm-analytics-report loads in chat

## Next: Live Zoho Data

Currently using mock data. To enable live Zoho CRM:

1. Get fresh token from https://api-console.zoho.com/
2. Update token in ~/.hermes/config.yaml
3. Restart Hermes

## Troubleshooting

**Q: Report shows "0 contacts"?**
A: Token may be invalid. Check ~/.hermes/config.yaml for ZOHO_CRM_ACCESS_TOKEN

**Q: Telegram bot doesn't respond to /crm_report?**
A: Ensure bot is running (check ps aux | grep hermes)

**Q: Want real data instead of mock?**
A: Generate fresh Zoho token and update config.yaml
