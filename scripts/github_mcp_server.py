#!/usr/bin/env python3
"""
Minimal GitHub MCP Server — stdio transport
Wraps GitHub REST API as MCP tools for Hermes Agent.

Usage: python3 github_mcp_server.py

Configured via environment variable:
    GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_...

Provides tools:
    - github_status        — Check GitHub API connectivity and auth
    - github_get_repo      — Get repository metadata
    - github_list_branches — List repository branches
    - github_list_commits  — List commits on a branch
    - github_get_commit    — Get a single commit with stats and files
    - github_get_contents  — List/get repository contents
    - github_create_issue  — Create an issue
    - github_list_issues   — List issues
    - github_create_pull_request — Create a pull request
    - github_push_commit   — Create a commit and push via Git Data API
"""

import os, sys, json, base64, urllib.request, urllib.error, traceback
from pathlib import Path

# ── Logging ───────────────────────────────────────────────────────────
DEBUG = os.environ.get("GITHUB_MCP_DEBUG", "0") == "1"

def log(msg):
    if DEBUG:
        sys.stderr.write(f"[GITHUB-MCP] {msg}\n")
        sys.stderr.flush()

# ── MCP Stdio Protocol ───────────────────────────────────────────────
def read_jsonrpc():
    """Read one JSON-RPC message from stdin."""
    raw = sys.stdin.readline()
    if not raw:
        return None
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        log(f"Failed to parse JSON-RPC: {e} — raw: {raw[:200]}")
        return None

def write_jsonrpc(response):
    """Write one JSON-RPC response to stdout."""
    out = json.dumps(response) + "\n"
    sys.stdout.write(out)
    sys.stdout.flush()
    log(f"→ {response.get('method', 'response')}, id={response.get('id', '?')}")

# ── GitHub API Helper ────────────────────────────────────────────────
PAT = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
API = "https://api.github.com"

def gh_get(path, params=None):
    """GET a GitHub API endpoint."""
    url = f"{API}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {PAT}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "Hermes-GitHub-MCP/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        log(f"  GH API GET {path} → HTTP {e.code}: {body}")
        return {"error": e.code, "body": body}
    except Exception as e:
        log(f"  GH API GET {path} → Exception: {e}")
        return {"error": str(e)}

def gh_post(path, data=None, method="POST"):
    """POST/PATCH a GitHub API endpoint."""
    url = f"{API}{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"token {PAT}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "Hermes-GitHub-MCP/1.0")
    if data is not None:
        data_bytes = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
        req.data = data_bytes
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        log(f"  GH API {method} {path} → HTTP {e.code}: {body}")
        return {"error": e.code, "body": body}
    except Exception as e:
        log(f"  GH API {method} {path} → Exception: {e}")
        return {"error": str(e)}

# ── Tool Definitions ─────────────────────────────────────────────────

TOOLS = [
    {
        "name": "github_status",
        "description": "Check GitHub API connectivity and authentication status",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "github_get_repo",
        "description": "Get repository metadata (name, owner, default branch, etc.)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner (e.g. Mahesh-2701)"},
                "repo": {"type": "string", "description": "Repository name (e.g. Hermes_Agent)"},
            },
            "required": ["owner", "repo"],
        },
    },
    {
        "name": "github_list_branches",
        "description": "List branches in a repository",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
            },
            "required": ["owner", "repo"],
        },
    },
    {
        "name": "github_list_commits",
        "description": "List recent commits on a branch",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "sha": {"type": "string", "description": "Branch name or commit SHA (optional)"},
                "per_page": {"type": "integer", "default": 20},
            },
            "required": ["owner", "repo"],
        },
    },
    {
        "name": "github_get_commit",
        "description": "Get a single commit with full stats, files changed, and patch",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "sha": {"type": "string", "description": "Commit SHA or branch/tag name"},
            },
            "required": ["owner", "repo", "sha"],
        },
    },
    {
        "name": "github_get_contents",
        "description": "List or get repository contents (files, directories)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "path": {"type": "string", "description": "Path inside repo (optional, defaults to root)"},
                "sha": {"type": "string", "description": "Branch/tag/commit SHA (optional)"},
            },
            "required": ["owner", "repo"],
        },
    },
    {
        "name": "github_create_issue",
        "description": "Create a new issue in a repository",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "title": {"type": "string"},
                "body": {"type": "string", "description": "Issue body (optional)"},
                "labels": {"type": "array", "items": {"type": "string"}, "description": "Label names (optional)"},
            },
            "required": ["owner", "repo", "title"],
        },
    },
    {
        "name": "github_list_issues",
        "description": "List open issues in a repository",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "state": {"type": "string", "default": "open", "description": "open, closed, or all"},
                "per_page": {"type": "integer", "default": 20},
            },
            "required": ["owner", "repo"],
        },
    },
    {
        "name": "github_create_pull_request",
        "description": "Create a pull request",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "title": {"type": "string"},
                "body": {"type": "string", "description": "PR description (optional)"},
                "head": {"type": "string", "description": "Branch name to merge from"},
                "base": {"type": "string", "description": "Branch name to merge into (default: main/master)"},
            },
            "required": ["owner", "repo", "title", "head"],
        },
    },
    {
        "name": "github_push_commit",
        "description": "Create a commit and push to a branch via the Git Data API",
        "inputSchema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "repo": {"type": "string"},
                "branch": {"type": "string", "description": "Branch to push to"},
                "message": {"type": "string", "description": "Commit message"},
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path in repo"},
                            "content": {"type": "string", "description": "File content (string)"},
                            "sha": {"type": "string", "description": "Existing blob SHA for updates (optional)"},
                        },
                        "required": ["path", "content"],
                    },
                },
            },
            "required": ["owner", "repo", "branch", "message", "files"],
        },
    },
]

# ── Tool Implementations ─────────────────────────────────────────────

def tool_status(params):
    log("→ github_status")
    if not PAT:
        return {"content": [{"type": "text", "text": "ERROR: GITHUB_PERSONAL_ACCESS_TOKEN not set in environment"}], "isError": True}
    
    repo = gh_get("/repos/Mahesh-2701/Hermes_Agent")
    if "error" in repo:
        detail = f"API error: {repo['error']}"
    else:
        detail = f"{repo.get('full_name')} (private={repo.get('private')}, default_branch={repo.get('default_branch')})"
    
    user = gh_get("/user")
    username = user.get("login", "?") if "error" not in user else "?"
    
    return {
        "content": [{"type": "text", "text": f"GitHub MCP Status:\n- Auth: {'OK' if PAT else 'MISSING'} (PAT length={len(PAT) if PAT else 0})\n- User: {username}\n- Repo: {detail}\n- API: reachable"}],
    }

def tool_get_repo(params):
    log(f"→ github_get_repo: {params.get('owner')}/{params.get('repo')}")
    result = gh_get(f"/repos/{params['owner']}/{params['repo']}")
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']} — {result.get('body', '')}"}], "isError": True}
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

def tool_list_branches(params):
    log(f"→ github_list_branches: {params['owner']}/{params['repo']}")
    result = gh_get(f"/repos/{params['owner']}/{params['repo']}/branches")
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']}"}], "isError": True}
    branches = [b["name"] for b in result]
    return {"content": [{"type": "text", "text": f"Branches in {params['owner']}/{params['repo']}:\n" + "\n".join(f"  - {b}" for b in branches)}]}

def tool_list_commits(params):
    log(f"→ github_list_commits: {params['owner']}/{params['repo']}")
    sha = params.get("sha", "")
    per_page = params.get("per_page", 20)
    path = f"/repos/{params['owner']}/{params['repo']}/commits"
    if sha:
        path += f"?sha={sha}&per_page={per_page}"
    else:
        path += f"?per_page={per_page}"
    result = gh_get(path)
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']}"}], "isError": True}
    if not result:
        return {"content": [{"type": "text", "text": "No commits found"}]}
    lines = []
    for c in result:
        sha_short = c["sha"][:8]
        msg = c["commit"]["message"].split("\n")[0][:80]
        date = c["commit"]["author"]["date"][:10]
        lines.append(f"  {sha_short}  {date}  {msg}")
    return {"content": [{"type": "text", "text": f"Recent commits in {params['owner']}/{params['repo']}:\n" + "\n".join(lines)}]}

def tool_get_commit(params):
    log(f"→ github_get_commit: {params['owner']}/{params['repo']}@{params['sha']}")
    result = gh_get(f"/repos/{params['owner']}/{params['repo']}/commits/{params['sha']}")
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']} — {result.get('body', '')}"}], "isError": True}
    c = result.get("commit", {})
    stats = result.get("stats", {})
    files = result.get("files", [])
    lines = [
        f"Commit: {c.get('sha', '?')[:16]}",
        f"Message: {c.get('message', '?').split(chr(10))[0][:100]}",
        f"Author: {c.get('author', {}).get('name', '?')} <{c.get('author', {}).get('email', '?')}>",
        f"Date: {c.get('author', {}).get('date', '?')}",
        f"",
        f"Stats: {stats.get('total', '?')} files changed, {stats.get('additions', '?')} additions, {stats.get('deletions', '?')} deletions",
        f"",
        f"Files ({len(files)}):",
    ]
    for f in files[:30]:
        lines.append(f"  {f['status']:7s} {f['filename']} ({f.get('size', '?')} bytes)")
    if len(files) > 30:
        lines.append(f"  ... +{len(files)-30} more files")
    return {"content": [{"type": "text", "text": "\n".join(lines)}]}

def tool_get_contents(params):
    log(f"→ github_get_contents: {params['owner']}/{params['repo']}/{params.get('path', '/')}")
    owner = params["owner"]
    repo = params["repo"]
    path = params.get("path", "")
    sha = params.get("sha", "")
    url = f"/repos/{owner}/{repo}/contents/{path}" if path else f"/repos/{owner}/{repo}/contents/"
    if sha:
        url += f"?ref={sha}"
    result = gh_get(url)
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']} — {result.get('body', '')}"}], "isError": True}
    if isinstance(result, list):
        lines = []
        for item in result:
            kind = "📁" if item["type"] == "dir" else "📄"
            size = f" ({item.get('size', 0)/1024:.1f} KB)" if item.get("size") else ""
            lines.append(f"  {kind} {item['name']}{size}")
        return {"content": [{"type": "text", "text": f"Contents of {owner}/{repo}/{path or '/'}:\n" + "\n".join(lines)}]}
    else:
        content = base64.b64decode(result.get("content", "")).decode(errors="replace")
        preview = content[:500] + ("..." if len(content) > 500 else "")
        return {"content": [{"type": "text", "text": f"File: {owner}/{repo}/{path}\nSize: {result.get('size', 0)} bytes\n\n--- Content (first 500 chars) ---\n{preview}"}]}

def tool_create_issue(params):
    log(f"→ github_create_issue: {params['owner']}/{params['repo']}")
    result = gh_post(f"/repos/{params['owner']}/{params['repo']}/issues", data={
        "title": params["title"],
        "body": params.get("body", ""),
        "labels": params.get("labels", []),
    })
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']} — {result.get('body', '')}"}], "isError": True}
    return {"content": [{"type": "text", "text": f"Issue created:\n- Number: #{result.get('number')}\n- Title: {result.get('title')}\n- URL: {result.get('html_url')}\n- State: {result.get('state')}"}]}

def tool_list_issues(params):
    log(f"→ github_list_issues: {params['owner']}/{params['repo']}")
    result = gh_get(f"/repos/{params['owner']}/{params['repo']}/issues?state={params.get('state', 'open')}&per_page={params.get('per_page', 20)}")
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']}"}], "isError": True}
    if not result:
        return {"content": [{"type": "text", "text": "No issues found"}]}
    lines = []
    for issue in result:
        labels = ", ".join([l["name"] for l in issue.get("labels", [])]) or "none"
        lines.append(f"  #{issue['number']:4d} [{labels}] {issue['title']} (opened {issue['created_at'][:10]})")
    return {"content": [{"type": "text", "text": f"Issues in {params['owner']}/{params['repo']} (state={params.get('state', 'open')}):\n" + "\n".join(lines)}]}

def tool_create_pull_request(params):
    log(f"→ github_create_pull_request: {params['owner']}/{params['repo']}")
    result = gh_post(f"/repos/{params['owner']}/{params['repo']}/pulls", data={
        "title": params["title"],
        "body": params.get("body", ""),
        "head": params["head"],
        "base": params.get("base", "main"),
    })
    if "error" in result:
        return {"content": [{"type": "text", "text": f"Error: {result['error']} — {result.get('body', '')}"}], "isError": True}
    return {"content": [{"type": "text", "text": f"Pull request created:\n- Number: #{result.get('number')}\n- Title: {result.get('title')}\n- URL: {result.get('html_url')}\n- State: {result.get('state')}\n- Head: {result.get('head', {}).get('ref', '?')}\n- Base: {result.get('base', {}).get('ref', '?')}"}]}

def tool_push_commit(params):
    log(f"→ github_push_commit: {params['owner']}/{params['repo']}:{params['branch']}")
    owner, repo, branch = params["owner"], params["repo"], params["branch"]
    message = params["message"]
    files = params["files"]
    
    # Step 1: Get current branch SHA
    ref_result = gh_get(f"/repos/{owner}/{repo}/git/refs/heads/{branch}")
    if "error" in ref_result:
        return {"content": [{"type": "text", "text": f"Error getting branch ref: {ref_result['error']} — {ref_result.get('body', '')}"}], "isError": True}
    
    parent_sha = ref_result["object"]["sha"]
    
    # Step 2: Create blobs for each file
    blobs = {}
    for f in files:
        content = f["content"]
        if isinstance(content, str):
            content = content.encode()
        encoded = base64.b64encode(content).decode()
        blob_result = gh_post(f"/repos/{owner}/{repo}/git/blobs", data={"content": encoded, "encoding": "base64"})
        if "error" in blob_result:
            return {"content": [{"type": "text", "text": f"Error creating blob for {f['path']}: {blob_result['error']}"}], "isError": True}
        blobs[f["path"]] = {"sha": blob_result["sha"], "mode": "100644"}
    
    # Step 3: Create tree
    tree_entries = []
    for f in files:
        tree_entries.append({"path": f["path"], "mode": "100644", "type": "blob", "sha": blobs[f["path"]]["sha"]})
    
    tree_result = gh_post(f"/repos/{owner}/{repo}/git/trees", data={"tree": tree_entries, "base_tree": parent_sha})
    if "error" in tree_result:
        return {"content": [{"type": "text", "text": f"Error creating tree: {tree_result['error']} — {tree_result.get('body', '')}"}], "isError": True}
    
    tree_sha = tree_result["sha"]
    
    # Step 4: Create commit
    commit_result = gh_post(f"/repos/{owner}/{repo}/git/commits", data={
        "message": message, "tree": tree_sha, "parents": [parent_sha],
    })
    if "error" in commit_result:
        return {"content": [{"type": "text", "text": f"Error creating commit: {commit_result['error']} — {commit_result.get('body', '')}"}], "isError": True}
    
    commit_sha = commit_result["sha"]
    
    # Step 5: Update ref
    ref_result = gh_post(f"/repos/{owner}/{repo}/git/refs/heads/{branch}", data={"sha": commit_sha, "force": True})
    if "error" in ref_result:
        return {"content": [{"type": "text", "text": f"Error updating ref: {ref_result['error']} — {ref_result.get('body', '')}"}], "isError": True}
    
    return {"content": [{"type": "text", "text": f"Commit pushed to {owner}/{repo}:{branch}\n- Commit SHA: {commit_sha[:16]}\n- Message: {message}\n- Files: {len(files)}"}]}

# ── Tool Dispatch ────────────────────────────────────────────────────

TOOL_HANDLERS = {
    "github_status": tool_status,
    "github_get_repo": tool_get_repo,
    "github_list_branches": tool_list_branches,
    "github_list_commits": tool_list_commits,
    "github_get_commit": tool_get_commit,
    "github_get_contents": tool_get_contents,
    "github_create_issue": tool_create_issue,
    "github_list_issues": tool_list_issues,
    "github_create_pull_request": tool_create_pull_request,
    "github_push_commit": tool_push_commit,
}

# ── MCP Method Handlers ──────────────────────────────────────────────

def handle_initialize(msg):
    """MCP initialize — respond with protocol info and capabilities."""
    log(f"→ initialize from {msg.get('params', {}).get('clientInfo', {})}")
    write_jsonrpc({
        "jsonrpc": "2.0",
        "id": msg.get("id"),
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"tools": TOOLS},
            },
            "serverInfo": {
                "name": "github-mcp-server",
                "version": "1.0.0",
            },
        },
    })

def handle_tools_list(msg):
    """MCP tools/list — return the tool list."""
    log("→ tools/list")
    write_jsonrpc({
        "jsonrpc": "2.0",
        "id": msg.get("id"),
        "result": {"tools": TOOLS},
    })

def handle_tools_call(msg):
    """MCP tools/call — invoke a tool."""
    params = msg.get("params", {})
    tool_name = params.get("name", "")
    tool_args = params.get("arguments", {})
    log(f"→ tools/call: {tool_name} args={json.dumps(tool_args)[:200]}")
    
    handler = TOOL_HANDLERS.get(tool_name)
    if handler is None:
        log(f"  Unknown tool: {tool_name}")
        write_jsonrpc({
            "jsonrpc": "2.0",
            "id": msg.get("id"),
            "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
        })
        return
    
    try:
        result = handler(tool_args)
        write_jsonrpc({
            "jsonrpc": "2.0",
            "id": msg.get("id"),
            "result": result,
        })
    except Exception as e:
        log(f"  Tool error: {e}\n{traceback.format_exc()}")
        write_jsonrpc({
            "jsonrpc": "2.0",
            "id": msg.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
        })

def handle_ping(msg):
    """MCP ping — respond with pong."""
    log("→ ping")
    write_jsonrpc({
        "jsonrpc": "2.0",
        "id": msg.get("id"),
        "result": True,
    })

# ── Main Loop ────────────────────────────────────────────────────────

METHOD_HANDLERS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
    "ping": handle_ping,
}

def main():
    log("GitHub MCP Server starting...")
    log(f"PAT length: {len(PAT) if PAT else 0}")
    log(f"Tools registered: {len(TOOLS)}")
    
    # Send initialize result immediately (some clients expect this)
    write_jsonrpc({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"tools": TOOLS},
            },
            "serverInfo": {"name": "github-mcp-server", "version": "1.0.0"},
        },
    })
    
    # Send initialized notification
    write_jsonrpc({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    })
    
    log("Server ready, waiting for requests...")
    
    while True:
        msg = read_jsonrpc()
        if msg is None:
            log("stdin closed, exiting")
            break
        
        method = msg.get("method", "")
        log(f"← {method} id={msg.get('id', '?')}")
        
        handler = METHOD_HANDLERS.get(method)
        if handler:
            try:
                handler(msg)
            except Exception as e:
                log(f"Error handling {method}: {e}\n{traceback.format_exc()}")
                write_jsonrpc({
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                })
        else:
            log(f"Unknown method: {method}")
            write_jsonrpc({
                "jsonrpc": "2.0",
                "id": msg.get("id"),
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            })

if __name__ == "__main__":
    main()
