#!/usr/bin/env python3
"""Project Lead Generation Script.

Discovers IT project leads for your company — businesses actively looking to build:
- Fullstack web applications
- Mobile apps
- AI/ML solutions
- E-commerce platforms
- Custom software/SaaS
- MVPs for startups

Usage:
    python3 lead_generation.py --dry-run          # Preview without storing
    python3 lead_generation.py                    # Run full discovery cycle
    python3 lead_generation.py --type fullstack   # Only fullstack projects
    python3 lead_generation.py --type mobile      # Only mobile projects
    python3 lead_generation.py --type ai          # Only AI/ML projects
    python3 lead_generation.py --type ecommerce   # Only e-commerce projects
    python3 lead_generation.py --type saas        # Only SaaS projects
    python3 lead_generation.py --type custom      # Only custom software
    python3 lead_generation.py --type mvp         # Only MVP projects
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
except ImportError:
    print("ERROR: google-api-python-client not installed.")
    sys.exit(1)

IST = ZoneInfo("Asia/Kolkata")
NOW = datetime.now(IST)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, ".leads_config.json")
CONFIG = {}
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        CONFIG = json.load(f)

SHEET_ID = CONFIG.get("LEADS_SHEET_ID", "1guNSf6QdXZ7rQ5zshGVSNcWpkz94Jzgbhk0LjBC7KIU")
SHEET_URL = CONFIG.get("SHEET_URL", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}")

# Project Types We Target
PROJECT_TYPES = {
    "fullstack": "Fullstack Web Application",
    "mobile": "Mobile App (iOS/Android/React Native/Flutter)",
    "ai": "AI/ML Solution (Chatbot, RAG, Computer Vision, NLP)",
    "ecommerce": "E-commerce Platform (Shopify, WooCommerce, Custom)",
    "saas": "SaaS Product (Multi-tenant, Subscription)",
    "custom": "Custom Software (ERP, CRM, Dashboard, Portal)",
    "mvp": "MVP/Prototype (Startup product, Proof of Concept)",
}

# Search Queries — Project-Focused
SEARCH_QUERIES = {
    "fullstack": [
        "looking for fullstack developer project React Node.js",
        "need web application development company project",
        "hiring for fullstack web development project India",
        "React Node.js project outsourcing India company",
        "fullstack web app development project quote India",
    ],
    "mobile": [
        "looking for mobile app development company project",
        "need iOS Android app developer project",
        "React Native Flutter app project outsourcing India",
        "mobile app development project hiring company",
        "cross-platform mobile app project India budget",
    ],
    "ai": [
        "looking for AI ML development project company",
        "need chatbot RAG solution development project",
        "AI ML project outsourcing India company",
        "generative AI project development hiring India",
        "machine learning solution project company India",
    ],
    "ecommerce": [
        "looking for ecommerce website development project",
        "Shopify WooCommerce custom development project",
        "ecommerce platform development company India",
        "online store web development project hiring",
        "multivendor marketplace development project India",
    ],
    "saas": [
        "looking for SaaS product development company",
        "multi-tenant subscription platform development project",
        "SaaS MVP development company India",
        "custom SaaS solution development project hiring",
        "enterprise SaaS product development outsourcing",
    ],
    "custom": [
        "custom software development project company India",
        "ERP CRM dashboard development project hiring",
        "enterprise web application development project",
        "business automation software development project",
        "custom portal development company India project",
    ],
    "mvp": [
        "MVP development project startup India company",
        "prototype development project startup funding",
        "proof of concept development project India",
        "startup product development company project",
        "rapid MVP prototyping development project hiring",
    ],
}

# Sheet Headers (Project-Focused)
PROJECT_HEADERS = [
    "Project ID",
    "Date Found",
    "Client Company",
    "Project Title",
    "Project Type",
    "Description",
    "Tech Stack",
    "Budget Range",
    "Location",
    "Contact Person",
    "Contact Role",
    "Email",
    "Phone",
    "Source",
    "Source URL",
    "Lead Status",
    "Priority",
    "Notes",
    "Last Updated",
]


def get_service():
    """Get Google Sheets API service."""
    token_path = os.path.expanduser("~/.hermes/google_token.json")
    if not os.path.exists(token_path):
        print(f"No token found at {token_path}")
        return None
    
    with open(token_path) as f:
        td = json.load(f)
    
    creds = Credentials(
        token=td.get("token"),
        refresh_token=td.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=td.get("client_id"),
        client_secret=td.get("client_secret"),
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    
    try:
        creds.refresh(None)
    except Exception:
        pass
    
    return build("sheets", "v4", credentials=creds)


def normalize_url(url: str) -> str:
    """Normalize URLs for deduplication comparison."""
    if not url:
        return ""
    url = url.strip().lower().rstrip("/")
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url


def normalize_name(name: str) -> str:
    """Normalize company name for comparison."""
    if not name:
        return ""
    return re.sub(r"[^a-z0-9]", "", name.lower().strip())


def load_existing_leads(svc) -> List[Dict]:
    """Load all existing project leads for deduplication."""
    try:
        result = svc.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range="LEADS!A:Z",
        ).execute()
        values = result.get("values", [])
        if len(values) <= 1:
            return []
        
        headers = values[0]
        records = []
        for row in values[1:]:
            record = {}
            for i, header in enumerate(headers):
                record[header] = row[i] if i < len(row) else ""
            records.append(record)
        return records
    except Exception as e:
        print(f"Warning: Could not load existing leads: {e}")
        return []


def is_duplicate(project: Dict, existing_leads: List[Dict]) -> Optional[str]:
    """Check if project is duplicate."""
    project_url = normalize_url(project.get("Source URL", ""))
    project_title = normalize_name(project.get("Project Title", ""))
    project_company = normalize_name(project.get("Client Company", ""))

    for existing in existing_leads:
        ex_url = normalize_url(existing.get("Source URL", ""))
        if project_url and ex_url and project_url == ex_url:
            return f"URL match: {ex_url}"

        ex_title = normalize_name(existing.get("Project Title", ""))
        ex_company = normalize_name(existing.get("Client Company", ""))
        
        if project_title and ex_title and project_title == ex_title:
            return f"Title match: {ex_title}"
        
        if project_company and ex_company and project_company == ex_company:
            if project_title and ex_title and (project_title[:20] in ex_title or ex_title[:20] in project_title):
                return f"Company + partial title match: {ex_company}"

    return None


def generate_project_id(seq: int) -> str:
    """Generate unique project ID."""
    return f"PROJ-{NOW.strftime('%Y%m%d')}-{seq:04d}"


def store_project(svc, project: Dict) -> bool:
    """Store a project lead in the Google Sheet."""
    try:
        row = [
            project.get("Project ID", ""),
            NOW.strftime("%Y-%m-%d %H:%M"),
            project.get("Client Company", ""),
            project.get("Project Title", ""),
            project.get("Project Type", ""),
            project.get("Description", ""),
            project.get("Tech Stack", ""),
            project.get("Budget Range", ""),
            project.get("Location", ""),
            project.get("Contact Person", ""),
            project.get("Contact Role", ""),
            project.get("Email", ""),
            project.get("Phone", ""),
            project.get("Source", ""),
            project.get("Source URL", ""),
            project.get("Lead Status", "New"),
            project.get("Priority", "Medium"),
            project.get("Notes", ""),
            NOW.strftime("%Y-%m-%d %H:%M"),
        ]
        
        svc.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range="LEADS!A2",
            valueInputOption="USER_ENTERED",
            body={"values": [row]},
        ).execute()
        return True
    except Exception as e:
        print(f"Failed to store project: {e}")
        return False


def search_project_sources(svc, project_types: List[str]) -> List[Dict]:
    """Output search queries for project leads. These are processed by Hermes web_search in cron."""
    candidates = []
    
    for ptype in project_types:
        if ptype not in SEARCH_QUERIES:
            continue
        
        queries = SEARCH_QUERIES[ptype]
        for query in queries:
            # Output search markers for Hermes cron agent to process
            print(f"SEARCH:{ptype}|{query}")
    
    return candidates


def send_telegram_notification(projects: List[Dict], stats: Dict):
    """Output Telegram notification. Always sends, even if no projects found."""
    lines = [
        "📊 PROJECT LEAD GENERATION UPDATE",
        f"Run Time: {NOW.strftime('%d %b %Y · %H:%M IST')}",
        "",
        "━━━━━━━━━━━━━━━━━━",
    ]
    
    if projects:
        lines.extend([
            f"🚨 NEW PROJECT LEADS FOUND: {len(projects)}",
            "",
        ])
        for i, project in enumerate(projects, 1):
            lines.extend([
                f"{i}. {project.get('Client Company', 'Unknown')}",
                f"   {project.get('Project Title', 'No Title')}",
                f"   Type: {project.get('Project Type', 'N/A')} | Budget: {project.get('Budget Range', 'N/A')}",
                f"   Location: {project.get('Location', 'N/A')} | Source: {project.get('Source', 'N/A')}",
                f"   {project.get('Description', '')[:80]}",
                "",
            ])
    else:
        lines.extend([
            "📭 NO NEW PROJECT LEADS",
            "",
            "All sources checked — no new qualified project leads found at this time.",
            "Next run will check for new opportunities.",
        ])
    
    lines.extend([
        "━━━━━━━━━━━━━━━━━━",
        "",
        "📊 Run Stats:",
        f"Project Types: {', '.join(stats.get('project_types', []))}",
        f"Searches Run: {stats.get('searches_run', 0)}",
        f"Candidates Found: {stats.get('candidates_found', 0)}",
        f"New Leads: {stats.get('new', 0)}",
        f"Duplicates Skipped: {stats.get('duplicates', 0)}",
        f"High Priority: {stats.get('high', 0)}",
        f"Medium Priority: {stats.get('medium', 0)}",
        f"Low Priority: {stats.get('low', 0)}",
        "",
        f"🔗 Sheet: {SHEET_URL}",
    ])
    
    message = "\n".join(lines)
    print(message)


def main():
    parser = argparse.ArgumentParser(description="Project Lead Generation")
    parser.add_argument("--dry-run", action="store_true", help="Preview without storing")
    parser.add_argument("--type", type=str, help="Comma-separated project types")
    args = parser.parse_args()

    # Determine project types to search
    if args.type:
        project_types = [t.strip() for t in args.type.split(",")]
    else:
        project_types = list(PROJECT_TYPES.keys())

    print("=" * 60)
    print("PROJECT LEAD GENERATION")
    print(f"Run Time: {NOW.strftime('%d %b %Y · %H:%M IST')}")
    print(f"Sheet: {SHEET_URL}")
    print(f"Project Types: {', '.join(project_types)}")
    print("=" * 60)

    # Get Google Sheets service
    svc = get_service()
    if not svc:
        print("ERROR: Cannot connect to Google Sheets")
        sys.exit(1)

    # Load existing leads for deduplication
    existing_leads = load_existing_leads(svc)
    print(f"Existing project leads in CRM: {len(existing_leads)}")

    # Output search queries for Hermes cron agent
    candidates = search_project_sources(svc, project_types)
    
    # In standalone mode, candidates will be empty
    # In Hermes cron mode, web_search will find real projects
    
    # Stats
    total_searches = sum(len(SEARCH_QUERIES.get(pt, [])) for pt in project_types)
    
    stats = {
        "project_types": project_types,
        "searches_run": total_searches,
        "candidates_found": len(candidates),
        "new": len(candidates),
        "duplicates": 0,
        "rejected": 0,
        "high": 0,
        "medium": len(candidates),
        "low": 0,
    }
    
    # Output summary
    print("\n" + "=" * 60)
    print("PROJECT LEAD GENERATION SUMMARY")
    print("=" * 60)
    print(f"Project Types: {', '.join(project_types)}")
    print(f"Search Queries: {total_searches}")
    print(f"Candidates Found: {len(candidates)}")
    print(f"Sheet: {SHEET_URL}")
    print("=" * 60)

    # Notification
    send_telegram_notification(candidates, stats)

    # JSON output
    output = {
        "ok": True,
        "timestamp": NOW.isoformat(),
        "stats": stats,
        "new_projects": candidates,
        "sheet_url": SHEET_URL,
    }
    print(f"\n__JSON_OUTPUT__:{json.dumps(output, default=str)}")


if __name__ == "__main__":
    main()
