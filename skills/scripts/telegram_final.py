#!/usr/bin/env python3
"""Send a comprehensive competitor intelligence summary to Telegram."""

import os, sys, json, yaml
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
CHAT_ID = "5191016577"


def get_token():
    for var in ["HERMES_MANAGER_TELEGRAM_TOKEN", "HERMES_TELEGRAM_TOKEN",
                 "TELEGRAM_BOT_TOKEN"]:
        t = os.environ.get(var, "")
        if t and len(t) > 20:
            return t
    return None


def send(token, chat_id, msg):
    import urllib.request, urllib.parse
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode()
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()).get("ok", False)
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    comp_file = DATA_DIR / "competitors.yaml"
    people_file = DATA_DIR / "people.yaml"
    
    with open(comp_file) as f:
        comps = yaml.safe_load(f).get("competitors", [])
    with open(people_file) as f:
        people = yaml.safe_load(f).get("people", [])
    
    high = [c for c in comps if c.get("priority") == "high"]
    medium = [c for c in comps if c.get("priority") == "medium"]
    low = [c for c in comps if c.get("priority") == "low"]
    
    msg = f"""<b>🤖 Hermes Competitor Intelligence</b>
<i>Setup complete — {datetime.utcnow().strftime('%d %b %Y')}</i>

<b>📊 OVERVIEW</b>
Competitors tracked: <b>{len(comps)}</b>
People monitored: <b>{len(people)}</b>
High priority: <b>{len(high)}</b> | Medium: <b>{len(medium)}</b> | Low: <b>{len(low)}</b>

<b>🏢 HIGH PRIORITY ({len(high)})</b>
"""
    
    for c in high:
        name = c["name"]
        website = c.get("website", "N/A")
        github = c.get("github", "N/A") or "N/A"
        prods = ", ".join(c.get("products", [])[:3]) or "Various"
        msg += f"• <b>{name}</b>\n  {website} | GitHub: {github}\n  Products: {prods}\n"
    
    msg += f"""
<b>📈 MEDIUM PRIORITY ({len(medium)})</b>
"""
    for c in medium[:10]:
        name = c["name"]
        prods = ", ".join(c.get("products", [])[:2]) or "Various"
        msg += f"• <b>{name}</b> — {prods}\n"
    if len(medium) > 10:
        msg += f"• ... and {len(medium) - 10} more\n"
    
    msg += f"""
<b>👤 KEY PERSONALITIES ({len(people)})</b>
"""
    # Group by company
    by_company = {}
    for p in people:
        company = p.get("company", "Independent")
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(p)
    
    for company, ppl in list(by_company.items())[:5]:
        company_name = company if company else "Independent/Founders"
        names = ", ".join(p["name"] for p in ppl[:3])
        msg += f"• <b>{company_name}</b>: {names}\n"
    
    msg += f"""
<b>🔄 AUTOMATION</b>
• Collection: Every 6 hours (high-priority competitors)
• Daily report: 9:00 AM IST
• Weekly report: Monday 9:00 AM IST
• Alerts: Telegram (dedup 24h cooldown)

<b>📱 COMMANDS</b>
• "Track Company X" — Add competitor
• "What changed today?" — Recent changes
• "Competitor report" — Full report
• "Who is hiring AI engineers?" — Hiring signals

<b>⚡ READY TO MONITOR</b>
 Hermes will now track these companies and alert you to significant changes.
 First collection cycle running now...
"""
    
    token = get_token()
    if send(token, CHAT_ID, msg):
        print(f"✓ Sent comprehensive summary to Telegram!")
        print(f"  {len(comps)} competitors, {len(people)} people")
    else:
        print("✗ Failed to send")


if __name__ == "__main__":
    main()
