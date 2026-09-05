---
name: external-platform-integration
description: "Track agent work through external platforms with hooks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  external-platform-integration:
    tags: [integration, api, task-management, composio, multica, workflow, automation]
    related_skills: [google-workspace, github-issues, notion]
    homepage: https://github.com/NousResearch/hermes-agent
    category: autonomous-ai-agents
---

# External Platform Integration

Connect Hermes agent work to external platforms so every task, input, output, and status update is tracked in a central system — not scattered across chat. The pattern has two layers:

1. **Task/board layer** — an external issue tracker (Multica, Linear, Jira, GitHub Issues) where work gets created, tracked through statuses, and commented on.
2. **Execution layer** — an external app-integration platform (Composio, Zapier, Make) that actually performs actions across connected apps (Gmail, Slack, GitHub, Google Sheets, etc.).

The hook module wraps both, so every agent action flows through the platform automatically.

## When to Use

- User wants all their tasks, inputs, outputs tracked in an external system
- User wants agent actions to flow through connected apps (Gmail, GitHub, Sheets, Slack, etc.)
- User has an API token or key for an external platform and wants a reusable hook
- Building a "single source of truth" dashboard for agent work

## Architecture: Dual-Board Pattern

```
User request
    │
    ├── Task Board (Multica/Linear/Jira)
    │   ├── Create issue (status: todo)
    │   ├── Move to in_progress when work starts
    │   ├── Comment with progress / outputs / findings
    │   ├── Move to in_review when result is ready
    │   └── Move to done / blocked / cancelled at end
    │
    └── Execution Platform (Composio/Zapier)
        └── Actually perform the work across connected apps
            (send email, create GitHub issue, read Sheets, etc.)
```

The task board is the "what's happening" dashboard. The execution platform is the "do the thing" engine. They stay in sync because the hook module updates both.

## Step 1: Verify Platform Connectivity

Before building the hook, verify the API key/token works. Identify which key type you have.

### Composio Key Types (critical distinction)

| Key type | Prefix | Use with | Endpoint |
|---|---|---|---|
| **Consumer key** | `ck_*` | MCP protocol only | `connect.composio.dev/mcp` |
| **Platform/API key** | `ak_*` | Python SDK + REST API | `backend.composio.dev` |

If you have a `ck_*` key and the Python SDK returns `401 Invalid API key`, that's expected — the SDK needs an `ak_*` key. Go to the dashboard → API Keys to generate one.

### Multica Token

Multica uses a single PAT (Personal Access Token) with `mul_` prefix. Works with both CLI and REST API directly. Set `MULTICA_TOKEN` env var or pass it to the hook.

### Verification pattern

```python
import os, json, urllib.request

# Multica
token = os.environ.get("MULTICA_TOKEN")
req = urllib.request.Request(
    "https://api.multica.ai/api/me",
    headers={"Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(req) as resp:
    print(json.loads(resp.read())["name"])

# Composio (ak_* key)
api_key = os.environ.get("COMPOSIO_API_KEY")
from composio import Composio
client = Composio(api_key=api_key)
# If this succeeds without 401, you have the right key type
```

## Step 2: Install Required SDKs

```bash
# Composio Python SDK (works on Windows — unlike the CLI installer)
uv pip install composio composio-client

# Or with pip
pip install composio composio-client
```

**Platform note:** The Composio CLI installer (`curl -fsSL https://composio.dev/install | sh`) explicitly blocks Windows (`MINGW64/MSYS/CYGWIN` check). Use the Python SDK instead — `uv pip install composio composio-client` works fine on Windows.

## Step 3: Build the Hook Module

Create a Python file that wraps the platform API. Full template in `references/hook-module-pattern.md`.

```python
import os, json, urllib.request

TOKEN = os.environ.get("MULTICA_TOKEN", "mul_...")
WORKSPACE_ID = os.environ.get("MULTICA_WORKSPACE_ID", "...")
BASE_URL = "https://api.multica.ai"

def _headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "X-Workspace-ID": WORKSPACE_ID,
    }

def _call(method, path, body=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=_headers(), method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read()), resp.status

def start_task(title, description=""):
    body = {"title": title, "description": description, "status": "todo"}
    data, status = _call("POST", "/api/issues", body)
    return data

def update_status(issue_id, status):
    valid = {"backlog", "todo", "in_progress", "in_review", "done", "blocked", "cancelled"}
    if status not in valid:
        raise ValueError(f"Invalid status: {status}")
    data, _ = _call("PUT", f"/api/issues/{issue_id}", {"status": status})
    return data

def comment(issue_id, text):
    data, _ = _call("POST", f"/api/issues/{issue_id}/comments", {"content": text})
    return data

def summary():
    """Print all issues grouped by status."""
    data, _ = _call("GET", "/api/issues")
    issues = data.get("issues", [])
    grouped = {}
    for issue in issues:
        st = issue.get("status", "unknown")
        grouped.setdefault(st, []).append(issue)
    for st in ["backlog", "todo", "in_progress", "in_review", "blocked", "done", "cancelled"]:
        items = grouped.get(st, [])
        if items:
            print(f"[{st.upper()}] ({len(items)})")
            for issue in items:
                print(f"  {issue.get('identifier')}: {issue.get('title')}")

class PlatformAPI:
    def start_task(self, *a, **kw): return start_task(*a, **kw)
    def update_status(self, *a, **kw): return update_status(*a, **kw)
    def comment(self, *a, **kw): return comment(*a, **kw)
    def summary(self, *a, **kw): return summary(*a, **kw)

platform = PlatformAPI()
```

## Step 4: Track Every Task Through the Platform

Pattern for any work the agent does:

```python
from multica_hook import mca

task = mca.start_task("Build the API client", "Python HTTP client with retry and timeout")
mca.update_status(task["id"], "in_progress")
mca.comment(task["id"], "Scaffolded project, writing base Client class")
mca.comment(task["id"], "Added exponential backoff retry logic")
mca.update_status(task["id"], "in_review")
mca.comment(task["id"], "Code complete, ready for review")
mca.update_status(task["id"], "done")
mca.comment(task["id"], "Merged and deployed")
```

### Quick-access helper

```python
def track_task(title, description="", labels=None):
    issue = start_task(title, description, labels)
    iid = issue["id"]
    class Task:
        def go(self, status, note=None):
            update_status(iid, status)
            if note: comment(iid, f"[{status}] {note}")
        def progress(self, note):
            comment(iid, f"[in_progress] {note}")
        def review(self, note=None):
            update_status(iid, "in_review")
            if note: comment(iid, f"[in_review] {note}")
        def done(self, note=""):
            update_status(iid, "done")
            if note: comment(iid, f"[done] {note}")
        def blocked(self, reason):
            update_status(iid, "blocked")
            comment(iid, f"[blocked] {reason}")
    return Task()

# Usage:
task = mca.track_task("My project")
task.go("in_progress", "Started")
task.progress("Halfway through")
task.review("Ready")
task.done("All done!")
```

## Step 5: Composio Execution Integration

Once you have the `ak_*` platform key, use the Composio SDK to execute actions:

```python
import os
from composio import Composio

client = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
session = client.create(user_id="mahesh")
tools = client.tools.get(user_id="mahesh", toolkits=["google_sheets"], limit=50)
result = client.tools.execute(
    slug="google_sheets.LIST_SHEETS",
    arguments={"spreadsheet_id": "your-sheet-id"},
    user_id="mahesh",
    session_id=session.session_id
)
```

See `references/composio-quick-ref.md` for the tool discovery and execution workflow.

## Pitfalls

### Windows + Composio CLI

The Composio CLI installer (`curl -fsSL https://composio.dev/install | sh`) **rejects Windows** outright. The script checks `uname -s` for `MINGW64`/`MSYS`/`CYGWIN` and bails. **Use the Python SDK instead** — `uv pip install composio composio-client` works fine on Windows.

### Composio key type mismatch

If the Python SDK returns `401 Invalid API key: ck_**...`, you're using a `ck_*` consumer key where the SDK needs an `ak_*` platform key:
- `ck_*` → MCP endpoint only (`connect.composio.dev/mcp`, `x-consumer-api-key` header)
- `ak_*` → REST API + SDK (`backend.composio.dev`, `x-api-key` header)

Fix: generate an `ak_*` key from the Composio dashboard → API Keys page.

### MCP endpoint requires session handshake

The MCP endpoint (`connect.composio.dev/mcp`) needs a proper MCP protocol flow: initialize first (gets `Mcp-Session-Id`), then tools/list and tool calls use that session ID. Raw HTTP POSTs without the session header get `400 Bad Request: Server not initialized`.

### Multica comment field name

Multica's comment API expects `content`, not `body`. Using `{"body": "text"}` returns `400 {"error": "content is required"}`. Use `{"content": "text"}`.

### Multica batch-update endpoint bug

As of v0.2.16, `POST /api/issues/batch-update` returns 200 with `{"updated": N}` but does NOT persist field changes. Use individual `PUT /api/issues/<uuid>` calls instead. Fixed in PR #1759.

## Related

- `references/hook-module-pattern.md` — full hook module template with error handling
- `references/composio-quick-ref.md` — Composio tool discovery, session management, execution patterns
- `references/platform-key-types.md` — key type reference for Composio and other platforms
