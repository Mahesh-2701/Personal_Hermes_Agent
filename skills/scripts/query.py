#!/usr/bin/env python3
"""Competitor Intelligence - Query Interface"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
EVENTS_FILE = DATA_DIR / "events" / "events.jsonl"
REPORTS_DIR = DATA_DIR / "reports"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"


def load_events(hours=None, days=None, event_types=None):
    events = []
    if not EVENTS_FILE.exists():
        return events
    
    cutoff = None
    if hours:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
    elif days:
        cutoff = datetime.utcnow() - timedelta(days=days)
    
    with open(EVENTS_FILE) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                if cutoff:
                    event_time = datetime.fromisoformat(event.get("detected_at", ""))
                    if event_time >= cutoff:
                        events.append(event)
                else:
                    events.append(event)
            except (json.JSONDecodeError, ValueError):
                continue
    
    if event_types:
        events = [e for e in events if e.get("event_type") in event_types]
    
    return events


def load_competitors():
    if COMPETITORS_FILE.exists():
        import yaml
        with open(COMPETITORS_FILE) as f:
            data = yaml.safe_load(f) or {}
        return data.get("competitors", [])
    return []


def resolve_query(query):
    query_lower = query.lower()
    competitors = load_competitors()
    
    days = 1
    if "today" in query_lower:
        days = 1
    elif "this week" in query_lower or "week" in query_lower:
        days = 7
    elif "this month" in query_lower or "month" in query_lower:
        days = 30
    elif "all" in query_lower or "ever" in query_lower:
        days = 365
    
    event_type_filter = None
    type_map = {
        "pricing": "pricing_change",
        "product": ["product_launch", "product_update", "feature_added", "feature_removed"],
        "hiring": ["hiring_change", "job_opened"],
        "github": ["github_release", "github_activity"],
        "news": "company_news",
        "website": "website_change",
    }
    
    for keyword, types in type_map.items():
        if keyword in query_lower:
            event_type_filter = types
            break
    
    entity_filter = None
    for comp in competitors:
        name = comp["name"].lower()
        comp_id = comp["id"].lower()
        if name in query_lower or comp_id in query_lower:
            entity_filter = comp["id"]
            break
    
    events = load_events(days=days, event_types=event_type_filter)
    
    if entity_filter:
        events = [e for e in events if e.get("entity_id") == entity_filter]
    
    events.sort(key=lambda e: e.get("detected_at", ""), reverse=True)
    
    return events, competitors, entity_filter


def format_response(events, competitors, entity_filter, query):
    lines = []
    
    if not competitors:
        lines.append("No competitors are being tracked yet.")
        return "\n".join(lines)
    
    if entity_filter:
        comp = next((c for c in competitors if c["id"] == entity_filter), None)
        if comp:
            lines.append(f"Competitor: {comp['name']}")
            lines.append(f"  Website: {comp.get('website', 'N/A')}")
            lines.append(f"  GitHub: {comp.get('github', 'N/A')}")
            lines.append(f"  Priority: {comp.get('priority', 'medium')}")
            lines.append("")
    
    if not events:
        if entity_filter:
            comp_name = next((c["name"] for c in competitors if c["id"] == entity_filter), "Unknown")
            lines.append(f"No significant changes detected for {comp_name} in this time period.")
        else:
            lines.append("No significant changes detected across tracked competitors.")
        lines.append("")
        lines.append("Note: Automated collection found no meaningful changes.")
        lines.append("Sources may not have been checked yet, or changes")
        lines.append("may be below the detection threshold.")
        return "\n".join(lines)
    
    lines.append(f"Found {len(events)} event(s):\n")
    
    by_competitor = {}
    for event in events:
        comp_name = event.get("entity_name", event.get("entity_id", "unknown"))
        if comp_name not in by_competitor:
            by_competitor[comp_name] = []
        by_competitor[comp_name].append(event)
    
    for comp_name, comp_events in sorted(by_competitor.items()):
        lines.append(f"{comp_name}")
        for event in comp_events:
            event_type = event.get("event_type", "unknown").replace("_", " ").title()
            confidence = event.get("confidence", "").upper()
            detected = event.get("detected_at", "")[:10]
            
            lines.append(f"  [{detected}] {event_type} ({confidence})")
            
            old_val = event.get("old_value", "")
            new_val = event.get("new_value", "")
            if old_val:
                lines.append(f"    Before: {old_val}")
            if new_val:
                lines.append(f"    After:  {new_val}")
            
            desc = event.get("description", "")
            if desc:
                lines.append(f"    {desc}")
        lines.append("")
    
    lines.append(f"Total: {len(events)} events across {len(by_competitor)} competitor(s)")
    return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Competitor Intelligence Query")
    parser.add_argument("query", nargs="?", help="Natural language query")
    parser.add_argument("--entity", help="Filter by entity ID")
    parser.add_argument("--hours", type=int, help="Last N hours")
    parser.add_argument("--days", type=int, help="Last N days")
    parser.add_argument("--type", help="Filter by event type")
    parser.add_argument("--list", action="store_true", help="List tracked competitors")
    args = parser.parse_args()
    
    if args.list:
        competitors = load_competitors()
        if not competitors:
            print("No competitors tracked yet.")
        else:
            print(f"Tracked Competitors ({len(competitors)}):\n")
            for comp in competitors:
                print(f"  {comp['name']} ({comp['id']})")
                print(f"    Website: {comp.get('website', 'N/A')}")
                print(f"    GitHub: {comp.get('github', 'N/A')}")
                print(f"    Priority: {comp.get('priority', 'medium')}")
                print()
        return
    
    if not args.query:
        parser.print_help()
        return
    
    events, competitors, entity_filter = resolve_query(args.query)
    response = format_response(events, competitors, entity_filter, args.query)
    print(response)


if __name__ == "__main__":
    main()
