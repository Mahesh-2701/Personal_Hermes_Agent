# PRIVACY_AND_RETENTION.md

**Office Hermes Memory: Data Governance, Compliance & Privacy**

Version: 1.0.0 | Updated: 2026-09-11

---

## Overview

This document defines how memory data is classified, protected, retained, and purged in Office Hermes. It ensures compliance with organizational policies (GDPR, HIPAA, SOC2, etc.) and establishes clear responsibility for data handling.

---

## Data Classification

Memory entries are classified by sensitivity level. Classification determines:
- Where data can be stored
- Who can access it
- How long to retain it
- What encryption/audit requirements apply

### Classification Levels

#### PUBLIC
- Can be shared externally
- Examples: Project tech stack, generic coding conventions
- **Retention:** Indefinite (low value for deletion)
- **Encryption:** Not required
- **Audit:** Basic logging OK
- **Example Entry:** "Project uses Go 1.22 + PostgreSQL 16"

#### INTERNAL
- Internal company use only
- Examples: Infrastructure facts, team processes, office conventions
- **Retention:** 2 years (then archive)
- **Encryption:** Recommended (TLS in transit)
- **Audit:** Standard (log reads/writes)
- **Example Entry:** "Dev server 10.0.1.50 runs Debian 12. SSH key at ~/.ssh/dev_ed25519."

#### CONFIDENTIAL
- Business-sensitive; unauthorized access = business impact
- Examples: Customer data, financial info, strategic decisions
- **Retention:** 1 year active, 7-year archive
- **Encryption:** Required at rest + in transit
- **Audit:** Full audit trail (all access logged)
- **Example Entry:** "Q4 revenue target: $10M. Customer churn rate: 2.3%."
- **NEVER store:** Individual customer details, API secrets, passwords

#### RESTRICTED
- Highly regulated; unauthorized access = legal liability
- Examples: PII (health, financial SSN), payment data, regulated customer info
- **Retention:** Compliance-mandated (7 years for finance, 10 for healthcare)
- **Encryption:** Required everywhere (AES-256 at rest, TLS 1.3 in transit)
- **Audit:** Immutable, tamper-evident log (every read/write)
- **Access:** Role-based (only authorized users, separate system)
- **NEVER store:** Passwords, API keys, customer SSNs, health records, payment info

### Classification Rules for Agents

**Before storing anything in memory:**

```
1. Is it a credential, password, or auth token?
   → BLOCK (never store credentials in memory)

2. Does it contain PII (email, name, SSN, health data, payment info)?
   → Classify RESTRICTED (or don't store)

3. Is it business-sensitive (financials, customer data, strategy)?
   → Classify CONFIDENTIAL

4. Is it infrastructure/process info (non-sensitive, internal use)?
   → Classify INTERNAL

5. Is it public/non-sensitive (tech stack, generic conventions)?
   → Classify PUBLIC
```

---

## Automated Privacy Enforcement

### Credential Scanning

Memory writes are scanned for credential patterns before acceptance. Blocks include:

| Pattern | Examples | Action |
|---------|----------|--------|
| `password[=:]` | `password=secret123` | BLOCK |
| `api.?key[=:]` | `api_key=sk-abc...` | BLOCK |
| `token[=:]` | `token=Bearer xyz` | BLOCK |
| `secret[=:]` | `GITHUB_SECRET=xyz` | BLOCK |
| `aws_access_key` | AWS credentials | BLOCK |
| `rsa.?private.?key` | PEM private keys | BLOCK |
| `ssh.?private.?key` | SSH keys | BLOCK |

If detected, agent is prompted to remove and resubmit.

### PII Scanning

Patterns checked for Personally Identifiable Information:

| Pattern | Examples | Action |
|---------|----------|--------|
| Email | `john@example.com` | FLAG (review with user) |
| SSN | `123-45-6789` | BLOCK |
| Credit Card | `4532-1111-2222-3333` | BLOCK |
| Phone (full) | `+1-555-123-4567` | FLAG |
| Names (if flagged) | `John Doe` | Manual review |

### Configuration

Enable/disable in `~/.hermes/config.yaml`:

```yaml
memory:
  privacy_enforcement: true
  
  # Credential patterns to block
  blocked_patterns:
    - "password[\\s]*="
    - "api[_-]?key[\\s]*="
    - "token[\\s]*="
    - "secret[\\s]*="
    - "aws_access_key"
    - "rsa.?private.?key"
    - "ssh.?private.?key"
    
  # PII patterns to block
  pii_patterns:
    - "\\d{3}-\\d{2}-\\d{4}"  # SSN
    - "\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}"  # Credit card
    
  # Warnings (do not block, but flag)
  warning_patterns:
    - "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"  # Email
    - "\\+?1?[\\s-]?\\(?\\d{3}\\)?[\\s-]?\\d{3}[\\s-]?\\d{4}"  # Phone
```

---

## Retention Policies

### Default (Standard Office)

| Classification | Active Retention | Archive Retention | Auto-Purge |
|---|---|---|---|
| PUBLIC | Indefinite | N/A | Never |
| INTERNAL | 2 years | 3 years (then delete) | Yes, after 5 years |
| CONFIDENTIAL | 1 year | 7 years | Yes, after 8 years |
| RESTRICTED | Per compliance | Per compliance | Per compliance |

### Regulated Environments (Finance/Healthcare/Legal)

| Classification | Active Retention | Archive Retention | Auto-Purge |
|---|---|---|---|
| PUBLIC | Indefinite | N/A | Never |
| INTERNAL | 3 years | 7 years | Yes, after 10 years |
| CONFIDENTIAL | 3 years | 7 years | Yes, after 10 years |
| RESTRICTED | **Compliance-mandated** (7+ years) | Indefinite | Per audit |

### Configuration in config.yaml

```yaml
memory:
  retention_policy: "standard"  # or "regulated"
  
  retention:
    public:
      active_days: null         # Indefinite
      archive_days: null
      auto_purge: false
      
    internal:
      active_days: 730          # 2 years
      archive_days: 1095        # 3 years
      auto_purge: true
      
    confidential:
      active_days: 365          # 1 year
      archive_days: 2555        # 7 years
      auto_purge: true
      
    restricted:
      active_days: 2555         # 7 years minimum (compliance)
      archive_days: null        # Indefinite
      auto_purge: false         # Manual only
```

### Archival Process

When an entry reaches "archive" status:

1. **Flagged for review** — Audit log notes entry as "archived"
2. **Moved to archive store** — Separate encrypted backup (not active memory)
3. **Removed from active prompt** — No longer loaded in system prompt
4. **Searchable but read-only** — Can still query via `hermes archive search`, but cannot edit
5. **Retained per policy** — Then purged automatically (if configured)

### Manual Purge

Organizational admins can force-purge entries before retention window:

```bash
# List archived entries
hermes memory archive list --older-than 2023-01-01

# View before purging
hermes memory archive view [entry_id]

# Purge (requires approval from 2 admins)
hermes memory archive purge [entry_id] --approve-by [admin1] --approve-by [admin2]

# Bulk purge (classification = INTERNAL, older than 2 years, not flagged)
hermes memory purge --classification internal --older-than 2023-09-11 --force --audit-reason "scheduled_retention"
```

---

## GDPR Compliance

### Data Subject Access Request (DSAR)

If a data subject requests their data:

1. **Identify:** Find all memory entries mentioning this subject
2. **Export:** Compile in human-readable format
3. **Respond:** Send within 30 days of request

```bash
# Find entries for subject
hermes memory search "john@example.com"
hermes memory search "customer ID 12345"

# Export to PDF/CSV
hermes memory export --subject-id [id] --format pdf > dsar_response.pdf
```

### Right to Erasure ("Right to be Forgotten")

If data subject requests deletion:

1. **Verify:** Confirm request legitimacy
2. **Sanitize:** Remove all personally identifiable data
3. **Archive:** Move to compliance archive (not deleted immediately)
4. **Confirm:** Send confirmation to subject

```bash
# Sanitize entry (replace PII with [REDACTED])
hermes memory sanitize [entry_id] --mode redact

# Purge after verification
hermes memory purge [entry_id] --reason "gdpr_erasure" --subject-id [id]
```

### Lawful Basis

Document the lawful basis for storing each RESTRICTED entry:

| Basis | Example | Retention |
|---|---|---|
| Consent | User explicitly approved data storage | Only while consent valid |
| Contract | Data necessary for service delivery | Duration of contract + 7 years |
| Legal Obligation | Required by law (tax, regulatory) | Duration of obligation |
| Vital Interest | Emergency safety data | Only as long as necessary |
| Public Task | Government/official functions | As defined by law |
| Legitimate Interest | Necessary for operations (auditing) | Balanced against privacy |

Configured in OFFICE_CONTEXT.md under "Legal Basis for Processing":

```yaml
office_context:
  gdpr_lawful_basis:
    customer_data: "contract"
    employee_data: "legal_obligation"  
    audit_logs: "legitimate_interest"
    emergency_contacts: "vital_interest"
```

---

## HIPAA Compliance (Healthcare)

If handling Protected Health Information (PHI):

### De-identification

Remove or encrypt all identifiers before storing:

- Patient names → [PATIENT_ID]
- Medical record numbers → [MRN]
- Dates of birth → [AGE_RANGE]
- Patient addresses → [REGION]
- Phone/email/social media → [CONTACT_REDACTED]

### Minimum Necessary

Store only data required for immediate purpose:

```
WRONG: "Patient John Doe (DOB 1990-05-15) from 123 Main St has Type 2 diabetes, 
       HbA1c 7.2%, on metformin 1000mg BID"

RIGHT: "Patient [ID_12345] with metabolic condition, HbA1c 7.2%, on standard 
       diabetes medication"
```

### Audit Logging (Required)

Every access to PHI must be logged:

```bash
# HIPAA audit trail enabled automatically
hermes config set memory.hipaa_audit_logging true

# View HIPAA audit log
hermes audit log --filter "memory" --classification restricted
```

### Business Associate Agreement (BAA)

If using Hermes with PHI, sign a BAA with Nous Research. Configuration:

```yaml
memory:
  compliance_framework: "hipaa"
  baa_signed: true
  baa_signature_date: "2026-09-01"
  audit_logging: true               # Mandatory
  encryption_at_rest: true          # AES-256
  encryption_in_transit: "tls13"    # TLS 1.3 minimum
```

---

## SOC2 Compliance

### Control Objectives Met

Memory system satisfies these SOC2 Trust Service Criteria:

| Criterion | How Memory System Complies |
|---|---|
| **CC6.1 – Logical/Physical Access Control** | Role-based access; file permissions 700 (user only) |
| **CC7.1 – Audit Log Retention** | Immutable logs; 7-year retention |
| **CC7.2 – Information System Monitoring** | Privacy scanning; credential detection |
| **CC8.1 – Change Management** | Git-tracked OFFICE_CONTEXT; approval gates |
| **CC9.1 – Encryption** | TLS 1.3 in transit; AES-256 at rest (configurable) |

### Audit Readiness

To prepare for SOC2 audit:

```bash
# Generate compliance report
hermes audit report --type soc2 --from 2026-01-01 --to 2026-09-11 > soc2_report.json

# Export audit logs for external auditor
hermes audit export --format csv --destination auditor_share/
```

---

## PCI DSS Compliance (Payment Processing)

### Restricted Data in Memory

Memory system is NOT approved for storing:

- ❌ Full Primary Account Numbers (PAN)
- ❌ Card Verification Values (CVV)
- ❌ Personal Account Numbers (PAN)
- ❌ Full Track data
- ❌ Expiry dates (if combined with PAN)

### Approved Substitutes

Store tokenized/masked data instead:

```
WRONG: "Stripe API key: sk_live_abc123xyz..."
RIGHT: "Stripe API key: sk_live_[REDACTED_6_CHARS] (stored in Vault)"

WRONG: "Customer card: 4532-1111-2222-3333"
RIGHT: "Customer token: stripe_cus_abc123"
```

### Configuration for Payment Systems

```yaml
memory:
  compliance_framework: "pci_dss"
  
  # Automatically redact payment data
  auto_redact_patterns:
    - "\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}"  # Credit cards
    - "sk_live_.*"                                       # Stripe keys
    - "pk_live_.*"                                       # Publishable keys
    - "rk_live_.*"                                       # Restricted keys
```

---

## Data Breach Incident Response

If memory data is compromised:

### Immediate Actions (0–4 hours)

1. **Detect & Contain:** Stop unauthorized access
2. **Preserve Evidence:** Do not alter memory files
3. **Notify Incident Commander:** Page on-call + security team
4. **Assess Scope:** How much data? Which classification?

### Investigation (4–48 hours)

```bash
# Audit all recent writes to memory
hermes audit log --filter "memory" --last-hours 72 --severity critical

# Check for unauthorized accounts
hermes audit log --filter "auth_failed" --last-hours 72

# Export full audit trail for forensics
hermes audit export --format json --destination /secure/forensics/
```

### Notification (Within 72 hours for GDPR)

If RESTRICTED data breached:

```bash
# Prepare breach report (template)
hermes audit breach-report --classification restricted > breach_notification.md

# Contents:
# - What data breached (classification, sensitivity)
# - When discovered
# - Affected individuals (count, not names)
# - Steps taken to mitigate
# - Recommendations for data subjects
```

### Post-Incident

- [ ] Rotate all credentials in compromised window
- [ ] Audit cloud storage (if backups affected)
- [ ] Enable enhanced logging for 90 days
- [ ] Schedule post-mortem with team
- [ ] Document lessons learned

---

## Data Residency & Sovereignty

### Regional Restrictions

Configure where memory data can be stored:

```yaml
memory:
  data_residency: "EU"    # or "US", "APAC", "HYBRID"
  
  # Restrict backups to region
  backup_location: "eu-west-1"
  
  # Reject entries with geolocation mismatches
  enforce_residency: true
```

### GDPR (EU Data)

EU personal data must be processed in EU. Configuration:

```yaml
memory:
  compliance_framework: "gdpr"
  data_residency: "EU"
  backup_location: "eu-central-1"  # Frankfurt preferred
  transfer_mechanism: "scc"        # Standard Contractual Clauses
```

### CCPA (California Consumer Data)

California residents have right to know/delete. Implement:

```bash
# CCPA-specific audit report
hermes audit report --type ccpa --state california > ccpa_report.json
```

---

## Checklist for Compliance

### Initial Setup
- [ ] Data classification documented (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED)
- [ ] Retention policy selected (standard or regulated)
- [ ] Privacy enforcement enabled in config
- [ ] Credentials/PII patterns configured
- [ ] Compliance framework specified (GDPR/HIPAA/SOC2/PCI-DSS/none)

### Ongoing Operations
- [ ] Quarterly audit of retention compliance
- [ ] Monthly privacy scan (detect credential leaks)
- [ ] Annual data classification review
- [ ] Semi-annual backup restoration test
- [ ] Incident response plan tested annually

### Compliance Audit Ready
- [ ] Audit logging enabled and verified
- [ ] Breach notification procedures documented
- [ ] Data subject request process tested
- [ ] Incident response plan in place
- [ ] Training completed (team + auditors)

---

## Support & Questions

- **Privacy Officer:** contact compliance team
- **DSAR Requests:** submit to dpo@[organization]
- **Incident Response:** escalate to security@[organization]
- **Compliance Audit:** coordination via audit@[organization]
