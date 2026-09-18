---
name: google-workspace-assistant
description: Access and manage Gmail, Calendar, Sheets, Drive, and Docs.
version: 1.0.0
author: Mahi
license: MIT
platforms: [linux, macos, windows]
tags: [google, gmail, calendar, sheets, crm, drive, docs, chat, assistant]
---

# Google Workspace Chat Assistant

Natural language interface to your entire Google Workspace. When Mahi asks for any data from Gmail, Calendar, Sheets, Drive, or Docs — retrieve it, display it clearly, and offer to modify or create new data as requested.

## Trigger

Use this skill when the user asks questions like:
- "What's on my calendar today?"
- "Show me unread emails"
- "What projects are overdue?"
- "Add a new task to my CRM"
- "Send an email to..."
- "Create a meeting for..."
- "Find that document about..."
- "Update the spreadsheet with..."

## Prerequisites

- The `google-workspace` skill must be loaded (provides the underlying API access)
- OAuth credentials must be set up at `~/.hermes/google_token.json`
- Run `python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check` to verify auth

## Workflow

### Step 1: Identify the Service
Determine which Google Workspace service the user is asking about:
| Service | Keywords |
|---------|----------|
| Gmail | email, mail, inbox, unread, send, reply, message |
| Calendar | calendar, meeting, event, schedule, appointment, free/busy |
| Sheets | spreadsheet, crm, project, task, lead, row, cell, sheet |
| Drive | file, document, folder, upload, download, share |
| Docs | doc, document, notes, write, append |

### Step 2: Parse the Intent
Determine what the user wants to do:
- **READ/SEARCH** — retrieve and display data
- **CREATE** — add new data (events, emails, rows, files)
- **UPDATE** — modify existing data
- **DELETE** — remove data (always confirm first)

### Step 3: Execute the Command
Use the `google-workspace` skill's CLI commands:

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

#### Gmail Examples
```bash
$GAPI gmail search "is:unread" --max 10
$GAPI gmail get MESSAGE_ID
$GAPI gmail send --to "recipient@email.com" --subject "Subject" --body "Message body"
$GAPI gmail reply MESSAGE_ID --body "Reply message"
```

#### Calendar Examples
```bash
$GAPI calendar list --start $(date -u +%Y-%m-%dT00:00:00Z) --end $(date -u +%Y-%m-%dT23:59:59Z)
$GAPI calendar create --summary "Meeting" --start "2026-03-01T10:00:00+05:30" --end "2026-03-01T11:00:00+05:30" --attendees "person@email.com"
$GAPI calendar delete EVENT_ID
```

#### Sheets (CRM) Examples
```bash
$GAPI sheets get SHEET_ID "'Sheet1'!A1:Z100"
$GAPI sheets append SHEET_ID "'Sheet1'!A:Z" --values '[["value1","value2"]]'
$GAPI sheets update SHEET_ID "'Sheet1'!A1:B2" --values '[["Name","Status"]]'
```

#### Drive Examples
```bash
$GAPI drive search "report" --max 10
$GAPI drive upload /path/to/file.pdf --parent FOLDER_ID
$GAPI drive download FILE_ID --output ~/Downloads/file.pdf
$GAPI drive share FILE_ID --email person@email.com --role writer
```

#### Docs Examples
```bash
$GAPI docs get DOC_ID
$GAPI docs create --title "New Document" --body "Initial content"
$GAPI docs append DOC_ID --text "Additional content"
```

### Step 4: Display Results
Format the JSON output into a readable, user-friendly format:
- Use bullet lists for multiple items
- Highlight important information (overdue items, urgent emails)
- Include relevant metadata (dates, times, IDs)

### Step 5: Offer Follow-up
After displaying data, offer relevant actions:
- "Would you like me to reply to this email?"
- "Should I add this to your calendar?"
- "Do you want me to update the CRM?"

## Safety Rules

1. **ALWAYS confirm before:** sending emails, creating events, modifying data, deleting, sharing, uploading.
2. **Show what will happen** — display the exact command/output and ask for approval.
3. **Never auto-execute destructive operations.**
4. **Respect privacy** — don't display full email bodies in shared channels.

## Common Requests

| User Says | What to Do |
|-----------|------------|
| "What's on my calendar today?" | List today's events, format as schedule |
| "Show me unread emails" | Search is:unread, show from/subject/date |
| "What projects are overdue?" | Read CRM sheet, filter by due date < today |
| "Add a new lead to CRM" | Ask for details, confirm, append row |
| "Send email to X" | Ask for subject/body, confirm, send |
| "Schedule a meeting" | Ask for details, confirm, create event |
| "Find document about X" | Search Drive, show matching files |
| "Mark task as done" | Ask which task, confirm, update sheet |

## Error Handling

| Error | Response |
|-------|----------|
| `NOT_AUTHENTICATED` | Guide user through OAuth setup |
| `REFRESH_FAILED` | Ask user to re-authenticate |
| `HttpError 403` | Check API scopes, may need re-auth |
| `HttpError 429` | Rate limit hit, wait and retry |
| Empty results | Inform user no data found |

## Notes

- All times in IST (Asia/Kolkata) unless specified otherwise
- CRM spreadsheet ID: `1Zf0TrJVhzW6tnlKaG0MMCoe9kiKPHMg1A5l1DmFmNFc`
- Format dates as: "17 Sep 2026, 2:30 PM IST"
