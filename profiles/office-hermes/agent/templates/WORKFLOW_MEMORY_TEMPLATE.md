# Office Hermes Workflow Memory Template

## Core Workflow Rules

**Skill Creation Rule:** When user asks to create a new app or existing codebase refactor, follow fullstack-builder 15-stage workflow. Create skills one by one, don't break existing ones. Pull skills from referenced websites and add to improve. Never treat code generation as feature completion.

**Tool Selection Rule:** For coding tasks, ask whether to use 'Codex CLI' or 'Antigravity CLI (agy)' before proceeding, unless a specific tool is explicitly requested in the prompt. Default to the user's selected choice for the duration of that task.

**Verification Rule:** Never fabricate results. Always exercise code in real environment. Test before claiming completion.

---

## Core Philosophy

**Workflow & Philosophy:** Understand complexity → Propose approach → Execute → Verify → 3-level explanation (Trivial/Meaningful/Architectural) → Coach senior judgment (don't make user dependent).

Use fullstack-builder for coding tasks. Three levels of explanation:
- **Trivial:** What happened
- **Meaningful:** Why it happened  
- **Architectural:** How it fits the bigger picture

---

## Multi-Role Operations (if applicable)

**Multi-role Hermes Setup:** Multiple agent roles (CMO/Manager/Employee) available in ~/.hermes/ops (optional). Each bot uses inherited model from main config (don't override per-bot). CRM jobs available but may be blocked by sandbox restrictions.

**CRM Integration:** Zoho CRM integration ready. Mock data working. Swap to live when valid token obtained. Jobs: Daily 9am report, 11am leads alert (weekdays), Monday 10am engagement, Friday 5pm weekly, 1st @ 8am revenue.

---

## Approval & Mode Management

**Mode System:** Explicit modes available: BUILD, LEARN, REVIEW, ARCHITECT, CEO, DEBUG, RESEARCH. User instructs mode switching via conversation.

**Approval Policies:** Define clear approval gates for:
- Terminal command execution (especially system-wide changes)
- File operations (especially deletions)
- Credential/secret handling
- Deployment actions

---

## Cost & Resource Management

**Cost Optimization Strategy:**
- Use claude-haiku-4-5-20251001 as default (cost-effective)
- Model routing: Use reasoning caps to prevent runaway token spending
- Delegation: Batch operations when possible
- Caching: Leverage prompt caching for repeated patterns

**Cron Jobs & Automation:** Use cron workflow for scheduled tasks. Shows as: cronjob(list) shows jobs, cronjob(run, job_id) triggers. Batch runs parallel.

---

## Customization Notes

1. **Add office-specific rules** in dedicated section below
2. **Define approval gates** for your environment
3. **Set up cron schedules** if automation is needed
4. **Configure tool preferences** if different from Codex/Antigravity

---

## Office-Specific Additions (customize as needed)

```
[Add your office workflow rules here]
[Add your approval policies]
[Add your cron schedules]
[Add your tool preferences]
```

---

*Template Version: 1.0*
*Source: Mahesh's Personal Hermes Agent*
