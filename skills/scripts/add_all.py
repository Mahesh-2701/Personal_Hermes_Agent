#!/usr/bin/env python3
"""Add all AI competitors and IT personalities."""

import os
import sys
import yaml
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"
PEOPLE_FILE = DATA_DIR / "people.yaml"


def load_auth():
    """Load Telegram auth from Hermes auth.json"""
    auth_file = Path.home() / ".hermes" / "auth.json"
    if auth_file.exists():
        with open(auth_file) as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}


def get_telegram_token():
    """Get the Telegram bot token from auth."""
    auth = load_auth()
    
    # Try different key patterns
    for key in auth:
        if "telegram" in key.lower() and "token" in key.lower():
            val = auth[key]
            if val and len(str(val)) > 20:
                return str(val)
    
    # Try nested structure
    if isinstance(auth, dict):
        for section in ["telegram", "platforms", "credentials"]:
            if section in auth and isinstance(auth[section], dict):
                for k, v in auth[section].items():
                    if "token" in str(k).lower() and v and len(str(v)) > 20:
                        return str(v)
    
    return None


def load_all():
    if COMPETITORS_FILE.exists():
        with open(COMPETITORS_FILE) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {"competitors": []}
    
    if PEOPLE_FILE.exists():
        with open(PEOPLE_FILE) as f:
            pdata = yaml.safe_load(f) or {}
    else:
        pdata = {"people": []}
    
    return data.get("competitors", []), pdata.get("people", [])


def save_all(competitors, people):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(COMPETITORS_FILE, "w") as f:
        yaml.dump({"competitors": competitors}, f, default_flow_style=False)
    with open(PEOPLE_FILE, "w") as f:
        yaml.dump({"people": people}, f, default_flow_style=False)


def add_competitor(name, website, github, priority, products=[]):
    competitors, people = load_all()
    # Remove duplicates
    competitors = [c for c in competitors if c["name"] != name]
    
    base_id = "company_" + name.lower().replace(" ", "_")[:30]
    counter = 1
    comp_id = base_id
    while any(c["id"] == comp_id for c in competitors):
        comp_id = f"{base_id}_{counter}"
        counter += 1
    
    comp = {
        "id": comp_id,
        "name": name,
        "website": website,
        "github": github,
        "priority": priority,
        "products": products,
        "sources": {
            "website": bool(website),
            "github": bool(github),
            "news": True,
            "youtube": True,
            "twitter": True,
            "linkedin": True,
            "reddit": True,
        },
        "created_at": datetime.utcnow().isoformat(),
    }
    
    competitors.append(comp)
    save_all(competitors, people)
    print(f"  Added: {name} ({comp_id}) - {priority}")
    return comp_id


def add_person(name, company_id, role):
    competitors, people = load_all()
    # Check duplicate
    if any(p["name"] == name for p in people):
        print(f"  Skipping {name} (already tracked)")
        return
    
    base_id = "person_" + name.lower().replace(" ", "_")[:30]
    counter = 1
    person_id = base_id
    while any(p["id"] == person_id for p in people):
        person_id = f"{base_id}_{counter}"
        counter += 1
    
    person = {
        "id": person_id,
        "name": name,
        "company": company_id,
        "role": role,
        "sources": {"x": True, "linkedin": False, "news": True},
        "added_at": datetime.utcnow().isoformat(),
    }
    
    people.append(person)
    save_all(competitors, people)
    print(f"  Added: {name} - {role}")


print("=== Adding Competitors ===\n")

add_competitor("Anthropic", "https://anthropic.com", "anthropic-ai", "high",
               ["Claude", "Claude API", "Claude Desktop", "Claude 3", "Claude 3.5", "Artifacts"])
add_competitor("Google DeepMind", "https://deepmind.google", "google-deepmind", "high",
               ["Gemini", "Gemini API", "AlphaFold", "Vertex AI", "Imagen"])
add_competitor("Meta AI", "https://ai.meta.com", "facebookresearch", "high",
               ["LLaMA", "LLaMA 2", "LLaMA 3", "LLaMA 3.1", "LLaMA 3.2", "Segment Anything"])
add_competitor("Mistral AI", "https://mistral.ai", "mistralai", "high",
               ["Mistral", "Mistral Large", "Mistral Small", "Codestral", "Mixtral"])
add_competitor("DeepSeek", "https://deepseek.com", "deepseek-ai", "high",
               ["DeepSeek-V2", "DeepSeek-V3", "DeepSeek-R1", "DeepSeek-Coder"])
add_competitor("xAI", "https://x.ai", "xai-org", "high",
               ["Grok", "Grok-2", "Grok-3"])
add_competitor("Cohere", "https://cohere.com", "cohere-ai", "medium",
               ["Command", "Embed", "Rerank", "Aya"])
add_competitor("Hugging Face", "https://huggingface.co", "huggingface", "medium",
               ["Transformers", "Diffusers", "Pipelines", "Inference API", "Hub"])
add_competitor("Stability AI", "https://stability.ai", "Stability-AI", "medium",
               ["Stable Diffusion", "Stable Video", "Stable Audio", "SDXL"])
add_competitor("EleutherAI", "https://eleuther.ai", "EleutherAI", "low",
               ["GPT-Neo", "GPT-J", "Pythia", "Pile"])

print(f"\nCompetitors added. Total: ", end="")
competitors, _ = load_all()
print(f"{len(competitors)}")

print("\n=== Adding People ===\n")

# Get competitor IDs
comp_ids = {c["name"]: c["id"] for c in competitors}

add_person("Sam Altman", comp_ids.get("OpenAI"), "CEO of OpenAI")
add_person("Greg Brockman", comp_ids.get("OpenAI"), "President & Co-founder of OpenAI")
add_person("Dario Amodei", comp_ids.get("Anthropic"), "CEO of Anthropic")
add_person("Daniela Amodei", comp_ids.get("Anthropic"), "President of Anthropic")
add_person("Sundar Pichai", comp_ids.get("Google DeepMind"), "CEO of Google & Alphabet")
add_person("Demis Hassabis", comp_ids.get("Google DeepMind"), "CEO of DeepMind")
add_person("Yann LeCun", comp_ids.get("Meta AI"), "Chief AI Scientist at Meta")
add_person("Andrej Karpathy", comp_ids.get("Meta AI"), "Former Director of AI at Tesla / NVIDIA")
add_person("Mark Zuckerberg", comp_ids.get("Meta AI"), "CEO of Meta")
add_person("Arthur Mensch", comp_ids.get("Mistral AI"), "CEO of Mistral AI")
add_person("Elon Musk", comp_ids.get("xAI"), "CEO of xAI / Tesla / SpaceX")
add_person("Clément Delangue", comp_ids.get("Hugging Face"), "CEO of Hugging Face")
add_person("Emad Mostaque", comp_ids.get("Stability AI"), "Former CEO of Stability AI")
add_person("Aidan Gomez", comp_ids.get("Cohere"), "Co-founder & CEO of Cohere")

# Additional IT / VC personalities
add_person("Jensen Huang", "", "CEO of NVIDIA")
add_person("Lisa Su", "", "CEO of AMD")
add_person("Andrew Ng", "", "Founder of DeepLearning.AI")
add_person("Fei-Fei Li", "", "Professor at Stanford / AI researcher")
add_person("Naval Ravikant", "", "AngelList co-founder / investor")
add_person("Marc Andreessen", "", "Co-founder of a16z")
add_person("Ben Horowitz", "", "Co-founder of a16z")
add_person("Elad Gil", "", "AI investor / entrepreneur")

people = load_all()[1]
print(f"\nPeople tracked: {len(people)}")
print("\n=== DONE ===")
