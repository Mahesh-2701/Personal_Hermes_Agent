# Security Guidelines — Office Hermes Profile

**CRITICAL**: This repository contains NO secrets, credentials, or sensitive data.

## What Is NEVER Included

### API Keys & Tokens

```
❌ ANTHROPIC_API_KEY
❌ OPENAI_API_KEY
❌ ZOHO_CRM_TOKEN
❌ GMAIL_SERVICE_ACCOUNT_JSON
❌ TELEGRAM_BOT_TOKEN
❌ GITHUB_TOKEN
❌ Any auth token or API key
```

### Credentials & Secrets

```
❌ Passwords
❌ Private keys (RSA, SSH, TLS)
❌ OAuth tokens
❌ Session cookies
❌ Bearer tokens
❌ Encryption keys
❌ Database credentials
```

### Personal/Private Data

```
❌ Personal email addresses
❌ Phone numbers
❌ Home addresses
❌ Private calendar/contacts
❌ Personal project details
❌ Confidential memories/notes
❌ Private repository links
```

### Sensitive Configuration

```
❌ Machine identifiers (hostnames, MAC addresses)
❌ Network configuration details
❌ Server IP addresses
❌ Internal URLs
❌ OAuth client secrets
❌ MCP authentication credentials
```

## What IS Included

### Agent Personality & Rules

✓ Identity (SOUL.md)  
✓ Behavioral rules  
✓ Approval policies  
✓ Escalation procedures  
✓ Communication patterns  

### Configuration Templates

✓ Example configurations  
✓ Configuration schema  
✓ Default settings  
✓ Environment variable references  

### Skill Definitions

✓ Skill code and logic  
✓ Usage documentation  
✓ Integration points  
✓ Permission requirements  

### Memory Architecture

✓ Memory schemas  
✓ Lifecycle policies  
✓ Initialization templates  
✓ Structure documentation  

### Documentation

✓ Architecture  
✓ Troubleshooting  
✓ Usage examples  
✓ Extension guides  

## Environment-Specific Configuration

### Before Installation

1. **Create .env file** (git-ignored)
   ```bash
   cp config/templates/environment.example.yaml .env
   ```

2. **Add your secrets to .env**
   ```yaml
   ANTHROPIC_API_KEY: sk-...
   ZOHO_CRM_TOKEN: your_token_here
   GMAIL_SERVICE_ACCOUNT: /path/to/credentials.json
   TELEGRAM_BOT_TOKEN: bot_token_here
   ```

3. **Never commit .env**
   ```bash
   # .gitignore already includes:
   .env
   .env.*
   *.pem
   *.key
   credentials.*
   secrets/
   tokens/
   ```

### Loading Secrets

Use environment variables, not hardcoded values:

```bash
# In ~/.hermes/config.yaml or scripts:
anthropic_api_key: ${ANTHROPIC_API_KEY}
zoho_token: ${ZOHO_CRM_TOKEN}

# Or in Python:
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
```

## Pre-Commit Security Checks

### Manual Verification

Before committing changes:

```bash
# Check for secrets in staged files
git diff --cached | grep -iE "key|token|secret|password"

# Should return: (empty)

# Check for .env or credential files
git status | grep -E "\.env|secrets|credentials|\.pem|\.key"

# Should return: (empty)
```

### Automated Checks

Run security audit:

```bash
python3 scripts/verify/security-audit.py
```

Output should show:
```
✓ No API keys detected
✓ No tokens detected
✓ No private keys detected
✓ No credentials files
✓ .gitignore complete
✓ All .env files ignored
✓ Safe to commit
```

## Credential Rotation

When credentials are compromised:

1. **Immediately regenerate** in the source system
2. **Update .env** with new credential
3. **Restart Hermes** to apply changes
4. **Remove old credential** from all systems
5. **Document rotation** in security logs

Example: If ANTHROPIC_API_KEY is compromised:

```bash
# 1. Regenerate in Anthropic console
# 2. Update .env
export ANTHROPIC_API_KEY="sk-new-key-here"

# 3. Restart Hermes
hermes --restart

# 4. Verify new key works
hermes "What is your model?"
# Should respond normally

# 5. Delete old key from Anthropic console
```

## MCP Server Credentials

MCP servers require authentication. Store credentials safely:

```bash
# Location: ~/.hermes/mcp-tokens/
# Contents: JSON files with server-specific auth
# Access: Only readable by current user

ls -la ~/.hermes/mcp-tokens/
# n8n.json
# github.json
# gmail.json
```

When exporting/sharing:

```bash
# NEVER include mcp-tokens/ directory
# User must configure separately:

# 1. Copy template
cp mcp/configuration/auth-template.yaml ~/.hermes/mcp/n8n.yaml

# 2. Add credentials
nano ~/.hermes/mcp/n8n.yaml

# 3. Verify MCP works
hermes "Test n8n integration"
```

## Git Security

### .gitignore Protection

```
# Automatically excluded:
.env                          # Environment variables
.env.*                        # All .env variants
*.pem                         # Private keys
*.key                         # Encryption keys
credentials.*                 # Credential files
secrets/                      # Secrets directory
tokens/                       # Token directory
mcp-tokens/                   # MCP auth
~.hermes/memories/*.personal  # Private memories (if tagged)
```

### Before Pushing

```bash
# Final verification
python3 scripts/verify/security-audit.py --strict

# Review all changes
git diff origin/office-hermes --cached

# Ensure no secrets leaked
git log -p --all -- .env >/dev/null && echo "STOP: .env in history!"

# Safe to push
git push origin office-hermes
```

## For Team Sharing

When sharing Office Hermes with team members:

1. **Provide configuration template**
   ```bash
   # Send only:
   cp config/templates/environment.example.yaml team-member.env.template
   ```

2. **Document each required secret**
   ```markdown
   - ANTHROPIC_API_KEY: Get from Anthropic console
   - ZOHO_CRM_TOKEN: Personal Access Token from Zoho
   - GMAIL_SERVICE_ACCOUNT: JSON credentials file
   ```

3. **Provide setup guide**
   ```bash
   # See INSTALL.md sections on environment config
   ```

4. **Never share .env or credentials directly**

## Incident Response

If credentials are accidentally committed:

### Immediate Actions

```bash
# 1. Stop and rotate compromised credential immediately
export NEW_KEY="sk-new-..."

# 2. Remove from git history (requires force push authority)
git-filter-branch --tree-filter 'rm -f .env' -- --all

# 3. Force push (coordinated with team)
git push origin office-hermes --force

# 4. Notify team
# "Credentials were committed. Regenerated and removed from history."

# 5. Verify removal
git log --all -- .env
# Should show: (nothing)
```

### Prevention

- Use pre-commit hooks (see `.git/hooks/pre-commit`)
- Regular security audits
- Keep .gitignore current
- Never paste credentials in code
- Use environment variables exclusively

## Security Audit Procedure

Run full security audit before any major operation:

```bash
# Complete audit
python3 scripts/verify/security-audit.py --full

# Output should show:
# ✓ No secrets in repository
# ✓ .env properly ignored
# ✓ All credentials external
# ✓ mcp-tokens protected
# ✓ Memory privacy rules applied
# ✓ Safe to proceed
```

## Compliance

This profile meets requirements for:

- No embedded secrets in code
- Environment variable management
- Credential isolation
- Audit trails for access
- Secure credential rotation
- Access control via roles/permissions

## FAQ

**Q: Can I commit my .env file?**  
A: No. Never. .env is in .gitignore for this reason.

**Q: Where do I put API keys?**  
A: In `.env` file (not in repo) or environment variables.

**Q: What if I accidentally committed a secret?**  
A: Immediately rotate the credential. See "Incident Response" section.

**Q: How do I share Office Hermes with my team?**  
A: Share the repository. Each person configures their own .env.

**Q: Are memories included in the export?**  
A: No. Personal memories stay private. Only templates are exported.

---

**Version**: 1.0.0  
**Last Updated**: 2026-09-11  
**Status**: Ready for Production
