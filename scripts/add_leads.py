#!/usr/bin/env python3
"""Add real project leads found by this run to the Google Sheet."""
import json
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
except ImportError:
    print("ERROR: google-api-python-client not installed.")
    sys.exit(1)

IST = ZoneInfo("Asia/Kolkata")
NOW = datetime.now(IST)
SHEET_ID = "1guNSf6QdXZ7rQ5zshGVSNcWpkz94Jzgbhk0LjBC7KIU"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")

with open(TOKEN_PATH) as f:
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

svc = build("sheets", "v4", credentials=creds)


def normalize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip().lower().rstrip("/")
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url


def normalize_name(name: str) -> str:
    if not name:
        return ""
    return re.sub(r"[^a-z0-9]", "", name.lower().strip())


def load_existing():
    result = svc.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="LEADS!A:Z"
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


def is_duplicate(project, existing):
    p_url = normalize_url(project.get("Source URL", ""))
    p_title = normalize_name(project.get("Project Title", ""))
    p_company = normalize_name(project.get("Client Company", ""))

    for ex in existing:
        ex_url = normalize_url(ex.get("Source URL", ""))
        if p_url and ex_url and p_url == ex_url:
            return f"URL match: {ex_url}"

        ex_title = normalize_name(ex.get("Project Title", ""))
        ex_company = normalize_name(ex.get("Client Company", ""))

        if p_title and ex_title and p_title == ex_title:
            return f"Title match: {ex_title}"

        if p_company and ex_company and p_company == ex_company:
            if p_title and ex_title and (p_title[:20] in ex_title or ex_title[:20] in p_title):
                return f"Company + partial title match: {ex_company}"
    return None


def store(project):
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


PROJECTS = [
    {
        "Client Company": "India-based EdTech founder",
        "Project Title": "Learning Management System (LMS) for Web & Mobile",
        "Project Type": "Fullstack / SaaS",
        "Description": "Build a modern, scalable LMS for organizations, instructors, and students. Features: course browsing/enrollment, video & document lessons, quizzes/assessments, assignments, certificates, progress tracking, role-based admin/instructor/student dashboards, payment gateway, notifications, analytics. Client explicitly asks for estimated timeline and cost, and prior LMS/EdTech examples.",
        "Tech Stack": "React/Next.js, Node.js, PHP/Laravel, Flutter, PostgreSQL/MySQL, AWS (open to recommendations)",
        "Budget Range": "Not specified — hourly, Expert level, 1-3 months; client asks for estimate",
        "Location": "India (client location per Upwork profile)",
        "Contact Person": "Not publicly listed",
        "Contact Role": "Client / Founder",
        "Email": "",
        "Phone": "",
        "Source": "Upwork",
        "Source URL": "https://www.upwork.com/freelance-jobs/apply/Learning-Management-System-LMS-Application-Development_~022100545266545669814/",
        "Lead Status": "New",
        "Priority": "High",
        "Notes": "Explicit scoped project with detailed requirements. Client asks for prior LMS examples, architecture approach, timeline and cost estimate. Strong ICP match — fullspec EdTech SaaS build.",
    },
    {
        "Client Company": "Canada-based automotive diagnostics startup (Brampton, ON)",
        "Project Title": "AI-Powered Automotive Diagnostics Platform",
        "Project Type": "Fullstack / AI/ML",
        "Description": "Build a web-based diagnostic platform for automotive mechanics. Includes: vehicle diagnostics interface, AI-driven diagnostic tools, data collection and analysis workflows. Part-time engagement (1-3 months) with potential for future work. Client has 7 prior hires and $326 spent on Upwork.",
        "Tech Stack": "React, Node.js, Python, API, HTML5",
        "Budget Range": "$15-35/hr hourly, 1-3 months",
        "Location": "Brampton, Canada (client location per Upwork profile)",
        "Contact Person": "Not publicly listed",
        "Contact Role": "Client / Founder",
        "Email": "",
        "Phone": "",
        "Source": "Upwork",
        "Source URL": "https://www.upwork.com/freelance-jobs/apply/AI-Full-Stack-Developer-for-Automotive-Diagnostics_~022100587446384497908/",
        "Lead Status": "New",
        "Priority": "High",
        "Notes": "AI/ML project with explicit scope. Established client (Oct 2022, 7 hires). Build + AI integration. Good ICP match for AI/ML + fullstack.",
    },
    {
        "Client Company": "UK-based business (Craig S., client name)",
        "Project Title": "Web App Code Review, Testing, Fix & Ongoing Maintenance",
        "Project Type": "Fullstack / Custom Software",
        "Description": "Client has a small existing web app (builder tool — records stored on device, email-based report sharing). Wants: A) code & security review (fixed price), B) real-device testing on iPhones/Android (home-screen install behaviour, offline, camera, voice dictation), C) fix findings (fixed price or day rate), D) ongoing annual maintenance (small fixes, yearly access code change), E) optional: App Store/Play Store listing + small server for automatic report delivery + customer data storage.",
        "Tech Stack": "Web app (stack not specified — client wants reviewer to assess)",
        "Budget Range": "Not set — client explicitly not looking for cheapest quote, wants proper cost + approach",
        "Location": "United Kingdom (client location per PeoplePerHour profile)",
        "Contact Person": "Craig S.",
        "Contact Role": "Client / Business Owner",
        "Email": "",
        "Phone": "",
        "Source": "PeoplePerHour",
        "Source URL": "https://www.peopleperhour.com/freelance-jobs/technology-programming/mobile-app-development/help-to-check-and-develop-a-web-app-4521642",
        "Lead Status": "New",
        "Priority": "Medium",
        "Notes": "Well-defined scope with 5 distinct quoted work items. UK client, 4 reviews, 2 prior projects. No budget set but serious about quality over price. Smaller initial scope but potential ongoing maintenance relationship.",
    },
    {
        "Client Company": "US-based business (client member since Sep 16, 2026)",
        "Project Title": "Mobile App Development for Business",
        "Project Type": "Mobile App (iOS/Android/React Native)",
        "Description": "Build a functional mobile app for a business. Scope: build app, improve user experience, ensure smooth performance across devices. Work closely with client team to understand requirements, develop features, deliver reliable solution. Experience with mobile app development and user-focused design important.",
        "Tech Stack": "React Native, iOS, Android, iPad App Development",
        "Budget Range": "$15-50/hr hourly, 1-3 months",
        "Location": "United States (client location per Upwork profile)",
        "Contact Person": "Not publicly listed",
        "Contact Role": "Client / Business Owner",
        "Email": "",
        "Phone": "",
        "Source": "Upwork",
        "Source URL": "https://www.upwork.com/freelance-jobs/apply/Mobile-App-Development-for-Business_~022100571875858622196/",
        "Lead Status": "New",
        "Priority": "Medium",
        "Notes": "US-based client, new account (Sep 16, 2026). Scope is relatively vague ('mobile app for business') — client likely early in defining requirements. Good mobile app opportunity but needs discovery call to clarify.",
    },
    {
        "Client Company": "Pakistan-based company (Gilgit)",
        "Project Title": "Full-Stack Engineer for Scalable Web & SaaS Applications",
        "Project Type": "Fullstack / SaaS",
        "Description": "Long-term collaboration to build and maintain modern web apps, SaaS platforms, APIs, and business systems. Client wants someone who can take ownership, write clean production-ready code, solve problems independently, and grow with the project. Ongoing features, improvements, maintenance, and new projects. Contract-to-hire opportunity.",
        "Tech Stack": "React, Next.js, TypeScript, Node.js, Python/FastAPI, PostgreSQL, REST APIs. Mobile apps, AI integrations, scalable SaaS architecture are a plus.",
        "Budget Range": "$15-30/hr hourly, 6+ months, contract-to-hire",
        "Location": "Gilgit, Pakistan (client location per Upwork profile)",
        "Contact Person": "Not publicly listed",
        "Contact Role": "Client / Hiring Manager",
        "Email": "",
        "Phone": "",
        "Source": "Upwork",
        "Source URL": "https://www.upwork.com/freelance-jobs/apply/Full-Stack-Engineer-for-Scalable-Web-SaaS-Applications_~022100530084269384627/",
        "Lead Status": "New",
        "Priority": "Medium",
        "Notes": "Long-term (6+ months) fullstack SaaS opportunity, contract-to-hire. New client account (Sep 15, 2026). 20-50 proposals already. Solid tech stack match but rate is on lower end.",
    },
]


def main():
    existing = load_existing()
    print(f"Existing leads in CRM: {len(existing)}")

    new_count = 0
    dup_count = 0
    rejected = 0

    for i, project in enumerate(PROJECTS, 1):
        pid = f"PROJ-{NOW.strftime('%Y%m%d')}-{i:04d}"
        project["Project ID"] = pid

        dup = is_duplicate(project, existing)
        if dup:
            print(f"  SKIP #{i}: Duplicate — {dup}")
            dup_count += 1
            continue

        try:
            store(project)
            print(f"  ADDED #{i}: {project['Project Title']} [{project['Priority']}] — {project['Source']}")
            new_count += 1
        except Exception as e:
            print(f"  FAILED #{i}: {project['Project Title']} — {e}")
            rejected += 1

    print("\n" + "=" * 60)
    print("ADD RESULTS")
    print(f"  New leads added: {new_count}")
    print(f"  Duplicates skipped: {dup_count}")
    print(f"  Failed: {rejected}")
    print("=" * 60)

    # JSON output for the cron run summary
    output = {
        "ok": True,
        "timestamp": NOW.isoformat(),
        "added": new_count,
        "duplicates": dup_count,
        "failed": rejected,
        "projects": [p["Project Title"] for p in PROJECTS],
    }
    print(f"\n__JSON_OUTPUT__:{json.dumps(output, default=str)}")


if __name__ == "__main__":
    main()
