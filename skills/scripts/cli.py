#!/usr/bin/env python3
"""
Competitor Intelligence — CLI Entry Point
Main command interface for the competitor intelligence system.
"""

import os
import sys
import argparse
from pathlib import Path

SKILL_DIR = Path(os.path.expanduser("~/.hermes/skills/competitor-intelligence"))
SCRIPTS_DIR = SKILL_DIR / "scripts"
DATA_DIR = Path(os.path.expanduser("~/.hermes/data/competitor-intelligence"))

def run_script(script_name, args):
    """Run a script from the scripts directory."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"Error: Script not found: {script_name}")
        return 1
    
    import subprocess
    result = subprocess.run(
        [sys.executable, str(script_path)] + args,
        capture_output=False
    )
    return result.returncode

def main():
    parser = argparse.ArgumentParser(
        description="Competitor Intelligence System",
        prog="competitor-intelligence"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Track command
    track_parser = subparsers.add_parser("track", help="Track a competitor")
    track_parser.add_argument("name", help="Competitor name")
    track_parser.add_argument("--website", help="Website URL")
    track_parser.add_argument("--github", help="GitHub organization")
    track_parser.add_argument("--priority", 
                             choices=["high", "medium", "low"],
                             default="medium",
                             help="Tracking priority")
    track_parser.add_argument("--refresh", action="store_true",
                             help="Collect baseline after adding")
    
    # Stop tracking command
    stop_parser = subparsers.add_parser("stop-tracking", help="Stop tracking a competitor")
    stop_parser.add_argument("name", help="Competitor name or ID")
    
    # Show competitors
    show_parser = subparsers.add_parser("show", help="Show tracked competitors")
    show_parser.add_argument("--competitors", action="store_true", help="Show competitors")
    show_parser.add_argument("--people", action="store_true", help="Show people")
    show_parser.add_argument("--products", action="store_true", help="Show products")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check a competitor for changes")
    check_parser.add_argument("entity", help="Entity ID to check")
    check_parser.add_argument("--source", help="Specific source to check")
    
    # Refresh command
    refresh_parser = subparsers.add_parser("refresh", help="Force refresh collection")
    refresh_parser.add_argument("entity", help="Entity ID to refresh")
    
    # Change queries
    change_parser = subparsers.add_parser("changes", help="Query changes")
    change_parser.add_argument("--today", action="store_true", help="Changes today")
    change_parser.add_argument("--week", action="store_true", help="Changes this week")
    change_parser.add_argument("--entity", help="Specific entity")
    change_parser.add_argument("--type", help="Filter by event type")
    
    # Report commands
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument("--daily", action="store_true", help="Daily report")
    report_parser.add_argument("--weekly", action="store_true", help="Weekly report")
    report_parser.add_argument("--date", help="Specific date (YYYY-MM-DD)")
    report_parser.add_argument("--week-start", help="Week start (YYYY-MM-DD)")
    report_parser.add_argument("--output", action="store_true", 
                              help="Print to stdout")
    
    # Source health
    health_parser = subparsers.add_parser("health", help="Source health status")
    
    # Collection commands
    collect_parser = subparsers.add_parser("collect", help="Run collection")
    collect_parser.add_argument("--all", action="store_true", help="Collect all")
    collect_parser.add_argument("--priority-high", action="store_true",
                                help="Only high priority")
    collect_parser.add_argument("--entity", help="Specific entity")
    collect_parser.add_argument("--check-errors", action="store_true",
                                help="Check for errors")
    
    # Diff commands
    diff_parser = subparsers.add_parser("diff", help="Run diff detection")
    diff_parser.add_argument("--all", action="store_true", help="Diff all")
    diff_parser.add_argument("--entity", help="Specific entity")
    diff_parser.add_argument("--source", help="Specific source")
    diff_parser.add_argument("--list", action="store_true", help="List recent events")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Route to appropriate script
    if args.command == "track":
        # Use entity_resolve.py to add
        exit_code = run_script("entity_resolve.py", [
            "--add",
            "--name", args.name,
            "--website", args.website or "",
            "--github", args.github or "",
            "--priority", args.priority
        ])
        
        if exit_code == 0 and args.refresh:
            # Then collect
            run_script("collect.py", [f"company_{args.name.lower().replace(' ', '_')}"])
    
    elif args.command == "stop-tracking":
        # Would need to implement removal - for now just report
        print(f"Stop tracking: {args.name}")
        print("(This would remove from registry in full implementation)")
    
    elif args.command == "show":
        if args.competitors:
            run_script("entity_resolve.py", ["--list"])
        elif args.people or args.products:
            print("People/Products views coming soon.")
        else:
            run_script("entity_resolve.py", ["--list"])
    
    elif args.command == "check":
        run_script("diff.py", [args.entity] + 
                  (["--source", args.source] if args.source else []))
    
    elif args.command == "refresh":
        run_script("collect.py", [args.entity])
        run_script("diff.py", [args.entity])
    
    elif args.command == "changes":
        if args.today:
            run_script("query.py", [
                f"What changed today{' for ' + args.entity if args.entity else ''}"
            ])
        elif args.week:
            run_script("query.py", [
                f"What changed this week{' for ' + args.entity if args.entity else ''}"
            ])
        elif args.entity:
            run_script("query.py", args.entity)
        elif args.type:
            run_script("query.py", f"Show {args.type}")
        else:
            print("Specify --today, --week, --entity, or --type")
    
    elif args.command == "report":
        if args.daily:
            date_arg = ["--date", args.date] if args.date else ["--today"]
            run_script("report.py", ["daily"] + date_arg + (["--output"] if args.output else []))
        elif args.weekly:
            week_arg = ["--week-start", args.week_start] if args.week_start else []
            run_script("report.py", ["weekly"] + week_arg + (["--output"] if args.output else []))
        else:
            print("Specify --daily or --weekly")
    
    elif args.command == "health":
        if DATA_DIR / "source_health.json".exists():
            import json
            with open(DATA_DIR / "source_health.json") as f:
                health = json.load(f)
            print("Source Health Status:")
            print("=" * 50)
            for entity_id, sources in health.items():
                print(f"\n{entity_id}:")
                for source, info in sources.items():
                    status = info.get("status", "unknown")
                    icon = "✓" if status == "working" else "✗"
                    print(f"  {icon} {source}: {status}")
        else:
            print("No source health data available yet.")
            print("Run 'collect --all' first to populate.")
    
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
            run_script("collect.py", args_list)
        else:
            print("Specify --all, --entity, or --check-errors")
    
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
            run_script("diff.py", args_list)
        else:
            print("Specify --all, --entity, or --list")
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
