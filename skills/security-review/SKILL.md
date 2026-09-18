---
name: security-review
description: >
  Security review skill for software applications. Covers OWASP Top 10 (2025), OWASP API
  Security Top 10 (2023), authentication/authorization review, input validation, injection
  prevention, secrets management, dependency security, CORS, headers, data protection,
  session management, and secure coding practices. Use when reviewing application security
  before deployment or as part of the final review stage.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  security-review:
    tags: [security, owasp, owasp-top-10, owasp-api-security, authentication, authorization, input-validation, injection-prevention, secrets-management, dependency-security, cors, headers, data-protection, session-management, secure-coding, penetration-testing]
    related_skills: [fullstack-builder, architecture, backend, frontend, api-design]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# Security Review Skill

You are Mahi's security review specialist.

Your job is to review the application for security issues — authentication, authorization, input validation, injection vulnerabilities, secrets exposure, dependency risks, insecure configurations, and other security concerns.

Based on OWASP Top 10 (2025) and OWASP API Security Top 10 (2023).

---

## What This Skill Covers

### OWASP Top 10 (2025) — Web Application Security

1. **Broken Access Control** — users can act outside their intended permissions
   - Missing authorization checks on endpoints
   - Privilege escalation (user accessing admin functions)
   - Horizontal privilege escalation (user A accessing user B's data)
   - CORS misconfiguration allowing unauthorized access
   - Directory traversal, path manipulation

2. ** Cryptographic Failures** — sensitive data exposed or poorly protected
   - Data transmitted in clear text (no HTTPS)
   - Weak or outdated cryptographic algorithms
   - Keys mismanaged (hardcoded, exposed, not rotated)
   - Sensitive data stored without encryption
   - Passwords stored with weak hashing

3. **Injection** — untrusted data interpreted as code
   - SQL injection (string concatenation in queries)
   - NoSQL injection
   - OS command injection
   - LDAP injection
   - XSS (reflected, stored, DOM-based)
   - SSRF (server making requests to attacker-specified URLs)

4. **Insecure Design** — security not considered in design phase
   - Missing threat modeling
   - No security requirements
   - Trusting client-side controls
   - Insufficient validation architecture

5. **Security Misconfiguration** — system not secured properly
   - Default accounts/passwords left enabled
   - Debug mode enabled in production
   - Unnecessary features enabled (services, pages, methods)
   - Missing security headers
   - Error messages exposing internals
   - Cloud storage misconfigured (public buckets)

6. **Vulnerable and Outdated Components** — using components with known vulnerabilities
   - Outdated dependencies with known CVEs
   - Unpatched systems
   - Using abandoned/unmaintained components
   - Not monitoring dependency vulnerabilities

7. **Identification and Authentication Failures** — auth mechanisms broken or weak
   - Weak password policies
   - Credentials exposed (in URLs, logs, code)
   - Session fixation
   - Weak session management (predictable IDs, no expiration)
   - No multi-factor authentication where appropriate
   - Credential stuffing/brute force not protected against

8. **Software and Data Integrity Failures** — trusting unverified data or code
   - Relying on plugins/extensions without verifying integrity
   - Downloading code without verifying signatures
   - CI/CD pipeline compromises
   - Insecure deserialization
   - Auto-update without integrity verification

9. **Security Logging and Monitoring Failures** — can't detect or respond to breaches
   - Insufficient logging (what's logged, what's not)
   - Logs not monitored
   - Logs not protected (attackers can modify/delete)
   - No alerting for security events
   - Missing audit trail for sensitive operations

10. **Server-Side Request Forgery (SSRF)** — server makes requests to attacker-controlled URLs
    - User-supplied URLs fetched by server without validation
    - Access to internal services exposed
    - Cloud metadata endpoints accessible
    - No allowlist of permitted targets

### OWASP API Security Top 10 (2023)

1. **Broken Object Level Authorization (BOLA)** — accessing other users' objects by changing ID
2. **Broken Authentication** — API auth mechanisms broken or weak
3. **Broken Object Property Level Authorization** — excessive data exposure, mass assignment
4. **Unrestricted Resource Consumption** — no rate limiting, resource exhaustion
5. **Broken Function Level Authorization** — unauthorized access to functions
6. **Unrestricted Access to Sensitive Business Flows** — business logic abuse
7. **Server-Side Request Forgery (SSRF)** — same as web Top 10
8. **Security Misconfiguration** — same as web Top 10
9. **Improper Inventory Management** — shadow APIs, deprecated APIs still accessible
10. **Unsafe Consumption of APIs** — trusting third-party API data without validation

### Common Security Areas

#### Authentication
- Password hashing (bcrypt, argon2 — never plain text, never weak hashes)
- Session management (secure cookies, expiration, rotation, invalidation)
- Token-based auth (JWT — proper signing, expiration, validation, don't store sensitive data in JWT)
- OAuth/OIDC — correct flow, proper scopes, token validation
- MFA where appropriate
- Brute force protection (rate limiting, account lockout considerations)
- Credential recovery (secure reset, no information leakage)

#### Authorization
- Check authorization on every protected endpoint (not just UI)
- Resource-level checks (user can only access their own resources)
- Role-based access control (RBAC) — correct role checks
- Function-level checks (user can only call authorized functions)
- Avoid horizontal privilege escalation

#### Input Validation
- Validate all input at the boundary
- Type validation (string, number, boolean, array, object)
- Range validation (length, size, numeric range, date range)
- Format validation (email, URL, phone — use appropriate validators)
- Sanitization where needed (HTML, SQL, commands)
- Reject unexpected input, don't just clean it

#### Injection Prevention
- SQL: parameterized queries only, never string concatenation
- NoSQL: careful with query operators, validate input
- OS commands: avoid if possible, escape properly if necessary
- XSS: encode output for context (HTML, JavaScript, CSS, URL)
- SSRF: validate/whitelist URLs, block internal targets
- LDAP, XPath, other injection vectors — validate, parameterize

#### Data Protection
- HTTPS everywhere (TLS)
- Sensitive data encrypted at rest where appropriate
- Passwords never stored in plain text
- Minimal data collection (don't store what you don't need)
- PII handled appropriately
- Data retention policies

#### Secrets Management
- Secrets in environment variables or secret managers, never in code
- No secrets in version control (gitignore, no accidental commits)
- Rotate secrets periodically
- Different secrets for different environments
- Access to secrets limited (least privilege)

#### Dependencies
- Use trusted sources
- Monitor for vulnerabilities (npm audit, pip audit, Dependabot, Snyk)
- Keep dependencies updated
- Lockfile integrity (don't hand-edit, review changes)
- Minimize dependencies (each is a risk surface)

#### Security Headers
- **HSTS** — Force HTTPS (Strict-Transport-Security)
- **X-Frame-Options** — prevent clickjacking (DENY or SAMEORIGIN)
- **X-Content-Type-Options** — prevent MIME sniffing (nosniff)
- **Content-Security-Policy (CSP)** — restrict resource loading
- **X-XSS-Protection** — legacy, but consider
- **Referrer-Policy** — control referrer information
- **Permissions-Policy** — restrict browser features

#### CORS
- Configure allowed origins (not `*` for sensitive APIs)
- Allow only needed methods and headers
- Handle preflight correctly
- Don't rely on CORS as security mechanism (it's browser-enforced)

#### Session Management
- Session IDs are random, unpredictable
- Session expiration (absolute and idle)
- Session invalidation on logout, password change
- Secure cookies (Secure, HttpOnly, SameSite)
- No session IDs in URLs

#### Error Handling (Security Aspect)
- No stack traces in production errors
- No internal paths in error messages
- No database details exposed
- Generic error messages to clients, detailed in logs
- Consistent error responses

#### Logging (Security Aspect)
- Log security events (auth failures, access violations, input validation failures)
- Log with enough detail to investigate
- Don't log sensitive data (passwords, tokens, PII)
- Logs protected from tampering
- Logs monitored/alerted

---

## What to Produce

When performing a security review:

1. **Review scope** — what was reviewed (frontend, backend, API, database, infrastructure)
2. **Findings** — each finding with:
   - Description
   - Severity (Critical, High, Medium, Low, Informational)
   - Location (file, endpoint, component)
   - Impact (what could happen)
   - Recommendation (how to fix)
3. **What was verified as secure** — positive findings too
4. **Overall assessment** — security posture summary

---

## Severity Levels

| Level | Description | Example |
|-------|-------------|---------|
| **Critical** | Exploitable vulnerability with severe impact | SQL injection on login, auth bypass, exposed secrets |
| **High** | Significant vulnerability, exploitable | Missing auth on endpoint, XSS in user input, weak passwords |
| **Medium** | Vulnerability with limited impact or difficult exploitation | Missing security header, verbose errors, weak session settings |
| **Low** | Minor issue, limited impact | Missing Security header, cosmetic issue, minor misconfiguration |
| **Informational** | Worth noting, no immediate action | Recommendations, best practices not followed, future considerations |

---

## Review Process

### Step 1: Understand the Application
- What does it do?
- Who are the users?
- What data does it handle (sensitive or not)?
- What are the critical flows (auth, payments, data access)?

### Step 2: Review Authentication & Authorization
- How do users authenticate?
- How is authorization checked?
- Are all protected endpoints actually protected?
- Can users access other users' data?
- Can users escalate privileges?

### Step 3: Review Input Handling
- Is all input validated?
- Is output encoded for context?
- Are queries parameterized?
- Are there any injection vectors?

### Step 4: Review Data Protection
- Is HTTPS used?
- Are secrets protected?
- Is sensitive data encrypted at rest?
- Are passwords hashed properly?

### Step 5: Review Dependencies
- Are dependencies up to date?
- Any known vulnerabilities?
- Dependencies from trusted sources?

### Step 6: Review Configuration
- Debug mode off in production?
- Security headers set?
- CORS configured correctly?
- Error messages not exposing internals?
- Default accounts removed?

### Step 7: Review Logging & Monitoring
- Security events logged?
- Logs protected?
- Monitoring/alerting in place?

---

## Output Format

```markdown
## Security Review: [Application Name]

**Date:** [date]
**Scope:** [what was reviewed]
** reviewer:** [who reviewed]

---

## Findings

### Critical
(none / list)

### High
(none / list)

### Medium
(none / list)

### Low
(none / list)

### Informational
(none / list)

---

### Finding: [Title]

**Severity:** [Critical/High/Medium/Low/Informational]
**Location:** [file/endpoint/component]
**Description:** [what the issue is]
**Impact:** [what could happen if exploited]
**Recommendation:** [how to fix it]
**Evidence:** [any evidence, code snippet, request/response]

---

## Positive Findings (What's Done Well)

- [security practice that's correctly implemented]

---

## Overall Assessment

[Summary of security posture, major concerns, recommendations]

---

## Next Steps

- [priority order for fixing issues]
```

---

## Integration with FullStack Builder

This skill is loaded during **Stage 13 (Security & Reliability Review)** of the fullstack-builder workflow.

It reviews:
- Backend code (auth, validation, injection, secrets)
- Frontend code (XSS, input handling, CSRF)
- API design (auth, authorization, rate limiting)
- Configuration (secrets, headers, debugging)
- Dependencies (vulnerabilities, sources)

**Security review happens before final report** — issues found must be addressed.

---

## Red Flags

- SQL injection (string concatenation in queries)
- No authentication on protected endpoints
- No authorization checks (any user can access any resource)
- Passwords in plain text
- Secrets in code or version control
- Debug mode enabled in production
- Missing HTTPS
- CORS wildcard (`*`) on sensitive API
- No input validation
- Reflected XSS (user input rendered without encoding)
- Stored XSS (user input stored and rendered without encoding)
- Weak password hashing (MD5, SHA1, no salt)
- No rate limiting on auth endpoints
- Session IDs in URLs
- Stack traces in production errors
- Known vulnerabilities in dependencies
- Default credentials left enabled
- Missing security headers
- Insufficient logging of security events
