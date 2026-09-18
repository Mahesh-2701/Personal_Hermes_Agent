#!/usr/bin/env python3
"""
Competitor Intelligence - Alert System

Generates alerts for significant competitor events with deduplication.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
EVENTS_FILE = DATA_DIR / "events" / "events.jsonl"
ALERTS_FILE = DATA_DIR / "alerts" / "alert_state.json"
COOLDOWN_HOURS = 24


def load_events(days=1):
    events = []
    if not EVENTS_FILE.exists():
        return events
    
    cutoff = datetime.utcnow() - timedelta(days=days)
    with open(EVENTS_FILE) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                event_time = datetime.fromisoformat(event.get("detected_at", ""))
                if event_time >= cutoff:
                    events.append(event)
            except:
                continue
    return events


def load_alert_state():
    if ALERTS_FILE.exists():
        with open(ALERTS_FILE) as f:
            return json.load(f)
    return {"alerted": {}}


def save_alert_state(state):
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTS_FILE, "w") as f:
        json.dump(state, f, indent=2)


def should_alert(event, state):
    key = f"{event.get('entity_id')}:{event.get('event_type')}"
    for k, t in state.get("alerted", {}).items():
        if k == key:
            last = datetime.fromisoformat(t)
            if datetime.utcnow() - last < timedelta(hours=COOLDOWN_HOURS):
                return False
    return True


def get_significant(events):
    sig_types = {"pricing_change", "product_launch", "feature_added", 
                 "feature_removed", "hiring_change", "funding", 
                 "acquisition", "leadership_change"}
    return [e for e in events if e.get("event_type") in sig_types]


def format_alert(event):
    icon_map = {
        "pricing_change": "[PRICING]", "product_launch": "[LAUNCH]",
        "feature_added": "[FEATURE+]", "feature_removed": "[FEATURE-]",
        "hiring_change": "[HIRING]", "funding": "[FUNDING]",
        "acquisition": "[ACQ]", "leadership_change": "[LEADER]",
        "github_release": "[RELEASE]", "github_activity": "[GITHUB]",
        "website_change": "[WEBSITE]", "company_news": "[NEWS]",
    }
    icon = icon_map.get(event.get("event_type", ""), "[CHANGE]")
    name = event.get("entity_name", event.get("entity_id", "Unknown"))
    etype = event.get("event_type", "unknown").replace("_", " ").title()
    conf = event.get("confidence", "").upper()
    time = event.get("detected_at", "")[:16]
    
    lines = [f"{icon} COMPETITOR ALERT", "", 
             f"Entity: {name}", f"Type: {etype}", f"Confidence: {conf}", f"Time: {time}", ""]
    
    if event.get("old_value"):
        lines.append(f"Previous: {event['old_value']}")
    if event.get("new_value"):
        lines.append(f"Current: {event['new_value']}")
    
    desc = event.get("description", "")
    if desc:
        lines.extend(["", f"Details: {desc}"])
    
    sources = event.get("event_sources", [])
    if sources:
        lines.extend(["", f"Sources: {', '.join(sources)}"])
    
    return "\n".join(lines)


def send_telegram(text):
    """Send alert via Telegram using your main bot."""
    # Your main bot token
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token or len(token) < 20:
        # Fallback to known main bot token
        token = "8914691230:AAGTm0tJtAg_IjNtYzodjy97UVrCn8rx2h4"
    
    chat_id = "5191016577"  # Mahesh's chat ID
    
    if not token or len(token) < 20:
        print("[Alert] Telegram not configured")
        print(text)
        return False
    try:
        import urllib.request, urllib.parse
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat, "text": text, "parse_mode": "Markdown"
        }).encode()
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as r:
            if json.loads(r.read()).get("ok"):
                print("[Alert] Telegram sent")
                return True
    except Exception as e:
        print(f"[Alert] Telegram failed: {e}")
    return False


def check_alerts():
    print("=" * 50)
    print("COMPETITOR INTELLIGENCE - ALERT CHECK")
    print("=" * 50, "\n")
    
    events = load_events(days=1)
    significant = get_significant(events)
    state = load_alert_state()
    
    if not significant:
        print("No significant events requiring alerts.")
        return
    
    print(f"Found {len(significant)} significant event(s)\n")
    
    sent = 0
    for event in significant:
        if should_alert(event, state):
            text = format_alert(event)
            print(text)
            print()
            
            key = f"{event.get('entity_id')}:{event.get('event_type')}"
            state.setdefault("alerted", {})[key] = datetime.utcnow().isoformat()
            send_telegram(text)
            sent += 1
        else:
            print(f"Skipping (cooldown): {event.get('entity_name')} - {event.get('event_type')}")
    
    save_alert_state(state)
    print(f"\nAlerts sent: {sent}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Competitor Intelligence Alerts")
    parser.add_argument("--check", action="store_true", help="Check for alerts")
    parser.add_argument("--list", action="store_true", help="List recent alerts")
    parser.add_argument("--clear", action="store_true", help="Clear alert state")
    args = parser.parse_args()
    
    if args.clear:
        save_alert_state({"alerted": {}})
        print("Alert state cleared.")
    elif args.list:
        state = load_alert_state()
        alerts = state.get("alerted", {})
        if alerts:
            print("Recent alerts:")
            for k, t in sorted(alerts.items(), reverse=True)[:10]:
                print(f"  {t[:16]} - {k}")
        else:
            print("No recent alerts.")
    else:
        check_alerts()


if __name__ == "__main__":
    main()
