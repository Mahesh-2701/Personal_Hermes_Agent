---
name: zoho-crm-chat
description: "Use when Mahesh asks about Zoho CRM data in chat — leads, deals, tasks, contacts, accounts. Translates natural chat requests into the right zoho_crm_mcp tool calls and reports back in plain summary."
version: 1.0.0
---

# Zoho CRM Chat Skill

This skill sits on top of the `zoho-crm-mcp` MCP server. When Mahesh asks about Zoho CRM data in conversation, use this skill to interpret the request, pick the right tool, call it, and report the result in a clean human-friendly summary.

## When to activate

Activate this skill whenever Mahesh's chat message mentions any of:

- **Leads** — "show my leads", "who are my prospects", "any new leads", "lead summary"
- **Deals / Projects** — "what deals are pending", "project pipeline", "deal status", "which deals are stuck"
- **Tasks / Pending works** — "what tasks are due", "pending works", "my to-dos", "upcoming tasks"
- **Contacts** — "list my contacts", "who do I know at X company", "contact details"
- **Accounts / Companies** — "what companies are in CRM", "account list"
- **General CRM questions** — "what's in my CRM", "give me a CRM summary", "CRM overview"

Also activate when Mahesh says "fetch from Zoho", "check Zoho CRM", or "pull CRM data".

## How it works

```
Mahesh's chat → interpret intent → pick tool → call zoho_crm_* MCP tool → format summary → report
```

### Step 1: Interpret the request

Map the user's words to a Zoho CRM module and action:

| User says... | Module | Action | Tool to call |
|---|---|---|---|
| "leads", "prospects", "new leads" | Leads | list | `zoho_crm_list_contacts` (or `zoho_crm_search` with module=leads) |
| "deals", "projects", "pipeline" | Deals | list | `zoho_crm_list_deals` |
| "tasks", "pending", "to-do" | Tasks | list | `zoho_crm_list_tasks` |
| "contacts", "people" | Contacts | list | `zoho_crm_list_contacts` |
| "companies", "accounts" | Accounts | list | `zoho_crm_list_accounts` |
| "search X", "find X in CRM" | any | search | `zoho_crm_search` with module + search term |
| "details of X" (by name/ID) | any | get one | `zoho_crm_get_module` or `zoho_crm_get_record` |
| "summary", "overview", "CRM status" | all | aggregate | call multiple list tools, then summarize |

**Important:** The Zoho CRM module for "leads" may need to be fetched via `zoho_crm_search` with `module=leads` or `zoho_crm_get_module` with `module=Leads`, since there's no dedicated `zoho_crm_list_leads` tool. Use `zoho_crm_get_module` with `module=Leads` for listing leads.

### Step 2: Call the tool

Use the appropriate `zoho_crm_*` tool from the MCP server. Default limit: 20 records. For searches, pass the search term.

If the tool returns an error:
- **401 / token error**: pause and tell Mahesh the Zoho token needs refreshing. Point him to the skill doc for how to generate a new one.
- **403 / forbidden**: tell Mahesh the token doesn't have the right scope for that module.
- **Empty result (0 records)**: report honestly that there's no data in that module. Don't fabricate.

### Step 3: Format the report

Keep summaries concise and scannable. Use this template:

```
## [Module] — Zoho CRM

Total: N records

1. Name — key detail
   - detail1, detail2
2. Name — key detail
   ...

[If empty: "No [module] found in Zoho CRM."]
```

For deals, always show amount and stage.
For tasks, always show status and due date.
For leads, show name, company, and status.

### Step 4: Offer follow-up

After reporting, offer natural next steps:
- *"Want me to search for a specific lead/company?"*
- *"Want more details on any of these?"*
- *"Want me to check another module?"*

## Tool reference (from zoho-crm-mcp)

| Tool | When to use |
|---|---|
| `zoho_crm_list_contacts` | List contacts (paginated) |
| `zoho_crm_get_contact` | Get one contact by ID |
| `zoho_crm_list_deals` | List deals/pipeline |
| `zoho_crm_get_deal` | Get one deal by ID |
| `zoho_crm_list_accounts` | List accounts/companies |
| `zoho_crm_get_account` | Get one account by ID |
| `zoho_crm_list_tasks` | List tasks |
| `zoho_crm_get_task` | Get one task by ID |
| `zoho_crm_list_users` | List CRM users |
| `zoho_crm_search` | Search any module by keyword |
| `zoho_crm_get_module` | Generic list any module (use for Leads) |
| `zoho_crm_get_record` | Generic get any record |
| `zoho_crm_aggregation` | Count/grouped aggregation |

## Important notes

- **Token expiry**: Zoho access tokens expire after 1 hour. If calls start returning 401, tell Mahesh to generate a fresh token at api-console.zoho.com and paste it here.
- **Read-only**: All tools are GET-only. Don't promise to create/update/delete records — that requires write scopes and additional tools.
- **No data ≠ error**: If a module returns 0 records, that's a valid result. Report it honestly.
- **Idempotent**: You can re-run the same query — Zoho data doesn't change between calls in a conversation unless Mahesh edits it elsewhere.

## Example conversations

**User:** "Show me my leads"
→ Call `zoho_crm_get_module` with `module=Leads, limit=20`
→ Report: "Here's what's in your Leads module — N leads found..."

**User:** "What deals are in my pipeline?"
→ Call `zoho_crm_list_deals` with `limit=20`
→ Report: list deals with name, amount, stage

**User:** "Any tasks due this week?"
→ Call `zoho_crm_list_tasks` with `limit=20`
→ Filter by due date in your head, report the relevant ones

**User:** "Search for Acme Corp in my CRM"
→ Call `zoho_crm_search` with `module=accounts, search=Acme Corp`
→ Also try `module=contacts` with same search
→ Report matches

**User:** "Give me a CRM overview"
→ Call `zoho_crm_list_contacts`, `zoho_crm_list_deals`, `zoho_crm_list_tasks`, `zoho_crm_list_accounts` 
→ Summarize each with counts and top entries
