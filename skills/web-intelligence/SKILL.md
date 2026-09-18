---
name: web-intelligence
description: Use for Firecrawl and ScrapeGraphAI web extraction.
version: 1.0.0
author: Jarvis
category: productivity
---

# Web Intelligence Protocol

## Dual Web Extraction System

1. **Firecrawl** (Primary): Discovery, scraping, crawling, interaction, agentic research.
2. **ScrapeGraphAI** (Specialist/Fallback): Complex AI-driven structured extraction.

## Workflow Strategy

1. **Classify**: Is this discovery (Firecrawl), standard scrape (Firecrawl), or complex semantic extraction (ScrapeGraphAI)?
2. **Execute**: Run primary engine.
3. **Validate**: Check completeness, relevance, and structure.
4. **Fallback**: If primary fails, switch engine and retry once.
5. **Report**: Return accurate, cited results or honest limitations.

## When to use which

- **Firecrawl**: Search, known URL scrape, map, crawl, interact (clicks/forms), agentic research.
- **ScrapeGraphAI**: Complex structured data, graph-based extraction, semantic extraction, or when Firecrawl yields malformed results.

## Failure Protocol
- Never assume success.
- If one engine fails or provides poor data, switch to the other immediately.
- Use cascading strategy: Simple -> Search -> Discovery -> Interact -> Complex Extraction.
- Do not repeat same failed operation twice.

## Traceability
- Always preserve source URLs.
- Verify structured output against the requested schema.
