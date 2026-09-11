# Hermes Skills Manifest Export

Complete inventory of 147 Hermes skills across 26 categories, with detailed metadata for portability, dependencies, and MCP requirements.

**Generated:** 2026-09-11  
**Location:** `~/office-hermes-export/skills/`

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| **Total Skills** | 147 |
| **Categories** | 26 |
| **Portable Skills** | 63 (43%) |
| **Environment-Specific** | 71 (48%) |
| **Skills with Dependencies** | 125 (85%) |
| **Skills with MCP Requirements** | 9 (6%) |

---

## 📁 Files in This Export

### Core Files

- **`SKILLS_MANIFEST.yaml`** (115 KB)
  - Complete inventory of all 147 skills
  - Full metadata for each skill
  - Category statistics
  - YAML format for programmatic access

- **`skill-categories.md`**
  - Executive summary by category
  - Portability analysis
  - Dependency classification
  - Export recommendations

- **`MANIFEST_STRUCTURE.md`**
  - Field definitions and data model
  - Sample entries with explanations
  - Query examples
  - Usage guide

### Category Reference

- **`categories/*.md`** (26 files)
  - One markdown file per category
  - Skill list with status indicators
  - Dependency counts
  - Example: `categories/oh-my-hermes.md`

---

## 🎯 Key Features

### Portability Analysis
Each skill is marked as **Portable** or **Environment-Specific**:
- **Portable (63 skills):** No secrets, credentials, or platform-specific tools required
- **Environment-Specific (71 skills):** Requires API keys, CLIs, or platform access

### Dependency Tracking
All external tool and service dependencies are documented:
- Direct CLI tools (git, gh, bc, etc.)
- Cloud platform SDKs (AWS, Azure, GCP)
- Integration platforms (Zapier, n8n, Basecamp)
- MCP servers (Figma, Notion, Canva, etc.)

### Category Organization
Skills grouped into 26 logical categories:
- **oh-my-hermes (111):** Core Hermes framework
- **ultraloop-workflows (9):** Performance orchestration
- **software-development, ai-engineering, productivity, etc.**

---

## 📋 Category Overview

### 🔷 Oh-My-Hermes (111 skills)
The heart of Hermes automation framework.
- Policy overlays (browser, files, terminal)
- Workflow orchestrators (plan, decide, ops-review)
- Specialized workflows (code-review, codebase-onboarding)
- **Portable:** 39 (35%) | **Env-Specific:** 64 (58%)

### 🔷 Ultraloop Workflows (9 skills)
Ultra-performance execution and consensus planning.
- **Examples:** ulw-plan, ulw-research, ulw-maestro, ulw-work
- **Portable:** 3 (33%) | **Env-Specific:** 2 (22%)

### 🔷 Foundational (13 skills)
Framework and orchestration skills.
- software-development, ai-engineering, autonomous-ai-agents
- github, devops, fullstack-development, testing
- **Portable:** 10 (77%)

### 🔷 Specialized (13 skills)
Domain-specific automation.
- research, creative, media, email, note-taking
- social-media, smart-home, cybersecurity, web
- mlops, productive, addyosmani, testing
- **Portable:** 10 (77%)

### 🔷 Integrated Services (7 skills)
External platform integrations.
- crm-analytics (3), github (2), basecamp, n8n, multi-bot-gateway
- **Portable:** 1 (14%) | **Env-Specific:** 6 (86%)

---

## 🚀 Getting Started

### 1. Understand the Manifest
Start with **`skill-categories.md`** for:
- Category descriptions
- Portability analysis
- Export recommendations
- MCP requirement documentation

### 2. Review YAML Structure
See **`MANIFEST_STRUCTURE.md`** for:
- Field definitions
- Sample entries
- Query examples
- Data model details

### 3. Explore Category Docs
Check **`categories/*.md`** for:
- Per-category skill lists
- Status indicators (portable, env-specific)
- Dependency counts

### 4. Access Full Details
Query **`SKILLS_MANIFEST.yaml`** for:
- Complete skill metadata
- All dependencies
- Supporting file references

---

## 💡 Common Use Cases

### Export Skills for Another Hermes Instance
```bash
# Find all portable skills (no setup required)
yq '.skills[][] | select(.portable == true) | .name' SKILLS_MANIFEST.yaml
```

### Find Skills with Specific Dependencies
```bash
# Find all skills needing Docker
yq '.skills[][] | select(.dependencies[] | contains("docker")) | {name, deps: .dependencies}' SKILLS_MANIFEST.yaml
```

### Get Category Statistics
```bash
# View detailed stats per category
yq '.categories' SKILLS_MANIFEST.yaml
```

### Find MCP-Dependent Skills
```bash
yq '.skills[][] | select(.mcp_requirements != null and (.mcp_requirements | length) > 0)' SKILLS_MANIFEST.yaml
```

---

## 📊 Category Breakdown

### Largest Categories
1. **oh-my-hermes** (111 skills)
   - Core Hermes workflows and policy overlays
   - 39 portable, 64 env-specific

2. **ultraloop-workflows** (9 skills)
   - Advanced orchestration and research
   - 3 portable, 2 env-specific

### Fully Portable Categories
- addyosmani (1/1)
- ai-engineering (1/1)
- autonomous-ai-agents (1/1)
- creative (1/1)
- devops (1/1)
- email (1/1)
- fullstack-development (1/1)
- media (1/1)
- mlops (1/1)
- note-taking (1/1)
- productivity (1/1)
- research (1/1)
- smart-home (1/1)
- social-media (1/1)
- software-development (1/1)
- testing (1/1)
- web (1/1)

### Environment-Specific Categories
- **basecamp-integration** (0/1 portable)
- **multi-bot-gateway** (0/1 portable)
- **n8n-automation** (0/1 portable)
- **crm-analytics** (1/3 portable)
- **github** (1/2 portable)

---

## 🔗 Dependencies Summary

### Top Dependency Categories

| Category | Count | Example Skills |
|----------|-------|-----------------|
| Cloud SDKs | 8 | aws, azure, gcp |
| Development Tools | 6 | git, gh CLI, docker |
| Integration Platforms | 5 | n8n, Zapier, Basecamp |
| APIs & REST | 4 | Various SaaS |
| MCP Servers | 9 | Figma, Notion, Zoho |

### Skills with Most Dependencies
- Many oh-my-hermes skills have 10+ dependencies
- Specialized skills typically have 3-5 dependencies
- Portable skills generally have 0-2 dependencies

---

## 🛡️ Security & Portability

### Safe to Export (Portable)
- ✅ All addyosmani skills
- ✅ All creative tools
- ✅ Core research skills
- ✅ Software development orchestration
- ✅ Policy overlays (omh-browser, omh-files, omh-terminal)

### Requires Organization Setup
- ⚠️ GitHub integration (gh CLI auth)
- ⚠️ CRM skills (Zoho/Salesforce credentials)
- ⚠️ Productivity tools (API keys)
- ⚠️ Slack/Discord integrations

### Platform-Specific (Skip for General Export)
- 🔒 Apple skills (macOS-only)
- 🔒 Multi-bot-gateway (Telegram-specific)
- 🔒 N8n (requires n8n instance)

---

## 📚 Related Documentation

- **[Hermes Documentation](https://hermes-agent.nousresearch.com/docs)** - Official Hermes docs
- **`~/.hermes/skills/*/SKILL.md`** - Full documentation for each skill
- **`~/.hermes/skills/*/DESCRIPTION.md`** - Category descriptions

---

## 🔍 Quick Reference

### Querying Tips

**Get portable skills count:**
```bash
yq '[.skills[][] | select(.portable == true)] | length' SKILLS_MANIFEST.yaml
```

**List all skills in a category:**
```bash
yq '.skills["oh-my-hermes"][].name' SKILLS_MANIFEST.yaml
```

**Find skills by dependency:**
```bash
yq '.skills[][] | select(.dependencies | map(select(. == "terraform")) | length > 0) | .name' SKILLS_MANIFEST.yaml
```

**Export as JSON:**
```bash
yq -o json '.' SKILLS_MANIFEST.yaml > skills.json
```

---

## 📝 Notes

1. **Portability:** Determined by presence of credentials/secrets keywords and platform-specific tools
2. **Dependencies:** Auto-extracted from SKILL.md; may include false positives
3. **MCP Requirements:** Explicit MCP server references only
4. **Supporting Files:** Shows up to 5 additional files per skill
5. **Descriptions:** Truncated; see full SKILL.md for complete details

---

## 🎓 For More Information

See individual files in this export:
- **`MANIFEST_STRUCTURE.md`** - Data model and field definitions
- **`skill-categories.md`** - Category guide and recommendations
- **`categories/*.md`** - Per-category reference documents
- **`SKILLS_MANIFEST.yaml`** - Complete machine-readable inventory

---

*Generated: 2026-09-11 | Total Skills: 147 | Categories: 26*
