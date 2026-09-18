#!/usr/bin/env python3
"""Competitor Intelligence — Entity Resolution Utility"""

import re
import yaml
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"


class EntityResolver:
    def __init__(self):
        self.competitors = {}
        self.aliases = {}
        self._load()
    
    def _load(self):
        if COMPETITORS_FILE.exists():
            with open(COMPETITORS_FILE) as f:
                data = yaml.safe_load(f) or {}
            
            for comp in data.get("competitors", []):
                comp_id = comp["id"]
                self.competitors[comp_id] = comp
                
                name = comp.get("name", "")
                if name:
                    self.aliases[name.lower()] = comp_id
                    self.aliases[name.lower().replace(" ", "")] = comp_id
                
                website = comp.get("website", "")
                if website:
                    domain = self._extract_domain(website)
                    if domain:
                        self.aliases[domain] = comp_id
                
                github = comp.get("github", "")
                if github:
                    self.aliases[github.lower()] = comp_id
                    self.aliases[f"@{github.lower()}"] = comp_id
                
                for product in comp.get("products", []):
                    self.aliases[product.lower()] = comp_id
        
        print(f"Loaded {len(self.competitors)} competitors, {len(self.aliases)} aliases")
    
    def _extract_domain(self, url):
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else None
    
    def resolve(self, query):
        query = query.strip().lower()
        
        if query in self.aliases:
            comp_id = self.aliases[query]
            return ("competitor", comp_id, self.competitors.get(comp_id, {}))
        
        for alias, comp_id in self.aliases.items():
            if alias in query or query in alias:
                return ("competitor", comp_id, self.competitors.get(comp_id, {}))
        
        return None
    
    def add_competitor(self, name, website="", github="", priority="medium", 
                       products=None, sources=None):
        base_id = "company_" + re.sub(r'[^a-z0-9]', '_', name.lower()).strip('_')
        counter = 1
        comp_id = base_id
        while comp_id in self.competitors:
            comp_id = f"{base_id}_{counter}"
            counter += 1
        
        competitor = {
            "id": comp_id,
            "name": name,
            "website": website,
            "github": github,
            "priority": priority,
            "products": products or [],
            "sources": sources or {
                "website": True,
                "github": bool(github),
                "news": True,
                "youtube": True,
                "twitter": True,
                "linkedin": True,
                "reddit": True,
            },
            "created_at": datetime.utcnow().isoformat(),
        }
        
        self.competitors[comp_id] = competitor
        
        self.aliases[name.lower()] = comp_id
        if website:
            domain = self._extract_domain(website)
            if domain:
                self.aliases[domain] = comp_id
        if github:
            self.aliases[github.lower()] = comp_id
            self.aliases[f"@{github.lower()}"] = comp_id
        for product in products or []:
            self.aliases[product.lower()] = comp_id
        
        data = {"competitors": list(self.competitors.values())}
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(COMPETITORS_FILE, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        
        print(f"Added competitor: {name} (ID: {comp_id})")
        return comp_id
    
    def list_competitors(self):
        return list(self.competitors.values())
    
    def remove_competitor(self, comp_id):
        if comp_id in self.competitors:
            del self.competitors[comp_id]
            self.aliases = {}
            for comp in self.competitors.values():
                name = comp.get("name", "")
                if name:
                    self.aliases[name.lower()] = comp["id"]
                website = comp.get("website", "")
                if website:
                    domain = self._extract_domain(website)
                    if domain:
                        self.aliases[domain] = comp["id"]
                github = comp.get("github", "")
                if github:
                    self.aliases[github.lower()] = comp["id"]
            
            data = {"competitors": list(self.competitors.values())}
            with open(COMPETITORS_FILE, "w") as f:
                yaml.dump(data, f, default_flow_style=False)
            
            print(f"Removed competitor: {comp_id}")
            return True
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Competitor Intelligence - Entity Resolution")
    parser.add_argument("query", nargs="?", help="Resolve entity name/alias")
    parser.add_argument("--add", action="store_true", help="Add a competitor")
    parser.add_argument("--name", help="Competitor name")
    parser.add_argument("--website", help="Website URL")
    parser.add_argument("--github", help="GitHub username/org")
    parser.add_argument("--priority", choices=["high", "medium", "low"], default="medium")
    parser.add_argument("--products", help="Comma-separated product names")
    parser.add_argument("--remove", help="Remove competitor by ID")
    parser.add_argument("--list", action="store_true", help="List all competitors")
    
    args = parser.parse_args()
    
    resolver = EntityResolver()
    
    if args.list:
        competitors = resolver.list_competitors()
        if not competitors:
            print("No competitors tracked yet.")
        else:
            print(f"Tracked Competitors ({len(competitors)}):")
            for comp in competitors:
                print(f"\n  {comp['name']} ({comp['id']})")
                print(f"    Website: {comp.get('website', 'N/A')}")
                print(f"    GitHub: {comp.get('github', 'N/A')}")
                print(f"    Priority: {comp.get('priority', 'medium')}")
                print(f"    Products: {', '.join(comp.get('products', [])) or 'None'}")
    
    elif args.remove:
        if resolver.remove_competitor(args.remove):
            print(f"Successfully removed: {args.remove}")
        else:
            print(f"Competitor not found: {args.remove}")
    
    elif args.add:
        if not args.name:
            print("Error: --name is required")
            return
        products = args.products.split(",") if args.products else []
        resolver.add_competitor(
            name=args.name,
            website=args.website or "",
            github=args.github or "",
            priority=args.priority,
            products=products
        )
    
    elif args.query:
        result = resolver.resolve(args.query)
        if result:
            entity_type, entity_id, data = result
            print(f"Resolved: {args.query}")
            print(f"  Type: {entity_type}")
            print(f"  ID: {entity_id}")
            print(f"  Name: {data.get('name', 'N/A')}")
            print(f"  Website: {data.get('website', 'N/A')}")
            print(f"  GitHub: {data.get('github', 'N/A')}")
            print(f"  Priority: {data.get('priority', 'medium')}")
        else:
            print(f"Not found: {args.query}")
            print("Use --add to add as a competitor.")
    
    else:
        print("Usage:")
        print("  entity_resolve.py <query>           - Resolve entity")
        print("  entity_resolve.py --list            - List all competitors")
        print("  entity_resolve.py --add --name X    - Add competitor")
        print("  entity_resolve.py --remove <id>     - Remove competitor")


if __name__ == "__main__":
    main()
