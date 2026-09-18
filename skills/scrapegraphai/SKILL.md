---
name: scrapegraphai
description: Use for ScrapeGraphAI web scraping and AI-driven extraction.
version: 1.0.0
author: Jarvis
category: productivity
---

# ScrapeGraphAI Skill

ScrapeGraphAI is a Python library for AI-driven web scraping using graphs.

## Installation

```bash
pip install scrapegraphai
```

## Usage Example

```python
from scrapegraphai.graphs import SearchGraph

graph = SearchGraph(
    prompt="Find top websites for...",
    source="duckduckgo",
    config={
        'llm': {
            'api_key': 'YOUR_KEY',
            'model': 'gpt-4o'
        },
        'embeddings': {
            'model': 'all-MiniLM-L6-v2'
        }
    }
)
result = graph.run()
```

## Available Graphs

- **SearchGraph**: Search the web
- **SmartScraperGraph**: Scrape a page with AI
- **DeepScraperGraph**: Deep scraping
- **OmniScraperGraph**: Multi-source scraping
- **CSVScraperGraph**: Scrape CSV files
- **JSONScraperGraph**: Scrape JSON
- **MDScraperGraph**: Scrape Markdown
- **ScreenshotScraperGraph**: Take screenshots

## When to Use

- When Firecrawl fails or returns insufficient structured data
- When AI-driven extraction is needed
- For complex semantic extraction tasks
- For graph-based data extraction

## Fallback Protocol

1. Try Firecrawl first for general web tasks
2. If Firecrawl fails, switch to ScrapeGraphAI
3. Validate results
4. Report findings or limitations
