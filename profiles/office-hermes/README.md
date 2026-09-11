# Office Hermes — Portable Agent Configuration Profile

**A reproducible, portable Hermes agent environment for teams and cross-platform deployment.**

## What is This?

Office Hermes is a complete, portable profile of a production-grade AI agent system. It contains:

* **Agent identity & personality** — rules, protocols, operational behavior
* **172+ reusable skills** — organized by functional category
* **Configuration system** — runtime settings, guardrails, memory
* **Workflow automation** — scheduled jobs, coordination patterns
* **Memory architecture** — structured, portable templates
* **MCP integrations** — Model Context Protocol definitions
* **Multi-role profiles** — CEO, Designer, Tester, and more
* **Bootstrap process** — step-by-step installation & verification

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/Mahesh-2701/Personal_Hermes_Agent.git --branch office-hermes
   cd Personal_Hermes_Agent/profiles/office-hermes
   ```

2. **Run bootstrap** (on a fresh Hermes installation)
   ```bash
   bash scripts/install/bootstrap.sh
   ```

3. **Configure environment-specific values**
   ```bash
   cp config/templates/environment.example.yaml .env
   # Edit .env with your API keys, email, workspace paths, etc.
   ```

4. **Verify installation**
   ```bash
   python3 scripts/verify/health-check.py
   ```

5. **Import profile**
   ```bash
   python3 scripts/import/import-profile.py
   ```

That's it! Your fresh Hermes is now configured with the Office Hermes profile.

## Key Features

### **Production-Grade Architecture**

- Agent identity and personality rules
- Comprehensive action approval policies
- Secret/credential handling protocols
- Memory lifecycle management
- Tool and MCP permission matrices
- Escalation & fallback behaviors

### **172+ Reusable Skills**

Organized by category:

* **oh-my-hermes** (120+) — Multi-agent coordination, automation, workflows
* **addyosmani** — Engineering practices, code review, design
* **autonomous-ai-agents** — Agent orchestration, delegation
* **software-development** — Full-stack dev, testing, debugging
* **productivity** — Gmail, Sheets, Docs, Calendar integration
* **research** — OSINT, threat intelligence, data analysis
* **ai-engineering** — Model selection, RAG, prompt engineering
* And 20+ more categories

### **Complete Documentation**

- Architecture overview (`docs/architecture.md`)
- Component reference (`docs/components.md`)
- Security guidelines (`SECURITY.md`)
- Troubleshooting (`docs/troubleshooting.md`)
- AI context for agent understanding (`docs/ai-context.md`)

### **Extensibility**

- Clear skill creation templates
- Workflow composition patterns
- Memory schema extensions
- Custom profile support
- MCP registration process

## Component Overview

```
agent/           → Identity, rules, protocols
config/          → Runtime settings, templates
skills/          → All 172+ skills organized by category
memory/          → Architecture, schemas, templates
mcp/             → Model Context Protocol definitions
workflows/       → Automation & scheduling
commands/        → Custom commands & aliases
settings/        → Display, compression, guardrails
docs/            → Comprehensive documentation
scripts/         → Installation, verification, export
profiles/        → Role-specific profiles
multi-bot/       → Optional multi-bot architecture
```

## Installation Requirements

- **Hermes Agent**: Latest stable version
- **Python**: 3.11+
- **Node.js**: 16+ (for some skills)
- **Git**: 2.30+
- **OS**: macOS, Linux, or Windows (with WSL2)

See `DEPENDENCIES.md` for full details.

## Environment-Specific Configuration

The profile requires configuration for:

- **API Keys**: Anthropic, OpenAI, n8n, Zoho CRM, etc.
- **Email**: Gmail account & workspace
- **Cloud Storage**: Google Drive paths
- **Workspace**: Local directory paths, project structures
- **Platform Integration**: Telegram, Slack, Discord channels

See `config/templates/environment.example.yaml` for all required values.

## Security

**CRITICAL**: This repository contains NO secrets.

All credentials must be configured separately:

```bash
# After cloning, configure:
# 1. API keys in ~/.hermes/config.yaml (or env vars)
# 2. Service account credentials in ~/.hermes/secrets/
# 3. MCP authentication in ~/.hermes/mcp-tokens/
```

See `SECURITY.md` for complete guidelines.

## For AI Agents

This repository is designed to be AI-readable:

- **docs/ai-context.md** — Structured context for LLM understanding
- **MANIFEST.yaml** — Complete component inventory
- **Skill metadata** — Extracted from each SKILL.md
- **Clear taxonomy** — Components organized by type & purpose
- **Explicit rules** — All behavioral rules documented

An AI agent can use this to understand the architecture, find relevant skills, understand constraints, and extend the system safely.

## Export & Sync

Use the built-in export skill to keep this profile synchronized with your running Hermes:

```bash
# From Hermes terminal:
# "Export the current Hermes configuration"
# "Sync Office Hermes profile"
# "Update Office Hermes with current state"
```

See `skills/export-hermes-profile/SKILL.md` for details.

## Roadmap

- [ ] Import/export workflow automation
- [ ] Role-based profile variants
- [ ] Team collaboration templates
- [ ] Cross-platform testing
- [ ] CI/CD integration examples
- [ ] Cost optimization guides

## Contributing

To improve Office Hermes:

1. **Test** on a fresh Hermes installation
2. **Document** changes clearly
3. **Run security checks** (`scripts/verify/security-audit.py`)
4. **Update MANIFEST.yaml**
5. **Submit PR** to `office-hermes` branch

## License

This profile is part of Personal Hermes Agent and follows the repository's license.

## Support

- **Troubleshooting**: See `docs/troubleshooting.md`
- **FAQ**: See `docs/faq.md`
- **Issues**: Report via GitHub issues
- **Architecture questions**: Read `docs/architecture.md`

---

**Version**: 1.0.0  
**Last Updated**: 2026-09-11  
**Maintainer**: Hermes Export System
