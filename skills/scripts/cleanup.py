#!/usr/bin/env python3
"""Keep the better versions of competitors (with products) and remove duplicates."""

import sys
sys.path.insert(0, '/Users/apple/.hermes/skills/competitor-intelligence/scripts')
import yaml
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"


def main():
    with open(COMPETITORS_FILE) as f:
        data = yaml.safe_load(f) or {}
    
    competitors = data.get("competitors", [])
    print(f"Before: {len(competitors)} competitors\n")
    
    # Group by normalized name
    by_name = {}
    for comp in competitors:
        name = comp["name"].strip()
        if name not in by_name:
            by_name[name] = []
        by_name[name].append(comp)
    
    # For each group, keep the one with more data (products preferred)
    final = []
    removed = []
    
    for name, entries in by_name.items():
        if len(entries) == 1:
            final.append(entries[0])
        else:
            # Pick the one with products or most recent
            with_products = [e for e in entries if e.get("products")]
            if with_products:
                best = max(with_products, key=lambda x: len(x.get("products", [])))
            else:
                best = max(entries, key=lambda x: x.get("created_at", ""))
            
            final.append(best)
            for e in entries:
                if e["id"] != best["id"]:
                    removed.append(e["name"])
                    print(f"  Removed duplicate: {e['name']} ({e['id']})")
            
            print(f"  Kept: {best['name']} ({best['id']})")
    
    data["competitors"] = final
    
    with open(COMPETITORS_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print(f"\nAfter: {len(final)} competitors (removed {len(removed)} duplicates)")
    print("\nFinal tracked competitors:")
    for comp in final:
        priority = comp.get("priority", "N/A").upper()
        products = comp.get("products", [])
        print(f"\n  [{priority}] {comp['name']} ({comp['id']})")
        print(f"    Website: {comp.get('website', 'N/A')}")
        print(f"    GitHub: {comp.get('github', 'N/A')}")
        if products:
            print(f"    Products: {', '.join(products)}")


if __name__ == "__main__":
    main()
