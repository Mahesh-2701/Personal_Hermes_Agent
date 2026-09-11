# Office Hermes Memory System Export

This directory contains portable memory system templates, schemas, and documentation for deploying Hermes in an office environment.

## Directory Structure

- **schemas/** — JSON Schema definitions for memory structure, validation rules, and data types
- **templates/** — Markdown templates for initializing office-context memories
- **instructions/** — Operational guides, lifecycle policies, privacy rules, and initialization procedures

## Quick Start

1. Review **instructions/INITIALIZATION.md** for setup walkthrough
2. Customize **templates/** for your organization context
3. Apply schemas in **schemas/** to validate memory entries
4. Follow **instructions/PRIVACY_AND_RETENTION.md** for compliance rules

## Key Design Principles

- **No personal data exported** — All templates are generic office structures
- **Portable & self-contained** — No dependencies on specific users or systems
- **Privacy-first** — Built-in retention, sanitization, and audit rules
- **Scalable** — Support multi-user office deployments with shared memory policies
- **Lifecycle-aware** — Clear versioning, expiration, and archival procedures

## Files Overview

| File | Purpose |
|------|---------|
| `schemas/memory-schema.json` | Core memory data structure and validation |
| `schemas/user-profile-schema.json` | User/office-context profile structure |
| `schemas/office-context-schema.json` | Organization-level shared memory |
| `templates/USER_TEMPLATE.md` | Generic user profile template |
| `templates/MEMORY_TEMPLATE.md` | Agent notes/learning template |
| `templates/OFFICE_CONTEXT_TEMPLATE.md` | Org-level policies and conventions |
| `instructions/INITIALIZATION.md` | Setup, deployment, and first-run guide |
| `instructions/PRIVACY_AND_RETENTION.md` | Data retention, compliance, sanitization |
| `instructions/MEMORY_LIFECYCLE.md` | Add/update/archive/purge procedures |
| `instructions/AUDIT_TRAIL.md` | Logging, versioning, and compliance tracking |

## Integration with Hermes Config

Link these templates to your Hermes deployment via `~/.hermes/config.yaml`:

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200      # ~800 tokens (standard)
  user_char_limit: 1375        # ~500 tokens (standard)
  write_approval: true         # Gate writes for office environments
  retention_policy: "office"   # Use office-level retention rules
  audit_logging: true          # Track all memory mutations
  privacy_enforcement: true    # Scan for sensitive data patterns
```

## Configuration Presets

### Standard Office (Default)
- Write approval required for all memory changes
- Audit logging enabled
- Retention: 90 days active, 1-year archival
- Privacy scanning: blocks credential patterns, PII regex

### Regulated (Finance/Healthcare/Legal)
- Strict write approval with 2-person review
- Full audit trail with tamper detection
- Retention: 7-year archival per compliance
- Privacy scanning: enhanced PII + regulated data patterns
- Encryption at rest (config-driven)

### Development/Test
- Write approval optional (configurable)
- Minimal audit logging
- Retention: 30 days, auto-purge
- Privacy scanning: disabled

---

**Version:** 1.0  
**Last Updated:** 2026-09-11  
**Status:** Portable & Production-Ready
