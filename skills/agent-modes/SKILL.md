---
name: agent-modes
description: "Use when switching agent modes: plan, develop, test, fix."
version: 1.0.0
author: Hermes + Mahi
---

# Agent Modes (Cursor-Style Workflow Orchestration)

This skill defines 5 Cursor-style agent modes for Hermes, allowing dynamic switching between focused operational stances based on the user's prompt or explicit mode commands.

## Mode Definitions & Behaviors

### 1. PLAN Mode
- **Trigger**: "Plan", "Design", "Architecture", or prompt asking how to approach a feature/system.
- **Core Objective**: Analyze requirements, inspect system architecture, identify risks and edge cases, and produce a structured, step-by-step implementation plan without writing raw code yet.
- **Loaded Skills/Tools**: `plan`, `architecture`, `codebase-inspection`.
- **Output**: Markdown plan outlining files to create/modify, data flows, APIs, and edge cases.

### 2. DEVELOP Mode (Builder)
- **Trigger**: "Develop", "Build", "Implement", "Create", or coding tasks.
- **Core Objective**: Implement features end-to-end with production-grade code, adhering to existing project conventions and architecture.
- **Loaded Skills/Tools**: `fullstack-builder`, `frontend`, `backend`, `database`, `api-design`, file tools.
- **Output**: Working code artifacts, verified implementation, and execution summary.

### 3. TEST Mode
- **Trigger**: "Test", "Verify", "TDD", "Write tests", "Check coverage".
- **Core Objective**: Write unit and integration tests, verify system correctness, test edge cases, and enforce test-driven development.
- **Loaded Skills/Tools**: `testing`, `test-driven-development`, terminal/test runners.
- **Output**: Test suite execution results, coverage reports, verified correctness.

### 4. FIX Mode
- **Trigger**: "Fix", "Debug", "Error", "Bug", "Troubleshoot".
- **Core Objective**: Systematic 4-phase root cause debugging (understand, isolate, fix, verify). Fix regressions and error logs defensively.
- **Loaded Skills/Tools**: `systematic-debugging`, terminal, file patch tools.
- **Output**: Root cause explanation, clean patch, and test verification.

### 5. DEVELOPER / ARCHITECT Mode (Reviewer)
- **Trigger**: "Review", "Architect", "Security check", "Optimize", "Senior review".
- **Core Objective**: Provide senior/staff-level code review, security audit, scalability analysis, and architecture critique.
- **Loaded Skills/Tools**: `code-review`, `security-review`, `architecture`.
- **Output**: Actionable review report covering security, performance, maintainability, and trade-offs.

## Mode Selection & Routing Rules
1. **Explicit Switch**: When the user says "Switch to [Mode] mode" or "Use [Mode]", immediately adopt that mode's persona, load relevant specialist skills, and apply its rules.
2. **Implicit Routing**: Infer the correct mode from the user's prompt intent (e.g. an error stack trace triggers **FIX** mode; a broad architecture question triggers **PLAN** mode).
3. **Multi-Stage Workflow**: For large features, sequence through modes: **PLAN** → **DEVELOP** → **TEST** → **FIX** (if needed) → **DEVELOPER** (review).
