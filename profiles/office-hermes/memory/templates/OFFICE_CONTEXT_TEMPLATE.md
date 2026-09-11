# OFFICE_CONTEXT_TEMPLATE.md

**Template Version:** 1.0.0  
**Scope:** Organization-wide shared memory (accessible to all deployed agents with appropriate access controls)  
**Status:** Portable & Role-Based

---

## Organization Profile

### Basic Info
- **Organization Name:** [e.g., Acme Corp Technology]
- **Deployment Environment:** [prod|staging|test]
- **Primary Region:** [US|EU|APAC]
- **Industry:** [software|finance|healthcare|legal|ecommerce]
- **Applicable Compliance:** [GDPR|HIPAA|SOC2|PCI-DSS|ISO27001]

---

## Infrastructure Standards

### Cloud & Deployment
- **Primary Provider:** [AWS|GCP|Azure|On-Premise|Hybrid]
- **Approved Regions:** [e.g., us-east-1, eu-west-1]
- **Container Orchestration:** [Kubernetes|Docker Compose|ECS|None]
- **Default Container Registry:** [ECR|GCR|ACR|Docker Hub]

### Supported Runtimes & Databases
- **Languages (Min Versions):** 
  - Python 3.11+
  - Node.js 18+ (LTS)
  - Go 1.21+
  - Rust 1.70+
  
- **Approved Databases:**
  - PostgreSQL 14+ (primary SQL)
  - MySQL 8+ (for legacy systems)
  - Redis 7.x (cache/queue)
  - DynamoDB (AWS-only projects)

### Observability
- **Log Aggregation:** [Splunk|Datadog|ELK|CloudWatch]
- **Metrics:** [Prometheus|Datadog|CloudWatch|New Relic]
- **APM:** [Datadog|New Relic|Dynatrace|Jaeger]
- **Alerting:** [PagerDuty|Opsgenie|AlertManager]

---

## Security Policies

### Data Classification
- **Public:** Non-sensitive, shareable externally
- **Internal:** Employee/company data, internal use only
- **Confidential:** Business-sensitive (financials, strategies)
- **Restricted:** Highly regulated (customer PII, health data, payment info)

### Encryption Requirements
- **Data at Rest:** [Required for all|Required for Confidential+|Optional]
- **Data in Transit:** [TLS 1.3 mandatory|TLS 1.2+ acceptable]
- **Key Management:** Vault (centralized) | AWS KMS | External HSM
- **Key Rotation:** Every 90 days for active keys

### Access Control
- **Model:** [RBAC|ABAC|Zero Trust]
- **MFA:** Required for prod access
- **SSH Keys:** Ed25519 4096-bit minimum
- **Credential Rotation:** Every 90 days (mandatory)

### Audit & Logging
- **Log Retention:** 7 years (compliance requirement)
- **Immutable Storage:** All logs stored write-once
- **SIEM Integration:** All security events to [platform]
- **Change Tracking:** Git history + audit log for all infrastructure changes

---

## Code Standards

### Code Review & Testing
- **PR Approvals Required:** 2 (at least 1 senior engineer)
- **Test Coverage Minimum:** 85% on main branches
- **Linting Required:** Yes (blocking CI)
- **SAST Scanning:** Semgrep + CodeQL on all PRs

### Language-Specific Standards

#### Python
- **Version:** 3.11+ (LTS)
- **Style:** PEP 8 (enforced via black formatter)
- **Type Hints:** Required (mypy strict mode)
- **Docstrings:** Google-style docstrings mandatory

#### TypeScript/JavaScript
- **Version:** Node 18+ LTS
- **Style:** AirBnB + Prettier (auto-format on save)
- **Type Checking:** TypeScript strict mode
- **Linting:** ESLint + Prettier

#### Go
- **Version:** 1.21+ LTS
- **Style:** gofmt (standard)
- **Testing:** `go test -cover` (minimum 85%)
- **Linting:** golangci-lint mandatory in CI

#### Rust
- **Version:** 1.70+ stable
- **Style:** rustfmt (standard)
- **Testing:** `cargo test` (all platforms)
- **Clippy Warnings:** None allowed in prod code

### Documentation Requirements
- **README.md:** All repos must have (setup, running, testing, deployment)
- **API Docs:** OpenAPI/Swagger for HTTP APIs
- **Architecture:** ARCHITECTURE.md for components >1,000 LOC
- **ADRs:** Architecture Decision Records for major decisions (in docs/adr/)

---

## Deployment & Release

### CI/CD Platform
- **Primary:** GitHub Actions
- **Secondary:** [if applicable for monorepos]
- **Manual Triggers:** Production deployments require human approval

### Branching Strategy
- **Model:** Trunk-based development (main stable always)
- **Convention:** Feature branches → PR → main (not develop)
- **Naming:** feature/*, bugfix/*, hotfix/* (conventional commits)
- **Main Protection:** 2 approvals + all CI passing + security review

### Release Process
- **Cadence:** [Continuous|Weekly|Biweekly]
- **Versioning:** Semantic versioning (v1.2.3)
- **Release Candidate:** Pre-release tags (v1.2.3-rc1)
- **Change Advisory Board:** Yes (CAB meeting before prod deployment)

### Production Deployment
- **Window:** M–F, 9 AM–4 PM UTC (no weekend deployments)
- **Approval:** Oncall + Tech Lead + Security review
- **Rollback:** Automatic if error rate >5% in first 5 min, or manual via dashboard
- **Monitoring:** Post-deploy bake time 15 min before marking complete

### Disaster Recovery
- **RTO:** 1 hour maximum
- **RPO:** 15 minutes
- **DR Testing:** Quarterly (documented in incident report)
- **Backup Strategy:** Daily incremental, weekly full, replicated to separate region

---

## Office-Wide Conventions

### Commit Messages
Format: `type(scope): subject`
- Types: feat, fix, refactor, docs, test, chore, ci
- Scope: affected component (e.g., 'auth', 'api', 'db')
- Subject: lowercase, imperative, max 72 chars
- Example: `fix(auth): prevent token expiry race condition`

### Pull Requests
- Title: Same as commit (will be squashed)
- Description: Link to issue, describe changes, call out breaking changes
- Reviewers: Auto-assigned from CODEOWNERS file
- SLA: Review within 24 hours during business days

### Issue Tracking
- **Platform:** GitHub Issues
- **Labels:** priority, type, status, team
- **Priorities:** P0 (critical, fix immediately) | P1 (urgent, this sprint) | P2 (next sprint) | P3 (backlog)
- **Closure:** Link commits/PRs; don't close without code references

### Documentation
- **Location:** Docs in repo under docs/ (rendered as GitHub Pages)
- **Format:** Markdown (not Word/Google Docs for version control)
- **Ownership:** Tech lead or designated DRI
- **Update Cadence:** Along with code; docs reviews blocking PRs if outdated

### Security Review Checklist
- [ ] No secrets in code (git secrets hook enabled)
- [ ] Input validation on all user-facing inputs
- [ ] SQL queries use parameterized/ORM patterns (no string concat)
- [ ] Auth checks on all protected endpoints
- [ ] Rate limiting on public APIs
- [ ] Encryption enabled for Confidential+ data
- [ ] Logging doesn't capture passwords/tokens

---

## Team Contacts & Escalation

### On-Call & Escalation
- **On-Call Rotation:** PagerDuty schedule (link)
- **Escalation Path:** L1 (on-call) → L2 (team lead) → L3 (engineering manager) → CTO
- **Critical Alert:** Triggers SMS + Slack @channel

### Department Contacts
- **Security:** security@[org] (incident response)
- **Compliance:** compliance@[org] (regulatory/audit questions)
- **DevOps/Infra:** #infrastructure Slack channel
- **Database Admin:** dba@[org] (production DB changes)

### Incident Response
- **Critical (P0):** War room (Zoom link auto-created), incident commander assigned
- **High (P1):** Slack thread with async updates, daily standup
- **Severity:** Based on customer impact (X customers × Y severity score)

---

## Approved Tools & Integrations

### Monitoring & Observability
- ✅ Datadog (primary APM & logs)
- ✅ PagerDuty (alerting & on-call)
- ✅ Sentry (error tracking)
- ❌ Splunk (discontinued; migrate to Datadog)

### Development Tools
- ✅ GitHub Enterprise
- ✅ JetBrains IDEs (licensed)
- ✅ VS Code (free)
- ✅ Docker Desktop
- ❌ Gitea (use GitHub only)

### Communication
- ✅ Slack (primary)
- ✅ Zoom (video conferencing)
- ✅ Google Workspace (email, docs)
- ❌ Discord (security policy violation)

---

## Frequently Asked Questions (FAQ) for Agents

**Q: Can I commit directly to main?**  
A: No. All changes must go through a PR with 2 approvals + passing CI.

**Q: What's the policy on deps (dependencies)?**  
A: Approved language versions only. Pin to LTS. Run `make audit` to scan for CVEs. Update quarterly.

**Q: Can I deploy to production myself?**  
A: No. Oncall or tech lead must trigger deployment via CI/CD. Post a link in #deployments channel.

**Q: How do I handle a security incident?**  
A: Post in #security-incident (private channel), do NOT share details publicly. Security team will guide response.

**Q: Where do I store API keys and secrets?**  
A: Vault only. Never in code, .env, or config files. Rotate quarterly.

**Q: What's the SLA for infrastructure changes?**  
A: 2-week review window before applying to prod. Submit change request in GitHub (use template).

---

## Metadata

- **Created:** YYYY-MM-DD
- **Last Updated:** YYYY-MM-DD
- **Updated By:** [Governance Committee|Tech Lead|Security Officer]
- **Approval Required for Changes:** Yes (2+ stakeholders)
- **Review Cycle:** Quarterly (January, April, July, October)
- **Next Review:** YYYY-MM-DD
- **Version History:** [Link to change log or GitHub]
