Skill creation rule (user's explicit instruction): When user asks to create a new app or existing codebase, follow fullstack-builder 15-stage workflow. Create skills one by one, don't break existing ones. Pull skills from referenced websites and add to improve. Never treat code generation as feature completion.
§
Cron Workflow: cronjob(list) shows jobs, cronjob(run, job_id) triggers. Batch runs parallel. 3 CRM jobs blocked by sandbox Python restrictions.
§
Workflow & Philosophy: Understand complexity -> Propose approach -> Execute -> Verify -> 3-level explanation (Trivial/Meaningful/Architectural) -> Coach senior judgment (don't make user dependent). Use fullstack-builder for coding tasks.
§
User preference: For coding tasks, Hermes must ask whether to use 'Codex CLI' or 'Antigravity CLI (agy)' before proceeding, unless a specific tool is explicitly requested in the prompt. Default to the user's selected choice for the duration of that task.
§
Skill: hermes-role-bots-operations created — multi-bot (CMO/Manager/Employee) Telegram deployment, pairing per-bot-home, model inheritance from main config (don't override per-bot), CRM skill tested. Pitfall: "token limit" errors mask insufficient paid-model credits. See references/multi-bot-crm-integration.md.
§
Web Intelligence Protocol: Firecrawl primary engine for web discovery/scraping. If Firecrawl fails, switch to ScrapeGraphAI as fallback. Mahesh explicitly stated: 'if firecrawl fails use scrapegraphai only'.
§
Mahesh building animated React/Next.js website, researching top animated sites (Apple Music, OpenAI Astra 6) for animation tech stack inspiration (GSAP, Framer Motion, Three.js, etc.).
§
User is asking about data loss after a Hermes update. Specifically asking about 'old memory', 'context', and 'souls' (likely referring to skills or persistent data).
§
Mahesh knows how to use 'hermes cron' CLI commands and prefers using the terminal for managing system tasks rather than expecting AI-only tools. He wants to know why his cron jobs were "lost" (they were just in a different tool namespace) and wants to be hands-on with managing/fixing them.