---
name: verifying-delegated-code-work
description: "Verify a coding agent's tests-pass claim before trusting it."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [verification, codex, claude-code, opencode, delegation, testing, real-data, agentic-coding]
    related_skills: [codex, claude-code, opencode, systematic-debugging]
---

# Verifying Delegated Code Work

## Core principle

When a coding agent (Codex, Claude Code, opencode, or a `delegate_task` subagent)
reports "implemented and verified, tests pass," that self-report is **not**
evidence of correctness on its own. The same agent wrote both the
implementation and the tests, from the same assumptions about the world
(field names, API shapes, environment, config format). A test suite that
agrees with itself proves internal consistency, not real-world correctness.

**The fix is cheap and non-negotiable: after any delegated build reports
success, independently exercise the REAL code path against REAL inputs —
a real API, a real file, a real dataset, a real deployment/runtime context —
before reporting the work as done.** Re-running the agent's own test suite
yourself is necessary but not sufficient; it catches regressions, not the
class of bug below.

## Bug classes that slip through a coding agent's own green test suite

These are not hypothetical — each was caught in a single real session only
because a live dry run was performed after the agent claimed success:

1. **Wrong field/column names.** The agent guesses a name ("task name")
   that doesn't match the real data source's actual header ("task
   description"). Its own test fixture uses the same guessed name, so the
   test passes while every real record silently falls back to a placeholder
   (e.g. "Untitled"). **Verification:** run against the real data source and
   read the actual field values in the output, not just the schema.

2. **Silent capability downgrade under sandbox/network constraints.** A
   dependency install fails inside the agent's sandbox (no network access),
   and the agent quietly falls back to a weaker implementation (e.g. writing
   JSON with a `.yaml` extension instead of real YAML) that its own tests
   never exercise because they only check the fallback's behavior.
   **Verification:** check that the actual on-disk artifact matches its
   claimed format/semantics, not just that some loader can parse it.

3. **Individually-correct pieces that combine wrong.** Two fields are each
   independently correct in isolation, but the final rendered/composed
   output duplicates or contradicts itself when put together (e.g. a
   "detail" string that repeats the customer name a display line already
   shows). No single unit-test assertion catches this — only reading the
   actual composed output does. **Verification:** read the literal rendered
   output a real end user would see, not just the intermediate data
   structures.

4. **Uncapped/unfiltered real-world volume.** Logic that's correct at small
   scale (a 2-row test fixture) produces unusable output at real scale (30+
   rows) — violates a "signal over noise" requirement the test suite never
   encoded because its fixtures were too small to reveal it. **Verification:**
   run against the full real dataset, not a small illustrative subset.

5. **Environment/subprocess boundary mismatches.** Code reads
   `os.environ["SOME_VAR"]` and works fine when the parent process (e.g. an
   interactive gateway) already loaded that var from a `.env` file — but
   breaks the instant the same code runs as an independent subprocess (a
   cron job, a scheduled task, a container) that never inherited it. A
   mocked test that patches the env var directly cannot see this class of
   failure at all. **Verification:** run the exact invocation path production
   will actually use (same process ancestry / env inheritance chain), not
   just the code function in isolation.

6. **A shared sort/priority function silently mis-ranks a special-cased
   item.** A generic ranking helper reads a common field (e.g. `"due"`) that
   most items have but a newly-added item type doesn't — the helper's
   documented "missing = sorts last" fallback then buries exactly the item
   that was supposed to rank FIRST (a P0 security alert ending up behind
   ordinary overdue tasks). Every mocked test still passes because they
   assert presence in a list, not position — nothing asserts "is this item
   first." **Verification:** for any item explicitly meant to be top-ranked,
   print the real rendered, ordered output and confirm it visually — don't
   trust a membership assertion as a proxy for an ordering claim.

7. **The agent dies mid-task with no error surfaced in its own summary.**
   A coding agent's process can hit a hard external failure partway through
   (e.g. "model at capacity") after already writing real files to disk, but
   before running any of the requested verification (tests, dry run, commit).
   The tail of its log ends abruptly after a diff dump with no coherent final
   "tests pass / verified" section — easy to miss if you only grep for
   success language. **Verification:** always confirm the delegated agent's
   own report contains an actual final summary with real command output, not
   just code changes; if the log/transcript ends without one, treat the whole
   task as unverified and run every checklist item below yourself — the
   partial work already on disk is usually still worth keeping and finishing
   by hand rather than re-dispatching from scratch.

## Practical checklist after any delegated build

- [ ] Re-run the agent's own test suite yourself, independently — don't take
      "tests pass" in the agent's final message at face value.
- [ ] Read at least one real, live output end-to-end (not a mocked/canned
      fixture) — an actual API response, an actual file's contents, an
      actual rendered message a user would see.
- [ ] If the real path can't be exercised (no live credentials, no test
      environment available), say so explicitly rather than extrapolating
      success from the test suite alone. Never present an unverified
      delegated result as verified.
- [ ] Check the deployment/runtime boundary specifically if the code will
      run in a different process context than however it was tested
      (cron/subprocess vs. interactive session, container vs. host, etc.).
- [ ] When a real bug is found, fix it yourself and re-verify — don't just
      re-dispatch the same agent and trust the second self-report either.

## Long-running delegated builds

Substantial builds (many files + a full test run) can exceed a foreground
terminal call's timeout mid-write. Coding agents like Codex often write
files incrementally as they go, so a killed foreground call can leave
partially-applied, uncommitted work behind rather than a clean no-op —
inspect `git status`/`git diff` after any timeout before assuming nothing
happened. Prefer dispatching long builds in the background
(`terminal(..., background=true, notify=true)` or `delegate_task`) and
polling the actual output/log file directly; a supervising tool's own
poll/wait status can report `exited` or empty output while the underlying
process is still alive — cross-check with a process listing (e.g. `ps aux`)
for the real PID before concluding a run has actually finished.
