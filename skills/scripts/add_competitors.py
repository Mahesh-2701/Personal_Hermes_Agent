#!/usr/bin/env python3
"""
Add multiple competitors to the registry at once.
"""

import sys
sys.path.insert(0, '/Users/apple/.hermes/skills/competitor-intelligence/scripts')
from entity_resolve import EntityResolver

resolver = EntityResolver()

competitors_to_add = [
    # Top AI Companies - High Priority
    {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "github": "anthropic-ai",
        "priority": "high",
        "products": ["Claude", "Claude API", "Claude Desktop"],
    },
    {
        "name": "Google DeepMind",
        "website": "https://deepmind.google",
        "github": "google-deepmind",
        "priority": "high",
        "products": ["Gemini", "Gemini API", "AlphaFold"],
    },
    {
        "name": "Meta AI",
        "website": "https://ai.meta.com",
        "github": "facebookresearch",
        "priority": "high",
        "products": ["LLaMA", "LLaMA 2", "LLaMA 3", "Segment Anything"],
    },
    {
        "name": "Mistral AI",
        "website": "https://mistral.ai",
        "github": "mistralai",
        "priority": "high",
        "products": ["Mistral", "Mistral Large", "Mistral Small"],
    },
    {
        "name": " DeepSeek",
        "website": "https://deepseek.com",
        "github": "deepseek-ai",
        "priority": "high",
        "products": ["DeepSeek-V2", "DeepSeek-Coder", "DeepSeek-R1"],
    },
    {
        "name": "xAI",
        "website": "https://x.ai",
        "github": "xai-org",
        "priority": "high",
        "products": ["Grok", "Grok-2", "Grok-3"],
    },
    {
        "name": "Cohere",
        "website": "https://cohere.com",
        "github": "cohere-ai",
        "priority": "medium",
        "products": ["Command", "Embed", "Rerank"],
    },
    {
        "name": "Hugging Face",
        "website": "https://huggingface.co",
        "github": "huggingface",
        "priority": "medium",
        "products": ["Transformers", "Diffusers", "Inference API"],
    },
    {
        "name": "Stability AI",
        "website": "https://stability.ai",
        "github": "Stability-AI",
        "priority": "medium",
        "products": ["Stable Diffusion", "Stable Video", "Stable Audio"],
    },
    {
        "name": "EleutherAI",
        "website": "https://eleuther.ai",
        "github": "EleutherAI",
        "priority": "low",
        "products": ["GPT-Neo", "GPT-J", "Pythia"],
    },
]

for comp in competitors_to_add:
    resolver.add_competitor(
        name=comp["name"],
        website=comp["website"],
        github=comp["github"],
        priority=comp["priority"],
        products=comp.get("products", []),
    )
    print()

print(f"\nTotal competitors now tracked: {len(resolver.competitors)}")
