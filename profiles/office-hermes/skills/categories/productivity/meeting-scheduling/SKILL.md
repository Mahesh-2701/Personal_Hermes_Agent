---
name: meeting-scheduling
description: "Use when scheduling a meeting. Confirms before creating."
version: 1.0.0
author: Hermes Agent (built for Mahesh's personal ops system)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [calendar, scheduling, meetings, google-workspace, confirmation-flow]
    related_skills: [google-workspace]
---

# Meeting Scheduling (Phase 11)

Handles natural-language meeting scheduling requests end-to-end: resolve
person -> resolve time -> check conflicts -> propose -> WAIT FOR EXPLICIT
CONFIRMATION -> create event + send invite -> report result.

This is a CONSEQUENTIAL ACTION per Mahesh's explicit policy (confirm-first,
always, no auto-approval rule configured). Never skip the confirmation step.

## Prerequisites

Requires the `google-workspace` skill's OAuth already set up (Calendar +
Contacts scopes). Check with:
```bash
/Users/apple/.hermes/hermes-agent/venv/bin/python3 /Users/apple/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
```
Always use `/Users/apple/.hermes/hermes-agent/venv/bin/python3` for any
google-workspace script call — system python3 lacks the required libs.

## Procedure

### 1. Parse the request

Extract from the user's message:
- Person name(s) (may be multiple attendees)
- Date/time (resolve relative terms — "tomorrow", "next Tuesday", "this
  afternoon" — against the current date, Asia/Kolkata timezone, since that's
  Mahesh's default timezone unless stated otherwise)
- Duration (default 30 minutes if not specified)
- Topic/purpose (may be implicit — infer a reasonable summary if not stated)

If the date/time is genuinely ambiguous (e.g. "next Tuesday" when today IS
a Tuesday — could mean this week or next), ASK rather than guess. Do not
silently pick one interpretation for a real ambiguity.

### 2. Resolve the person to an email address

```bash
GAPI="/Users/apple/.hermes/hermes-agent/venv/bin/python3 /Users/apple/.hermes/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI contacts list --max 200
```

**Contacts status (verified 09 Sep 2026):** the People API is enabled and
the call succeeds, but Mahesh's Google Contacts is currently empty (0
saved contacts) — so lookups will legitimately return no match until he
adds real contacts there. This is a data gap, not an API/auth problem;
do not attempt to "fix" it or work around it programmatically.

Given contacts is empty right now:
- **Contacts API works and exactly one match** -> use that email, proceed.
- **Contacts API errors, or zero/multiple matches** -> ask Mahesh directly
  for the email address; do not guess a plausible-looking email, and do
  not silently retry the same call repeatedly.
- **Multiple matches** (e.g. two "John"s) -> list the candidates (name +
  email) and ask Mahesh which one, before proceeding.
- **Match has no email address on file** -> ask Mahesh for the email.

### 3. Check calendar for conflicts

```bash
$GAPI calendar list --start <ISO_START_OF_DAY> --end <ISO_END_OF_DAY>
```
Look for any existing event overlapping the proposed slot.
- **No conflict** -> proceed to step 4 with the originally requested time.
- **Conflict exists** -> do NOT silently double-book. Propose 1-3 nearby
  alternative slots (same day if possible, checking those don't also
  conflict) and present them alongside the original request when asking
  for confirmation — let Mahesh choose, don't unilaterally reschedule.

### 4. Propose and get EXPLICIT confirmation

Always show, before creating anything:
```
Meeting:
<Person> <email>
<Date> <start>–<end> (IST)
Topic: <topic>
<if conflict was found: "Note: conflicts with <existing event>, alternative slots: ...">

Proceed with creating the meeting and sending the invitation?
```
Use the `clarify` tool for this confirmation, not a plain text question —
it's a real yes/no gate, not a rhetorical one. Do NOT create the event or
send anything until the user explicitly confirms. A non-answer, "maybe",
or an unrelated reply is NOT confirmation — treat it as "not yet", ask again
or stop.

### 5. Execute only after confirmation

```bash
$GAPI calendar create --summary "<topic>" \
  --start <ISO_START-with-timezone-offset> --end <ISO_END-with-timezone-offset> \
  --attendees "<email1>,<email2>" \
  --description "<topic details if any>"
```
ISO times MUST include the `+05:30` (IST) offset explicitly (or convert to
UTC `Z` if the attendee's timezone differs and that's been established) —
never pass a naive datetime string.

Creating the event with `attendees` set automatically sends the calendar
invitation email via Google Calendar's own invite mechanism — no separate
`gmail send` call is needed or wanted for the invite itself.

### 6. Report the result

Confirm to Mahesh: event created, htmlLink, who was invited, and that the
invite email has gone out. If the API call fails, report the exact error —
never claim success without the API response confirming `status: created`.

## Rescheduling / Cancelling

Same confirm-first rule applies. For cancellation:
```bash
$GAPI calendar delete <EVENT_ID>
```
Always confirm which event (show its current details) before deleting.
For rescheduling: confirm old slot -> new slot, then delete + create (or
use a Calendar update call if google_api.py exposes one — check before
assuming delete+recreate is the only path, since delete+recreate loses the
original event ID and any existing RSVPs).

## Non-goals (for now)

- No availability-checking against the *attendee's* calendar (only
  Mahesh's own primary calendar) — Google Calendar doesn't expose another
  user's busy/free without their calendar being shared.
- No automatic timezone detection for external attendees — ask if it
  matters for the specific meeting (e.g. explicitly cross-timezone).
- No trusted auto-approval rule exists yet — every single scheduling
  action requires explicit confirmation, per Mahesh's explicit choice.
  If he later asks to set up an auto-approval rule for a specific
  recurring case, that changes this skill's step 4 — until then, always
  confirm.
