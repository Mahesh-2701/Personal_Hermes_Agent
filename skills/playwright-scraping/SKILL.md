---
name: playwright-scraping
description: Scraping JS-heavy sites with Playwright.
version: 1.0.0
author: Jarvis
category: productivity
---

# Playwright Web Scraping Skill

Direct browser-based scraping for accurate extraction from JavaScript-heavy websites.

## When to Use

- Firecrawl fails or returns empty (JS-heavy SPAs)
- Need accurate rendering of dynamic pages
- Need screenshots of pages
- Need to scroll to trigger lazy content
- Need to detect libraries/frameworks a page uses
- Need full control over scraping

## Why Playwright Beats API Scrapers

| Aspect | Firecrawl | Playwright |
|--------|-----------|------------|
| JS execution | Limited | Full browser |
| Rate limits | 12/min | None |
| Blocked sites | Many | None |
| Screenshots | No | Full page PNG |
| Scroll | No | Full control |
| Lib detection | No | From bundle |

## Install

```bash
pip install playwright
playwright install chromium
```

## Basic Scrape

```python
import asyncio
from playwright.async_api import async_playwright

async def scrape(url, scroll=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        for _ in range(scroll):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
        html = await page.content()
        text = await page.evaluate("document.body.innerText")
        shot = await page.screenshot(full_page=True)
        await browser.close()
        return {"html": html, "text": text, "screenshot": shot}

r = asyncio.run(scrape("https://example.com"))
```

## Detect Animation Libraries

```python
async def detect_libs(page):
    return await page.evaluate("""
        () => {
            const chk = n => { try { return window[n] ? 'yes' : 'no'; } catch { return 'no'; } };
            return { gsap: chk('gsap'), three: chk('three'), framer: chk('framerMotion') };
        }
    """)
```

## Analyze JS Bundle

```python
import urllib.request, re

def analyze(url):
    js = urllib.request.urlopen(url).read().decode()
    pats = {
        'GSAP': [r'gsap\.', r'\.to\(', r'\.from\(', r'ScrollTrigger'],
        'Three.js': [r'THREE\.', r'three'],
        'Framer': [r'framer-motion', r'motion/react'],
    }
    return {lib: sum(len(re.findall(p, js, re.I)) for p in ps) for lib, ps in pats.items() if sum(len(re.findall(p, js, re.I)) for p in ps) > 0}

print(analyze("https://music.apple.com/assets/index~8bc3c631ba.js"))
# {'GSAP': 40, 'Three.js': 3}
```

## Full Workflow

1. Scrape page with Playwright (scroll, screenshot, extract scripts)
2. Download main JS bundle
3. Run pattern analysis (GSAP, Three.js, Framer refs)
4. Extract page structure (classes, IDs, scripts)
5. Feed all to Solar for deep analysis

## Example Analysis Script

```python
import json, re, urllib.request

with open("results.json") as f:
    data = json.load(f)

html = data["html"]

# Animation classes
classes = re.findall(r'class="([^"]+)"', html)
anim = set(c for cl in classes for c in cl.split() if any(k in c.lower() for k in ['anim','fade','slide','trans','motion']))

# Section IDs
ids = re.findall(r'id="([^"]+)"', html)
hero = [i for i in ids if 'hero' in i.lower()]

print(f"Anim classes: {len(anim)}, Hero sections: {len(hero)}")
```

## Tech Stack Detection

- `_next/static` in scripts = Next.js
- `svelte` refs in bundle = SvelteKit
- `gsap` refs = GSAP animations
- `THREE` refs = Three.js 3D
- Tailwind classes = Tailwind CSS

## Limitations

- Need `playwright install chromium`
- Some sites detect headless
- Large pages need truncation
- Full-page screenshots are big

## Files

- `/tmp/playwright_scrape.py` - Main script
- `/tmp/analyze_bundles.py` - Bundle analyzer
- `/tmp/scraping_results.json` - Example output
- `/tmp/analysis_summary.txt` - Example analysis
