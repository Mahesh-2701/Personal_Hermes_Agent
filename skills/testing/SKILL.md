---
name: testing
description: >
  Software testing skill. Covers unit testing, integration testing, E2E testing, TDD
  (test-driven development), the test pyramid, test design patterns (Arrange-Act-Assert,
  DAMP over DRY, state-based testing), mocking vs real implementations, test anti-patterns,
  and test automation. Use when writing tests, reviewing test quality, or setting up test
  infrastructure. Based on production-tested patterns from Addy Osmani's agent-skills.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  testing:
    tags: [testing, tdd, unit-testing, integration-testing, e2e-testing, test-pyramid, test-design, arrange-act-assert, damp-over-dry, mocking, anti-patterns, test-automation, playwright, jest, vitest, cypress]
    related_skills: [fullstack-builder, frontend, backend, browser-qa]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# Testing Skill

You are Mahi's testing specialist.

Your job is to ensure code is tested properly — not just "has tests," but has the **right** tests, written the **right** way, at the **right** level.

Based on production-tested patterns from Addy Osmani's agent-skills TDD skill.

---

## What This Skill Covers

### Test-Driven Development (TDD)

**The Cycle:**
```
RED → Write a failing test → GREEN → Write minimal code to pass → REFACTOR → Clean up → repeat
```

**Rules:**
- Write the test first. A test that passes immediately proves nothing.
- Make it pass with minimal code. Don't over-engineer.
- Refactor after green. Improve code without changing behavior.
- Run tests after every refactor.

**For bug fixes — the Prove-It Pattern:**
1. Write a test that reproduces the bug (it should FAIL)
2. Fix the bug
3. Test passes (bug fixed, regression guarded)
4. Run full suite (no regressions)

### The Test Pyramid

```
          ╱╲
         ╱  ╲         E2E Tests (~5%)
        ╱    ╲        Full user flows, real browser
       ╱──────╲
      ╱        ╲      Integration Tests (~15%)
     ╱          ╲     Component/API interactions, boundaries
    ╱────────────╲
   ╱              ╲   Unit Tests (~80%)
  ╱                ╲  Pure logic, isolated, milliseconds each
 ╱──────────────────╲
```

**Invest most effort in small, fast tests.** Few E2E tests, but they cover critical paths.

### Test Sizes (Resource Model)

| Size | Constraints | Speed | Example |
|------|------------|-------|---------|
| **Small** | Single process, no I/O, no network, no DB | Milliseconds | Pure function tests, data transforms |
| **Medium** | Multi-process OK, localhost only, no external services | Seconds | API tests with test DB, component tests |
| **Large** | Multi-machine OK, external services allowed | Minutes | E2E tests, performance benchmarks, staging integration |

### When to Use Each Level

```
Is it pure logic with no side effects?
  → Unit test (small)

Does it cross a boundary (API, database, file system)?
  → Integration test (medium)

Is it a critical user flow that must work end-to-end?
  → E2E test (large) — limit to critical paths
```

---

## Writing Good Tests

### The TDD Cycle in Detail

**RED — Write a Failing Test**

```typescript
// This test fails because createTask doesn't exist yet
describe('TaskService', () => {
  it('creates a task with title and default status', async () => {
    const task = await taskService.createTask({ title: 'Buy groceries' });
    expect(task.id).toBeDefined();
    expect(task.title).toBe('Buy groceries');
    expect(task.status).toBe('pending');
    expect(task.createdAt).toBeInstanceOf(Date);
  });
});
```

**GREEN — Make It Pass**

```typescript
// Minimal implementation — just enough to pass
export async function createTask(input: { title: string }): Promise<Task> {
  const task = {
    id: generateId(),
    title: input.title,
    status: 'pending' as const,
    createdAt: new Date(),
  };
  await db.tasks.insert(task);
  return task;
}
```

**REFACTOR — Clean Up**

With tests green, improve the code: extract shared logic, improve naming, remove duplication. Run tests after every refactor.

### The Prove-It Pattern (Bug Fixes)

**Never start by trying to fix the bug.** Start by writing a test that reproduces it.

```
Bug report arrives
       │
       ▼
Write a test that demonstrates the bug
       │
       ▼
Test FAILS (confirming the bug exists)
       │
       ▼
Implement the fix
       │
       ▼
Test PASSES (proving the fix works)
       │
       ▼
Run full test suite (no regressions)
```

**Example:**

```typescript
// Bug: "Completing a task doesn't update the completedAt timestamp"

// Step 1: Write the reproduction test (it should FAIL)
it('sets completedAt when task is completed', async () => {
  const task = await taskService.createTask({ title: 'Test' });
  const completed = await taskService.completeTask(task.id);
  expect(completed.status).toBe('completed');
  expect(completed.completedAt).toBeInstanceOf(Date);  // This fails → bug confirmed
});

// Step 2: Fix the bug
export async function completeTask(id: string): Promise<Task> {
  return db.tasks.update(id, {
    status: 'completed',
    completedAt: new Date(),  // This was missing
  });
}

// Step 3: Test passes → bug fixed, regression guarded
```

### Arrange-Act-Assert Pattern

```typescript
it('marks overdue tasks when deadline has passed', () => {
  // Arrange: Set up the test scenario
  const task = createTask({
    title: 'Test',
    deadline: new Date('2025-01-01'),
  });

  // Act: Perform the action being tested
  const result = checkOverdue(task, new Date('2025-01-02'));

  // Assert: Verify the outcome
  expect(result.isOverdue).toBe(true);
});
```

### One Assertion Per Concept

```typescript
// Good: Each test verifies one behavior
it('rejects empty titles', () => { ... });
it('trims whitespace from titles', () => { ... });
it('enforces maximum title length', () => { ... });

// Bad: Everything in one test — harder to understand what failed
it('validates titles correctly', () => {
  expect(() => createTask({ title: '' })).toThrow();
  expect(createTask({ title: '  hello  ' }).title).toBe('hello');
  expect(() => createTask({ title: 'a'.repeat(256) })).toThrow();
});
```

### Name Tests Descriptively

```typescript
// Good: Reads like a specification
describe('TaskService.completeTask', () => {
  it('sets status to completed and records timestamp', ...);
  it('throws NotFoundError for non-existent task', ...);
  it('is idempotent — completing an already-completed task is a no-op', ...);
  it('sends notification to task assignee', ...);
});

// Bad: Vague names
describe('TaskService', () => {
  it('works', ...);
  it('handles errors', ...);
  it('test 3', ...);
});
```

---

## Test Design Principles

### Test State, Not Interactions

Assert on the **outcome**, not on which methods were called internally.

```typescript
// Good: Tests what the function does (state-based)
it('returns tasks sorted by creation date, newest first', async () => {
  const tasks = await listTasks({ sortBy: 'createdAt', sortOrder: 'desc' });
  expect(tasks[0].createdAt.getTime())
    .toBeGreaterThan(tasks[1].createdAt.getTime());
});

// Bad: Tests how the function works internally (interaction-based)
// Breaks when you refactor, even if behavior is unchanged
it('calls db.query with ORDER BY created_at DESC', async () => {
  await listTasks({ sortBy: 'createdAt', sortOrder: 'desc' });
  expect(db.query).toHaveBeenCalledWith(
    expect.stringContaining('ORDER BY created_at DESC')
  );
});
```

### DAMP Over DRY in Tests

In production code, DRY (Don't Repeat Yourself) is usually right. In tests, **DAMP (Descriptive And Meaningful Phrases)** is better.

A test should read like a specification — self-contained, understandable without tracing through shared helpers.

```typescript
// DAMP: Each test is self-contained and readable
it('rejects tasks with empty titles', () => {
  const input = { title: '', assignee: 'user-1' };
  expect(() => createTask(input)).toThrow('Title is required');
});

it('trims whitespace from titles', () => {
  const input = { title: '  Buy groceries  ', assignee: 'user-1' };
  const task = createTask(input);
  expect(task.title).toBe('Buy groceries');
});
```

Duplication in tests is acceptable when it makes each test independently understandable.

### Prefer Real Implementations Over Mocks

Use the simplest test double that gets the job done.

```
Preference order (most to least preferred):
1. Real implementation → Highest confidence, catches real bugs
2. Fake → In-memory version of a dependency (e.g., fake DB)
3. Stub → Returns canned data, no behavior
4. Mock (interaction) → Verifies method calls — use sparingly
```

Use mocks only when: the real implementation is too slow, non-deterministic, or has side effects you can't control (external APIs, email sending). Over-mocking creates tests that pass while production breaks.

### Edge Cases to Consider

- Null/undefined inputs
- Empty strings, arrays, objects
- Boundary values (min, max, just over max)
- Invalid formats (bad email, bad date)
- Concurrent operations (if applicable)
- Error paths (network failure, DB failure, timeout)
- Idempotency (what happens if called twice?)

---

## Test Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Tests break when refactoring even if behavior unchanged | Test inputs and outputs, not internal structure |
| Flaky tests (timing, order-dependent) | Erode trust in the test suite | Use deterministic assertions, isolate test state |
| Testing framework code | Wastes time testing third-party behavior | Only test YOUR code |
| Snapshot abuse | Large snapshots nobody reviews, break on any change | Use snapshots sparingly and review every change |
| Tests that pass on first run | They may not be testing what you think | Make sure the test would fail without the implementation |
| "All tests pass" but no tests were run | False confidence | Verify the test command actually ran tests |
| Bug fixes without reproduction tests | No regression guard | Always write the failing test first |

---

## Test Automation & Infrastructure

### Discover the Stack First

Before writing tests, discover how **this** repository tests:
- **Language and build system** — package.json, pom.xml, pyproject.toml, go.mod, etc.
- **Test framework and configuration** — how to run a single test vs the full suite
- **Existing conventions** — where tests live, naming patterns
- **Documented commands** — README, CONTRIBUTING, CI workflows

Run the repository's focused-test command during the TDD loop and its full-suite command before completion. Never assume a default like `npm test`.

### CI Integration
- Tests run on every change (PR, commit)
- Failing tests block merge
- Full suite runs on main branch too
- Tests are fast enough to not slow development

---

## Integration with FullStack Builder

This skill is loaded during **Stage 8 (Automated QA)** of the fullstack-builder workflow.

It guides:
- What to test at each level
- How to write meaningful tests
- TDD approach for new functionality
- Prove-It Pattern for bug fixes
- Test pyramid balance

Works alongside:
- `frontend` — frontend test patterns
- `backend` — backend test patterns
- `browser-qa` — E2E browser testing

---

## Verification Checklist

After completing any implementation:

- [ ] Every new behavior has a corresponding test
- [ ] The full suite passes, run with the repository's own test command
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe the behavior being verified
- [ ] No tests were skipped or disabled
- [ ] Tests would fail without the implementation (not just passing by coincidence)

---

## Red Flags

- Writing code without any corresponding tests
- Reaching for a default test command without checking what this repository uses
- Tests that pass on the first run (make sure they test the right thing)
- "All tests pass" but no tests were actually run
- Bug fixes without reproduction tests
- Tests that test framework behavior instead of application behavior
- Test names that don't describe expected behavior
- Skipping tests to make suite pass
- Running same test command twice without code changes (adds nothing)
- "I'll write tests after" — you won't, and they'll test implementation not behavior
- Over-mocking — tests pass while production breaks
