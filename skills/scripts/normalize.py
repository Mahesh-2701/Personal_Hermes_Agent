#!/usr/bin/env python3
"""
Competitor Intelligence — Content Normalizer
Strips noise (timestamps, tracking params, nav noise) from collected content.
"""

import re
import hashlib
from typing import Dict, Any, Optional

class ContentNormalizer:
    """Normalizes collected content for comparison and storage."""
    
    # Patterns to strip as noise
    NOISE_PATTERNS = [
        (r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL, 'script'),
        (r'<style[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL, 'style'),
        (r'<!--.*?-->', re.DOTALL, 'comment'),
        (r'<nav[^>]*>.*?</nav>', re.IGNORECASE | re.DOTALL, 'nav'),
        (r'<footer[^>]*>.*?</footer>', re.IGNORECASE | re.DOTALL, 'footer'),
        (r'<header[^>]*>.*?</header>', re.IGNORECASE | re.DOTALL, 'header'),
        (r'cookie[\s_-]?banner', re.IGNORECASE, 'cookie_banner'),
        (r'accept[\s_-]?cookies', re.IGNORECASE, 'cookie_btn'),
        (r'google-analytics', re.IGNORECASE, 'analytics'),
        (r'gtag\.js', re.IGNORECASE, 'analytics'),
        (r'facebook\.pixel', re.IGNORECASE, 'pixel'),
        (r'_ga=[^"&]*', 'cookie_param'),
        (r'_gid=[^"&]*', 'cookie_param'),
        (r'utm_[^&"\s]*', 'tracking_param'),
        (r'fbclid=[^&"\s]*', 'tracking_param'),
        (r'gclid=[^&"\s]*', 'tracking_param'),
        (r'tracking', re.IGNORECASE, 'tracking'),
        (r'adsbygoogle', re.IGNORECASE, 'ads'),
        (r'doubleclick', re.IGNORECASE, 'ads'),
        (r'cloudflare[\s_-]?challenge', re.IGNORECASE, 'cf_challenge'),
        (r'captcha', re.IGNORECASE, 'captcha'),
        (r'timestamp[\s:]*\d{10,}','timestamp'),
        (r'updated[\s:]*\d{4}-\d{2}-\d{2}','date'),
    ]
    
    def normalize(self, content: str) -> str:
        """Remove noise from content for clean comparison."""
        if not content:
            return ""
        
        normalized = content
        
        # Strip HTML noise
        for pattern, flags, _ in self.NOISE_PATTERNS:
            if isinstance(flags, int):
                normalized = re.sub(pattern, '', normalized, flags=flags)
            else:
                normalized = re.sub(pattern, '', normalized)
        
        # Strip remaining HTML tags (keep text content)
        normalized = re.sub(r'<[^>]+>', ' ', normalized)
        
        # Decode HTML entities
        normalized = normalized.replace('&nbsp;', ' ')
        normalized = normalized.replace('&amp;', '&')
        normalized = normalized.replace('&lt;', '<')
        normalized = normalized.replace('&gt;', '>')
        normalized = normalized.replace('&quot;', '"')
        
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = re.sub(r'\n\s*\n', '\n\n', normalized)
        
        # Strip leading/trailing whitespace
        normalized = normalized.strip()
        
        return normalized
    
    def normalize_url(self, url: str) -> str:
        """Remove tracking parameters from URLs."""
        if not url:
            return ""
        
        # Remove query parameters that are tracking-related
        url = re.sub(r'[?&](utm_[^&]*)', '', url)
        url = re.sub(r'[?&](fbclid=[^&]*)', '', url)
        url = re.sub(r'[?&](gclid=[^&]*)', '', url)
        url = re.sub(r'[?&](ref=[^&]*)', '', url)
        url = re.sub(r'[?&](source=[^&]*)', '', url)
        
        # Sort remaining params for consistent comparison
        if '?' in url:
            base, params = url.split('?', 1)
            param_dict = {}
            for param in params.split('&'):
                if '=' in param:
                    key, val = param.split('=', 1)
                    param_dict[key] = val
                else:
                    param_dict[param] = ''
            
            # Remove empty or noise params
            cleaned = {}
            for k, v in param_dict.items():
                if k.lower() not in ('utm_source', 'utm_medium', 'utm_campaign', 
                                       'utm_term', 'utm_content', 'ref', 'source', ''):
                    cleaned[k] = v
            
            if cleaned:
                sorted_params = '&'.join(f"{k}={v}" for k, v in sorted(cleaned.items()))
                url = f"{base}?{sorted_params}"
            else:
                url = base
        
        return url
    
    def compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of normalized content."""
        normalized = self.normalize(content)
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def extract_text_content(self, html: str) -> str:
        """Extract meaningful text content from HTML."""
        # Remove scripts, styles, nav, footer, header
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<header[^>]*>.*?</header>', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Decode entities
        for entity, char in [('&nbsp;', ' '), ('&amp;', '&'), ('&lt;', '<'), 
                              ('&gt;', '>'), ('&quot;', '"'), ('&#39;', "'")]:
            text = text.replace(entity, char)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_key_content(self, html: str, focus_areas=None) -> Dict[str, str]:
        """Extract key content sections from HTML."""
        if focus_areas is None:
            focus_areas = ['main', 'article', 'content', 'body']
        
        result = {}
        
        # Try to extract main content area
        for area in focus_areas:
            pattern = f'<{area}[^>]*>(.*?)</{area}>'
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            if matches:
                result[area] = self.extract_text_content(matches[0])
                break
        
        # If no specific area found, use full body
        if not result:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
            if body_match:
                result['body'] = self.extract_text_content(body_match.group(1))
        
        return result


def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Content Normalizer")
    parser.add_argument("input", nargs="?", help="Input text to normalize")
    parser.add_argument("--hash", action="store_true", help="Compute hash of normalized content")
    args = parser.parse_args()
    
    normalizer = ContentNormalizer()
    
    if args.input:
        normalized = normalizer.normalize(args.input)
        print(normalized[:5000])
        
        if args.hash:
            print(f"\n--- HASH ---")
            print(normalizer.compute_hash(args.input))
    else:
        print("Usage:")
        print("  normalize.py <text>           — Normalize text")
        print("  normalize.py <text> --hash   — Normalize and compute hash")


if __name__ == "__main__":
    main()
