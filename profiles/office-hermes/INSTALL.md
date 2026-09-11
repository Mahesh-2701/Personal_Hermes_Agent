# Installation Guide — Office Hermes Profile

Complete step-by-step instructions to install Office Hermes on a fresh machine.

## Prerequisites

- [ ] Hermes Agent installed and working (`hermes --version`)
- [ ] Python 3.11+ installed
- [ ] Node.js 16+ installed (for some skills)
- [ ] Git 2.30+ installed
- [ ] 2+ GB free disk space
- [ ] Text editor (VSCode recommended)

## Installation Steps

### Step 1: Clone the Profile

```bash
# Clone the Personal_Hermes_Agent repository
git clone https://github.com/Mahesh-2701/Personal_Hermes_Agent.git
cd Personal_Hermes_Agent

# Switch to office-hermes branch
git checkout office-hermes

# Navigate to the profile
cd profiles/office-hermes
```

### Step 2: Review the Architecture

```bash
# Read the core documentation
cat README.md                    # Overview
cat MANIFEST.yaml               # Component inventory
cat DEPENDENCIES.md             # Version requirements
cat SECURITY.md                 # Secret handling
```

### Step 3: Prepare Environment Configuration

```bash
# Create environment file
cp config/templates/environment.example.yaml .env

# Open and edit with your values
# (Use your text editor)
nano .env

# Key values to configure:
# - HERMES_HOME: (usually ~/.hermes)
# - ANTHROPIC_API_KEY: your API key
# - GMAIL_SERVICE_ACCOUNT: path to credentials JSON
# - WORKSPACE_HOME: your project directory
# - TELEGRAM_BOT_TOKEN: (if using Telegram)
# - ZOHO_CRM_TOKEN: (if using CRM)
```

### Step 4: Verify Configuration

```bash
# Run configuration validator
python3 scripts/verify/configuration-check.py

# Should output:
# ✓ .env file valid
# ✓ Required API keys present
# ✓ Paths accessible
# ✓ Python version OK
# ✓ Node version OK
```

### Step 5: Run Bootstrap

```bash
# Bootstrap installs skills, MCPs, and initializes structure
bash scripts/install/bootstrap.sh

# Monitor output for:
# [✓] Creating directory structure
# [✓] Installing core skills
# [✓] Registering MCP servers
# [✓] Initializing memory
# [✓] Verifying installation

# This typically takes 5-15 minutes depending on your connection
```

### Step 6: Import Profile Configuration

```bash
# Apply Office Hermes configuration to your Hermes
python3 scripts/import/import-profile.py

# This:
# - Applies config.yaml settings
# - Registers skills
# - Sets up workflows
# - Initializes memory structure
# - Configures MCPs
```

### Step 7: Initialize Memory

```bash
# Create initial user profile (non-personal template)
python3 scripts/migrate/init-memory.py

# Prompts you to customize:
# - Your name/role
# - Workspace context
# - Key projects
# - Communication preferences
# - Integration channels
```

### Step 8: Health Check

```bash
# Run comprehensive health check
python3 scripts/verify/health-check.py

# Should report:
# ✓ Hermes running
# ✓ Skills loaded (172+)
# ✓ MCPs ready
# ✓ Memory initialized
# ✓ Configuration valid
# ✓ API keys validated
# ✓ All systems operational
```

### Step 9: Verify Workflows

```bash
# Test key workflows
hermes "What is your core mission?"
hermes "List your installed skills"
hermes "Show me the architecture"

# Expected:
# - Clear identity responses
# - Skill inventory from exported skills
# - Architecture documentation accessible
```

### Step 10: Run Security Audit

```bash
# Final security verification
python3 scripts/verify/security-audit.py

# Checks for:
# - Accidentally exposed secrets
# - Unencrypted credentials
# - Unsafe permissions
# - Insecure configurations

# Should report:
# ✓ No secrets detected
# ✓ All credentials secured
# ✓ Permissions correct
# ✓ Configuration secure
```

## Troubleshooting

### Bootstrap Fails

```bash
# Check logs
tail -100 bootstrap.log

# Common issues:
# - Python version too old → upgrade to 3.11+
# - Node.js missing → install from nodejs.org
# - Disk space → free up space
# - Permission denied → check file permissions
```

### Skills Not Loading

```bash
# Verify skills directory
ls -la ~/.hermes/skills/ | wc -l

# Should show 172+ directories
# If fewer, re-run bootstrap:
bash scripts/install/bootstrap.sh --force-skills
```

### Configuration Not Applied

```bash
# Check .env values
cat .env | grep -v "^#"

# Verify Hermes sees them
hermes "What is your model?"
# Should show configured model

# Re-apply if needed:
python3 scripts/import/import-profile.py --force
```

### Memory Not Initialized

```bash
# Check memory status
cat ~/.hermes/memories/USER.md

# If empty, reinitialize:
python3 scripts/migrate/init-memory.py --reset

# Verify:
cat ~/.hermes/memories/USER.md | head -20
```

### Security Audit Warnings

```bash
# If audit finds issues:
python3 scripts/verify/security-audit.py --verbose

# Review SECURITY.md for remediation
cat SECURITY.md

# Common: credentials in .env file
# Solution: move to environment variables
export ANTHROPIC_API_KEY="sk-..."
```

## Post-Installation

### Customize Profiles

You now have multiple profiles available:

```bash
# Switch profiles in ~/.hermes/config.yaml
profile: default           # All skills enabled
profile: ceo               # Strategic focus
profile: designer          # Design tools
profile: tester            # Testing tools
```

### Configure Workflows

Office Hermes includes scheduled workflows:

```bash
# View configured jobs
hermes "List scheduled workflows"

# Edit workflow configuration:
nano config/office/workflows.yaml

# Reload workflows:
python3 scripts/import/import-profile.py --workflows-only
```

### Extend with Custom Skills

To add your own skills:

```bash
# Use skill template
cp templates/skill-template.md ~/.hermes/skills/my-category/my-skill/SKILL.md

# Edit and register:
# (Hermes will auto-discover)
```

## Verification Checklist

After installation, verify:

- [ ] Hermes runs without errors
- [ ] `hermes --version` shows version
- [ ] 172+ skills listed by `hermes "list skills"`
- [ ] Memory initialized (`cat ~/.hermes/memories/USER.md`)
- [ ] Configuration applied (`hermes "what is your model?"`)
- [ ] MCPs registered (`hermes "list mcp servers"`)
- [ ] Health check passes
- [ ] No secrets in git status
- [ ] Workflows scheduled
- [ ] Can execute a simple task

## Next Steps

1. **Read architecture** — `docs/architecture.md`
2. **Explore skills** — `docs/skills.md`
3. **Understand workflows** — `docs/workflows.md`
4. **Customize settings** — `config/office/config.office.yaml`
5. **Add integrations** — `mcp/configuration/`

## Support

If you encounter issues:

1. Check `docs/troubleshooting.md`
2. Review relevant documentation in `docs/`
3. Run `python3 scripts/verify/health-check.py --verbose`
4. Check logs: `tail ~/.hermes/logs/hermes.log`

---

**Duration**: Typically 15-30 minutes  
**Difficulty**: Intermediate (some config required)  
**Support**: See SUPPORT.md
