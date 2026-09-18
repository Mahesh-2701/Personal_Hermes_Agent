#!/usr/bin/env python3
"""
Competitor Intelligence — CLI Entry Point

Usage:
    python3 cli.py track "OpenAI" --website https://openai.com --priority high
    python3 cli.py track "Anthropic" --website https://anthropic.com
    python3 cli.py show --competitors
    python3 cli.py collect --all
    python3 cli.py diff --all
    python3 cli.py changes --today
    python3 cli.py report --daily
    python3 cli.py report --weekly --output
    python3 cli.py health
    python3 cli.py query "What changed about OpenAI today?"
"""

import os
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent / "scripts"

def run_script(script_name, args=None):
    """Run a Python script from the scripts directory."""
    script_path = SCRIPT_DIR / script_name
    if not script_path.exists():
        print(f"Error: Script not found: {script_name}")
        return 1
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    print(f"\n{'=' * 60}")
    print(f"Running: {script_name} {' '.join(args or [])}")
    print(f"{'=' * 60}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Competitor Intelligence CLI",
        prog="competitor-intelligence"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Track
    track_parser = subparsers.add_parser("track", help="Track a competitor")
    track_parser.add_argument("name", help="Competitor name")
    track_parser.add_argument("--website", help="Website URL")
    track_parser.add_argument("--github", help="GitHub organization")
    track_parser.add_argument("--priority", 
                             choices=["high", "medium", "low"],
                             default="medium")
    track_parser.add_argument("--refresh", action="store_true",
                             help="Collect data after adding")
    
    # Stop tracking
    stop_parser = subparsers.add_parser("stop-tracking", 
                                        help="Stop tracking a competitor")
    stop_parser.add_argument("name", help="Competitor name or ID")
    
    # Show
    show_parser = subparsers.add_parser("show", help="Show tracked entities")
    show_parser.add_argument("--competitors", action="store_true")
    show_parser.add_argument("--people", action="store_true")
    show_parser.add_argument("--products", action="store_true")
    
    # Check changes
    check_parser = subparsers.add_parser("check", help="Check for changes")
    check_parser.add_argument("entity", nargs="?", help="Entity ID")
    check_parser.add_argument("--all", action="store_true")
    
    # What changed
    changes_parser = subparsers.add_parser("changes", help="Query changes")
    changes_parser.add_argument("--today", action="store_true")
    changes_parser.add_argument("--week", action="store_true")
    changes_parser.add_argument("--entity", help="Specific entity")
    changes_parser.add_argument("--type", help="Filter by event type")
    
    # Report
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument("--daily", action="store_true")
    report_parser.add_argument("--weekly", action="store_true")
    report_parser.add_argument("--date", help="Date (YYYY-MM-DD)")
    report_parser.add_argument("--week-start", help="Week start (YYYY-MM-DD)")
    report_parser.add_argument("--output", action="store_true", 
                              help="Print to stdout")
    
    # Health
    health_parser = subparsers.add_parser("health", help="Source health")
    
    # Collect
    collect_parser = subparsers.add_parser("collect", help="Collect data")
    collect_parser.add_argument("--all", action="store_true")
    collect_parser.add_argument("--priority-high", action="store_true")
    collect_parser.add_argument("--entity", help="Specific entity")
    collect_parser.add_argument("--check-errors", action="store_true")
    
    # Diff
    diff_parser = subparsers.add_parser("diff", help="Detect changes")
    diff_parser.add_argument("--all", action="store_true")
    diff_parser.add_argument("--entity", help="Specific entity")
    diff_parser.add_argument("--source", help="Specific source")
    diff_parser.add_argument("--list", action="store_true")
    
    # Alerts
    alert_parser = subparsers.add_parser("alerts", help="Alert management")
    alert_parser.add_argument("--check", action="store_true")
    alert_parser.add_argument("--deliver", action="store_true")
    alert_parser.add_argument("--list", action="store_true")
    
    # Query
    query_parser = subparsers.add_parser("query", help="Natural language query")
    query_parser.add_argument("query", nargs="?", help="Query string")
    query_parser.add_argument("--list-competitors", action="store_true")
    query_parser.add_argument("--list-events", action="store_true")
    
    # Init
    init_parser = subparsers.add_parser("init", help="Initialize data directory")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Route to appropriate script
    if args.command == "init":
        return run_script("init.py")
    
    elif args.command == "track":
        args_list = [
            "--add",
            "--name", args.name,
            "--website", args.website or "",
            "--github", args.github or "",
            "--priority", args.priority
        ]
        exit_code = run_script("entity_resolve.py", args_list)
        
        if exit_code == 0 and args.refresh:
            entity_id = "company_" + args.name.lower().replace(" ", "_").replace("-", "_")
            run_script("collect.py", [entity_id])
    
    elif args.command == "stop-tracking":
        print(f"Stop tracking: {args.name}")
        print("(This would remove from registry — implement in full version)")
    
    elif args.command == "show":
        if args.competitors:
            return run_script("entity_resolve.py", ["--list"])
        elif args.people:
            print("People view not yet implemented")
        elif args.products:
            print("Products view not yet implemented")
        else:
            return run_script("entity_resolve.py", ["--list"])
    
    elif args.command == "check":
        if args.all:
            return run_script("diff.py", ["--all"])
        elif args.entity:
            if args.source:
                return run_script("diff.py", [args.entity, "--source", args.source])
            else:
                return run_script("diff.py", [args.entity])
        else:
            print("Specify --all or an entity ID")
            return 1
    
    elif args.command == "changes":
        if args.today:
            return run_script("query.py", ["What changed today"])
        elif args.week:
            return run_script("query.py", ["What changed this week"])
        elif args.entity:
            return run_script("query.py", [f"What changed about {args.entity}"])
        elif args.type:
            return run_script("query.py", [f"Show {args.type}"])
        else:
            print("Specify --today, --week, --entity, or --type")
            return 1
    
    elif args.command == "report":
        if args.daily:
            date_args = []
            if args.date:
                date_args = ["--date", args.date]
            else:
                date_args = ["--today"]
            return run_script("report.py", ["daily"] + date_args + 
                            (["--output"] if args.output else []))
        elif args.weekly:
            week_args = []
            if args.week_start:
                week_args = ["--week-start", args.week_start]
            return run_script("report.py", ["weekly"] + week_args + 
                            (["--output"] if args.output else []))
        else:
            print("Specify --daily or --weekly")
            return 1
    
    elif args.command == "health":
        return run_script("entity_resolve.py", ["--list"])
    
    elif args.command == "collect":
        args_list = []
        if args.all:
            args_list.append("--all")
        if args.priority_high:
            args_list.append("--priority-high")
        if args.entity:
            args_list.append(args.entity)
        if args.check_errors:
            args_list.append("--check-errors")
        
        if args_list:
            return run_script("collect.py", args_list)
        else:
            print("Specify --all, --entity, or --check-errors")
            return 1
    
    elif args.command == "diff":
        args_list = []
        if args.all:
            args_list.append("--all")
        if args.entity:
            args_list.append(args.entity)
        if args.source:
            args_list.extend(["--source", args.source])
        if args.list:
            args_list.append("--list")
        
        if args_list:
            return run_script("diff.py", args_list)
        else:
            print("Specify --all, --entity, or --list")
            return 1
    
    elif args.command == "alerts":
        if args.check:
            return run_script("alert.py", ["--check"])
        elif args.deliver:
            return run_script("alert.py", ["--deliver"])
        elif args.list:
            return run_script("alert.py", ["--list"])
        else:
            print("Specify --check, --deliver, or --list")
            return 1
    
    elif args.command == "query":
        if args.list_competitors:
            return run_script("query.py", ["--list-competitors"])
        elif args.list_events:
            return run_script("query.py", ["--list-events"])
        elif args.query:
            return run_script("query.py", [args.query])
        else:
            print("Specify a query or --list-competitors/--list-events")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
