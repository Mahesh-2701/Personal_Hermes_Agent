---
name: zoho-crm-mcp
description: "Use when connecting Zoho CRM to Hermes via MCP. Covers setup, OAuth token generation, read-only config, and available tools."
version: 1.0.0
---

# Zoho CRM MCP for Hermes

A Model Context Protocol server that gives Hermes read-only access to your Zoho CRM data — contacts, deals, accounts, tasks, users, and any custom module.

## What's Installed

**Server script:**
`~/.hermes/scripts/zoho_crm_mcp_server.py`

**Config files updated:**
- `~/.hermes/ops/bot_homes/employee/config/config.yaml`
- `~/.hermes/ops/bot_homes/manager/config/config.yaml`
- `~/.hermes/ops/bot_homes/cmo/config/config.yaml`
- `~/.hermes/config.yaml` (main — needs manual edit, see below)

**Tools exposed (all read-only):**
| Tool | Description |
|---|---|
| `mcp_zoho_crm_list_contacts` | List contacts (paginated, searchable) |
| `mcp_zoho_crm_get_contact` | Get one contact by ID |
| `mcp_zoho_crm_list_deals` | List deals pipeline |
| `mcp_zoho_crm_get_deal` | Get one deal by ID |
| `mcp_zoho_crm_list_accounts` | List companies/accounts |
| `mcp_zoho_crm_get_account` | Get one account by ID |
| `mcp_zoho_crm_list_tasks` | List tasks |
| `mcp_zoho_crm_get_task` | Get one task by ID |
| `mcp_zoho_crm_list_users` | List CRM users |
| `mcp_zoho_crm_search` | Search any module by keyword |
| `mcp_zoho_crm_get_module` | Generic list any module |
| `mcp_zoho_crm_get_record` | Generic get any record |
| `mcp_zoho_crm_aggregation` | Count/grouped aggregation |

## Step 1: Generate a Read-Only Zoho OAuth Token

You need a Zoho API client with **read-only scopes**.

### Option A: Use the Zoho Developer Console (easiest)

1. Go to https://api-console.zoho.com/
2. Create a new client (or use an existing one)
3. Note your `Client ID` and `Client Secret`
4. Generate an access token with these scopes:
   - `ZohoCRM.modules.READ` (full read access) — or pick individual ones like `ZohoCRM.Contacts.READ`, `ZohoCRM.Deals.READ`, etc.
5. Copy the access token (looks like `1000.abc123...`)

### Option B: Use OAuth 2.0 Authorization Code Flow

```
POST https://accounts.zoho.com/oauth/v2/token
  grant_type=authorization_code
  code=<auth_code>
  client_id=<client_id>
  client_secret=<client_secret>
  redirect_uri=<your_redirect_uri>
```

The response gives you an `access_token` and `refresh_token`.

### Required Scopes for Read-Only Access

| Scope | What it grants |
|---|---|
| `ZohoCRM.modules.READ` | Read all standard modules |
| `ZohoCRM.Contacts.READ` | Contacts only |
| `ZohoCRM.Deals.READ` | Deals/pipeline only |
| `ZohoCRM.Accounts.READ` | Accounts/companies only |
| `ZohoCRM.Tasks.READ` | Tasks only |
| `ZohoCRM.Users.READ` | Users list only |

For the full-featured setup later, you'd add write scopes like `ZohoCRM.modules.ALL` or individual `.WRITE`/`.ALL` scopes.

## Step 2: Configure the Token

The MCP server reads credentials from environment variables set in the config.yaml `env` block.

**File to edit:**
`~/.hermes/ops/bot_homes/<bot>/config/config.yaml`

Find the `zoho_crm` block and set the token:

```yaml
  zoho_crm:
    command: /Users/apple/.hermes/hermes-agent/venv/bin/python
    args:
      - /Users/apple/.hermes/scripts/zoho_crm_mcp_server.py
    env:
      ZOHO_CRM_ACCESS_TOKEN: "1000.your_actual_token_here"
      ZOHO_CRM_ORG_ID: ""          # optional: for multi-org accounts
    timeout: 60
    connect_timeout: 30
    sampling:
      enabled: false
```

**For the main Hermes config** (`~/.hermes/config.yaml`), add the same `zoho_crm` block under the existing `mcp_servers:` section — just copy the block from any bot config.

**Do NOT commit tokens to version control.** The token is only in your local config files.

## Step 3: Restart Hermes

MCP servers are discovered at Hermes startup. After editing config:

```bash
# If Hermes is running as a service / background process:
# Restart it (the exact command depends on how you run it)

# For the CLI:
hermes shutdown   # or kill the process
hermes            # restart
```

On restart, Hermes will:
1. Launch `zoho_crm_mcp_server.py` as a subprocess
2. Call `list_tools()` to discover the 13 Zoho CRM tools
3. Register them with the `mcp_zoho_crm_*` prefix
4. Make them available in every conversation

## Step 4: Verify It Worked

Once Hermes restarts, ask it:

> "List the first 5 contacts from Zoho CRM"

If the token is configured, Hermes will call `mcp_zoho_crm_list_contacts` and return records. If the token is missing or invalid, you'll get an error message telling you to configure it.

You can also check the tool names are registered:

> "What Zoho CRM tools do you have available?"

## How It Works (Under the Hood)

```
Hermes Agent
  └─ reads config.yaml → mcp_servers.zoho_crm
       └─ spawns: python zoho_crm_mcp_server.py
            └─ stdio transport (stdin/stdout JSON-RPC)
                 └─ Server("zoho_crm_readonly")
                      ├─ list_tools() → 13 Tool definitions
                      └─ call_tool(name, args)
                           └─ httpx2 GET https://www.zohoapis.com/crm/v2/...
                                └─ Authorization: Zoho-oauthtoken <token>
```

Each tool call:
1. Hermes calls the MCP tool by name
2. The server translates it to the right Zoho CRM API v2 endpoint
3. `httpx2` makes the HTTPS request with the OAuth token in headers
4. Zoho returns JSON → server formats it → Hermes gets the result

## Read-Only Guarantee

All 13 tools are **GET-only**. There are no create/update/delete tools. Even if you asked Hermes to "update a contact", it would only be able to read — it cannot call any write endpoints because none are implemented.

When you're ready for full access, I'll add:
- `zoho_crm_create_contact`, `zoho_crm_update_contact`, `zoho_crm_delete_contact`
- Same for deals, accounts, tasks
- Bulk operations, file upload, and custom module write support
- The token will need additional scopes: `ZohoCRM.modules.ALL` or individual `.WRITE`/`.ALL` scopes

## Troubleshooting

**"ZOHO_CRM_ACCESS_TOKEN is not configured"**
→ Set the token in config.yaml under `mcp_servers.zoho_crm.env.ZOHO_CRM_ACCESS_TOKEN`

**"Failed to connect to MCP server 'zoho_crm'"**
→ Check that `/Users/apple/.hermes/hermes-agent/venv/bin/python` exists and the script path is correct. Look at Hermes startup logs.

**"401 Unauthorized" on every call**
→ Token expired. Zoho access tokens expire after 1 hour. Generate a new one. (For production use, implement refresh token flow — you'd need to add a token refresh mechanism to the server.)

**"403 Forbidden" on specific modules**
→ Your token doesn't have the scope for that module. Check the scopes you requested when generating the token.

**Tools not showing up**
→ Restart Hermes after editing config. MCP tools are discovered at startup only.
