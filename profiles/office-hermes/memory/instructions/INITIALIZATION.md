# INITIALIZATION.md

**Office Hermes Memory System Setup Guide**

Version: 1.0.0 | Updated: 2026-09-11

---

## Overview

This guide walks you through initializing the memory system for Office Hermes. The memory system provides persistent context across sessions via three components:

1. **MEMORY.md** — Agent's personal notes (~2,200 chars, ~800 tokens)
2. **USER.md** — User profile (~1,375 chars, ~500 tokens)
3. **OFFICE_CONTEXT.md** — Organization-wide policies (shared, unlimited)

---

## Pre-Deployment Checklist

Before bringing Hermes online, ensure:

- [ ] Organization policy review (security, compliance, data classification)
- [ ] Team identified who will maintain OFFICE_CONTEXT.md (usually Governance/Security)
- [ ] USER profiles drafted for each Hermes deployment (if multi-user)
- [ ] Hermes home directory prepared (`~/.hermes/`)
- [ ] Config file (config.yaml) created with memory settings
- [ ] Backup strategy defined (memory files are critical)
- [ ] Audit logging configured (compliance requirement)

---

## Quick Start (Single User / Small Team)

### Step 1: Create Hermes Home & Memory Directory

```bash
mkdir -p ~/.hermes/memories
chmod 700 ~/.hermes ~/.hermes/memories
```

### Step 2: Copy Templates to ~/.hermes/memories

```bash
# Copy portable templates (rename to remove _TEMPLATE)
cp ~/office-hermes-export/memory/templates/USER_TEMPLATE.md ~/.hermes/memories/USER.md
cp ~/office-hermes-export/memory/templates/MEMORY_TEMPLATE.md ~/.hermes/memories/MEMORY.md
cp ~/office-hermes-export/memory/templates/OFFICE_CONTEXT_TEMPLATE.md ~/.hermes/memories/OFFICE_CONTEXT.md
```

### Step 3: Customize USER.md

Edit `~/.hermes/memories/USER.md`:

```markdown
# Replace these placeholders with your organization context:

- **User Identifier:** engineering_team
- **Role in Organization:** developer
- **Team/Department:** Backend Engineering
- **Timezone:** UTC
- **Primary Languages:** Python, TypeScript
- **Experience Level:** senior
- **Verbosity:** concise
- ...
```

**Key:** Remove ALL personal identifiers. Use generic role/team names.

### Step 4: Customize MEMORY.md

Leave mostly empty initially. The agent will populate this as it learns:

```markdown
Office runs Ubuntu 22.04 LTS; dev server at 10.0.1.50. PostgreSQL 16, Redis 7.x.
§
Main repo: ~/src/product-api (Go 1.22). Tests: make test. CI: GitHub Actions.
§
...
```

### Step 5: Initialize OFFICE_CONTEXT.md

Edit `~/.hermes/memories/OFFICE_CONTEXT.md` with your organization's:
- Infrastructure standards
- Security policies
- Code review requirements
- Release procedures
- On-call & escalation contacts

**Critical:** This is the single source of truth. Ensure stakeholder sign-off.

### Step 6: Configure config.yaml

Add to `~/.hermes/config.yaml`:

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200        # Standard
  user_char_limit: 1375          # Standard
  write_approval: true            # RECOMMENDED for office
  retention_policy: "office"
  audit_logging: true
  privacy_enforcement: true

display:
  memory_notifications: on        # Get updates when agent learns
```

### Step 7: Verify Setup

```bash
# Check file permissions (should be readable/writable by user only)
ls -la ~/.hermes/memories/

# Verify Hermes loads memories at startup
hermes status memory
```

### Step 8: Initial Session

Start Hermes:

```bash
hermes chat
```

You should see in the system prompt:

```
══════════════════════════════════════════════════════════════
MEMORY (your personal notes) [45% — 990/2,200 chars]
══════════════════════════════════════════════════════════════
[Your memory entries here, separated by §]

══════════════════════════════════════════════════════════════
USER PROFILE [62% — 855/1,375 chars]
══════════════════════════════════════════════════════════════
[Your profile entries]
```

If you see this, memory is loaded and ready!

---

## Multi-User / Multi-Deployment Setup

For organizations deploying Hermes to multiple users or teams:

### Architecture Overview

```
~/.hermes/config.yaml (main config)
~/.hermes/memories/
  ├── OFFICE_CONTEXT.md (SHARED — all agents read)
  └── USER.md / MEMORY.md (PER-USER or PER-PROFILE)

~/.hermes/profiles/
  ├── default/
  │   └── config.yaml (inherits main config)
  ├── team_a/
  │   ├── config.yaml (team-specific overrides)
  │   └── memories/ (team's own MEMORY.md, USER.md)
  └── team_b/
      ├── config.yaml
      └── memories/
```

### Step 1: Create Multi-Profile Setup

```bash
mkdir -p ~/.hermes/profiles/{default,team_a,team_b}
mkdir -p ~/.hermes/profiles/team_a/memories
mkdir -p ~/.hermes/profiles/team_b/memories
```

### Step 2: Central OFFICE_CONTEXT.md

Create ONE shared `~/.hermes/memories/OFFICE_CONTEXT.md` (at Hermes root level, not in profiles).

All agents read this. Modify only with governance approval.

```bash
cp ~/office-hermes-export/memory/templates/OFFICE_CONTEXT_TEMPLATE.md \
   ~/.hermes/memories/OFFICE_CONTEXT.md
```

### Step 3: Per-Profile USER.md & MEMORY.md

Each profile (or user) gets its own memories:

```bash
# Team A
cp ~/office-hermes-export/memory/templates/USER_TEMPLATE.md \
   ~/.hermes/profiles/team_a/memories/USER.md
cp ~/office-hermes-export/memory/templates/MEMORY_TEMPLATE.md \
   ~/.hermes/profiles/team_a/memories/MEMORY.md

# Team B
cp ~/office-hermes-export/memory/templates/USER_TEMPLATE.md \
   ~/.hermes/profiles/team_b/memories/USER.md
cp ~/office-hermes-export/memory/templates/MEMORY_TEMPLATE.md \
   ~/.hermes/profiles/team_b/memories/MEMORY.md
```

### Step 4: Profile-Specific config.yaml

Each profile inherits main config but can override:

```bash
# ~/.hermes/profiles/team_a/config.yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  write_approval: true              # Gate writes for team_a
  audit_logging: true
  retention_policy: "office"

agent:
  model: "claude-3-5-sonnet"        # Different model for this team
  
# Inherits everything else from ~/.hermes/config.yaml
```

### Step 5: Deploy Per-Profile

Start agents on different profiles:

```bash
# Main Hermes (default profile)
hermes chat

# Team A deployment
HERMES_PROFILE=team_a hermes chat

# Team B deployment
HERMES_PROFILE=team_b hermes chat
```

---

## Data Format & Validation

### MEMORY.md Format

- **Delimiter:** § (section sign, U+00A7)
- **Char Limit:** 2,200 max
- **Entry Structure:** Freeform text, one entry per section
- **Metadata:** Optional — can track creation/update dates as comments

Example:

```markdown
# Agent's personal notes (2,200 char limit)

Environment: Ubuntu 22.04, PostgreSQL 16, Redis 7.x. Docker & Podman installed.
§
Project: ~/src/api (Go 1.22, chi router, sqlc). Tests: make test.
§
Learned: Avoid UDP multicast on prod network (legacy limitation). Use TCP fallback.
§
```

### USER.md Format

- **Delimiter:** § (section sign)
- **Char Limit:** 1,375 max
- **No Personal Identifiers:** Use role/team names only
- **Structure:** Freeform text, one entry per section

Example:

```markdown
# User profile (1,375 char limit)

Role: Senior Developer, Backend Team. Timezone: UTC.
§
Preferences: Concise responses, code examples appreciated, async-preferred.
§
Tech: Python, TypeScript, Go. Experience: 10+ years. Test-first developer.
§
Workspace: Linux, VS Code, zsh. GitHub Actions CI. Kubernetes deployment.
§
```

### OFFICE_CONTEXT.md Format

- **No Hard Limit** (but keep <15KB for readability)
- **Markdown Structure:** H2/H3 headings, organized sections
- **Approval Required:** Changes should go through governance
- **Version Control:** Store in Git for audit trail

---

## Validation & Testing

### Validate JSON Schemas

Use the provided schemas to validate memory structure:

```bash
# Validate memory entry against schema
python3 << 'EOF'
import json
import jsonschema

# Load schema
with open('~/office-hermes-export/memory/schemas/memory-schema.json') as f:
    schema = json.load(f)

# Load your MEMORY.md as JSON (parse freeform entries)
memory_data = {
  "version": "1.0.0",
  "metadata": {
    "created_at": "2026-09-10T10:00:00Z",
    "last_updated": "2026-09-11T15:30:00Z",
    "total_chars": 450,
    "entry_count": 3
  },
  "entries": [
    {"id": "env_001", "category": "environment", "content": "...", "created_at": "2026-09-10T10:00:00Z"}
  ]
}

try:
    jsonschema.validate(instance=memory_data, schema=schema)
    print("✓ Valid")
except jsonschema.ValidationError as e:
    print(f"✗ Invalid: {e.message}")
EOF
```

### Privacy Scan

Ensure no sensitive data leaks into memory:

```bash
# Check for credential patterns
grep -E 'password|api.?key|token|secret|aws_' ~/.hermes/memories/*.md && \
  echo "⚠ WARNING: Potential secrets detected" || echo "✓ No credential patterns found"

# Check for email addresses (PII)
grep -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' ~/.hermes/memories/*.md && \
  echo "⚠ WARNING: Email addresses detected (review privacy policy)" || echo "✓ No email addresses"
```

---

## First Run Checklist

- [ ] All three memory files created (USER.md, MEMORY.md, OFFICE_CONTEXT.md)
- [ ] Files placed in `~/.hermes/memories/` (or profile subdirectories)
- [ ] Hermes config.yaml updated with memory settings
- [ ] Write approval gate enabled (`write_approval: true`)
- [ ] Audit logging enabled (`audit_logging: true`)
- [ ] Privacy scanning enabled (`privacy_enforcement: true`)
- [ ] Permissions verified (files are not world-readable)
- [ ] Test session started; memory loaded in system prompt
- [ ] Backup strategy documented
- [ ] Team trained on memory usage guidelines
- [ ] Governance review scheduled (quarterly cadence)

---

## Common Issues & Troubleshooting

### Memory Not Loading

**Symptom:** Memory section missing from system prompt.

**Fix:**
```bash
# Check config
hermes config show | grep memory

# Verify file exists
ls -la ~/.hermes/memories/

# Restart Hermes
hermes logout && hermes login
```

### Character Limit Exceeded

**Symptom:** `memory add` returns "limit exceeded" error.

**Fix:**
1. Review current entries: `hermes memory list`
2. Consolidate overlapping entries with `replace`
3. Remove low-priority or expired entries with `remove`
4. Retry the add

### Write Approval Gate Stuck

**Symptom:** Memory writes staged but not approved; blocking normal operation.

**Fix:**
```bash
# List pending writes
hermes memory pending

# Review and approve
hermes memory approve [id]

# Or disable approval gate temporarily (not recommended in office)
hermes config set memory.write_approval false
```

### Merge Conflicts in OFFICE_CONTEXT.md

**Symptom:** Multiple people editing shared office context; Git conflicts.

**Fix:**
1. Designate ONE owner (e.g., Security/Governance team)
2. Implement pull request review requirement
3. Use Git branch protection rules
4. Lock file during bulk updates

---

## Next Steps

1. **Review PRIVACY_AND_RETENTION.md** — Data governance and compliance
2. **Review MEMORY_LIFECYCLE.md** — Add/update/archive procedures
3. **Review AUDIT_TRAIL.md** — Logging and compliance tracking
4. **Schedule quarterly review** — Governance cadence (Jan, Apr, Jul, Oct)
5. **Train team** — Share memory usage guidelines
6. **Monitor capacity** — Consolidate when > 80% full

---

## Support

For questions or issues:
- Check Hermes documentation: https://hermes-agent.nousresearch.com/docs
- Review memory.md in local Hermes installation
- Contact your Hermes administrator
