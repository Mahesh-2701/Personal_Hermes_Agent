#!/usr/bin/env python3
"""
Competitor Intelligence - Report Generator

Generates daily and weekly competitor intelligence reports.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
EVENTS_FILE = DATA_DIR / "events" / "events.jsonl"
REPORTS_DIR = DATA_DIR / "reports"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"


def load_events(hours=None, days=None):
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
    
    return events


def load_competitors():
    if COMPETITORS_FILE.exists():
        import yaml
        with open(COMPETITORS_FILE) as f:
            data = yaml.safe_load(f) or {}
        return data.get("competitors", [])
    return []


def group_by_competitor(events):
    grouped = {}
    for event in events:
        entity_name = event.get("entity_name", event.get("entity_id", "unknown"))
        if entity_name not in grouped:
            grouped[entity_name] = []
        grouped[entity_name].append(event)
    return grouped


def format_daily_report(events, competitors):
    today = datetime.utcnow().strftime("%d %B %Y")
    
    output = []
    output.append("=" * 60)
    output.append(f"COMPETITOR INTELLIGENCE")
    output.append(today)
    output.append("=" * 60)
    output.append("")
    
    grouped = group_by_competitor(events)
    
    if not events:
        output.append("IMPORTANT CHANGES")
        output.append("")
        output.append("No significant changes detected today.")
        output.append("")
        output.append("This means automated collection found no meaningful")
        output.append("changes in tracked competitors. Continue monitoring.")
    else:
        output.append("IMPORTANT CHANGES")
        output.append("")
        
        for entity_name, entity_events in sorted(grouped.items()):
            output.append(f"{entity_name}")
            for event in entity_events:
                event_type = event.get("event_type", "unknown").replace("_", " ").title()
                confidence = event.get("confidence", "").upper()
                
                output.append(f"  - {event_type} ({confidence})")
                
                old_val = event.get("old_value", "")
                new_val = event.get("new_value", "")
                if old_val:
                    output.append(f"    Before: {old_val}")
                if new_val:
                    output.append(f"    After:  {new_val}")
            output.append("")
        
        output.append("SOURCES")
        output.append("")
        output.append(f"Events detected: {len(events)}")
        output.append(f"Competitors monitored: {len(competitors)}")
    
    return "\n".join(output)


def format_weekly_report(events, competitors):
    week_start = (datetime.utcnow() - timedelta(days=7)).strftime("%d %B")
    week_end = datetime.utcnow().strftime("%d %B %Y")
    
    output = []
    output.append("=" * 60)
    output.append(f"COMPETITOR INTELLIGENCE - WEEKLY REPORT")
    output.append(f"Week of {week_start} - {week_end}")
    output.append("=" * 60)
    output.append("")
    
    grouped = group_by_competitor(events)
    
    output.append("1. EXECUTIVE SUMMARY")
    output.append("")
    
    total_events = len(events)
    high_confidence = sum(1 for e in events if e.get("confidence") == "high")
    pricing_changes = sum(1 for e in events if "pricing" in e.get("event_type", ""))
    product_changes = sum(1 for e in events if "product" in e.get("event_type", "") or "launch" in e.get("event_type", ""))
    hiring_signals = sum(1 for e in events if "hiring" in e.get("event_type", "") or "job" in e.get("event_type", ""))
    github_activity = sum(1 for e in events if "github" in e.get("event_type", "") or "release" in e.get("event_type", ""))
    
    output.append(f"Total events detected: {total_events}")
    output.append(f"High confidence events: {high_confidence}")
    output.append(f"Pricing changes: {pricing_changes}")
    output.append(f"Product launches/updates: {product_changes}")
    output.append(f"Hiring signals: {hiring_signals}")
    output.append(f"GitHub activity: {github_activity}")
    output.append("")
    
    if events:
        output.append("2. MAJOR COMPETITOR MOVEMENTS")
        output.append("")
        
        for entity_name, entity_events in sorted(grouped.items()):
            high_impact = [e for e in entity_events if e.get("confidence") in ("high", "medium")]
            if high_impact:
                output.append(f"{entity_name}")
                for event in high_impact[:5]:
                    event_type = event.get("event_type", "unknown").replace("_", " ").title()
                    output.append(f"  - {event_type}")
                    if event.get("description"):
                        output.append(f"    {event['description']}")
                output.append("")
    else:
        output.append("No significant events this week.")
        output.append("")
    
    output.append("3. COMPETITOR-BY-COMPETITOR BREAKDOWN")
    output.append("")
    
    for entity_name, entity_events in sorted(grouped.items()):
        output.append(f"{entity_name}")
        for event in entity_events:
            event_type = event.get("event_type", "unknown").replace("_", " ").title()
            output.append(f"  - {event_type} ({event.get('confidence', '').upper()})")
        output.append("")
    
    output.append("4. ITEMS REQUIRING FURTHER INVESTIGATION")
    output.append("")
    low_confidence = [e for e in events if e.get("confidence") == "low"]
    if low_confidence:
        for event in low_confidence[:5]:
            output.append(f"- {event.get('entity_name', 'Unknown')}: {event.get('event_type', 'unknown')}")
            output.append(f"  (Low confidence - may need manual verification)")
    else:
        output.append("No low-confidence items requiring follow-up.")
    output.append("")
    
    output.append("SOURCES")
    output.append("")
    output.append(f"Events analyzed: {len(events)}")
    output.append(f"Competitors tracked: {len(competitors)}")
    output.append(f"Report generated: {datetime.utcnow().isoformat()}")
    
    return "\n".join(output)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Competitor Intelligence Report Generator")
    parser.add_argument("report_type", nargs="?", choices=["daily", "weekly"], 
                        help="Type of report to generate")
    parser.add_argument("--output", action="store_true", help="Save to file")
    parser.add_argument("--days", type=int, default=1, help="Number of days to include")
    args = parser.parse_args()
    
    events = load_events(days=args.days)
    competitors = load_competitors()
    
    if args.report_type == "daily":
        report = format_daily_report(events, competitors)
        report_type = "Daily"
    elif args.report_type == "weekly":
        report = format_weekly_report(events, competitors)
        report_type = "Weekly"
    else:
        parser.print_help()
        return
    
    print(report)
    print("")
    
    if args.output:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        if args.report_type == "daily":
            date_str = datetime.utcnow().strftime("%Y%m%d")
            filename = REPORTS_DIR / f"daily_{date_str}.txt"
        else:
            week_start = (datetime.utcnow() - timedelta(days=7)).strftime("%Y%m%d")
            filename = REPORTS_DIR / f"weekly_{week_start}.txt"
        
        with open(filename, "w") as f:
            f.write(report)
        
        print(f"Report saved to: {filename}")


if __name__ == "__main__":
    main()
