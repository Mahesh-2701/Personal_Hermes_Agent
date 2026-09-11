---
name: firecrawl
description: >
  Web research, scraping, and data extraction skill using Firecrawl.
  Provides search, scrape, interact, crawl, map, parse, monitor, and
  research-index capabilities for AI agents. Use when Mahi needs web
  data, competitive research, content extraction, or recurring page monitoring.
  Routes to the right Firecrawl tool based on the task: search for
  discovery, scrape for known URLs, interact for JS-heavy/login pages,
  parse for local documents, monitor for recurring checks, research
  index for papers and GitHub.
version: 1.0.0
author: Jarvis
category: productivity
metadata:
  firecrawl:
    tags: [web, research, scraping, search, firecrawl, data-extraction, monitoring, competitive-intel, ux-research, design-research]
    related_skills: [stichdesign, google-workspace, bloggerwatcher, competitor-news-monitor, arxiv, grounded-citations]
    homepage: https://firecrawl.dev
    category: productivity
---

# Firecrawl Skill

Firecrawl gives you fast, reliable web context with search, scraping, interaction, document parsing, research, and monitoring tools.

Use Firecrawl when Mahi needs:

- **Search** — discover pages by query
- **Scrape** — extract clean content from a known URL
- **Interact** — handle JS-heavy pages, clicks, forms, login
- **Crawl / Map** — bulk extraction or URL discovery across a site
- **Parse** — convert local documents (PDF, DOCX, XLSX, etc.) to markdown
- **Monitor** — recurring page change detection with alerts
- **Research Index** — scientific papers, GitHub issues, PRs, READMEs

---

## When to Use

| Mahi says... | Use... |
|-------------|--------|
| "Find similar products to X" | `search` |
| "Scrape this URL" | `scrape` |
| "Research UX patterns for a dashboard" | `search` + `scrape` top results |
| "This page needs login / clicks" | `interact` |
| "Extract everything from this site" | `crawl` or `map` + `scrape` |
| "Parse this PDF/DOCX" | `parse` |
| "Track when this page changes" | `monitor` |
| "Find academic papers on X" | `research search-papers` |
| "Find related GitHub projects" | `research search-github` |

---

## Credential Check

Before using Firecrawl:

1. Check if `FIRECRAWL_API_KEY` is available in the environment or `.env`
2. If not set, check the keyless free tier (Path F from docs): `npx -y firecrawl-cli@latest scrape <url>` works without a key for search/scrape/interact/parse (rate-limited)
3. If neither works, tell Mahi Firecrawl needs an API key and point him to https://firecrawl.dev/signin

**API key format:** `fc-...`

**Base URL:** `https://api.firecrawl.dev/v2`

**Auth:** `Authorization: Bearer fc-YOUR_API_KEY`

---

## Tool Routing

### Search
Use when you need **discovery** — finding pages by topic.

```bash
# CLI (if installed)
firecrawl search "AI project management dashboard UX" -o results.json

# Or direct API
curl -s -X POST https://api.firecrawl.dev/v2/search \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI project management dashboard UX", "limit": 10}'
```

**When to search:**
- Mahi asks you to find similar products, competitors, design patterns
- You need to discover what exists before designing or building
- You're doing competitive research

**Search tip:** Search multiple angles. Don't stop at the first query.

---

### Scrape
Use when you have a **known URL** and need its content.

```bash
firecrawl scrape "https://example.com" -o content.md
```

**When to scrape:**
- You found a relevant page via search and want its actual content
- Mahi gives you a specific URL
- You need full page text, not just a snippet

**Scrape tip:** Scrape pages that search snippets can't fully answer. Skip low-value pages.

---

### Interact
Use when the page needs **clicks, forms, or login** — plain scrape won't work.

```bash
firecrawl interact "https://example.com/login" \
  --actions '[{"type":"click","selector":"#login-btn"},{"type":"type","selector":"#email","text":"user@example.com"}]'
```

**When to interact:**
- The page is JS-heavy or behind a login
- You need to click buttons, fill forms, navigate after load
- Scrape returns empty or incomplete content

---

### Crawl / Map
Use for **bulk extraction** across a site.

```bash
# Map — discover all URLs first
firecrawl map "https://example.com" -o urls.json

# Crawl — extract content from many pages
firecrawl crawl "https://example.com" -o crawled.json
```

**When to use:**
- You need content from a whole site or section
- Map first to discover URLs, then scrape/crawl the relevant ones
- Don't crawl the entire web — be targeted

---

### Parse
Use for **local documents** — PDF, DOCX, XLSX, etc.

```bash
firecrawl parse ./report.pdf -o report.md
```

**When to parse:**
- Mahi gives you a local file (PDF, DOCX, XLSX, HTML, etc.)
- The document doesn't have a public URL (use scrape for public URLs)
- You need clean markdown from a document

**Note:** Parse accepts files up to 50MB. Upload as multipart/form-data.

---

### Monitor
Use for **recurring change detection** — alert when a page changes.

```bash
firecrawl monitor create \
  --name "competitor-pricing" \
  --urls "https://example.com/pricing" \
  --schedule "every 24h" \
  --goal "Detect changes to pricing plans or new feature announcements"
```

**When to use:**
- Mahi wants to track a page over time ("alert me when...")
- The same URL needs checking repeatedly
- You want recurring checks with AI-powered change filtering

**Prefer monitor over repeated one-off scrapes** whenever the request implies recurrence.

---

### Research Index
Use for **academic papers and GitHub** research.

```bash
# Search papers
firecrawl research search-papers "reinforcement learning for UI generation"

# Inspect a paper
firecrawl research inspect-paper <paper-id>

# Find related papers
firecrawl research related-papers <paper-id>

# Search GitHub
firecrawl research search-github "AI coding agent UI"
```

**When to use:**
- Mahi asks about research, papers, academic work
- You need GitHub issues, PRs, READMEs for a technology
- The topic is technical/scientific and papers are relevant

---

## Default Workflow for Web Research

When Mahi asks you to research something online:

1. **Start with search** — discover what exists
2. **Identify the most relevant sources** — don't scrape everything
3. **Scrape important pages** — get actual content, not snippets
4. **Extract what matters** — patterns, features, data points
5. **Synthesize** — combine findings into a useful summary
6. **Cite sources** — keep URLs so claims are traceable

If the task becomes "wire Firecrawl into product code," that's a different path (build skills). For now, you're doing agent-side web work.

---

## Firecrawl in the StichDesign Workflow

In the stichdesign skill, Firecrawl is the **research layer** (Step 2).

When designing a UI:

1. Understand the product (Step 1)
2. **Research similar products with Firecrawl** (Step 2)
   - Search for competitors, similar products, UX patterns
   - Scrape top results for actual UI/content
   - Analyze patterns
3. Design direction (Step 3)
4. Generate Stitch design (Step 4)
5. Review (Step 5)
6. Present (Step 6)

**Research rules for design:**
- Research should influence design, not become copying
- Learn from established UX patterns
- Identify proven interaction models
- Combine ideas from multiple products
- Adapt to Mahi's actual requirements
- Do NOT clone competitors or copy branding

---

## Error Handling

If a Firecrawl call fails or returns unexpected output:

1. Check the API key is valid
2. Check rate limits (keyless tier is more limited)
3. Try a simpler query/scrape first
4. Use `firecrawl ask <jobId>` to diagnose: `POST https://api.firecrawl.dev/v2/support/ask` with `{question, jobId}`

---

## Rate Limits and Keyless Tier

| Tier | What's available | Limits |
|------|------------------|--------|
| **Keyless free** | search, scrape, interact, parse, research index | Rate-limited. Use as fallback. |
| **API key (free account)** | Full set of endpoints | Higher limits, all endpoints |
| **Paid** | Full capabilities, higher quotas | Depends on plan |

**Prefer getting an API key** when possible — it unlocks the full set of endpoints and higher limits. The keyless tier is a fallback.

Keyless access points:
- **CLI:** `npx -y firecrawl-cli@latest` (search, scrape, interact, parse work keyless)
- **MCP:** `https://mcp.firecrawl.dev/v2/mcp`
- **API:** research index endpoints work without Authorization header

---

## Quick Reference

```bash
# Search
firecrawl search "<query>" -o results.json

# Scrape
firecrawl scrape "<url>" -o content.md

# Interact
firecrawl interact "<url>" --actions '[...]'

# Map a site
firecrawl map "<url>" -o urls.json

# Crawl
firecrawl crawl "<url>" -o crawled.json

# Parse a document
firecrawl parse ./file.pdf -o file.md

# Monitor
firecrawl monitor create --name "<name>" --urls "<url>" --schedule "<sched>" --goal "<goal>"

# Research papers
firecrawl research search-papers "<query>"

# Research GitHub
firecrawl research search-github "<query>"
```

---

## Sources

- API docs: https://docs.firecrawl.dev
- Skills repo: https://github.com/firecrawl/skills
- Sign up: https://firecrawl.dev/signin
