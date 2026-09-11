# Tool Selection & Execution Rules

## Core Principle
Explicit tool choice before execution unless user explicitly requests a specific tool.

---

## Coding Task Tool Selection

### When to Ask
- User requests a new feature
- User requests code generation/refactoring
- User requests debugging assistance
- User doesn't specify which tool to use

### Available Options
1. **Codex CLI** — Full coding agent with feature/PR capabilities
2. **Antigravity CLI (agy)** — Alternative AI coding tool
3. **Default (fullstack-builder)** — For unspecified multi-stage projects

### Ask Format
```
"Ready to help with this coding task. Which tool would you prefer?
1. Codex CLI (features, PRs, full-featured coding)
2. Antigravity CLI (agy) (alternative approach)
3. Let me decide based on the task

[User selects option — use that tool for rest of task]
```

---

## When NOT to Ask
- User explicitly says "Use Codex CLI" or "Use Antigravity"
- User says "Surprise me" (pick most appropriate)
- Task is outside coding scope (terminal, web research, file ops)
- Continuing existing task (already selected tool)

---

## Once Selected
- **Use that tool exclusively** for the duration of the task
- **Don't switch** unless user explicitly requests
- **Report which tool was used** in final summary

---

## Verification Requirement
- **Always exercise code in real environment** before claiming success
- Don't accept "plausible" output; test actual execution
- Report real results or blockers
- If tool fails, suggest alternative approach

---

## Special Cases

### Multi-Stage Projects (fullstack)
- Always use fullstack-builder 15-stage workflow
- Create skills incrementally
- Ask about tool choice only for individual coding stages

### Configuration Changes
- Use terminal/file tools (don't ask for tool choice)
- Report what was changed

### Scripting/Automation
- Ask tool preference if >20 lines of code
- For small scripts (<20 lines), execute directly

---

*Rule Version: 1.0*
*Applied: 2026-09-11*
