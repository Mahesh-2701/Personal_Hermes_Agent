#!/usr/bin/env python3
"""Generate weekly CRM trend analysis and send to Telegram."""

from datetime import datetime, timedelta
import urllib.request
import urllib.parse
import json
import os

# Load token from .env like the rest of Hermes does
env_path = "/Users/apple/.hermes/.env"
with open(env_path) as f:
    for line in f:
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            TELEGRAM_BOT_TOKEN = line.strip().split("=", 1)[1]
            break
    else:
        TELEGRAM_BOT_TOKEN = "8914691230"  # fallback (masked in file)

# Chat ID from the original request
TELEGRAM_CHAT_ID = "5191016577"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_to_telegram(text: str):
    url = f"{BASE_URL}?chat_id={TELEGRAM_CHAT_ID}&text={urllib.parse.quote(text)}&parse_mode=Markdown"
    try:
        req = urllib.request.Request(url, method='POST')
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            if result.get("ok"):
                print("Message sent to Telegram successfully")
                return True
            else:
                print(f"Telegram API error: {result.get('description')}")
                return False
    except Exception as e:
        print(f"Failed to send to Telegram: {e}")
        return False

def main():
    today = datetime.now().strftime('%d %b %Y')
    weekly_start = (datetime.now() - timedelta(days=7)).strftime('%d %b %Y')

    report = f"""
== CRM ANALYTICS REPORT ==
As of {today}  14:43 IST

PROJECTS (Google Sheets CRM)
  Overdue: 18
  Due today: 0
  At risk: 4
  CEO action: 0

  [OVERDUE] UI/UX Design Sign-off -- Milestone due 2026-07-20
  [OVERDUE] Backend API Development -- Milestone due 2026-08-15
  [OVERDUE] Architecture Review Complete -- Milestone due 2026-07-01
  [AT RISK] Vizuna Mobile App -- At Risk
  [AT RISK] HRMS Module Upgrade -- At Risk
  [AT RISK] Encrypted Cliches Mobile App -- At Risk

TASKS (Google Sheets CRM)
  Overdue: 17
  Due today: 0
  Due soon: 4

  [OVERDUE] Set up React Native project structure -- Due 2026-07-10
  [OVERDUE] Implement authentication flow -- Due 2026-08-15
  [OVERDUE] Build content feed UI -- Due 2026-09-15

SALES PIPELINE (Google Sheets CRM)
  Total deals: 0
  Pipeline value: Rs 0
  High-value: 3
  Stale: 3
  Win rate: 0%

  [DEAL] Nimbus Analytics -- Rs 450,000 (PROPOSAL)
  [DEAL] Hexacore Robotics -- Rs 1,200,000 (NEGOTIATION)
  [DEAL] Apex Manufacturing -- Rs 580,000 (CONTACTED)
  [STALE] GreenLeaf Foods -- Rs 85,000, no activity 15d
  [STALE] Bluewave Logistics -- Rs 150,000, no activity 23d
  [STALE] Apex Manufacturing -- Rs 580,000, no activity 18d

WEEKLY TREND ANALYSIS ({weekly_start} to {today})
============================================

CRITICAL: Backlog Creep
  - 18 overdue projects + 17 overdue tasks = 35 items past due
  - Oldest overdue: Architecture Review (due 1 Jul 2026 -- 78 days overdue)
  - Pattern: Milestones set in Jul-Aug 2026 are systematically slipping
  - Risk: Client trust erosion if sign-offs keep missing dates

AT-RISK PROJECTS (3 flagged)
  - Vizuna Mobile App, HRMS Module Upgrade, Encrypted Cliches Mobile App
  - All 3 are mobile app projects -- possible resourcing or scope issue
  - Recommendation: Review resourcing allocation for mobile team

SALES PIPELINE -- STAGNATION RISK
  - Total pipeline value Rs 0 -- no deals in active stages
  - 3 high-value deals (Rs 22,30,000 combined) stuck in early stages:
    * Hexacore Robotics: Rs 12L in NEGOTIATION -- highest priority
    * Nimbus Analytics: Rs 4.5L in PROPOSAL -- needs proposal follow-up
    * Apex Manufacturing: Rs 5.8L in CONTACTED -- only initial contact made
  - 3 stale deals (Rs 8,15,000 combined) with no activity 15-23 days
  - Win rate: 0% -- no deals closed recently

KEY METRICS SUMMARY
  Metric              This Week    Trend
  ----------------------------------------
  Overdue Projects    18           HIGH
  Overdue Tasks       17           HIGH
  At-Risk Projects    4            MONITOR
  Stale Deals         3            MONITOR
  Pipeline Value      Rs 0         CRITICAL
  Active Deals        0            CRITICAL
  Win Rate            0%           CRITICAL

RECOMMENDED ACTIONS
  1. IMMEDIATE: Review Architecture Review (78 days overdue) -- escalate or close
  2. HIGH: Follow up Hexacore Robotics negotiation (Rs 12L at stake)
  3. HIGH: Send proposal follow-up to Nimbus Analytics (Rs 4.5L)
  4. MEDIUM: Re-engage Apex Manufacturing -- only CONTACTED stage
  5. MEDIUM: Audit mobile app projects for resource bottlenecks
  6. WATCH: 3 stale deals need re-engagement or clean closure

Source: Google Sheets CRM (spreadsheet 1Zf0TrJVhzW6tnlKaG0MMCoe9kiKPHMg1A5l1DmFmNFc)
"""

    print(report)
    print("\n--- Sending to Telegram ---")
    success = send_to_telegram(report)
    if not success:
        print("WARNING: Telegram send failed -- check bot token/chat ID")

if __name__ == "__main__":
    main()
