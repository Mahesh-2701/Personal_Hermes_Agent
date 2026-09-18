#!/usr/bin/env python3
"""
Competitor Intelligence — Diff Engine

Compares current snapshots against previous ones to detect meaningful changes.
Generates events for detected changes.
"""

import os
import sys
import json
import re
import subprocess
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
EVENTS_FILE = DATA_DIR / "events" / "events.jsonl"
SOURCE_HEALTH_FILE = DATA_DIR / "source_health.json"

FIRECRAWL_KEY = os.environ.get("FIRECRAWL_API_KEY", "")


def load_competitors():
    if (DATA_DIR / "competitors.yaml").exists():
        import yaml
        with open(DATA_DIR / "competitors.yaml") as f:
            data = yaml.safe_load(f) or {}
        return data.get("competitors", [])
    return []


def get_current_snapshot(entity_id, source_type):
    current_file = SNAPSHOTS_DIR / entity_id / source_type / "current.json"
    if current_file.exists():
        with open(current_file) as f:
            return json.load(f)
    return None


def get_previous_snapshot(entity_id, source_type):
    snapshot_dir = SNAPSHOTS_DIR / entity_id / source_type
    if not snapshot_dir.exists():
        return None
    
    snapshots = sorted(snapshot_dir.glob("*.json"))
    snapshots = [s for s in snapshots if s.name != "current.json"]
    
    if not snapshots:
        return None
    
    with open(snapshots[-1]) as f:
        return json.load(f)


def compute_hash(content):
    if not content:
        return None
    return hashlib.sha256(content.encode()).hexdigest()


def has_meaningful_change(old_snap, new_snap):
    old_content = old_snap.get("content", "")
    new_content = new_snap.get("content", "")
    
    if not old_content or not new_content:
        return False
    
    old_hash = compute_hash(old_content)
    new_hash = compute_hash(new_content)
    
    return old_hash != new_hash


def detect_content_changes(old_content, new_content):
    changes = []
    
    old_text = re.sub(r'<[^>]+>', ' ', old_content)
    new_text = re.sub(r'<[^>]+>', ' ', new_content)
    
    old_text = re.sub(r'\s+', ' ', old_text).strip()
    new_text = re.sub(r'\s+', ' ', new_text).strip()
    
    if len(old_text) < 200 or len(new_text) < 200:
        return changes
    
    words_old = set(old_text.lower().split())
    words_new = set(new_text.lower().split())
    
    significant_added = words_new - words_old
    significant_added = {w for w in significant_added if len(w) > 3}
    
    significant_removed = words_old - words_new
    significant_removed = {w for w in significant_removed if len(w) > 3}
    
    interesting_keywords = [
        'pricing', 'plans', 'features', 'api', 'enterprise', 'business',
        'pro', 'premium', 'free', 'trial', 'launch', 'new', 'update',
        'release', 'version', 'feature', 'security', 'privacy', 'compliance',
        'team', 'collaboration', 'ai', 'ml', 'machine', 'learning', 'llm',
        'automation', 'workflow', 'agent', 'assistant', 'integration',
    ]
    
    interesting_added = significant_added & set(interesting_keywords)
    interesting_removed = significant_removed & set(interesting_keywords)
    
    if interesting_added:
        changes.append({
            "type": "content_added",
            "description": f"New content detected ({len(interesting_added)} significant keywords)",
            "keywords": sorted(interesting_added)[:10],
        })
    
    if interesting_removed:
        changes.append({
            "type": "content_removed", 
            "description": f"Content appears to have been modified",
            "keywords": sorted(interesting_removed)[:10],
        })
    
    old_hash = compute_hash(old_text)
    new_hash = compute_hash(new_text)
    
    if old_hash != new_hash:
        changes.append({
            "type": "content_modified",
            "description": "Website content has been modified",
        })
    
    return changes


def detect_github_changes(old_data, new_data):
    changes = []
    
    try:
        old_json = json.loads(old_data) if isinstance(old_data, str) else old_data
        new_json = json.loads(new_data) if isinstance(new_data, str) else new_data
        
        old_stars = old_json.get("stargazerCount", 0)
        new_stars = new_json.get("stargazerCount", 0)
        
        if isinstance(old_stars, (int, float)) and isinstance(new_stars, (int, float)):
            if old_stars != new_stars:
                changes.append({
                    "type": "stars_changed",
                    "old_value": old_stars,
                    "new_value": new_stars,
                    "description": f"Stars changed from {old_stars} to {new_stars}",
                })
        
        old_updated = old_json.get("updatedAt", "")
        new_updated = new_json.get("updatedAt", "")
        
        if old_updated != new_updated and old_updated and new_updated:
            changes.append({
                "type": "last_updated_changed",
                "old_value": old_updated,
                "new_value": new_updated,
                "description": f"Last updated changed",
            })
        
        old_desc = old_json.get("description", "")
        new_desc = new_json.get("description", "")
        
        if old_desc != new_desc and old_desc and new_desc:
            changes.append({
                "type": "description_changed",
                "old_value": old_desc[:200] if old_desc else "",
                "new_value": new_desc[:200] if new_desc else "",
                "description": "Repository description changed",
            })
    
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass
    
    return changes


def save_event(event):
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def create_event(entity_id, source_type, changes, competitor=None):
    entity_name = competitor.get("name", entity_id) if competitor else entity_id
    
    events_created = []
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    entity_hash = hashlib.md5(entity_id.encode()).hexdigest()[:8]
    
    for change in changes:
        event_type = "website_change"
        old_value = change.get("old_value", "")
        new_value = change.get("new_value", "")
        confidence = "medium"
        
        if change.get("type") == "stars_changed":
            event_type = "github_activity"
            confidence = "high"
        elif change.get("type") == "content_modified":
            event_type = "website_change"
        elif change.get("type") in ("content_added", "added_content"):
            event_type = "website_change"
            confidence = "low"
        elif change.get("type") == "description_changed":
            event_type = "github_activity"
            confidence = "medium"
        
        event = {
            "event_id": f"{timestamp}{entity_hash}",
            "entity_id": entity_id,
            "entity_name": entity_name,
            "event_type": event_type,
            "detected_at": datetime.utcnow().isoformat(),
            "source_type": source_type,
            "source_url": competitor.get("website", "") if source_type == "website" else "",
            "old_value": old_value,
            "new_value": new_value,
            "confidence": confidence,
            "description": change.get("description", "Change detected"),
            "event_sources": [source_type] if source_type else [],
            "status": "new",
        }
        
        events_created.append(event)
    
    return events_created


def run_diff(entity_id, source_type="website"):
    competitor_data = load_competitors()
    competitor = None
    
    for comp in competitor_data:
        if comp["id"] == entity_id:
            competitor = comp
            break
    
    old_snap = get_previous_snapshot(entity_id, source_type)
    new_snap = get_current_snapshot(entity_id, source_type)
    
    if not old_snap or not new_snap:
        print(f"  No previous snapshot for {entity_id}/{source_type}")
        return False
    
    if not has_meaningful_change(old_snap, new_snap):
        print(f"  No change for {entity_id}/{source_type}")
        return False
    
    old_content = old_snap.get("content", "")
    new_content = new_snap.get("content", "")
    
    changes = []
    if source_type == "github":
        changes = detect_github_changes(old_content, new_content)
    elif source_type == "website":
        changes = detect_content_changes(old_content, new_content)
    else:
        changes = detect_content_changes(old_content, new_content)
    
    if not changes:
        print(f"  No specific changes for {entity_id}/{source_type}")
        return False
    
    events = create_event(entity_id, source_type, changes, competitor)
    
    for event in events:
        save_event(event)
        print(f"  EVENT: {event['event_type']} for {entity_id}")
        print(f"    {event.get('description', 'Change detected')}")
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Competitor Intelligence Diff Engine")
    parser.add_argument("entity_id", nargs="?", help="Entity ID to diff")
    parser.add_argument("--all", action="store_true", help="Diff all competitors")
    parser.add_argument("--source", default="website", help="Source type to check")
    parser.add_argument("--list", action="store_true", help="List recent events")
    args = parser.parse_args()
    
    if args.list:
        if EVENTS_FILE.exists():
            with open(EVENTS_FILE) as f:
                events = []
                for line in f:
                    if line.strip():
                        try:
                            events.append(json.loads(line))
                        except:
                            continue
            
            if events:
                events.sort(key=lambda e: e.get("detected_at", ""), reverse=True)
                print(f"\nRecent Events ({len(events)} total):\n")
                for event in events[:10]:
                    print(f"  {event['detected_at'][:10]} | {event['entity_name']}")
                    print(f"    Type: {event['event_type']}")
                    print(f"    Confidence: {event['confidence']}")
                    if event.get("old_value") or event.get("new_value"):
                        if event.get("old_value"):
                            print(f"    Before: {event['old_value']}")
                        if event.get("new_value"):
                            print(f"    After:  {event['new_value']}")
                    print()
            else:
                print("No events recorded yet.")
        else:
            print("No events file found.")
        return
    
    if args.entity_id:
        result = run_diff(args.entity_id, args.source)
        status = "Changes detected" if result else "No changes"
        print(f"\nDiff for {args.entity_id}/{args.source}: {status}")
    elif args.all:
        competitors = load_competitors()
        print(f"\nDiffing {len(competitors)} competitor(s)...\n")
        
        for comp in competitors:
            entity_id = comp["id"]
            print(f"--- {comp['name']} ({entity_id}) ---")
            
            for source in ["website", "github", "news"]:
                print(f"  Checking {source}...")
                run_diff(entity_id, source)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
