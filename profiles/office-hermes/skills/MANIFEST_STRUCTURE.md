# SKILLS_MANIFEST.yaml Structure Guide

## File Location
`~/office-hermes-export/skills/SKILLS_MANIFEST.yaml`

## Overview
A comprehensive YAML inventory of all 147 Hermes skills, organized by 26 categories, with detailed metadata for each skill including portability, dependencies, and MCP requirements.

---

## Top-Level Structure

```yaml
metadata:
  version: '1.0'
  generated_at: '2026-09-11T11:10:28.305132Z'
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

## Field Definitions

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Manifest version (1.0) |
| `generated_at` | ISO8601 | Generation timestamp |
| `total_skills` | int | Count of all skills |
| `total_categories` | int | Count of unique categories |
| `portable_skills` | int | Skills without secrets/env-deps |
| `environment_specific_skills` | int | Skills requiring setup |
| `skills_with_dependencies` | int | Skills with tool dependencies |
| `skills_with_mcp` | int | Skills requiring MCP servers |

### Category Statistics

| Field | Type | Description |
|-------|------|-------------|
| `total_skills` | int | Count of skills in category |
| `portable_skills` | int | Skills portable within category |
| `environment_specific` | int | Env-specific within category |
| `skills_with_dependencies` | int | Skills with deps in category |
| `skills_with_mcp` | int | Skills needing MCP in category |

### Skill Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier (unique) |
| `category` | string | Primary category |
| `description` | string | First 300 chars of description (from SKILL.md) |
| `trigger` | string | Use-case trigger phrase (first 100 chars) |
| `portable` | bool | No secrets/env-specific deps = true |
| `environment_specific` | bool | Requires platform/API setup = true |
| `dependencies` | array | External tools/CLIs needed (top 10) |
| `mcp_requirements` | array | MCP servers required |
| `has_supporting_files` | bool | Has files beyond SKILL.md |
| `supporting_files` | array | List of supporting files/dirs |

---

## Sample Entries

### Portable Skill Example

```yaml
- name: omh-decide
  category: oh-my-hermes
  description: "Decide between options: tradeoffs, a recommendation..."
  trigger: "Decide between options: tradeoffs, a recommendation..."
  portable: true
  environment_specific: false
  dependencies: []
  mcp_requirements: []
  has_supporting_files: false
  supporting_files: []
```

### Environment-Specific Skill Example

```yaml
- name: zoho-crm-chat
  category: crm-analytics
  description: "Use when Mahesh asks about Zoho CRM data..."
  trigger: "Use when Mahesh asks about Zoho CRM data..."
  portable: false
  environment_specific: true
  dependencies:
    - zoho-crm-mcp
    - zoho_crm_get_contact
    - zoho_crm_list_accounts
    - zoho_crm_list_deals
  mcp_requirements:
    - zoho
  has_supporting_files: true
  supporting_files:
    - DESCRIPTION.md
```

### Skill with Dependencies Example

```yaml
- name: basecamp-integration
  category: basecamp-integration
  description: "Use when connecting Hermes to Basecamp via CLI (bc)..."
  trigger: "Use when connecting Hermes to Basecamp via CLI..."
  portable: false
  environment_specific: true
  dependencies:
    - Basecamp
    - bc
    - client
    - config
  mcp_requirements:
    - basecamp
  has_supporting_files: false
  supporting_files: []
```

---

## Category Reference

### Skill Count by Category

| Category | Count | Portable | Env-Specific |
|----------|-------|----------|--------------|
| oh-my-hermes | 111 | 39 | 64 |
| ultraloop-workflows | 9 | 3 | 2 |
| software-development | 1 | 1 | 0 |
| ai-engineering | 1 | 1 | 0 |
| productivity | 1 | 1 | 0 |
| creative | 1 | 1 | 0 |
| research | 1 | 1 | 0 |
| github | 2 | 1 | 1 |
| crm-analytics | 3 | 1 | 2 |
| email | 1 | 1 | 0 |
| apple | 1 | 1 | 0 |
| smart-home | 1 | 1 | 0 |
| social-media | 1 | 1 | 0 |
| media | 1 | 1 | 0 |
| note-taking | 1 | 1 | 0 |
| mlops | 1 | 1 | 0 |
| devops | 1 | 1 | 0 |
| fullstack-development | 1 | 1 | 0 |
| autonomous-ai-agents | 1 | 1 | 0 |
| web | 1 | 1 | 0 |
| testing | 1 | 1 | 0 |
| cybersecurity | 1 | 1 | 0 |
| addyosmani | 1 | 1 | 0 |
| basecamp-integration | 1 | 0 | 1 |
| n8n-automation | 1 | 0 | 1 |
| multi-bot-gateway | 1 | 0 | 0 |

---

## Query Examples

### Find All Portable Skills
```bash
yq '.skills[][] | select(.portable == true) | .name' SKILLS_MANIFEST.yaml
```

### Find Skills with Specific Dependencies
```bash
yq '.skills[][] | select(.dependencies[] | contains("docker")) | .name' SKILLS_MANIFEST.yaml
```

### Find MCP-Requiring Skills
```bash
yq '.skills[][] | select(.mcp_requirements != null and (.mcp_requirements | length) > 0) | {name, mcp: .mcp_requirements}' SKILLS_MANIFEST.yaml
```

### Get Category Statistics
```bash
yq '.categories' SKILLS_MANIFEST.yaml
```

---

## Related Files

- **skill-categories.md** - Executive summary and category guide
- **categories/*.md** - Per-category reference documents
- **~/.hermes/skills/*/SKILL.md** - Full skill documentation

---

## Notes

1. **Portability determination:** Based on presence of secrets/credentials keywords and environment-specific tools
2. **Dependencies extraction:** Automatic scan of SKILL.md for tool mentions; may include false positives
3. **MCP requirements:** Extracted from explicit MCP server references
4. **Supporting files:** Lists up to 5 additional files/directories in skill folder
5. **Descriptions:** Truncated to 300 characters; see full SKILL.md for complete details

---

*Last Updated: 2026-09-11*
