# Hermes Skills Manifest Reference

**Generated:** 2026-09-11  
**Total Skills:** 147  
**Total Categories:** 26  

## Executive Summary

| Metric | Count |
|--------|-------|
| **Total Skills** | 147 |
| **Categories** | 26 |
| **Portable Skills** | 63 (43%) |
| **Environment-Specific** | 71 (48%) |
| **Skills with Dependencies** | 125 (85%) |
| **Skills with MCP Requirements** | 9 (6%) |

## Category Overview

### Oh-My-Hermes (111 skills)
The core framework skills for Hermes automation and workflows.
- **Portable:** 39 (35%)
- **Environment-Specific:** 64 (58%)
- **With Dependencies:** 110 (99%)
- **Examples:** omh-decide, omh-plan, omh-ops-review, omh-code-review

**Use When:** Orchestrating Hermes workflows, automating operations, or designing agent-based solutions.

---

### Ultraloop Workflows (9 skills)
Ultra-performance workflow orchestration skills (ulw-* family).
- **Portable:** 3 (33%)
- **Environment-Specific:** 2 (22%)
- **With Dependencies:** 9 (100%)
- **Examples:** ulw-plan, ulw-research, ulw-maestro, ulw-work

**Use When:** Need high-performance parallel execution, consensus planning, or deep research orchestration.

---

### Software Development (1 skills)
Orchestration and code review for software projects.
- **Examples:** software-development (master orchestration skill)
- **Portable:** Yes

---

### AI Engineering (1 skills)
Model selection, prompting, RAG, and agent strategies.
- **Examples:** ai-engineering
- **Portable:** Yes

---

### Productivity (1 skills)
Document, spreadsheet, and presentation automation.
- **Examples:** productivity
- **Portable:** Yes
- **Common Tools:** Airtable, Google Workspace, Notion, PDF, Excel

---

### Creative (1 skills)
Content generation, design, and visualization.
- **Examples:** creative
- **Portable:** Yes
- **Common Tools:** ASCII art, p5.js, Excalidraw, Comfyui

---

### Research (1 skills)
Academic research, literature review, and knowledge discovery.
- **Examples:** research
- **Portable:** Yes
- **Common Tools:** arXiv, OSINT

---

### GitHub (2 skills)
Version control, PR workflows, and repository management.
- **Portable:** 1
- **Environment-Specific:** 1
- **Examples:** github, hermes-github-backup
- **Common Tools:** gh CLI, git

---

### CRM Analytics (3 skills)
CRM data analysis and Zoho/Salesforce integration.
- **Portable:** 1
- **Environment-Specific:** 2
- **With Dependencies:** 2
- **MCP Requirements:** 2
- **Examples:** crm-analytics-report, zoho-crm-chat, zoho-crm-mcp

---

### Email (1 skills)
Email management and inbox operations.
- **Examples:** email
- **Portable:** Yes
- **Common Tools:** Himalaya, IMAP/SMTP

---

### Apple (1 skills)
macOS-specific integrations (Notes, Reminders, FindMy).
- **Portable:** No (macOS-only)
- **Examples:** apple
- **Common Tools:** memo CLI, remindctl, FindMy.app

---

### Smart Home (1 skills)
Smart lighting and home automation.
- **Portable:** Yes
- **Examples:** smart-home
- **Common Tools:** OpenHue (Philips Hue)

---

### Social Media (1 skills)
Social platform posting and monitoring.
- **Portable:** Yes
- **Examples:** social-media
- **Common Tools:** xurl (X/Twitter)

---

### Media (1 skills)
Audio, video, and content processing.
- **Portable:** Yes
- **Examples:** media
- **Common Tools:** YouTube transcripts, GIF search, Songsee

---

### Note-Taking (1 skills)
Knowledge management and vault operations.
- **Portable:** Yes
- **Examples:** note-taking
- **Common Tools:** Obsidian

---

### MLOps (1 skills)
Machine learning operations and model deployment.
- **Portable:** Yes
- **Examples:** mlops
- **Common Tools:** HuggingFace, vLLM, lm-eval-harness

---

### DevOps (1 skills)
Infrastructure, CI/CD, and systems operations.
- **Portable:** Yes
- **Examples:** devops

---

### FullStack Development (1 skills)
Web, backend, API, and database development.
- **Portable:** Yes
- **Examples:** fullstack-development

---

### Autonomous AI Agents (1 skills)
Multi-agent orchestration and delegation.
- **Portable:** Yes
- **Examples:** autonomous-ai-agents

---

### Web (1 skills)
Content extraction and blocked page recovery.
- **Portable:** Yes
- **Examples:** web

---

### Testing (1 skills)
Test infrastructure and quality assurance.
- **Portable:** Yes
- **Examples:** testing

---

### Cybersecurity (1 skills)
Security operations and threat analysis.
- **Portable:** Yes
- **Examples:** cybersecurity

---

### AddyOsmani (1 skills)
Production quality workflows from Addy Osmani's playbook.
- **Portable:** Yes
- **Examples:** addyosmani

---

### Basecamp Integration (1 skills)
Project management via Basecamp CLI.
- **Portable:** No (requires bc CLI + credentials)
- **Examples:** basecamp-integration
- **Common Tools:** bc CLI

---

### N8n Automation (1 skills)
Workflow automation via n8n platform.
- **Portable:** No (requires n8n instance)
- **Examples:** n8n-automation

---

### Multi-Bot Gateway (1 skills)
Telegram multi-bot coordination.
- **Portable:** No (requires Telegram bot credentials)
- **Examples:** multi-bot-gateway

---

## Portability Analysis

### Portable Skills (63 - Recommended for Export)
Skills with no secrets, credentials, or environment-specific dependencies:
- All **addyosmani** workflows
- All **creative** content tools
- All **research** skills
- All **software-development** orchestration
- Core **oh-my-hermes** policy overlays (browser, files, terminal)
- Most **ultraloop-workflows** (ulw-plan, ulw-research, ulw-qa)

### Environment-Specific (71 - Requires Setup)
Skills requiring external services, APIs, or platform-specific tools:
- **Apple** skills (macOS-only)
- **CRM** skills (require Zoho/Salesforce credentials)
- **GitHub** integrations (require gh CLI auth)
- **Basecamp** (requires bc CLI + credentials)
- **N8n** (requires n8n instance URL + API keys)
- **Telegram** (multi-bot-gateway)

---

## Dependency Classification

### Top 10 Most Common Dependencies

1. **MCP Servers** (9 skills)
   - figma, notion, canva MCPs
   - External tool integration layer

2. **Cloud Platforms** (8 skills)
   - AWS, Azure, GCP SDKs and CLIs

3. **Development Tools** (6 skills)
   - Git, GitHub, language-specific CLIs

4. **Integration Platforms** (5 skills)
   - Zapier, n8n, Basecamp

5. **APIs & Services** (4 skills)
   - Various REST/GraphQL APIs

---

## MCP (Model Context Protocol) Requirements

Skills requiring MCP servers:

| Skill | MCP Server | Purpose |
|-------|-----------|---------|
| crm-analytics-report | zoho | CRM data access |
| zoho-crm-chat | zoho | CRM chat integration |
| zoho-crm-mcp | zoho | Native MCP server |
| basecamp-integration | basecamp | Project management |
| github | github | Version control |
| hermes-github-backup | github | Repository backup |

---

## Recommended Export Checklist

### For Full Office/Organization Export
Include categories:
- ✓ addyosmani (production-ready workflows)
- ✓ ai-engineering (model selection & prompting)
- ✓ creative (content generation)
- ✓ research (knowledge discovery)
- ✓ software-development (code orchestration)
- ✓ oh-my-hermes (portable policy overlays: ~40/111 skills)
- ✓ ultraloop-workflows (portable ulw-* skills: ~3/9)

### Requires Organization-Specific Setup
- GitHub integration (gh CLI + credentials)
- CRM integrations (Zoho/Salesforce creds)
- Productivity tools (Google Workspace, Notion, Airtable)

### Platform-Specific (Skip for General Export)
- Apple (macOS-only)
- Multi-Bot Gateway (Telegram-specific)
- N8n Automation (requires n8n instance)

---

## Quick Reference: Skill Categories

```
Core Frameworks:
  - oh-my-hermes/        (111 skills, policy overlays)
  - ultraloop-workflows/ (9 skills, orchestration)

Development & Operations:
  - software-development/ (master orchestrator)
  - devops/              (infrastructure)
  - github/              (2 skills)

AI & Intelligence:
  - ai-engineering/      (models, prompting, RAG)
  - research/            (literature, OSINT)

Content & Creativity:
  - creative/            (design, visualization)
  - media/               (audio, video)

Business Operations:
  - productivity/        (docs, sheets, presentations)
  - crm-analytics/       (3 skills)

Integrations:
  - basecamp/            (project management)
  - github/              (version control)
  - email/               (messaging)
  - social-media/        (posting, monitoring)
  - note-taking/         (knowledge management)
  - smart-home/          (automation)

Specialized:
  - apple/               (macOS-specific)
  - autonomous-ai-agents/ (multi-agent)
  - mlops/               (ML operations)
  - testing/             (QA automation)
  - cybersecurity/       (security ops)
  - web/                 (content extraction)
```

---

## Generated Files

1. **SKILLS_MANIFEST.yaml** - Complete inventory with full metadata
2. **categories/*.md** - Per-category reference documents

---

## Usage Notes

- **Portable skills** can be copied as-is to other Hermes instances
- **Environment-specific skills** require configuration (API keys, CLIs, etc.)
- **MCP requirements** document tools that need MCP protocol support
- Review each skill's **SKILL.md** for detailed usage patterns before deploying

---

*See SKILLS_MANIFEST.yaml for complete skill-by-skill details.*
