---
name: hermes-command-interface
description: "Handle on-demand section/briefing requests via query CLI."
version: 1.0.0
author: Hermes Agent (built for Mahesh's personal ops system)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ops, query, telegram, on-demand, morning-brief]
    related_skills: [google-workspace, meeting-scheduling]
---

# Command Interface (Phase 28 revisited)

Handles on-demand natural-language requests for Mahesh's personal ops
data -- "show pending payments", "what meetings today", "give me today's
briefing", "why is project X at risk", "what changed in AI today" --
without waiting for the 8am cron or dumping the full 10-section report
when only one section was asked for.

This is a QUERY, not a workflow run. No state changes.

CRITICAL RULE -- NEVER SUMMARIZE OR CONDENSE: relay the script's printed
output VERBATIM -- same line breaks, same bullets, same numbers, same
wording. Do NOT paraphrase it into shorter prose, do NOT skip items to
save space, do NOT merge multiple sections into one paragraph. Mahesh has
explicitly reported this failure mode before ("it shows a simple chat
with some details only") -- treat any urge to summarize as a bug to avoid.

FOR A FULL BRIEFING REQUEST ("morning overview", "daily brief", "today's
briefing", "today's priorities", "full report"): Mahesh wants to see ALL
10 sections presented distinctly, the same way the 8am cron delivers them
as 10 separate Telegram messages -- not one squashed paragraph. Do this:

1. Run `--full-text` to get all sections with real data.
2. If you are replying inside a Telegram chat: call
   `providers.telegram_client.send_message(chat_id, text)` ONCE PER
   SECTION (split on the double-newline between sections, or reuse
   `telegram_client.split_for_telegram` per section like the cron does),
   the same way `workflows/morning_brief_report.py`'s own `main()` does.
   This is NOT double-delivery -- you are fulfilling Mahesh's live,
   explicit request right now, not re-triggering the scheduled cron job.
3. If you are NOT on Telegram (e.g. CLI chat): paste every section as a
   clearly separated block in your reply, each with its own header line,
   verbatim body text, in the same order as `--list-sections`. Never
   compress multiple sections into a single narrative paragraph.

FOR A SINGLE-SECTION REQUEST ("show pending payments", "what meetings
today"): just that one section's verbatim body, still not summarized.

Note: `overview` slug alone is ONLY the 5-item Morning Overview section
(top cross-domain priorities) -- it is NOT the same as a full briefing.
If Mahesh says "morning overview" meaning "my daily brief", treat it as
a full-briefing request per above, not just the overview slug.

## Procedure for a plain section request

1. Map the request to a slug (table below).
2. Run:
```bash
PYTHONPATH=/Users/apple/.hermes/ops /Users/apple/.hermes/hermes-agent/venv/bin/python3 /Users/apple/.hermes/ops/workflows/morning_brief_report.py --section <slug>
```
3. Relay the printed output VERBATIM as your reply -- do not summarize
   or shorten it (see the critical rule above). If it prints an error to
   stderr ("Unknown or unavailable section"), say so plainly.

For "give me today's briefing" / "today's priorities" / "full report",
use `--full-text` and follow the FULL BRIEFING procedure above (section-
by-section delivery, not a condensed summary).

## Slug reference

| Mahesh says... | slug |
|---|---|
| pending payments, invoices, overdue payments | `payments` |
| important emails, inbox | `emails` |
| meetings today, calendar | `calendar` |
| pending tasks, my tasks | `tasks` |
| project status, overdue projects | `projects` |
| Simbli leads, Simbli update | `simbli` |
| sales opportunities, pipeline | `sales` |
| cross-domain insights, connections | `correlation` |
| alerts, action required | `alerts` |
| top priorities, overview | `overview` |

`--list-sections` prints all valid slugs if you need to double check one.

## Reasoning-required queries (NOT a plain section dump)

- **"Why is project X at risk?"** -> run `--section projects`, find the
  specific project, then explain using FACT (what the data literally
  says) vs INFERENCE (your reasoning about why) -- never invent a reason
  the data doesn't support.
- **"What changed in AI today?"** -> read the LATEST file in
  `~/.hermes/cron/output/4674b442d478/` (the AI intelligence cron's own
  output) rather than re-running that cron -- it does real web scraping
  and takes ~3 minutes. Only trigger a fresh run if Mahesh explicitly
  asks for one. If today's file doesn't exist yet, say so plainly.
- **"Remind me about my next meeting"** -> run `--section calendar`,
  extract just the next upcoming event, don't dump the whole section.

## Non-goals

This skill only re-exposes existing provider data on demand -- it adds
no new data sources. If a section is unavailable (provider returned
`ok: False`), relay that honestly. Do not retry silently in a loop.
