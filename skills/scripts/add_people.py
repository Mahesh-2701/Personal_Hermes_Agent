#!/usr/bin/env python3
"""Add AI/IT personalities to the watchlist and fix competitor IDs."""

import sys
sys.path.insert(0, '/Users/apple/.hermes/skills/competitor-intelligence/scripts')
from entity_resolve import EntityResolver
import yaml
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
PEOPLE_FILE = DATA_DIR / "people.yaml"


def load_people():
    if PEOPLE_FILE.exists():
        with open(PEOPLE_FILE) as f:
            data = yaml.safe_load(f) or {}
        return data.get("people", [])
    return []


def save_people(people):
    PEOPLE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PEOPLE_FILE, "w") as f:
        yaml.dump({"people": people}, f, default_flow_style=False)


def add_person(name, company_id, role, sources=None):
    people = load_people()
    
    person_id = "person_" + name.lower().replace(" ", "_").replace("-", "_")[:30]
    
    # Check for duplicates
    for p in people:
        if p["id"] == person_id:
            print(f"  Skipping {name} (already tracked)")
            return
    
    person = {
        "id": person_id,
        "name": name,
        "company": company_id,
        "role": role,
        "sources": sources or {
            "x": True,
            "linkedin": True,
            "github": False,
            "website": False,
            "news": True,
        },
        "added_at": datetime.utcnow().isoformat(),
    }
    
    people.append(person)
    save_people(people)
    
    print(f"  Added: {name} ({role} at {company_id})")


# First, list current competitors
resolver = EntityResolver()
competitors = resolver.list_competitors()
print("Current competitors:")
for c in competitors:
    print(f"  {c['name']} -> {c['id']}")

print("\nAdding AI/IT personalities:")

# Map personalities to competitor IDs
people_to_add = [
    ("Sam Altman", "company_openai", "CEO"),
    ("Greg Brockman", "company_openai", "President & Co-founder"),
    ("Ilya Sutskever", "company_openai", "Co-founder (previously Chief Scientist)"),
    ("Dario Amodei", "company_anthropic_1", "CEO"),
    ("Daniela Amodei", "company_anthropic_1", "President"),
    ("Sundar Pichai", "company_google_deepmind_1", "CEO of Google & Alphabet"),
    ("Demis Hassabis", "company_google_deepmind_1", "CEO of DeepMind"),
    ("Yann LeCun", "company_meta_ai_1", "Chief AI Scientist at Meta"),
    ("Andrej Karpathy", "company_meta_ai_1", "Former Director of AI (now independent)"),
    ("Mark Zuckerberg", "company_meta_ai_1", "CEO of Meta"),
    ("Arthur Mensch", "company_mistral_1", "CEO of Mistral AI"),
    ("Jimmy Bailey", "company_deepseek_1", "CEO of DeepSeek (alias: Lianwen Wen)"),
    ("Elon Musk", "company_xai_1", "CEO of xAI"),
    ("Emad Mostaque", "company_stability_ai_1", "Former CEO of Stability AI"),
    ("Clément Delangue", "company_hugging_face", "CEO of Hugging Face"),
    ("Andrej Karpathy", "company_openai", "Founding member (previously)"),
]

for name, company, role in people_to_add:
    add_person(name, company, role)

print(f"\nTotal people tracked: {len(load_people())}")
