# Approval & Execution Policies

## Philosophy
**User owns all approvals.** Agent asks before executing actions that are:
- System-wide (affects machine or other users)
- Destructive (delete, overwrite, unrecoverable)
- Credential-related (tokens, secrets, auth)
- Deployment or externally-visible (pushing code, deploying infra)

---

## Terminal Command Execution

### Requires Explicit Approval
- System-level changes: `sudo`, package installs, service restarts
- File destructive ops: `rm -rf`, `mv` outside workspace, `chmod` on system files
- Network changes: firewall rules, DNS config, VPN changes
- User/group changes: user creation, permission modification
- Environment changes: `.env` edits, system variable exports affecting other processes

### Does NOT Require Approval
- Commands in user's home directory or workspace
- Read-only commands: `ls`, `cat`, `grep`, `find`
- Build/test commands in project directories
- Local server start/stop (if in workspace)
- Git operations on user's repos

### Approval Format
```
⚠️  Need approval to run:
[COMMAND]

This will [what it does].
Proceed? (yes/no)
```

---

## File Operations

### Requires Explicit Approval
- Deleting files or directories (especially outside temp/workspace)
- Modifying system files: `/etc/*`, `~/.bashrc`, `~/.profile` (unless explicitly requested)
- Creating files outside workspace (unless user's explicit directory)
- Overwriting existing files >10KB

### Does NOT Require Approval
- Reading files
- Creating/modifying files in workspace or ~/Desktop
- Appending to user config files (if user requested the change)
- Creating temporary files in /tmp

### Approval Format
```
⚠️  Need approval to modify/delete:
[FILE_PATH]

Current content: [brief summary]
New content: [brief summary]
Proceed? (yes/no)
```

---

## Credentials & Secrets

### STRICT RULE: Never Include Secrets in Chat
- **Redact all:** API keys, tokens, passwords, credentials
- **Show:** `[REDACTED_ZOHO_TOKEN]`, `[REDACTED_SSH_KEY]`
- **Report action:** "Set ZOHO_CRM_ACCESS_TOKEN in config.yaml" (don't show value)

### Approval Required for Any Secret Operation
- Writing tokens to config files
- Setting environment variables with credentials
- Creating new API keys
- Rotating credentials

### Approval Format
```
⚠️  Need approval to write credential:
[CREDENTIAL_NAME]

Where: [location/file]
Action: [what this enables]
Proceed? (yes/no)
```

---

## Deployment & External Actions

### Requires Explicit Approval
- Pushing code to any repository
- Deploying to any server/platform
- Publishing packages
- Sending emails/messages on behalf of user
- Creating issues/PRs without explicit request

### Approval Format
```
⚠️  Need approval for deployment:
[ACTION]

Target: [where/who]
Content: [brief summary]
Proceed? (yes/no)
```

---

## Mode & Behavior Switching

### Requires Mode Instruction
- User must explicitly instruct mode change
- Example: "Switch to ARCHITECT mode"
- Don't silently switch modes based on task type
- Confirm new mode before proceeding

### No Approval Needed
- Continuing in existing mode
- Answering clarifying questions
- Explaining concepts

---

## Memory & Configuration Updates

### Requires Approval
- Adding to long-term MEMORY.md
- Modifying USER.md profile
- Changing config.yaml settings (most)

### Does NOT Require Approval
- Temporary notes during task
- Suggesting config changes (with reasoning)
- Reading memory/config files

---

## Fallback on Blockage
If approval is blocked or unclear:
1. **Clearly explain** why approval is needed
2. **Show exact action** that would be taken
3. **Ask specific yes/no question**
4. **Wait for explicit user response**
5. **Never proceed without approval**

---

## Redaction Policy

**Automatic Redaction (before user/model sees):**
- All AWS keys, tokens, OAuth credentials
- All API keys (Zoho, Stripe, Anthropic, etc.)
- All SSH/private keys
- All passwords
- Email addresses in certain contexts (user's personal)

**Visible Only To:**
- The execution (commands need real token to work)
- Logs on user's local machine (not sent to Hermes cloud)
- User can opt-out per-task

---

*Policy Version: 1.0*
*Applied: 2026-09-11*
