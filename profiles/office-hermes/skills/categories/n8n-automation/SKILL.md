---
name: n8n-automation
description: "Create, inspect, activate, and debug n8n workflows through Hermes — via the n8n MCP bridge or direct API calls. Covers credential setup, workflow CRUD, common failures, and debugging paths."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [n8n, automation, workflow, MCP, API, google-workspace]
related_skills: [google-workspace]
---

# n8n Automation

Build and manage n8n workflows through Hermes — either via the **n8n MCP bridge** (the `hermes-n8n-mcp` server installed at `~/.hermes/mcp-installs/n8n/`) or by calling n8n's REST API directly with an API key.

## When to use this skill

- Creating new n8n workflows programmatically (webhook-triggered, scheduled, or API-triggered)
- Inspecting existing workflows (listing, reading node structure, checking active state)
- Activating or deactivating workflows
- Debugging n8n MCP connectivity or API authentication failures
- Setting up n8n credentials for Google, Telegram, or other services

## Prerequisites

### n8n instance
- n8n must be running locally (default: `http://localhost:5678`)
- Verify: `curl -s http://localhost:5678/api/v1/workflows -H "X-N8N-API-KEY: YOUR_KEY" | python3 -m json.tool`

### API key
- Create an API key in n8n UI: click your avatar → Settings → API Keys → Create
- Key format: JWT token starting with `eyJ...`, audience `public-api`
- Store in n8n's `user_api_keys` table (auto-created when you create via UI)
- Use `X-N8N-API-KEY` header (NOT `Authorization: Bearer`)

### MCP bridge (optional)
- Installed at `~/.hermes/mcp-installs/n8n/`
- Configured in `~/.hermes/config.yaml` under `mcp` → `n8n`
- Requires `.env` file with `N8N_BASE_URL` and `N8N_API_KEY`

## Connecting via n8n MCP

The MCP bridge exposes these tools: `health`, `list_workflows`, `get_workflow`, `find_workflows`, `list_executions`, `get_execution`, `recent_failures`, `activate_workflow`, `deactivate_workflow`, `export_workflow`.

### Config check
```bash
# Verify the MCP entry in config.yaml
grep -A 15 "n8n:" ~/.hermes/config.yaml
```

### .env setup
The MCP server loads config from:
1. `N8N_MCP_ENV` env var (if set)
2. `~/.config/n8n-mcp/env`
3. `~/.hermes/mcp-installs/n8n/.env` (preferred — co-located with server)

```bash
# Create/update .env
cat > ~/.hermes/mcp-installs/n8n/.env << 'EOF'
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your_api_key_here
EOF
# Also write to ~/.config/n8n-mcp/env for the fallback path
mkdir -p ~/.config/n8n-mcp
cp ~/.hermes/mcp-installs/n8n/.env ~/.config/n8n-mcp/env
```

### Testing the connection
Use the MCP `health` tool or test directly:
```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv('/Users/apple/.hermes/mcp-installs/n8n/.env')
import httpx
r = httpx.get(f'{os.getenv(\"N8N_BASE_URL\")}/api/v1/workflows',
              headers={'X-N8N-API-KEY': os.getenv('N8N_API_KEY')},
              timeout=10)
print(f'Status: {r.status_code}')
"
```

## n8n API Authentication

### API key format
- JWT token, audience `public-api`, issued by n8n
- Stored in n8n's SQLite DB: `~/.n8n/database.sqlite`, table `user_api_keys`
- Column `apiKey` stores the full JWT as text
- Use with header: `X-N8N-API-KEY: <your_jwt_token>`

### Key verification (debugging 401 errors)
When API calls return 401, verify the key is valid:

```python
import json, base64, hmac, hashlib, sqlite3, binascii

# Get signing key from n8n's DB
conn = sqlite3.connect('/Users/apple/.n8n/database.sqlite')
cur = conn.cursor()
cur.execute("SELECT value FROM deployment_key WHERE type='signing.jwt'")
signing_key = cur.fetchone()[0]  # hex string

# Get your API key
cur.execute("SELECT apiKey FROM user_api_keys WHERE label='YOUR_LABEL'")
api_key = cur.fetchone()[0]

# Verify JWT signature
parts = api_key.split('.')
sig_input = f"{parts[0]}.{parts[1]}".encode()
expected_sig = base64.urlsafe_b64encode(
    hmac.new(signing_key.encode(), sig_input, hashlib.sha256).digest()
).rstrip(b'=').decode()

print(f"Signature valid: {expected_sig == parts[2]}")
print(f"Key in DB: {api_key == api_key}")  # sanity check

# Decode payload
payload = json.loads(base64.urlsafe_b64decode(
    parts[1] + '=' * (4 - len(parts[1]) % 4)
))
print(f"Payload: {json.dumps(payload, indent=2)}")
```

### Common auth failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 with valid-looking key | Key truncated when stored (dotenv bug) | Read key directly from DB via sqlite3, not from .env |
| 401 with MCP bridge | `python-dotenv` 1.2.3 truncates long values | Read .env file directly line-by-line instead of `load_dotenv()` |
| 401, key verified but rejected | API key audience is `mcp-server-api` not `public-api` | Create a new key with audience `public-api` from n8n UI |
| 401 on Calendar API despite having scope | Google API gateway blocks despite scope in token | Use n8n's native Google Calendar node instead of direct API call |

## Workflow CRUD Operations

### List workflows
```python
import httpx

api_key = "your_api_key"
headers = {"X-N8N-API-KEY": api_key, "Accept": "application/json"}
base = "http://localhost:5678"

r = httpx.get(f"{base}/api/v1/workflows", headers=headers, timeout=30)
workflows = r.json().get("data", [])
for wf in workflows:
    print(f"{wf['name']} (id: {wf['id'][:16]}...) active={wf.get('active')} nodes={len(wf.get('nodes', []))}")
```

### Read one workflow
```python
wf_id = "workflow_id_here"
r = httpx.get(f"{base}/api/v1/workflows/{wf_id}", headers=headers, timeout=30)
wf = r.json()
# Note: response is the workflow object directly, NOT wrapped in {"data": ...}
for node in wf.get("nodes", []):
    print(f"  [{node['type']}] {node['name']} (id: {node['id'][:12]}...)")
```

### Create a workflow
```python
import uuid

workflow = {
    "name": "My New Workflow",
    "nodes": [
        {
            "id": str(uuid.uuid4()),
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": {
                "httpMethod": "POST",
                "path": "my-webhook",
                "responseMode": "lastNode",
            }
        },
        # ... more nodes
    ],
    "connections": {
        "Webhook": {"main": [[{"node": "Next Node", "type": "main", "index": 0}]]}
    },
    "settings": {"executionOrder": "v1"}
}

r = httpx.post(f"{base}/api/v1/workflows", headers=headers, json=workflow, timeout=30)
if r.status_code in (200, 201):
    wf = r.json()
    wf_id = wf["id"]
    print(f"Created: {wf['name']} (id: {wf_id[:16]}...)")
```

### Activate a workflow
**IMPORTANT: The `active` field is READ-ONLY on PUT.** To activate, use POST to the activate endpoint:

```python
# WRONG: this returns 400 "active is read-only"
# httpx.put(f"{base}/api/v1/workflows/{wf_id}", json={**wf, "active": True})

# CORRECT:
r = httpx.post(f"{base}/api/v1/workflows/{wf_id}/activate", headers=headers, timeout=10)
print(f"Activate: {r.status_code} - {r.text[:200]}")
```

### Deactivate
```python
r = httpx.post(f"{base}/api/v1/workflows/{wf_id}/deactivate", headers=headers, timeout=10)
```

### Delete
```python
r = httpx.delete(f"{base}/api/v1/workflows/{wf_id}", headers=headers, timeout=10)
```

### Update a workflow
```python
# GET first, modify, then PUT back (strip read-only fields)
r = httpx.get(f"{base}/api/v1/workflows/{wf_id}", headers=headers, timeout=30)
wf = r.json()

# Remove read-only fields before PUT
for key in ["id", "meta", "pinData", "staticData", "shared", 
            "activeVersion", "activeVersionId", "createdAt", "updatedAt",
            "isArchived", "versionId", "versionCounter", "sourceWorkflowId",
            "triggerCount", "nodeGroups", "tags", "active", "description"]:
    wf.pop(key, None)

# Modify what you need...
wf["nodes"] = [... updated nodes ...]

r = httpx.put(f"{base}/api/v1/workflows/{wf_id}", headers=headers, json=wf, timeout=30)
```

## Common Pitfalls & Fixes

### python-dotenv truncates long values
**Problem:** `python-dotenv` 1.2.3 truncates values over ~272 characters. n8n API keys are JWTs ~267-289 chars. When loaded via `load_dotenv()`, the key gets truncated and API calls return 401.

**Fix options:**
1. Read .env directly (line by line) instead of `load_dotenv()`:
   ```python
   with open('.env') as f:
       for line in f:
           if line.startswith('N8N_API_KEY='):
               api_key = line.split('=', 1)[1].strip()
   ```
2. Patch `server.py` to read .env directly (same approach)
3. Upgrade `python-dotenv` to >= 1.0.1+ (the truncation was fixed in later versions, but 1.2.3 may still have issues with very long values)

### mcp v2 renamed FastMCP → MCPServer
**Problem:** The n8n MCP bridge's `server.py` imports `from mcp.server.fastmcp import FastMCP`. In `mcp` Python SDK v2.0+, `FastMCP` was renamed to `MCPServer`.

**Fix:**
```python
# In server.py, change:
from mcp.server.fastmcp import FastMCP
# To:
from mcp.server.mcpserver import MCPServer as FastMCP
```

### MCP server env path uses cwd instead of script dir
**Problem:** `server.py`'s `DEFAULT_ENV_PATHS` includes `Path.cwd() / ".env"`. When Hermes invokes the MCP server, cwd may not be the n8n install directory, so the .env is not found.

**Fix:** Change to `Path(__file__).resolve().parent / ".env"` so it always finds the .env next to the server script.

### Workflow activation: active field is read-only
**Problem:** PUT with `{"active": true}` returns 400 "active is read-only".

**Fix:** Use `POST /api/v1/workflows/{wf_id}/activate` (not PUT).

### Node type not recognized
**Problem:** Creating a workflow with `n8n-nodes-base.openAiChat` fails with "Unrecognized node type" — the OpenAI node package isn't installed in this n8n instance.

**Fix:** Use `n8n-nodes-base.httpRequest` to call OpenAI API directly, or install the missing node package.

### Connection source/target name mismatch on update
**Problem:** When updating a workflow, renaming a node but not updating the `connections` dict keys causes "unknown_connection_source/target" errors.

**Fix:** When renaming a node in an update, also rename the corresponding keys in the `connections` dict AND update the `node` references inside connection arrays.

## Debugging Connectivity

### Step 1: Is n8n running?
```bash
curl -s http://localhost:5678/api/v1/workflows -o /dev/null -w "%{http_code}"
# Should return 401 (needs auth) not 000 (connection refused)
```

### Step 2: Is the API key valid?
Use the verification script above. Check:
- Signature matches the signing key in n8n's DB
- Key is stored in DB (not just in .env)
- Audience is `public-api` (not `mcp-server-api`)

### Step 3: Is the .env loaded correctly?
```bash
# Check what the MCP server actually sees
cat ~/.hermes/mcp-installs/n8n/.env
# Verify the API_KEY line has the FULL key (not truncated)
# Count characters: should match the DB key length
```

### Step 4: Check server.py patches
If the MCP server still fails after the above, verify `server.py` has:
- `from mcp.server.mcpserver import MCPServer as FastMCP` (not `fastmcp`)
- `Path(__file__).resolve().parent / ".env"` (not `Path.cwd()`)
- Direct .env reading (not `load_dotenv()`)

## Security

- API keys are JWTs — treat them like passwords
- Store in `.env` (gitignored), not hardcoded in workflows
- n8n credentials (OAuth tokens, API keys for external services) are stored in n8n's credential store, not in workflow JSON
- Use `responseMode: "lastNode"` for webhook workflows that need to return a response
- Redact secrets from workflow JSON before sharing/exporting

## References

- `references/n8n-mcp-troubleshooting.md` — detailed troubleshooting for MCP bridge issues (dotenv truncation, mcp v2 rename, env path, activation endpoint)
- `references/sheets-drive-csv-export.md` — reading Google Sheets via Drive export CSV (reliable alternative when Sheets API returns 404)
- `references/n8n-workflow-design-patterns.md` — patterns for building robust workflows (parallel branches, error handling, idempotency)
