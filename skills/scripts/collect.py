#!/usr/bin/env python3
"""
Competitor Intelligence - Collection Runner

Collects intelligence data for tracked competitors using available collectors.
Uses the cascading fallback chain.
"""

import os
import sys
import json
import yaml
import subprocess
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
EVENTS_FILE = DATA_DIR / "events" / "events.jsonl"
SOURCE_HEALTH_FILE = DATA_DIR / "source_health.json"

FIRECRAWL_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
SGAI_KEY = os.environ.get("SGAI_API_KEY", "")

SCRIPTS_DIR = Path.home() / ".hermes" / "skills" / "competitor-intelligence" / "scripts"

# Import social collection functions
sys.path.insert(0, str(SCRIPTS_DIR))
from social_collect import (
    search_x, search_reddit, search_youtube, search_linkedin,
    save_snapshot as social_save_snapshot,
    save_event as social_save_event,
)
def collect_social(entity_id, competitor):
    """Collect social media data for a competitor. Returns dict of sources."""
    name = competitor.get("name", "")
    if not name:
        return {}
    
    print(f"  Social: {name}")
    
    results = {}
    
    # X/Twitter
    print(f"    X/Twitter...", end=" ")
    tweets = search_x(f"{name} announcement news update")
    if tweets:
        content = json.dumps(tweets, indent=2)
        social_save_snapshot(entity_id, "social_x", content, {
            "source": "x_search",
            "query": f"{name} latest",
            "count": len(tweets),
        })
        results["x"] = content
        print(f"ok ({len(tweets)} posts)")
    else:
        print("none")
        results["x"] = None
    
    # Reddit
    print(f"    Reddit...", end=" ")
    reddit_posts = search_reddit(f"{name} feature product discussion")
    if reddit_posts:
        content = json.dumps(reddit_posts, indent=2)
        social_save_snapshot(entity_id, "social_reddit", content, {
            "source": "reddit_search",
            "query": f"{name} discussion",
            "count": len(reddit_posts),
        })
        results["reddit"] = content
        print(f"ok ({len(reddit_posts)} posts)")
    else:
        print("none")
        results["reddit"] = None
    
    # YouTube
    print(f"    YouTube...", end=" ")
    videos = search_youtube(f"{name} demo announcement product")
    if videos:
        content = json.dumps(videos, indent=2)
        social_save_snapshot(entity_id, "social_youtube", content, {
            "source": "youtube_search",
            "query": f"{name} video",
            "count": len(videos),
        })
        results["youtube"] = content
        print(f"ok ({len(videos)} videos)")
    else:
        print("none")
        results["youtube"] = None
    
    # LinkedIn
    print(f"    LinkedIn...", end=" ")
    linkedin_posts = search_linkedin(f"{name} company update hiring")
    if linkedin_posts:
        content = json.dumps(linkedin_posts, indent=2)
        social_save_snapshot(entity_id, "social_linkedin", content, {
            "source": "linkedin_search",
            "query": f"{name} update",
            "count": len(linkedin_posts),
        })
        results["linkedin"] = content
        print(f"ok ({len(linkedin_posts)} posts)")
    else:
        print("none")
        results["linkedin"] = None
    
    return results


def detect_social_events(entity_id, competitor, social_results):
    """Detect social media events for an entity."""
    name = competitor.get("name", entity_id)
    events_created = []
    
    type_map = {
        "x": "social_post",
        "reddit": "reddit_discussion",
        "youtube": "youtube_video",
        "linkedin": "social_post",
    }
    
    for source_type, content in social_results.items():
        if not content:
            continue
        
        try:
            data = json.loads(content)
            items = data if isinstance(data, list) else data.get("results", [])
            
            if not items or len(items) == 0:
                continue
            
            event_type = type_map.get(source_type, "social_post")
            sources = [f"social_{source_type}"]
            
            recent_items = items[:3]
            title_parts = []
            for item in recent_items:
                title = item.get("title", "")[:120]
                if title:
                    title_parts.append(title)
            
            description = f"{len(items)} social mentions found for {name} on {source_type}"
            if title_parts:
                description += f": {title_parts[0]}"
            
            event = social_save_event(
                entity_id=entity_id,
                entity_name=name,
                event_type=event_type,
                description=description,
                sources=sources,
                confidence="low",
            )
            events_created.append(event)
            
        except (json.JSONDecodeError, TypeError):
            continue
    
    return events_created


def load_competitors():
    if COMPETITORS_FILE.exists():
        with open(COMPETITORS_FILE) as f:
            return yaml.safe_load(f) or {"competitors": []}
    return {"competitors": []}


def save_snapshot(entity_id, source_type, content, metadata=None):
    snapshot_dir = SNAPSHOTS_DIR / entity_id / source_type
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    snapshot_file = snapshot_dir / f"{timestamp}.json"
    
    snapshot_data = {
        "timestamp": timestamp,
        "content": content[:50000] if content else "",
        "metadata": metadata or {},
        "content_hash": hashlib.md5((content or "").encode()).hexdigest() if content else None,
    }
    
    with open(snapshot_file, "w") as f:
        json.dump(snapshot_data, f, indent=2)
    
    current_file = snapshot_dir / "current.json"
    with open(current_file, "w") as f:
        json.dump(snapshot_data, f, indent=2)
    
    return snapshot_file


def update_source_health(entity_id, source_type, status, message=""):
    health = {}
    if SOURCE_HEALTH_FILE.exists():
        with open(SOURCE_HEALTH_FILE) as f:
            health = json.load(f)
    
    if entity_id not in health:
        health[entity_id] = {}
    
    health[entity_id][source_type] = {
        "status": status,
        "last_checked": datetime.utcnow().isoformat(),
        "message": message,
    }
    
    with open(SOURCE_HEALTH_FILE, "w") as f:
        json.dump(health, f, indent=2)


def collect_website(entity_id, competitor):
    website = competitor.get("website", "")
    if not website:
        return None
    
    print(f"  Website: {website}")
    
    # Level 2: Firecrawl
    if FIRECRAWL_KEY:
        try:
            import urllib.request
            
            url = "https://api.firecrawl.dev/v2/scrape"
            data = json.dumps({
                "url": website,
                "formats": ["markdown"],
                "onlyMainContent": True,
            }).encode()
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Authorization": f"Bearer {FIRECRAWL_KEY}",
                    "Content-Type": "application/json",
                },
            )
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
                content = result.get("content", {}).get("markdown", "")
                if content and len(content) > 200:
                    save_snapshot(entity_id, "website", content, {
                        "source": "firecrawl",
                        "url": website,
                    })
                    update_source_health(entity_id, "website", "working")
                    print(f"    OK: Firecrawl ({len(content)} chars)")
                    return content
        except Exception as e:
            print(f"    Firecrawl failed: {e}")
    
    # Level 1: Agent Reach via Jina Reader
    try:
        jina_url = f"https://r.jina.ai/{website}"
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "30", jina_url],
            capture_output=True, text=True, timeout=35
        )
        if result.returncode == 0 and len(result.stdout) > 200:
            content = result.stdout
            save_snapshot(entity_id, "website", content, {
                "source": "jina_reader",
                "url": website,
            })
            update_source_health(entity_id, "website", "working")
            print(f"    OK: Jina Reader ({len(content)} chars)")
            return content
    except Exception as e:
        print(f"    Jina Reader failed: {e}")
    
    # Level 4 fallback: urllib
    try:
        import urllib.request as urllib2
        req = urllib2.Request(
            website,
            headers={"User-Agent": "Mozilla/5.0 (compatible; Hermes-CI/1.0)"}
        )
        with urllib2.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            if len(content) > 200:
                save_snapshot(entity_id, "website", content, {
                    "source": "urllib",
                    "url": website,
                })
                update_source_health(entity_id, "website", "degraded")
                print(f"    OK: urllib ({len(content)} chars)")
                return content
    except Exception as e:
        print(f"    urllib failed: {e}")
    
    update_source_health(entity_id, "website", "failed")
    return None


def collect_github(entity_id, competitor):
    github = competitor.get("github", "")
    if not github:
        return None
    
    print(f"  GitHub: {github}")
    
    # Try gh CLI
    try:
        result = subprocess.run(
            ["gh", "repo", "view", github, "--json",
             "name,description,stargazerCount,updatedAt,language",
             "-q", "."],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            content = result.stdout.strip()
            save_snapshot(entity_id, "github", content, {
                "source": "gh_cli",
                "org": github,
            })
            update_source_health(entity_id, "github", "working")
            print(f"    OK: gh CLI ({len(content)} chars)")
            return content
    except Exception as e:
        print(f"    gh CLI failed: {e}")
    
    # Try GitHub API
    try:
        import urllib.request as urllib2
        api_url = f"https://api.github.com/orgs/{github}"
        req = urllib2.Request(api_url, headers={"User-Agent": "Hermes-CI/1.0"})
        with urllib2.urlopen(req, timeout=10) as resp:
            content = resp.read().decode()
            data = json.loads(content)
            save_snapshot(entity_id, "github", json.dumps(data, indent=2), {
                "source": "github_api",
                "org": github,
            })
            update_source_health(entity_id, "github", "working")
            print(f"    OK: GitHub API ({len(content)} chars)")
            return content
    except Exception as e:
        print(f"    GitHub API failed: {e}")
    
    update_source_health(entity_id, "github", "failed")
    return None


def collect_news(entity_id, competitor):
    name = competitor.get("name", "")
    if not name:
        return None
    
    print(f"  News: {name}")
    
    # Try Firecrawl search
    if FIRECRAWL_KEY:
        try:
            import urllib.request
            
            url = "https://api.firecrawl.dev/v2/search"
            data = json.dumps({
                "query": f"{name} latest news announcements updates",
                "limit": 10,
            }).encode()
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Authorization": f"Bearer {FIRECRAWL_KEY}",
                    "Content-Type": "application/json",
                },
            )
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
                web_results = result.get("data", {}).get("web", [])
                if web_results:
                    content = json.dumps(web_results, indent=2)
                    save_snapshot(entity_id, "news", content, {
                        "source": "firecrawl_search",
                        "query": f"{name} news",
                        "count": len(web_results),
                    })
                    update_source_health(entity_id, "news", "working")
                    print(f"    OK: Firecrawl search ({len(web_results)} results)")
                    return content
        except Exception as e:
            print(f"    Firecrawl search failed: {e}")
    
    # Fallback
    update_source_health(entity_id, "news", "degraded")
    return None


def collect_all_sources(entity_id, competitor):
    sources = competitor.get("sources", {})
    results = {}
    
    if sources.get("website"):
        results["website"] = collect_website(entity_id, competitor)
    
    if sources.get("github"):
        results["github"] = collect_github(entity_id, competitor)
    
    if sources.get("news"):
        results["news"] = collect_news(entity_id, competitor)
    
    if sources.get("social"):
        results["social"] = collect_social(entity_id, competitor)
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Competitor Intelligence Collection")
    parser.add_argument("entity_id", nargs="?", help="Entity ID to collect")
    parser.add_argument("--all", action="store_true", help="Collect all competitors")
    parser.add_argument("--priority-high", action="store_true", help="Only high priority")
    parser.add_argument("--check-errors", action="store_true", help="Check for errors")
    args = parser.parse_args()
    
    competitors_data = load_competitors()
    competitors = competitors_data.get("competitors", [])
    
    if args.check_errors:
        if SOURCE_HEALTH_FILE.exists():
            with open(SOURCE_HEALTH_FILE) as f:
                health = json.load(f)
            print("\nSource Health Status:\n")
            for entity_id, sources in health.items():
                for source, info in sources.items():
                    status = info.get("status", "unknown")
                    icon = "[OK]" if status == "working" else "[FAIL]"
                    print(f"  {icon} {entity_id}/{source}: {status}")
        else:
            print("No source health data yet.")
        return
    
    if args.entity_id:
        competitor = None
        for comp in competitors:
            if comp["id"] == args.entity_id:
                competitor = comp
                break
        
        if not competitor:
            print(f"Competitor not found: {args.entity_id}")
            return
        
        print(f"\n{'='*50}")
        print(f"Collecting: {competitor['name']} ({args.entity_id})")
        print(f"{'='*50}\n")
        
        results = collect_all_sources(args.entity_id, competitor)
        
        print("\nResults:")
        for source, content in results.items():
            status = "OK" if content else "FAIL"
            size = len(content) if content else 0
            print(f"  [{status}] {source}: {size} chars")
    
    elif args.all:
        if args.priority_high:
            competitors = [c for c in competitors if c.get("priority") == "high"]
        
        print(f"\n{'='*50}")
        print(f"Collecting for {len(competitors)} competitor(s)")
        print(f"{'='*50}\n")
        
        for competitor in competitors:
            entity_id = competitor["id"]
            print(f"\n{'='*50}")
            print(f"{competitor['name']} ({entity_id})")
            print(f"{'='*50}")
            
            results = collect_all_sources(entity_id, competitor)
            
            print("\nResults:")
            for source, content in results.items():
                status = "OK" if content else "FAIL"
                size = len(content) if content else 0
                print(f"  [{status}] {source}: {size} chars")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
