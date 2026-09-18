#!/usr/bin/env python3
"""Generate a sample competitor intelligence summary for Telegram."""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
CHAT_ID = "5191016577"


def load_competitors():
    comp_file = DATA_DIR / "competitors.yaml"
    if comp_file.exists():
        with open(comp_file) as f:
            data = yaml.safe_load(f) or {}
        return data.get("competitors", [])
    return []


def load_people():
    people_file = DATA_DIR / "people.yaml"
    if people_file.exists():
        with open(people_file) as f:
            data = yaml.safe_load(f) or {}
        return data.get("people", [])
    return []


def load_events(days=7):
    events_file = DATA_DIR / "events" / "events.jsonl"
    events = []
    if events_file.exists():
        with open(events_file) as f:
            for line in f:
                if line.strip():
                    try:
                        event = json.loads(line)
                        event_time = datetime.fromisoformat(event.get("detected_at", ""))
                        if event_time >= datetime.utcnow() - __import__("datetime").timedelta(days=days):
                            events.append(event)
                    except:
                        continue
    return events


def get_telegram_token():
    """Get your main bot token. Try employee bot first (your personal bot)."""
    # Your main personal bot is likely @Dci_employeebot
    for var in ["HERMES_EMPLOYEE_TELEGRAM_TOKEN", "HERMES_TELEGRAM_TOKEN",
                 "TELEGRAM_BOT_TOKEN", "HERMES_MANAGER_TELEGRAM_TOKEN",
                 "HERMES_CMO_TELEGRAM_TOKEN"]:
        token = os.environ.get(var, "")
        if token and len(token) > 20:
            return token
    return None


def send_telegram(token, chat_id, message):
    import urllib.request, urllib.parse
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }).encode()
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def generate_summary():
    competitors = load_competitors()
    people = load_people()
    events = load_events(days=7)
    
    high_priority = [c for c in competitors if c.get("priority") == "high"]
    medium_priority = [c for c in competitors if c.get("priority") == "medium"]
    
    # Group events by type
    by_type = {}
    for event in events:
        etype = event.get("event_type", "unknown")
        if etype not in by_type:
            by_type[etype] = []
        by_type[etype].append(event)
    
    # Generate HTML message
    lines = []
    lines.append("<b>🤖 Hermes Competitor Intelligence</b>")
    lines.append(f"<i>Last updated: {datetime.utcnow().strftime('%d %b %Y, %H:%M UTC')}</i>")
    lines.append("")
    lines.append("─" * 30)
    lines.append("")
    lines.append("<b>📊 STATUS</b>")
    lines.append(f"Competitors tracked: {len(competitors)}")
    lines.append(f"People monitored: {len(people)}")
    lines.append(f"Events this week: {len(events)}")
    lines.append("")
    lines.append("─" * 30)
    lines.append("")
    lines.append("<b>🏢 HIGH PRIORITY COMPETITORS ({})</b>".format(len(high_priority)))
    
    for comp in high_priority:
        products = comp.get("products", [])
        products_str = ", ".join(products[:3]) if products else "Various"
        lines.append(f"• <b>{comp['name']}</b> ({comp.get('website', 'N/A')})")
        lines.append(f"  Products: {products_str}")
    
    lines.append("")
    lines.append("─" * 30)
    lines.append("")
    lines.append("<b>📈 MEDIUM PRIORITY ({})</b>".format(len(medium_priority)))
    
    for comp in medium_priority:
        products = comp.get("products", [])
        products_str = ", ".join(products[:3]) if products else "Various"
        lines.append(f"• <b>{comp['name']}</b> — {products_str}")
    
    lines.append("")
    lines.append("─" * 30)
    
    if events:
        lines.append("")
        lines.append("<b>⚡ RECENT EVENTS (last 7 days)</b>")
        lines.append("")
        for event in events[:5]:
            etype = event.get("event_type", "unknown").replace("_", " ").title()
            conf = event.get("confidence", "").upper()
            name = event.get("entity_name", event.get("entity_id", "?"))
            lines.append(f"• <b>{name}</b> — {etype} ({conf})")
            if event.get("description"):
                lines.append(f"  {event['description'][:200]}")
    else:
        lines.append("")
        lines.append("<b>⏳ BASELINE COLLECTION IN PROGRESS</b>")
        lines.append("No events yet — first collection cycle completing...")
    
    lines.append("")
    lines.append("─" * 30)
    lines.append("")
    lines.append("<b>📋 COMMANDS</b>")
    lines.append("• Track Company X")
    lines.append("• What changed today?")
    lines.append("• Competitor report")
    lines.append("• Who is hiring AI engineers?")
    lines.append("")
    lines.append("─" * 30)
    lines.append("")
    lines.append("<i>Powered by Hermes Competitor Intelligence</i>")
    
    return "\n".join(lines)


def main():
    print("=" * 50)
    print("GENERATING COMPETITOR INTELLIGENCE SUMMARY")
    print("=" * 50)
    print()
    
    token = get_telegram_token()
    if not token:
        print("ERROR: No Telegram token found!")
        return 1
    
    message = generate_summary()
    
    print("Sending to Telegram...")
    success = send_telegram(token, CHAT_ID, message)
    
    if success:
        print("✓ Summary sent to Telegram!")
        print(f"Message:\n{message[:500]}...")
        return 0
    else:
        print("✗ Failed to send!")
        print(message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
