#!/usr/bin/env python3
"""
Initialize the competitor intelligence data directory.
"""

import os
from pathlib import Path

DATA_DIR = Path(os.path.expanduser("~/.hermes/data/competitor-intelligence"))


def init():
    """Create directory structure."""
    dirs = [
        DATA_DIR,
        DATA_DIR / "events",
        DATA_DIR / "snapshots",
        DATA_DIR / "reports" / "daily",
        DATA_DIR / "reports" / "weekly",
        DATA_DIR / "alerts",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created: {d}")
    
    # Create empty events file
    events_file = DATA_DIR / "events" / "events.jsonl"
    if not events_file.exists():
        events_file.touch()
        print(f"Created: {events_file}")
    
    # Create source health
    health_file = DATA_DIR / "source_health.json"
    if not health_file.exists():
        health_file.write_text("{}")
        print(f"Created: {health_file}")
    
    print("\nInitialization complete!")
    print(f"Data directory: {DATA_DIR}")


if __name__ == "__main__":
    init()
