---
name: antigravity-cli
description: Use to delegate complex coding tasks to Antigravity CLI.
trigger: "Use to delegate complex coding tasks to Antigravity CLI."
---

# Antigravity CLI (agy) Skill

## Purpose
Use Google's official **Antigravity CLI (`agy`)** as a specialized autonomous coding agent for complex, multi-step engineering tasks.

## Relationship
Hermes is the master orchestrator; Antigravity is the delegated implementation specialist. 
1. Hermes understands the objective, plans, and decides if `agy` is appropriate.
2. Hermes delegates the task to `agy` with precise context.
3. Hermes inspects the result, validates, runs tests, and reports to the user.

## When to Use
- Implementing features, complex refactoring, or multi-file changes.
- Debugging complex system issues.
- Repository-wide analysis or security reviews.
- AI/Agent system development.

## Best Practices
- **Delegation:** Use `agy --print "<task>"` for non-interactive delegation.
- **Context:** Always provide repository paths, constraints, and validation requirements (e.g., `npm run lint`).
- **Safety:** Verify `git status` before delegation. Never `git reset --hard` or `git push` without user approval.
- **Verification:** Never blindly trust `agy`. Run tests/builds after implementation.
- **Large Tasks:** Break into phases; checkpoint between them.
- **Secrets:** Never pass credentials or API keys in prompts.
- **Quota:** Do not waste `agy` usage on trivial tasks Hermes can perform directly.

## Workflow
1. Determine directory and repository state.
2. If task requires agentic orchestration, construct a structured prompt with Objective, Constraints, and Validation steps.
3. Execute: `cd /path/to/repo && agy --print "..."`
4. Inspect diffs, run `npm test` / `build`, and report results clearly.
5. If failed: capture traces, use `omh-agent-debug`, fix root cause, retry.

## Commands
- **Run task:** `/Users/apple/.local/bin/agy run --goal "..."`
- **Delegate non-interactive:** `/Users/apple/.local/bin/agy --print "..."`
- **Check status:** `/Users/apple/.local/bin/agy status`
- **List agents:** `/Users/apple/.local/bin/agy agents list`
- **Permission Management:** `/Users/apple/.local/bin/agy /permissions`
