# Hermes Skills Manifest Index

## 📋 Contents Overview

This directory contains a comprehensive inventory of 147 Hermes skills organized by 26 categories.

### 📄 Files

| File | Size | Purpose |
|------|------|---------|
| **README.md** | 8 KB | Overview, quick stats, usage guide |
| **SKILLS_MANIFEST.yaml** | 115 KB | Complete YAML inventory (machine-readable) |
| **skill-categories.md** | 9 KB | Category guide with recommendations |
| **MANIFEST_STRUCTURE.md** | 6 KB | Data model, field definitions, examples |
| **categories/*.md** | 26 files | Per-category reference documents |

---

## 🎯 Start Here

### I want to...

**...understand the inventory at a glance**
→ Start with **README.md**

**...learn about specific categories**
→ Read **skill-categories.md** for summaries

**...see the YAML data structure**
→ Check **MANIFEST_STRUCTURE.md** for field definitions

**...export skills for another instance**
→ Use **SKILLS_MANIFEST.yaml** + **skill-categories.md** portability section

**...query skills programmatically**
→ Load **SKILLS_MANIFEST.yaml** and use yq/python

**...find skills in a specific category**
→ See **categories/{category-name}.md**

---

## 📊 Manifest Statistics

```
Total Skills:          147
Total Categories:       26
Portable Skills:        63 (43%)
Environment-Specific:   71 (48%)
With Dependencies:     125 (85%)
With MCP Servers:        9 (6%)
```

---

## 🔷 Category Index

### Core Framework (120 skills)
- **oh-my-hermes** (111) - Policy overlays, workflows, orchestrators
- **ultraloop-workflows** (9) - Performance execution, consensus planning

### Development & Operations (17 skills)
- **software-development** (1) - Master orchestrator
- **ai-engineering** (1) - Model selection, prompting
- **github** (2) - Version control integration
- **devops** (1) - Infrastructure operations
- **fullstack-development** (1) - End-to-end development
- **testing** (1) - QA automation
- **autonomous-ai-agents** (1) - Multi-agent orchestration

### Content & Intelligence (5 skills)
- **research** (1) - Literature, OSINT
- **creative** (1) - Design, visualization
- **media** (1) - Audio, video processing

### Business & Operations (5 skills)
- **productivity** (1) - Documents, sheets, presentations
- **crm-analytics** (3) - CRM data, Zoho integration
- **email** (1) - Email management

### Connected Services (7 skills)
- **social-media** (1) - Social posting
- **note-taking** (1) - Knowledge management
- **smart-home** (1) - Home automation
- **basecamp-integration** (1) - Project management
- **n8n-automation** (1) - Workflow automation
- **multi-bot-gateway** (1) - Telegram bots
- **web** (1) - Content extraction

### Specialized (4 skills)
- **addyosmani** (1) - Production workflows
- **cybersecurity** (1) - Security operations
- **mlops** (1) - ML operations
- **apple** (1) - macOS integrations

---

## 🔍 Quick Queries

### View Manifest Statistics
```bash
yq '.metadata' SKILLS_MANIFEST.yaml
```

### List All Skills by Category
```bash
yq '.skills | keys' SKILLS_MANIFEST.yaml
```

### Find Portable Skills
```bash
yq '.skills[][] | select(.portable == true) | .name' SKILLS_MANIFEST.yaml | wc -l
```

### Get Skills with MCP Requirements
```bash
yq '.skills[][] | select(.mcp_requirements | length > 0) | {name, mcp: .mcp_requirements}' SKILLS_MANIFEST.yaml
```

### Export as JSON
```bash
yq -o json '.' SKILLS_MANIFEST.yaml > skills.json
```

---

## 📚 Category Files

Each category has a README with:
- Skill list with portable status
- Dependency counts
- Example use cases

**Example:** `categories/oh-my-hermes.md` (111 skills)
**Example:** `categories/ultraloop-workflows.md` (9 skills)
**Example:** `categories/crm-analytics.md` (3 skills)

---

## 🚀 Export Workflow

### Step 1: Review Portability
```bash
# Check what's portable
grep "portable: true" SKILLS_MANIFEST.yaml | wc -l
```

### Step 2: Identify Dependencies
```bash
# Find skills that need setup
grep -B3 "environment_specific: true" SKILLS_MANIFEST.yaml | grep "name:"
```

### Step 3: Check MCP Requirements
```bash
# Find MCP-dependent skills
yq '.skills[][] | select(.mcp_requirements | length > 0)' SKILLS_MANIFEST.yaml
```

### Step 4: Export Safe Skills
```bash
# List portable skills for transfer
yq '.skills[][] | select(.portable == true) | .name' SKILLS_MANIFEST.yaml
```

---

## 🛠️ Usage Examples

### Find Skills Needing Docker
```bash
yq '.skills[][] | select(.dependencies[] | contains("docker")) | .name' SKILLS_MANIFEST.yaml
```

### Get Skills by Dependency Type
```bash
yq '.skills[][] | select(.dependencies | length > 5) | {name, dep_count: (.dependencies | length)}' SKILLS_MANIFEST.yaml
```

### List Category Details
```bash
yq '.categories."oh-my-hermes"' SKILLS_MANIFEST.yaml
```

---

## 📖 Complete Documentation

### This Export
- **README.md** - Overview and getting started
- **skill-categories.md** - Category guide
- **MANIFEST_STRUCTURE.md** - Data model details
- **categories/*.md** - Per-category references

### External Resources
- **[Hermes Docs](https://hermes-agent.nousresearch.com/docs)** - Official documentation
- **~/.hermes/skills/*/SKILL.md** - Individual skill documentation
- **~/.hermes/skills/*/DESCRIPTION.md** - Category descriptions

---

## 📋 Manifest Format

### YAML Structure
```yaml
metadata:
  version: '1.0'
  generated_at: ISO8601_TIMESTAMP
  total_skills: 147
  total_categories: 26
  portable_skills: 63
  environment_specific_skills: 71
  skills_with_dependencies: 125
  skills_with_mcp: 9

categories:
  category_name:
    total_skills: N
    portable_skills: N
    environment_specific: N
    skills_with_dependencies: N
    skills_with_mcp: N

skills:
  category_name:
    - name: skill_name
      category: category_name
      description: "..."
      trigger: "..."
      portable: boolean
      environment_specific: boolean
      dependencies: [...]
      mcp_requirements: [...]
      has_supporting_files: boolean
      supporting_files: [...]
```

---

## 🔐 Security Notes

**Portable Skills (Safe to Export):**
- No credentials or secrets in SKILL.md
- No platform-specific tool requirements
- Ready to copy as-is

**Environment-Specific Skills:**
- Require API keys or authentication
- Depend on external platforms
- Need organization-specific setup

See **skill-categories.md** for detailed portability analysis.

---

## 📊 Export Readiness

| Category | Count | Portable | Ready to Export |
|----------|-------|----------|-----------------|
| oh-my-hermes | 111 | 39 | Partial (policy overlays yes) |
| ultraloop-workflows | 9 | 3 | Partial |
| ai-engineering | 1 | 1 | ✓ |
| creative | 1 | 1 | ✓ |
| research | 1 | 1 | ✓ |
| software-development | 1 | 1 | ✓ |
| crm-analytics | 3 | 1 | Partial |
| github | 2 | 1 | Partial |

---

*Last Updated: 2026-09-11*
*Skills Scanned: 147 across 26 categories*
