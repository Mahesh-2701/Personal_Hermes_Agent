#!/usr/bin/env python3
"""Update SKILL.md with current competitor counts."""

import sys, yaml
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"
PEOPLE_FILE = DATA_DIR / "people.yaml"
SKILL_FILE = Path.home() / ".hermes" / "skills" / "competitor-intelligence" / "SKILL.md"


def load_competitors():
    if COMPETITORS_FILE.exists():
        with open(COMPETITORS_FILE) as f:
            data = yaml.safe_load(f) or {}
        return data.get("competitors", [])
    return []


def load_people():
    if PEOPLE_FILE.exists():
        with open(PEOPLE_FILE) as f:
            data = yaml.safe_load(f) or {}
        return data.get("people", [])
    return []


def main():
    competitors = load_competitors()
    people = load_people()
    high = [c for c in competitors if c.get("priority") == "high"]
    medium = [c for c in competitors if c.get("priority") == "medium"]
    low = [c for c in competitors if c.get("priority") == "low"]
    
    print(f"Competitors: {len(competitors)} (H:{len(high)} M:{len(medium)} L:{len(low)})")
    print(f"People: {len(people)}")
    
    if not SKILL_FILE.exists():
        print("SKILL.md not found!")
        return
    
    content = SKILL_FILE.read_text()
    
    # Update counts
    content = content.replace("Supports 11+ AI competitors", f"Supports {len(competitors)}+ AI competitors")
    content = content.replace("and 24+ IT personalities", f"and {len(people)}+ IT personalities")
    content = content.replace("## TRACKED COMPETITORS (11)", f"## TRACKED COMPETITORS ({len(competitors)})")
    content = content.replace("## TRACKED PEOPLE (24)", f"## TRACKED PEOPLE ({len(people)})")
    content = content.replace("### High Priority (7)", f"### High Priority ({len(high)})")
    content = content.replace("### Medium Priority (3)", f"### Medium Priority ({len(medium)})")
    content = content.replace("### Low Priority (1)", f"### Low Priority ({len(low)})")
    
    SKILL_FILE.write_text(content)
    print("\nSKILL.md updated with current counts!")


if __name__ == "__main__":
    main()
