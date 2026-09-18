#!/usr/bin/env python3
"""
Daily AI Tech News Aggregator (standalone — uses requests, no Hermes runtime needed)
Fetches important AI/LLM news from reliable sources, filters junk, structures output.
Runs via cron at 10:30 AM IST daily.

Note: In the Hermes cron environment (with web toolset), the cron job agent
calls web_search/web_extract directly. This script is a fallback for standalone
execution via requests to a search API.
"""

import sys
import json
import re
from datetime import datetime, timezone, timedelta
from textwrap import dedent
from urllib.parse import urlparse, quote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ── Minimal web fetch via requests-compatible stdlib ──────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def http_get(url, headers=None, timeout=15):
    if HAS_REQUESTS:
        r = requests.get(url, headers=headers or {}, timeout=timeout)
        r.raise_for_status()
        return r.text
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")

def ist_now():
    tz = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(tz).strftime("%a %b %d, %Y · %I:%M %p IST")

# ── Search via DuckDuckGo HTML (no API key needed) ───────────────────
def ddg_search(query, limit=5):
    """Search using DuckDuckGo HTML endpoint. Returns list of {title, url, snippet}."""
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    try:
        html = http_get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"  WARN: DDG search failed for '{query[:40]}...': {e}", file=sys.stderr)
        return []

    results = []
    # Parse DDG HTML results
    # Result links are in <a class="result__a" href="...">title</a>
    # Snippets in <a class="result__snippet" href="...">text</a>
    link_pattern = re.compile(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)
    snippet_pattern = re.compile(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', re.DOTALL)

    links = link_pattern.findall(html)
    snippets = snippet_pattern.findall(html)

    for i, (raw_url, title_html) in enumerate(links[:limit]):
        # DDG wraps URLs in redirect
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        # Extract real URL from DDG redirect
        m = re.search(r'uddg=([^&]+)', raw_url)
        if m:
            from urllib.parse import unquote
            real_url = unquote(m.group(1))
        else:
            real_url = raw_url
        snippet = ""
        if i < len(snippets):
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
        if title and real_url.startswith("http"):
            results.append({"title": title, "url": real_url, "snippet": snippet})

    return results

def extract_url(url, char_limit=8000):
    """Fetch a URL and return its text content (basic extraction)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        html = http_get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"  WARN: extract failed for {url[:50]}: {e}", file=sys.stderr)
        return ""

    # Strip scripts, styles, tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:char_limit]


def scrape_and_filter():
    """Search + extract AI news, filter for signal over noise."""
    sources_searched = []
    articles = []

    # ── Phase 1: Search from top AI news sources ──────────────────────
    searches = [
        # Major AI labs directly
        ("OpenAI ChatGPT new model release announcement 2026", 5),
        ("Anthropic Claude new model announcement this week", 5),
        ("Google DeepMind Gemini new model release 2026", 5),
        ("new open source LLM model release this week 2026", 5),
        # AI applications / products
        ("new AI application product launch this week 2026", 5),
        ("AI startup new product release this week", 5),
        # News aggregators / newsletters
        ("The Batch AI newsletter latest edition", 3),
        ("Import AI newsletter recent edition", 3),
        ("AI news roundup this week important stories", 3),
        # Tech press
        ("TechCrunch artificial intelligence news this week", 3),
        ("VentureBeat AI news this week latest", 3),
        ("Ars Technica AI news this week", 3),
        # Community
        ("reddit r/artificial most important AI news this week", 3),
        ("reddit r/LLM new model releases this week", 3),
        # Regulation
        ("AI regulation policy news this week important", 3),
    ]

    print(f"[{ist_now()}] Searching {len(searches)} query streams...", file=sys.stderr)

    for query, limit in searches:
        results = ddg_search(query, limit=limit)
        for item in results:
            url = item.get("url", "")
            title = item.get("title", "")
            if url and title and url not in [a["url"] for a in articles]:
                articles.append({
                    "title": title,
                    "url": url,
                    "snippet": item.get("snippet", ""),
                    "source_query": query,
                })
                sources_searched.append(url)

    print(f"[{ist_now()}] Found {len(articles)} unique articles. Extracting top candidates...", file=sys.stderr)

    # ── Phase 2: Extract full content for top candidates ─────────────
    AUTHORITY_DOMAINS = [
        "openai.com", "anthropic.com", "blog.google", "deepmind.google",
        "arxiv.org", "techcrunch.com", "venturebeat.com", "arstechnica.com",
        "thebatch.ai", "importai.so", "tdrlhub.com", "ai.google",
        "meta.com", "cohere.com", "mistral.ai", "x.ai", "huggingface.co",
        "stability.ai", "midjourney.com", "reddit.com", "wired.com",
        "theverge.com", "reuters.com", "bloomberg.com",
    ]

    def domain_of(url):
        return urlparse(url).netloc.lower()

    def score(a):
        d = domain_of(a["url"])
        auth = any(domain in d for domain in AUTHORITY_DOMAINS if len(domain) > 5)
        has_model = any(kw in a["title"].lower() for kw in ["model", "llm", "gpt", "claude", "gemini", "llama", "mistral", "diffusion", "language model", "multimodal", "reasoning"])
        has_app = any(kw in a["title"].lower() for kw in ["app", "product", "launch", "release", "platform", "tool", "beta", "introduced", "announced", "startup"])
        is_roundup = any(kw in a["title"].lower() for kw in ["weekly", "roundup", "digest", "this week", "latest", "newsletter"])
        s = 0
        if auth: s += 3
        if has_model: s += 2
        if has_app: s += 2
        if is_roundup: s += 1
        return s

    articles.sort(key=score, reverse=True)

    extracted = []
    for i, art in enumerate(articles[:12]):
        url = art["url"]
        content = extract_url(url, char_limit=6000)
        art["content"] = content
        extracted.append(art)

    # ── Phase 3: Categorize ──────────────────────────────────────────
    categories = {
        "🔴 New Model / LLM Release": ["model", "llm", "gpt", "claude", "gemini", "llama", "mistral", "diffusion", "language model", "multimodal", "reasoning model", "arboretica"],
        "🟡 New AI Application / Product": ["app", "product", "launch", "release", "platform", "tool", "beta", "introduced", "announced", "startup", "agent"],
        "🟢 Research / Paper": ["paper", "arxiv", "research", "study", "benchmark", "achieved", "breakthrough", "scientists", "university"],
        "🔵 Company / Business": ["funding", "raised", "acquisition", "partnership", "enterprise", "business", "commercial", "valuation", "billion", "million"],
        "🟣 Regulation / Policy": ["regulation", "eu", "law", "policy", "safety", "ethics", "gov", "legislation", "white house", "executive order"],
    }

    categorized = {k: [] for k in categories}
    uncategorized = []

    for art in extracted:
        title_lower = (art.get("title", "") + " " + art.get("snippet", ""))[:600].lower()
        placed = False
        for cat, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                categorized[cat].append(art)
                placed = True
                break
        if not placed:
            uncategorized.append(art)

    # ── Phase 4: Build structured output ──────────────────────────────
    print(f"[{ist_now()}] Building structured report...", file=sys.stderr)

    lines = []
    lines.append("🤖 DAILY AI TECH NEWS — CURATED")
    lines.append(f"📅 {ist_now()}")
    lines.append("─" * 55)
    lines.append("")

    total = sum(len(v) for v in categorized.values()) + len(uncategorized)
    lines.append(f"📊 {total} articles scanned · top signals below")
    lines.append("")

    section_labels = {
        "🔴 New Model / LLM Release": "🔴 NEW MODELS & LLMs",
        "🟡 New AI Application / Product": "🟡 NEW AI APPS & PRODUCTS",
        "🟢 Research / Paper": "🟢 RESEARCH & PAPERS",
        "🔵 Company / Business": "🔵 COMPANY & BUSINESS",
        "🟣 Regulation / Policy": "🟣 REGULATION & POLICY",
    }

    has_content = False
    for cat, arts in categorized.items():
        if not arts:
            continue
        has_content = True
        label = section_labels.get(cat, cat.upper())
        lines.append(f"─── {label} ({len(arts)}) ───")
        lines.append("")
        for i, art in enumerate(arts, 1):
            title = art.get("title", "Untitled")
            url = art.get("url", "")
            snippet = (art.get("snippet", "") or "")[:200].replace("\n", " ")
            content_snippet = (art.get("content", "") or "")[:200].replace("\n", " ")

            lines.append(f"  {i}. **{title}**")
            if url:
                lines.append(f"     🔗 {url}")
            if snippet:
                lines.append(f"     └ {snippet}")
            elif content_snippet:
                lines.append(f"     📝 {content_snippet}")
            lines.append("")

    if uncategorized:
        has_content = True
        lines.append(f"─── OTHER NEWS ({len(uncategorized)}) ───")
        lines.append("")
        for i, art in enumerate(uncategorized[:4], 1):
            title = art.get("title", "Untitled")
            url = art.get("url", "")
            lines.append(f"  {i}. {title}")
            if url:
                lines.append(f"     🔗 {url}")
            lines.append("")

    if not has_content:
        lines.append("⚠️ No articles extracted this run. Sources may be unavailable.")
        lines.append("")

    lines.append("─" * 55)
    lines.append(f"🔍 Sources: OpenAI, Anthropic, Google DeepMind, TechCrunch AI, VentureBeat AI, Ars Technica, The Batch, Import AI, r/artificial, r/LLM + keyword searches")
    lines.append(f"🕐 Generated: {ist_now()}")
    lines.append("─" * 55)

    return "\n".join(lines)


if __name__ == "__main__":
    report = scrape_and_filter()
    print(report)
