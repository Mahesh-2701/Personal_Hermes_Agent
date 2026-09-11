---
name: basecamp-integration
description: >
  Use when connecting Hermes to Basecamp via CLI (bc) and/or MCP server.
  Covers initial read-only configuration, token setup, verifying connectivity,
  and later upgrading to full access. Always confirms the user's Basecamp
  account/company slug before writing any config. Never stores tokens in
  plaintext without telling the user.
---

# Basecamp Integration Skill

## What this covers

- **Basecamp CLI (`bc`)** — the official command-line tool from Basecamp/Hey
- **Basecamp MCP server** — community/serverless MCP wrapper so Hermes can call
  Basecamp tools through the Model Context Protocol

Both are configured in **read-only mode** by default. Full access is a separate
flag the user flips later.

---

## Quick reference

| Tool | What it does | Config path |
|------|-------------|-------------|
| `bc` CLI | List projects, todos, messages, files; create when enabled | `~/.bc/config` or env vars |
| MCP server | Hermes calls Basecamp via MCP tool definitions | Hermes MCP config (JSON/YAML) |

---

## Step 1 — Get your Basecamp API token (read-only scope)

1. Log in to Basecamp at `https://3.basecamp.com` (or your company's domain).
2. Go to **Settings → API Access** (or **Personal Access Tokens**).
3. Create a new token. Give it a name like `Hermes-Read`.
4. **Scopes:** select **read-only** / "View projects, messages, todos" — do NOT
   grant write/create scopes yet.
5. Copy the token. It looks like a long hex string.

> Tokens are shown once. If you lose it, generate a new one.

---

## Step 2 — Install the Basecamp CLI (`bc`)

### Homebrew (macOS / Linux)

```
brew install basecamp/tap/bc
```

### gem (any system with Ruby)

```
gem install basecamp-cli
```

### Verify

```
bc --version
```

Expected: something like `bc 1.x.x`.

---

## Step 3 — Configure `bc` for read-only access

### Option A — interactive (recommended first time)

```
bc configure
```

It will prompt for:

- **Account URL** — your Basecamp domain, e.g. `https://3.basecamp.com` or
  `https://basecamp.com/123456` (the company-specific domain).
- **Access token** — paste the token from Step 1.

This writes `~/.bc/config` (or `~/.config/bc/config.yaml` depending on version).

### Option B — env vars (for headless / Hermes automation)

```
export BASECAMP_ACCOUNT_URL="https://3.basecamp.com"
export BASECAMP_ACCESS_TOKEN="your-token-here"
```

For Hermes, put these in your Hermes config or pass them through the MCP
server's environment (see Step 5).

### Verify read-only connectivity

```
bc projects list
```

You should see your Basecamp projects. If you get `403` or "unauthorized",
the token is missing a read scope — regenerate it with read access.

Other useful read-only commands:

```
bc todos list --project="Project Name"
bc messages list --box="Project Name"
bc file_list --project="Project Name"
```

---

## Step 4 — Hermes skill usage (when user asks about Basecamp)

When the user says something like "what's in my Basecamp project", do this:

1. **Confirm the account domain** if not already known.
2. **Check `bc` is configured:** run `bc projects list` in terminal.
3. **Run the requested read command**, capture output.
4. **Summarize** for the user — do not dump raw JSON unless asked.

If `bc` is not installed or not configured, guide the user through Steps 2-3
above. Do NOT make up project names or todo items.

---

## Step 5 — MCP server setup (optional, for Hermes-native tool access)

If you want Hermes to call Basecamp as an MCP tool (rather than shelling out to
`bc`), use a Basecamp-compatible MCP server. Two common paths:

### Path A — community MCP server via stdio

Many community MCP servers run as stdio subprocesses. Add to your Hermes MCP
config something like:

```json
{
  "mcpServers": {
    "basecamp": {
      "command": "npx",
      "args": ["-y", "@community/basecamp-mcp-server"],
      "env": {
        "BASECAMP_ACCOUNT_URL": "https://3.basecamp.com",
        "BASECAMP_ACCESS_TOKEN": "your-read-only-token"
      }
    }
  }
}
```

> Replace `@community/basecamp-mcp-server` with the actual package name once
> you've picked one. Verify it supports read-only operations before trusting
> it with writes.

### Path B — custom lightweight MCP wrapper (Python)

If no maintained package exists, a minimal FastMCP wrapper around `bc` is
straightforward:

```python
# basecamp_mcp.py — minimal read-only MCP wrapper around `bc` CLI
from mcp.server.fastmcp import FastMCP
import subprocess, os, json

mcp = FastMCP("basecamp-readonly")

def run_bc(*args):
    env = os.environ.copy()
    env["BASECAMP_ACCOUNT_URL"] = os.environ["BASECAMP_ACCOUNT_URL"]
    env["BASECAMP_ACCESS_TOKEN"] = os.environ["BASECAMP_ACCESS_TOKEN"]
    result = subprocess.run(["bc"] + list(args), capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"bc failed: {result.stderr}")
    return result.stdout

@mcp.tool()
def list_projects() -> str:
    """List all Basecamp projects (read-only)."""
    return run_bc("projects", "list")

@mcp.tool()
def list_todos(project: str) -> str:
    """List todos for a project (read-only)."""
    return run_bc("todos", "list", "--project", project)

@mcp.tool()
def list_messages(project: str, box: str = "Messages") -> str:
    """List recent messages in a project box (read-only)."""
    return run_bc("messages", "list", "--project", project, "--box", box)
```

Run it:

```
BASECAMP_ACCOUNT_URL=... BASECAMP_ACCESS_TOKEN=... python basecamp_mcp.py
```

Then point Hermes' MCP config at that stdio process.

> **Read-only guarantee:** this wrapper only exposes `list`-style commands.
> Write/create tools are deliberately omitted. Add them later when the user
> grants full access.

---

## Step 6 — Verify everything works

Run this checklist:

```
# 1. bc CLI installed
bc --version

# 2. bc can read
bc projects list | head -5

# 3. (if using MCP) MCP server starts and exposes tools
#    Use your MCP client's tool-listing endpoint to confirm
#    "list_projects", "list_todos", "list_messages" appear
```

If any step fails, stop and fix it before claiming success.

---

## Step 7 — Upgrading to full access (future)

When the user is ready for write access:

1. Generate a **new token** with create/edit scopes (or add scopes to the
   existing one if Basecamp supports scope expansion).
2. Update `~/.bc/config` or the env var with the new token.
3. Verify write access with a safe, reversible operation:
   ```
   bc todos create --project="Test Project" --content="Hermes write-access test"
   bc todos complete <id>   # clean up after
   ```
4. Add the write tools to the MCP wrapper (if using one).
5. Tell the user exactly what write capabilities are now enabled.

---

## Security notes

- **Never commit tokens** to git, skills, or config files that go into version
  control. Use env vars or a secret store.
- **Read-only tokens** are safer to store long-term than write tokens.
- If a token is exposed, **rotate it immediately** from Basecamp settings.
- Prefer the read-only token in any MCP server env config.
- When in doubt, run `bc` commands yourself first and paste the output to
  Hermes — that's zero-configuration and always works.
