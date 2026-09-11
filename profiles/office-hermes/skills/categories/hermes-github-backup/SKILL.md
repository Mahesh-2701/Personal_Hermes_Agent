# Hermes Agent GitHub Backup Skill

Use when backing up, validating, exporting, syncing, or restoring the Hermes Agent configuration to/from a GitHub repository.

## Setup (one-time)

1. Set the GitHub PAT as an environment variable before running any GitHub operation:

   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="your-pat-here"
   ```

   On macOS with Hermes, the PAT is persisted in:

   ```
   ~/.hermes/mcp-tokens/github_pat.env
   ```

   Load it before operations:

   ```bash
   set -a; source ~/.hermes/mcp-tokens/github_pat.env; set +a
   ```

2. Clone or initialize the backup repository:

   ```bash
   git clone https://github.com/Mahesh-2701/Hermes_Agent.git ~/.hermes_backup
   ```

   Or, if already cloned:

   ```bash
   cd ~/.hermes_backup
   ```

3. The default repository for this workflow is:

   ```
   Mahesh-2701/Hermes_Agent
   ```

   Override with `HERMES_BACKUP_REPO` environment variable if needed.

## Available Commands

### export

Export the current Hermes configuration to a local staging directory (`~/.hermes_export`), ready for validation and commit.

What gets exported:

- `config.yaml` (sanitized — secrets redacted)
- All skills (`skills/**/*`)
- Profiles (`profiles/**/*` — excluding state databases, audio/image caches, live tokens)
- Memory (`memories/MEMORY.md`, `memories/USER.md`)
- Cron jobs (`cron/jobs.json` — sanitized)
- MCP configuration (from `config.yaml` — sanitized)
- `.env.example` (variable names only, no values)
- Auth structure (metadata only, no tokens)
- Scripts (`scripts/**/*`)
- Manifests and documentation

Secrets are ALWAYS redacted. Files containing live tokens are excluded or sanitized.

Usage:

```bash
# From the backup repo root:
./scripts/export.sh

# Or via skill invocation through Hermes
```

### validate

Validate the exported staging directory before any Git operation.

Checks performed:

- Required files present (manifest.json, config.yaml, skills/, profiles/, memory/, cron/)
- YAML/JSON syntax validity
- No secrets in any file (scans for API keys, tokens, passwords, OAuth creds, service account JSON, .env with values)
- Skill structure validity (each skill has SKILL.md)
- Profile structure validity
- Cron job structure validity
- .gitignore covers all secret patterns

If secrets are detected, validation FAILS and lists the offending files. Do not proceed to commit until secrets are removed.

Usage:

```bash
./scripts/validate.sh
```

### status

Show the current state of the backup repository and Hermes configuration.

Displays:

- Current branch
- Last backup commit (hash, message, date)
- Uncommitted changes (git status)
- Hermes config version
- Skill count
- Profile count
- Cron job count
- MCP server count
- Last export timestamp

Usage:

```bash
./scripts/status.sh
```

### diff

Compare current Hermes state against the Git repository.

Shows:

- Files added (in Hermes, not in Git)
- Files modified (different from Git version)
- Files deleted (in Git, not in Hermes)
- Summary counts by category (skills, profiles, memory, cron, config, mcp)

Does NOT push. Purely informational.

Usage:

```bash
./scripts/diff.sh
```

### sync

Full synchronization workflow: export → sanitize → validate → manifest → review → commit → push.

Workflow steps:

1. Run export to staging
2. Run secret sanitization pass
3. Run validation (fails fast on secrets)
4. Generate manifest.json
5. Show diff summary
6. ASK FOR EXPLICIT APPROVAL before any Git write
7. On approval: create branch (if needed), commit, push
8. Verify remote

Never pushes without explicit approval. Never pushes secrets.

Usage:

```bash
./scripts/sync.sh
```

On approval prompt, type `yes` to proceed or `no` to cancel.

### restore

Restore Hermes configuration from the repository to a target directory.

Safety rules:

- NEVER restore secrets from Git
- NEVER overwrite existing credentials with repository values
- ALWAYS show what will change before applying
- ALWAYS validate the target Hermes version compatibility
- ALWAYS detect missing dependencies
- ALWAYS detect required environment variables
- ALWAYS detect conflicts with existing configuration

Usage:

```bash
./scripts/restore.sh [--target /path/to/hermes] [--dry-run]
```

`--dry-run` shows what would change without applying anything.

## Secret Protection

### What is NEVER exported

- `GITHUB_PERSONAL_ACCESS_TOKEN` (and any PAT)
- OAuth access tokens
- OAuth refresh tokens
- Client secrets
- API keys with actual values
- Service account JSON files
- `.env` files with values
- `auth.json` token values
- `mcp-tokens/*.json` token values
- `google_token.json`
- `google_client_secret.json`
- Any file matching patterns in `.gitignore`

### .gitignore patterns

The repository `.gitignore` must include:

```gitignore
# Secrets
*.env
*.env.*
.env.*
mcp-tokens/*.json
mcp-tokens/*.client.json
auth.json
google_token.json
google_client_secret.json
*.secret
*.key
*.pem
*.p12
*.pfx

# Hermes runtime state (not configuration)
*.db
*.db-shm
*.db-wal
*.lock
*.sock
*.pid
*.heartbeat
*.etag
*.meta.json
cache/
audio_cache/
image_cache/
logs/
state.db
state/
runtime/
sessions/
pastes/
pending_messages/
terminal-sessions/
verification_evidence.db
processes.json
spawn-ledger.json
gateway*.json
gateway*.log
gateway*.lock
gateway*.pid
gateway*.sock
.fire-*.lock
.jobs.lock
.tick.lock
usage_audit.jsonl
notepad.db
output/

# OS files
.DS_Store
Thumbs.db
```

### SECRETS.example.env

Contains only variable names, no values:

```bash
# GitHub
GITHUB_PERSONAL_ACCESS_TOKEN=

# Google OAuth (client ID is safe, client_secret is NOT)
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=

# Other integrations as needed
FIREWORKS_API_KEY=
OPENROUTER_API_KEY=
```

### Security model

- The PAT lives ONLY in `mcp-tokens/github_pat.env` (chmod 600) and the environment
- The PAT is NEVER written to config.yaml
- The PAT is NEVER written to any skill
- The PAT is NEVER committed to Git
- The PAT is NEVER printed in logs or output
- Export always redacts secrets before writing to staging
- Validation fails if any secret is detected in staging
- Restore never writes secrets to the target

## Required Environment Variables

For a full restore on a new machine, the following are needed:

```bash
# Required for GitHub MCP and sync operations
GITHUB_PERSONAL_ACCESS_TOKEN=

# Required for Google Workspace MCP (OAuth flow will prompt)
# Client ID is in config.yaml — safe to export
# Client secret is in google_client_secret.json — NOT exported

# Required for Nous inference (OAuth flow will prompt)
# No env var needed — Hermes handles OAuth

# Optional — for secondary providers
FIREWORKS_API_KEY=
OPENROUTER_API_KEY=
```

## Restore Requirements

- Same or compatible Hermes version (check `hermes-setup --version` or `gateway_state.json` `code_version`)
- Node.js 20+ (for npx-based MCP servers)
- Git 2.x
- Python 3.10+ (for scripts)
- Network access to GitHub and configured MCP endpoints
- OAuth re-authorization for Google services, Notion, Canva, Figma, Hugging Face, Postman

## Migration to Another Machine

1. Install Hermes Agent on the target machine
2. Clone this repository:
   ```bash
   git clone https://github.com/Mahesh-2701/Hermes_Agent.git ~/.hermes_backup
   cd ~/.hermes_backup
   ```
3. Set required environment variables (PAT, API keys)
4. Run restore:
   ```bash
   ./scripts/restore.sh --target ~/.hermes --dry-run
   ```
5. Review the dry-run output
6. Run restore for real:
   ```bash
   ./scripts/restore.sh --target ~/.hermes
   ```
7. Re-authorize OAuth flows for Google services and other integrations
8. Verify cron jobs, skills, and profiles are intact
9. Start the gateway:
   ```bash
   hermes gateway run
   ```

## Architecture

```
~/.hermes/                          # Live Hermes installation
├── config.yaml                     # Main configuration (MCP servers, model, runtime)
├── skills/                         # 59 skills across 12 categories
├── profiles/                       # 4 profiles (ceo, default, designer, tester)
├── memories/                       # MEMORY.md + USER.md
├── cron/                           # cron/jobs.json + executions.db
├── mcp-tokens/                    # OAuth tokens (NEVER exported)
├── auth.json                      # OAuth auth state (NEVER exported)
├── scripts/                        # Custom scripts (ai_news_aggregator.py)
├── gateway_state.json             # Gateway runtime state
├── channel_directory.json         # Platform channel registry
└── .env                           # Environment variables (NEVER exported with values)

~/.hermes_backup/                   # Git repository (this repo)
├── skills/                         # Exported skills
├── profiles/                       # Exported profiles (sanitized)
├── memory/                         # Exported memory
├── cron/                          # Exported cron schedules
├── config/                        # Exported config.yaml (sanitized)
├── mcp/                           # MCP configuration (sanitized)
├── scripts/                       # export.sh, validate.sh, restore.sh, status.sh, diff.sh, sync.sh
├── manifest.json                  # Machine-readable manifest
├── .gitignore                     # Secret + runtime exclusion patterns
├── SECRETS.example.env            # Variable names only
├── SECURITY.md                    # Security policy
├── README.md                      # Documentation
└── docs/
    └── architecture.md            # Architecture reference
```

## Files

### scripts/export.sh

Exports Hermes configuration to `~/.hermes_export/`. Sanitizes secrets. Generates manifest.

### scripts/validate.sh

Validates the export in `~/.hermes_export/`. Scans for secrets. Checks structure. Returns non-zero on failure.

### scripts/status.sh

Shows Git status, last commit, Hermes config summary.

### scripts/diff.sh

Shows diff between live Hermes and Git repository.

### scripts/sync.sh

Full sync workflow with approval gate.

### scripts/restore.sh

Restores from repository to target directory with safety checks.

## GitHub MCP Server

This skill integrates with the official GitHub MCP server:

```
https://github.com/github/github-mcp-server
```

The MCP server is configured in `config.yaml` under `mcp_servers.github` and uses the PAT from the environment variable `GITHUB_PERSONAL_ACCESS_TOKEN`.

For operations that use the MCP server directly (push, PR creation, branch management), the skill delegates to the MCP tools. For file-level operations (export, validate, diff), it uses Git CLI directly.

## Approval Gate

ALL GitHub write operations require explicit user approval:

- `git commit`
- `git push`
- `git branch -D`
- Pull request creation
- Repository settings changes

Read-only operations (clone, fetch, status, diff) do not require approval.

The sync workflow always stops at the approval gate and shows:

- Repository
- Branch
- Files to commit (added/modified/deleted)
- Skills exported
- MCP servers exported
- Profiles exported
- Memory components exported
- Cron jobs exported
- Secrets detected
- Secrets removed
- Commit message

Then asks:

```
Do you approve committing and pushing this Hermes export to GitHub?
```

Only `yes` proceeds.
