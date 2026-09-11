# MEMORY_TEMPLATE.md

**Template Version:** 1.0.0  
**Store:** Agent Personal Notes (~2,200 char limit)  
**Entries:** Separated by § (section sign)

---

## Environment & Infrastructure

[EXAMPLE]
Office runs Ubuntu 22.04 LTS on primary dev workstations; staging server at 10.0.1.50 runs Debian 12. PostgreSQL 16, Redis 7.x. Docker & Podman installed. Kubernetes for prod (EKS us-east-1).
§

## Project Structure & Conventions

[EXAMPLE]
Main repo: ~/src/product-api (Go 1.22, chi router, sqlc for DB queries). Tests in ./tests/; run with 'make test'. CI via GitHub Actions. Code style: gofmt + golangci-lint mandatory. Commits: conventional commit format.
§

## Development Environment

[EXAMPLE]
VS Code with Vim keybindings. Default shell: zsh. Git branches: main (protected, 2 approvals required), develop (staging target). Remote: origin → GitHub, upstream → organization fork.
§

## Security & Compliance Notes

[EXAMPLE]
All prod deployments require security review + oncall sign-off. Secrets in Vault (access via vault CLI). TLS 1.3 minimum. Data classification: internal/confidential separated. GDPR check: verify no direct email logging.
§

## Team Workflows & Quirks

[EXAMPLE]
Standup: 10 AM UTC, async updates in #standup Slack. PR review SLA: 24 hours. Oncall escalation → #incidents. Critical bugs: emergency meeting, 15 min response. Deployment window: M-F 9 AM–4 PM UTC only.
§

## Discovered Tool Quirks

[EXAMPLE]
GitHub Actions: 'main' branch cache invalidates if matrix.os changes (flush with 'clear-cache' tag). Kubernetes: etcd snapshots at 3 AM UTC; avoid apply during backup window. Docker: buildkit slower than legacy with large contexts >500MB.
§

## Completed Work (Dated)

[EXAMPLE]
2026-09-10: Migrated database from MySQL 5.7 to PostgreSQL 16 (test schema working, prod cutover scheduled 2026-09-15).
2026-08-30: Refactored auth middleware, all tests green, deployed to staging.
§

## External Dependencies & Services

[EXAMPLE]
Payment processor: Stripe API (key in Vault secret 'stripe-prod'). Monitoring: Datadog (agent running on all nodes). Logs: ELK stack at logs.internal.office. PagerDuty integration for alerts.
§

## Known Limitations & Workarounds

[EXAMPLE]
Prod server at 10.0.1.50 doesn't support UDP multicast (legacy network). Workaround: use TCP fallback. Kubernetes ingress nginx can't do regex path rewrites; use service mesh (Istio) for complex routing.
§

---

## Guidelines for Your Organization

### What to Save Proactively
- User preferences & workflow habits
- Environment facts (OS, versions, infrastructure)
- Corrections to previous assumptions
- Project conventions & configurations
- Completed work with dates
- Discovered tool quirks & workarounds
- Office-wide policies (if not in OFFICE_CONTEXT)

### What to Skip
- Trivial facts ("the user uses Python")
- Easily re-discoverable info (web-searchable)
- Raw data dumps or large code blocks
- Session-specific ephemera
- Content already documented elsewhere

### Consolidation Strategy
When memory reaches 80% capacity (~1,760 chars):
1. Merge related entries (combine multiple "project X uses Y" notes into one comprehensive entry)
2. Remove entries older than 6 months (archive to external storage if needed)
3. Consolidate lessons learned into shorter bullets

### Character Limits
- **Hard limit:** 2,200 chars total (~800 tokens)
- **Soft limit:** 1,760 chars (consolidate before this)
- **Recommended entries:** 8–15 (max ~20)
- **Per entry:** 50–300 chars (dense, actionable)

---

## Metadata

- **Created:** YYYY-MM-DD
- **Last Updated:** YYYY-MM-DD
- **Current Usage:** X/2,200 chars (Y%)
- **Entry Count:** N entries
- **Last Consolidation:** YYYY-MM-DD
