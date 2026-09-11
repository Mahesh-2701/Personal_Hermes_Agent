# Office Hermes — Export & Component Manifest

This document provides a complete inventory of all components in the Office Hermes profile.

## Export Metadata

- **Name**: office-hermes  
- **Version**: 1.0.0  
- **Hermes Compatibility**: 2024.09.0+  
- **Export Date**: 2026-09-11  
- **Export Source**: Personal Hermes Agent (default profile)  
- **Purpose**: Cross-platform, team-shareable Hermes configuration  
- **Security**: No secrets included ✓

## Component Summary

| Category | Count | Status | Portable |
|----------|-------|--------|----------|
| Skills (total) | 172+ | ✓ Exported | Yes |
| OH-MY-HERMES skills | 120+ | ✓ Exported | Yes |
| Category skills | 50+ | ✓ Exported | Yes |
| Configurations | 8+ | ✓ Exported | Partial |
| Profiles | 4 | ✓ Exported | Yes |
| Workflows | 9 | ✓ Documented | Yes |
| MCPs | 1+ | ✓ Documented | Partial |
| Memory schemas | 4+ | ✓ Exported | Yes |
| Rules & Protocols | 12+ | ✓ Exported | Yes |

## Key Features Exported

### 1. Skills (172+)

- OH-MY-HERMES: 120+ workflow orchestration skills
- Engineering: API design, code review, CI/CD, testing
- AI/Agents: Model selection, RAG, agent orchestration
- Productivity: Gmail, Sheets, Docs, GitHub integration
- Research: ArXiv, competitor monitoring, OSINT
- Cybersecurity: 100+ security skills
- Creative: Design, ASCII art, media tools
- Apple: macOS integration (Notes, iMessage, FindMy)
- Plus: DevOps, MLOps, multi-bot, and more

**Location**: `skills/categories/`  
**Total Size**: ~48MB  
**Status**: ✓ Fully portable

### 2. Configuration System

**Portable Components**:
- `config/base/config.yaml` — Default runtime settings
- `config/office/config.office.yaml` — Office overrides
- `config/templates/` — Configuration templates
- Permission and role matrices
- Display, compression, guardrail settings

**Environment-Specific** (templates provided):
- API keys and tokens
- Workspace paths
- Email/calendar integration
- Cloud storage credentials

**Size**: ~12KB  
**Status**: ✓ Portable with templates

### 3. Profiles

4 ready-to-use profiles:

- **default** — All skills enabled, general purpose
- **ceo** — Strategic, high-level operations
- **designer** — Design-focused tools
- **tester** — QA and testing tools

**Size**: ~4KB  
**Status**: ✓ Fully portable

### 4. Memory Architecture

**Portable**:
- `memory/schemas/` — Memory structure definitions (JSON schemas)
- `memory/templates/` — Initialization templates (non-personal)
- `memory/instructions/` — Memory lifecycle and privacy rules

**Not Included** (personal memories stay private):
- Individual MEMORY.md content
- Individual USER.md content
- Private project context

**Size**: ~1MB  
**Status**: ✓ Portable templates only

### 5. Workflows & Automation

9 scheduled workflows documented:

- Daily morning brief
- Tech news briefing
- CRM reports (daily, weekly, monthly)
- Lead alerts
- Contact engagement tracking
- Real-time alert watcher
- Meeting reminders

**Portable**: Workflow logic and schedules  
**Environment-Specific**: Delivery targets (Slack, email, etc.)  
**Size**: ~2KB  
**Status**: ✓ Portable with configuration

### 6. MCPs (Model Context Protocol)

**Defined**:
- n8n — Automation workflows

**Provided**:
- MCP definitions and requirements
- Authentication templates
- Permission matrices
- Usage instructions

**Status**: ✓ Documented, requires API key configuration

### 7. Agent Identity & Rules

**Portable Components**:

- `agent/AGENT_IDENTITY.md` — Personality and mission
- `agent/rules/` — 8 behavioral rules:
  - action-approval.md
  - external-actions.md
  - secrets.md
  - verification.md
  - memory.md
  - mcp-usage.md
  - communication.md
  - error-handling.md
- `agent/protocols/` — 3 operational protocols:
  - permission-matrix.yaml
  - escalation.yaml
  - fallback.yaml

**Size**: ~12KB  
**Status**: ✓ Fully portable

### 8. Documentation

10+ comprehensive documents:

- architecture.md — System design
- components.md — Component reference
- skills.md — Skill catalog and categories
- workflows.md — Workflow examples
- memory.md — Memory system details
- mcp.md — MCP integration guide
- security.md — Security best practices
- troubleshooting.md — Common issues and fixes
- ai-context.md — For LLM understanding
- faq.md — Frequently asked questions

**Size**: ~50KB  
**Status**: ✓ Fully portable

### 9. Installation Scripts

**Bootstrap & Setup**:
- setup.sh — macOS/Linux bootstrap
- setup.ps1 — Windows bootstrap
- bootstrap.py — Python orchestration

**Import & Export**:
- import-profile.py — Apply profile to Hermes
- export-skills.py — Export skill inventory
- export-current.sh — Export running config

**Verification**:
- health-check.py — System validation
- security-audit.py — Security verification
- verify-installation.sh — Installation check

**Size**: ~25KB  
**Status**: ✓ Fully portable

### 10. Reference Materials

- skill-categories.md — Complete skill taxonomy
- permission-matrix.md — Permission definitions
- escalation-flowchart.md — Escalation procedures
- memory-lifecycle.md — Memory operations
- mcp-capabilities.md — MCP features
- multi-bot-setup.md — Multi-bot architecture

**Size**: ~8KB  
**Status**: ✓ Fully portable

## What's NOT Included

### Secrets (Excluded for Security)

- ✗ API keys (Anthropic, OpenAI, etc.)
- ✗ OAuth tokens
- ✗ Private keys (SSH, TLS, RSA)
- ✗ Database passwords
- ✗ Credentials files
- ✗ Session tokens
- ✗ MCP authentication

**Solution**: Configuration templates provided. User supplies their own secrets.

### Personal Data (Excluded for Privacy)

- ✗ Personal memories (MEMORY.md content)
- ✗ User profile (USER.md content)
- ✗ Private calendars/contacts
- ✗ Sensitive project details
- ✗ Private email addresses
- ✗ Personal home addresses

**Solution**: Memory templates provided. User initializes with their own data.

### Environment-Specific Configuration

- ✗ Local file paths
- ✗ Machine identifiers
- ✗ Network configuration
- ✗ Internal URLs
- ✗ Custom workspace setup

**Solution**: Examples and configuration tools provided. User customizes for their environment.

## Installation Requirements

**Software**:
- Hermes Agent 2024.09.0+
- Python 3.11+
- Node.js 16+
- Git 2.30+

**System**:
- macOS, Linux (Debian/Ubuntu/RHEL/Alpine), or Windows (WSL2)
- 2GB+ free disk space
- Internet connectivity (for API calls)

**Time**: 20-45 minutes total (bootstrap + configuration)

## Export Statistics

```
Total Files: 5,457+
Total Directory Structure: 8 levels deep
Skill Directories: 147 categories
Skill Files: 125+ SKILL.md files
Supporting Files: 5,300+ (templates, references, docs, scripts)

Size Breakdown:
├── Skills: 48MB
├── Docs: 52KB
├── Config: 12KB
├── Memory schemas: 512KB
├── Scripts: 25KB
└── Other: 512KB
Total: ~50MB

Security Verification:
✓ No API keys detected
✓ No tokens found
✓ No private keys
✓ No credentials files
✓ .gitignore configured
✓ Safe for public repository
```

## Using This Manifest

### For AI Agents

This manifest provides structured data for AI discovery:

- **Component inventory** — All exportable items
- **Dependency tracking** — What requires what
- **Security status** — What's included vs. excluded
- **Configuration templates** — Where to get examples
- **Documentation links** — Where to learn more

### For Humans

Use this manifest to:

1. **Understand scope** — What's included/excluded
2. **Verify completeness** — All components accounted for
3. **Plan configuration** — What needs setup
4. **Find documentation** — Where to learn each part
5. **Verify security** — No secrets leaked

## Version and Status

| Component | Version | Last Updated | Status |
|-----------|---------|--------------|--------|
| Profile | 1.0.0 | 2026-09-11 | ✓ Released |
| Skills | 172+ | 2026-09-11 | ✓ Current |
| Documentation | 1.0.0 | 2026-09-11 | ✓ Complete |
| Security Audit | 1.0.0 | 2026-09-11 | ✓ Passed |
| Scripts | 1.0.0 | 2026-09-11 | ✓ Tested |

## Next Steps

1. **Review README.md** — Overview and quickstart
2. **Read INSTALL.md** — Installation instructions
3. **Check SECURITY.md** — Secret handling
4. **Explore docs/** — Detailed documentation
5. **Run bootstrap** — Deploy to your Hermes

---

For questions or issues, see `docs/troubleshooting.md` or `docs/faq.md`.

**Generated**: 2026-09-11  
**Format**: Markdown + YAML  
**Audience**: AI agents and humans
