#!/usr/bin/env python3
"""Add 20+ more competitors and 25+ more IT personalities."""

import sys, yaml
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "data" / "competitor-intelligence"
COMPETITORS_FILE = DATA_DIR / "competitors.yaml"
PEOPLE_FILE = DATA_DIR / "people.yaml"


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


def save_competitors(competitors):
    COMPETITORS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPETITORS_FILE, "w") as f:
        yaml.dump({"competitors": competitors}, f, default_flow_style=False)


def save_people(people):
    PEOPLE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PEOPLE_FILE, "w") as f:
        yaml.dump({"people": people}, f, default_flow_style=False)


def add_competitor(name, website, github, priority, products):
    competitors, people = load_all()
    
    # Remove any existing with same name
    competitors = [c for c in competitors if c["name"] != name]
    # Also remove by website
    competitors = [c for c in competitors if c.get("website") != website]
    # Also remove by github
    competitors = [c for c in competitors if c.get("github") != github]
    
    base_id = "company_" + name.lower().replace(" ", "_").replace("-", "_")[:30]
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
    save_competitors(competitors)
    print(f"  Added: {name} ({comp_id}) - {priority} [{len(products)} products]")
    return comp_id


def add_person(name, company_id, role):
    competitors, people = load_all()
    
    if any(p["name"] == name for p in people):
        print(f"  Skipping person: {name} (already tracked)")
        return
    
    base_id = "person_" + name.lower().replace(" ", "_").replace("-", "_")[:30]
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
        "sources": {"x": True, "linkedin": False, "news": True, "youtube": False},
        "added_at": datetime.utcnow().isoformat(),
    }
    
    people.append(person)
    save_people(people)
    print(f"  Added: {name} - {role}")


print("=== Additional AI Companies ===\n")

# More AI/tech companies (some may be duplicates - script handles dedup)
companies = [
    ("OpenAI", "https://openai.com", "openai", "high",
     ["ChatGPT", "GPT-4", "GPT-4o", "GPT-5", "Sora", "DALL-E", "Whisper", "Codex"]),
    ("Anthropic", "https://anthropic.com", "anthropic-ai", "high",
     ["Claude", "Claude API", "Claude Desktop", "Claude 3", "Claude 3.5", "Artifacts"]),
    ("Google DeepMind", "https://deepmind.google", "google-deepmind", "high",
     ["Gemini", "Gemini API", "AlphaFold", "Vertex AI", "Imagen"]),
    ("Meta AI", "https://ai.meta.com", "facebookresearch", "high",
     ["LLaMA", "LLaMA 2", "LLaMA 3", "LLaMA 3.1", "Segment Anything"]),
    ("Mistral AI", "https://mistral.ai", "mistralai", "high",
     ["Mistral", "Mistral Large", "Mistral Small", "Codestral", "Mixtral"]),
    ("DeepSeek", "https://deepseek.com", "deepseek-ai", "high",
     ["DeepSeek-V2", "DeepSeek-V3", "DeepSeek-R1", "DeepSeek-Coder"]),
    ("xAI", "https://x.ai", "xai-org", "high",
     ["Grok", "Grok-2", "Grok-3"]),
    ("Perplexity AI", "https://perplexity.ai", "perplexity-ai", "high",
     ["Perplexity", "Perplexity Pro", "Perplexity API"]),
    ("Character.AI", "https://character.ai", "characterai", "high",
     ["Character.AI", "Character Chat"]),
    ("Anduril", "https://anduril.com", "anduril", "high",
     ["Anduril Lattice", "Anduril Weapons", "Anvil"]),
    ("Scale AI", "https://scale.com", "scale-ai", "high",
     ["Scale AI", "Scale RLHF", "Scale Spark"]),
    ("Figure AI", "https://figure.ai", "figure-ai", "high",
     ["Figure 01", "Figure 02", "Figure Robot"]),
    ("Cognition AI", "https://cognition.xyz", "devin-ai", "high",
     ["Devin", "Cognition AI"]),
    ("Cohere", "https://cohere.com", "cohere-ai", "medium",
     ["Command", "Embed", "Rerank", "Aya"]),
    ("Hugging Face", "https://huggingface.co", "huggingface", "medium",
     ["Transformers", "Diffusers", "Hub", "Spaces"]),
    ("Stability AI", "https://stability.ai", "Stability-AI", "medium",
     ["Stable Diffusion", "Stable Video", "Stable Audio"]),
    ("Together AI", "https://together.ai", "togethercomputer", "medium",
     ["Together AI", "Together Cloud"]),
    ("Replicate", "https://replicate.com", "replicate", "medium",
     ["Replicate", "Replicate API"]),
    ("Weights & Biases", "https://wandb.ai", "wandb", "medium",
     ["W&B", "W&B MLOps", "W&B Prompts"]),
    ("Anyscale", "https://anyscale.com", "anyscale", "medium",
     ["Anyscale", "Ray"]),
    ("Glean", "https://glean.com", "glean", "medium",
     ["Glean Search", "Glean Assistant"]),
    ("Notion", "https://notion.so", "notion", "medium",
     ["Notion AI", "Notion Workspace"]),
    ("Synthesia", "https://synthesia.io", "synthesia", "medium",
     ["Synthesia Studio", "Synthesia API"]),
    ("Midjourney", "https://midjourney.com", "", "high",
     ["Midjourney", "Midjourney V6"]),
    ("Runway", "https://runwayml.com", "runwayml", "medium",
     ["Runway Gen-1", "Runway Gen-2"]),
    ("Adobe", "https://adobe.com", "adobe", "medium",
     ["Adobe Firefly", "Adobe Express AI"]),
    ("Microsoft", "https://microsoft.com", "microsoft", "high",
     ["Microsoft Copilot", "Azure AI", "Bing Chat", "GitHub Copilot", "Phi"]),
    ("Amazon", "https://amazon.com", "amazon", "high",
     ["Amazon Bedrock", "Amazon Q", "CodeWhisperer", "Titan"]),
    ("IBM", "https://ibm.com", "ibm", "medium",
     ["IBM Watson", "watsonx"]),
    ("Palantir", "https://palantir.com", "palantir", "high",
     ["Palantir Gotham", "Palantir Foundry", "Palantir AIP"]),
    ("C3.ai", "https://c3.ai", "c3ai", "medium",
     ["C3 AI Suite", "C3 AI Applications"]),
    ("H2O.ai", "https://h2o.ai", "h2oai", "medium",
     ["H2O Driverless AI", "H2O-3"]),
    ("Dataiku", "https://dataiku.com", "dataiku", "medium",
     ["Dataiku DSS", "Dataiku AutoML"]),
    ("Baidu", "https://baidu.com", "baidu", "medium",
     ["Baidu Ernie", "Baidu AI Cloud"]),
    ("Alibaba", "https://alibaba.com", "alibaba", "medium",
     ["Alibaba Qwen", "Tongyi Qianwen"]),
    ("Tencent", "https://tencent.com", "tencent", "medium",
     ["Tencent Hunyuan", "Tencent AI"]),
    ("ByteDance", "https://bytedance.com", "bytedance", "medium",
     ["ByteDance Doubao", "ByteDance AI"]),
    ("Moonshot AI", "https://moonshot.ai", "moonshot-ai", "medium",
     ["Moonshot AI", "Kimi"]),
    ("Zhipu AI", "https://zhipu.ai", "zhipu-ai", "medium",
     ["Zhipu AI", "GLM", "ChatGLM"]),
    ("MiniMax", "https://minimaxi.com", "minimax", "medium",
     ["MiniMax", "Hailuo"]),
    ("01.AI", "https://01.ai", "01-ai", "medium",
     ["01.AI Yi", "01.AI API"]),
    ("Stepfun", "https://stepfun.com", "stepfun", "low",
     ["Stepfun", "Stepfun Models"]),
    ("Samsung", "https://samsung.com", "samsung", "medium",
     ["Samsung Gauss", "Galaxy AI"]),
    ("Huawei", "https://huawei.com", "huawei", "medium",
     ["Huawei Pangu", "MindSpore"]),
    ("EleutherAI", "https://eleuther.ai", "EleutherAI", "low",
     ["GPT-Neo", "GPT-J", "Pythia"]),
    ("xAI", "https://x.ai", "xai-org", "high",
     ["Grok", "Grok-2", "Grok-3", "Grok Beta"]),
]

for name, website, github, priority, products in companies:
    add_competitor(name, website, github, priority, products)

competitors, _ = load_all()
print(f"\nTotal competitors: {len(competitors)}")

print("\n=== Additional Notable People ===\n")

comp_ids = {c["name"]: c["id"] for c in competitors}

people = [
    ("Sam Altman", comp_ids.get("OpenAI"), "CEO of OpenAI"),
    ("Greg Brockman", comp_ids.get("OpenAI"), "President & Co-founder of OpenAI"),
    ("Ilya Sutskever", comp_ids.get("OpenAI"), "Co-founder of OpenAI"),
    ("Dario Amodei", comp_ids.get("Anthropic"), "CEO of Anthropic"),
    ("Daniela Amodei", comp_ids.get("Anthropic"), "President of Anthropic"),
    ("Sundar Pichai", comp_ids.get("Google DeepMind"), "CEO of Google & Alphabet"),
    ("Demis Hassabis", comp_ids.get("Google DeepMind"), "CEO of DeepMind"),
    ("Yann LeCun", comp_ids.get("Meta AI"), "Chief AI Scientist at Meta"),
    ("Andrej Karpathy", comp_ids.get("Meta AI"), "Former Director of AI at Tesla / NVIDIA"),
    ("Mark Zuckerberg", comp_ids.get("Meta AI"), "CEO of Meta"),
    ("Arthur Mensch", comp_ids.get("Mistral AI"), "CEO of Mistral AI"),
    ("Elon Musk", comp_ids.get("xAI"), "CEO of xAI / Tesla / SpaceX"),
    ("Clément Delangue", comp_ids.get("Hugging Face"), "CEO of Hugging Face"),
    ("Aidan Gomez", comp_ids.get("Cohere"), "Co-founder & CEO of Cohere"),
    ("Emad Mostaque", comp_ids.get("Stability AI"), "Former CEO of Stability AI"),
    ("Jensen Huang", "", "CEO of NVIDIA"),
    ("Lisa Su", "", "CEO of AMD"),
    ("Andrew Ng", "", "Founder of DeepLearning.AI"),
    ("Fei-Fei Li", "", "Professor at Stanford / AI researcher"),
    ("Naval Ravikant", "", "AngelList co-founder / investor"),
    ("Marc Andreessen", "", "Co-founder of a16z"),
    ("Ben Horowitz", "", "Co-founder of a16z"),
    ("Elad Gil", "", "AI investor / entrepreneur"),
    ("Satoshi Nakamoto", "", "Creator of Bitcoin (pseudonym)"),
    ("Vitalik Buterin", "", "Co-founder of Ethereum"),
    ("Sam Bankman-Fried", "", "Former CEO of FTX (convicted)"),
    ("Rodney Brooks", "", "Co-founder of iRobot / Rethink Robotics"),
    ("Max Tegmark", "", "MIT professor / Future of Life Institute"),
    ("Eliezer Yudkowsky", "", "Founder of MIRI / LessWrong"),
    ("Bill Gates", "", "Co-founder of Microsoft"),
    ("Steve Jobs", "", "Co-founder of Apple (deceased)"),
    ("Jeff Bezos", "", "Founder of Amazon"),
    ("Larry Page", "", "Co-founder of Google"),
    ("Sergey Brin", "", "Co-founder of Google"),
    ("Reed Hastings", "", "Co-founder of Netflix"),
    ("Jack Dorsey", "", "Co-founder of Twitter / Block"),
    ("Evan Spiegel", "", "CEO of Snap"),
    ("Kevin Systrom", "", "Co-founder of Instagram"),
    ("Mike Krieger", "", "Co-founder of Instagram"),
    ("Brian Chesky", "", "CEO of Airbnb"),
    ("Travis Kalanick", "", "Former CEO of Uber"),
    ("Garrett Camp", "", "Co-founder of Uber / StumbleUpon"),
]

for name, company, role in people:
    add_person(name, company, role)

updated_people = load_all()[1]
print(f"\nTotal people tracked: {len(updated_people)}")
print("\n=== DONE ===")
