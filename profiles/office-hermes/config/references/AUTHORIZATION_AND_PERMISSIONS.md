# ═══════════════════════════════════════════════════════════════════════════════
# HERMES AUTHORIZATION & PERMISSIONS SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
#
# This document describes how Hermes controls access to actions, data, and
# capabilities across multi-user/multi-role deployments.
#
# ARCHITECTURE:
#   1. User identifies via platform (Telegram ID, Slack user ID, etc.)
#   2. User assigned role (CEO, CTO, CMO, Manager, Employee, etc.)
#   3. Role checked against permission matrix (actions allowed per role)
#   4. Each action has risk level (LOW, MEDIUM, HIGH, CRITICAL)
#   5. HIGH/CRITICAL actions require additional confirmation + audit log
#
# SECURITY PRINCIPLE:
#   Fail closed (default DENY) + explicit allow list (whitelist, not blacklist)
#
# ═══════════════════════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────────────────────────────────────
# PART 1: ROLE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
#
# A role is a named set of capabilities. The role registry documents roles
# and their intent. Actual permissions are defined separately in the
# permissions matrix (PART 2).
#
# LOCATION: ~/.hermes/ops/bot_homes/{home}/config/roles.yaml
# SYNTAX:
#   roles:
#     role_name:
#       description: "Human-readable description"
#

roles:
  # ─ Tier 1: Executive Leadership ───────────────────────────────────────
  ceo:
    description: >
      Company executive with full operational visibility and control.
      Can read/write all data, deploy code, manage users, transfer funds.
      Requires approval for CRITICAL actions (users.manage, finance.transfer).

  cto:
    description: >
      Technology executive. Full control over engineering, deployment, infra.
      Can deploy code, manage servers, read reports. Cannot access finance.

  cmo:
    description: >
      Marketing executive. Full control over campaigns, marketing data, leads.
      Can send emails, schedule meetings, read sales data.
      Cannot deploy code or access finance.

  # ─ Tier 2: Management & Coordination ──────────────────────────────────
  manager:
    description: >
      Team/project manager. Can manage projects, tasks, meetings for own team.
      Cannot deploy, cannot access finance or sensitive engineering.

  # ─ Tier 3: Individual Contributors ───────────────────────────────────
  employee:
    description: >
      Standard employee. Read-only access to company/project info, own tasks.
      Can schedule own meetings, read email, view projects.
      Cannot deploy, no financial access, no admin capability.

  # ─ Legacy Roles (Deprecated but still valid) ─────────────────────────
  # These are checked via VALID_ROLES in providers/identity.py for backward
  # compatibility. Do NOT add new roles to this section; use above instead.
  #
  # OWNER      → Equivalent to CEO (full permissions)
  # ADMIN      → Equivalent to CTO (engineering + admin)
  # TRUSTED_USER → Equivalent to Manager
  # READ_ONLY  → Equivalent to Employee (read-only)
  # UNAUTHORIZED → No permissions (fail-closed default)


# ─────────────────────────────────────────────────────────────────────────────
# PART 2: PERMISSION MATRIX (Actions Allowed Per Role)
# ─────────────────────────────────────────────────────────────────────────────
#
# Each role lists explicit actions it's allowed to perform.
#
# Action naming convention:
#   {domain}.{operation}
#
# Domains:
#   - company     (read company info, org chart)
#   - projects    (view/edit projects, roadmaps)
#   - tasks       (view/edit tasks, assign)
#   - meetings    (schedule/modify calendar)
#   - email       (send/read email)
#   - finance     (view/edit financial data, transfer funds)
#   - marketing   (campaigns, leads, market intel)
#   - engineering (code, architecture, technical decisions)
#   - github      (repo access, PR/issue management)
#   - deployment  (deploy to production)
#   - servers     (manage infrastructure, SSH access)
#   - reports     (generate/access reports)
#   - ai_news     (market intelligence, AI news)
#   - users       (manage users, permissions, roles)
#
# LOCATION: ~/.hermes/ops/bot_homes/{home}/config/permissions.yaml
#
# SYNTAX:
#   roles:
#     role_name:
#       - action.name
#       - another.action
#

permission_matrix:
  ceo:
    # ─ Full company visibility ─────────────────────────────────────────
    - company.read                    # Read org chart, company data
    - company.write                   # (Not implemented yet)
    # ─ Project management ─────────────────────────────────────────────
    - projects.read
    - projects.write
    - tasks.read
    - tasks.write
    # ─ Meetings & calendar ─────────────────────────────────────────────
    - meetings.read
    - meetings.write
    # ─ Communication ──────────────────────────────────────────────────
    - email.read
    - email.send
    # ─ Finance (CRITICAL) ─────────────────────────────────────────────
    - finance.read
    - finance.write
    - finance.transfer                # Highest sensitivity
    # ─ Marketing ───────────────────────────────────────────────────────
    - marketing.read
    - marketing.write
    # ─ Engineering ────────────────────────────────────────────────────
    - engineering.read
    - engineering.write
    # ─ GitHub (code) ───────────────────────────────────────────────────
    - github.read
    - github.write
    # ─ Deployment (HIGH risk) ─────────────────────────────────────────
    - deployment.read
    - deployment.execute              # Deploy to production
    # ─ Infrastructure ─────────────────────────────────────────────────
    - servers.read
    - servers.execute                 # SSH, restart services
    # ─ Reports ────────────────────────────────────────────────────────
    - reports.read
    - reports.write
    # ─ Intelligence ───────────────────────────────────────────────────
    - ai_news.read
    # ─ User management (CRITICAL) ─────────────────────────────────────
    - users.read
    - users.manage                    # Add/remove/promote users
    # ─ System ─────────────────────────────────────────────────────────
    - hermes.config.change
    - hermes.skill.install

  cto:
    - company.read
    - projects.read
    - projects.write
    - tasks.read
    - tasks.write
    - meetings.read
    - meetings.write
    - engineering.read
    - engineering.write
    - github.read
    - github.write
    - deployment.read
    - deployment.execute
    - servers.read
    - servers.execute
    - reports.read
    - ai_news.read

  cmo:
    - company.read
    - projects.read                   # Read-only
    - tasks.read
    - tasks.write
    - meetings.read
    - email.read
    - email.send
    - marketing.read
    - marketing.write
    - reports.read
    - ai_news.read

  manager:
    - company.read
    - projects.read
    - projects.write
    - tasks.read
    - tasks.write
    - meetings.read
    - meetings.write
    - reports.read

  employee:
    - company.read                    # Read-only
    - projects.read
    - tasks.read                      # Read-only
    - meetings.read


# ─────────────────────────────────────────────────────────────────────────────
# PART 3: RISK LEVELS (Determines Approval Gate)
# ─────────────────────────────────────────────────────────────────────────────
#
# Each action has a risk level. Levels determine whether Hermes must
# ask for confirmation before executing.
#
# Levels (highest to lowest):
#   CRITICAL  → Requires explicit approval + review + audit log
#   HIGH      → Requires confirmation (1-step approval)
#   MEDIUM    → May require confirmation (context-dependent)
#   LOW       → Execute immediately (no approval)
#
# Approval workflow:
#   1. Agent determines action risk level
#   2. If risk >= HIGH, print confirmation dialog
#   3. User must type "yes" (not just Enter)
#   4. Action logged with user, role, timestamp, result
#
# LOCATION: ~/.hermes/ops/bot_homes/{home}/config/permissions.yaml
# SECTION: risk_levels
#

risk_levels:
  # ─ LOW RISK: Read-only, informational ──────────────────────────────
  projects.read: LOW
  tasks.read: LOW
  meetings.read: LOW
  company.read: LOW
  email.read: LOW
  reports.read: LOW
  ai_news.read: LOW
  github.read: LOW
  engineering.read: LOW
  servers.read: LOW
  deployment.read: LOW
  marketing.read: LOW
  finance.read: LOW
  users.read: LOW

  # ─ MEDIUM RISK: Data mutation, communication ───────────────────────
  email.send: MEDIUM           # Can be used for phishing/spam
  projects.write: MEDIUM       # Affects planning
  tasks.write: MEDIUM          # Affects task status
  meetings.write: MEDIUM       # Can be used for social engineering
  github.write: MEDIUM         # Affects code (but not prod)
  marketing.write: MEDIUM      # Affects brand/campaigns
  reports.write: MEDIUM        # Affects decision-making data

  # ─ HIGH RISK: Production/infrastructure changes ────────────────────
  deployment.execute: HIGH      # Affects production
  servers.execute: HIGH         # SSH, service restarts
  engineering.write: HIGH       # Core product decisions
  finance.write: HIGH           # Budget/spend changes
  hermes.config.change: HIGH    # System-level changes
  hermes.skill.install: HIGH    # Code execution + elevation

  # ─ CRITICAL RISK: Irreversible, org-wide impact ────────────────────
  finance.transfer: CRITICAL    # Moving money (non-revocable)
  users.manage: CRITICAL        # Add/remove/promote users (access control)


# ─────────────────────────────────────────────────────────────────────────────
# PART 4: HOW AUTHORIZATION WORKS (Execution Flow)
# ─────────────────────────────────────────────────────────────────────────────
#
# When agent performs an action:
#
#   1. ACTION INITIATED
#      Agent calls skill.send_email(to="user@example.com", ...)
#
#   2. ROLE LOOKUP
#      Provider.identity looks up user's role from database/provider
#      Example: Telegram user 12345 → role "cmo"
#
#   3. PERMISSION CHECK
#      Query permission matrix:
#        if "email.send" in permissions["cmo"]:
#          ✓ Allowed
#        else:
#          ✗ Denied (raise error)
#
#   4. RISK CHECK
#      Query risk_levels:
#        if risk_levels["email.send"] == MEDIUM:
#          → Require user confirmation
#        elif risk_levels["email.send"] == HIGH or CRITICAL:
#          → Require explicit approval + audit log
#
#   5. APPROVAL (if risk > LOW)
#      Dialog to user:
#        "CMO wants to send email to user@example.com"
#        "Risk: MEDIUM"
#        "Confirm? (yes/no)"
#
#   6. AUDIT LOG (if risk >= HIGH)
#      Record in audit table:
#        user_id: 12345
#        role: cmo
#        action: email.send
#        risk: MEDIUM
#        approved_at: 2026-09-11T16:39:00Z
#        to: user@example.com
#        status: approved/denied
#
#   7. EXECUTION (if approved)
#      Run tool with user context
#
#   8. LOGGING (always)
#      Store result + any errors


# ─────────────────────────────────────────────────────────────────────────────
# PART 5: MULTI-TENANT / MULTI-BOT SETUP
# ─────────────────────────────────────────────────────────────────────────────
#
# Hermes supports multiple isolated "bot homes" per deployment.
# Each bot home has its own:
#   - config/roles.yaml (role definitions)
#   - config/permissions.yaml (action matrix + risk levels)
#   - config/priority.yaml (triage weights for CEO/manager overview)
#
# Directory structure:
#   ~/.hermes/ops/bot_homes/
#   ├── cmo/                           # Bot home for CMO
#   │   ├── config/
#   │   │   ├── roles.yaml
#   │   │   ├── permissions.yaml
#   │   │   ├── priority.yaml
#   │   │   ├── telegram_bots.yaml     # Telegram credentials
#   │   │   └── identities.yaml        # User role mapping
#   ├── cto/                           # Bot home for CTO
#   │   ├── config/
#   │   │   └── ...
#   └── employee/                      # Bot home for employees
#       └── ...
#
# Each bot home maintains separate:
#   - Permissions matrix
#   - User roster
#   - Audit logs
#   - Session state
#
# This allows role-based access even within a single Hermes instance.


# ─────────────────────────────────────────────────────────────────────────────
# PART 6: BEST PRACTICES & HARDENING
# ─────────────────────────────────────────────────────────────────────────────
#
# PRINCIPLE 1: Fail Closed
#   - Default action is DENY (user not found → no access)
#   - Whitelist model: only listed actions are allowed
#   - Unknown actions → CRITICAL (requires approval)
#
# PRINCIPLE 2: Least Privilege
#   - Assign minimum role needed for job
#   - Regularly audit permissions (quarterly)
#   - Remove permissions when role changes
#
# PRINCIPLE 3: Audit Everything
#   - Log all actions, especially HIGH/CRITICAL
#   - Include context: who, what, when, why, result
#   - Archive logs (immutable, queryable)
#
# PRINCIPLE 4: Separate Concerns
#   - Separate roles for read vs. write
#   - Separate roles for prod vs. staging
#   - Separate roles for finance vs. engineering
#
# PRINCIPLE 5: Approval Gates
#   - CRITICAL actions require 2+ approvals
#   - Different approver than requester
#   - Time-bounded (approval expires after 24h)
#
# PRINCIPLE 6: Just-in-Time (JIT) Elevation
#   - Grant elevated role only for specific time window
#   - Require explicit reason/ticket
#   - Automatic downgrade after window closes
#   - Log each elevation + approver
#
# IMPLEMENTATION:
#   hermes --audit-log=json > audit.jsonl
#   → Query with: jq '. | select(.action=="finance.transfer")' audit.jsonl
#

# ═══════════════════════════════════════════════════════════════════════════════
# APPENDIX: EXAMPLE AUDIT LOG ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

audit_log_example:
  timestamp: "2026-09-11T16:39:22.123Z"
  user_id: "5191016577"           # Telegram user ID
  user_name: "Mahesh"
  bot_home: "cmo"
  role: "cmo"
  action: "email.send"
  risk_level: "MEDIUM"
  request_params:
    to: "john@company.com"
    subject: "Q4 Marketing Plan"
    body: "..."
  approval:
    required: true
    approved_by: "user:5191016577"  # Self-approved
    approved_at: "2026-09-11T16:39:23Z"
  execution:
    started_at: "2026-09-11T16:39:24Z"
    completed_at: "2026-09-11T16:39:25Z"
    status: "success"
    error: null
  destination: "audit_log"

# ═══════════════════════════════════════════════════════════════════════════════
