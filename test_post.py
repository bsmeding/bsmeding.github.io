#!/usr/bin/env python3
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path

def extract_front_matter(file_path):
    """Extract YAML front matter from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML front matter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None

# Test the specific post
post_file = Path("docs/blog/posts/2025/2025-08-10-building-reusable-network-automation-lab-with-containerlab.md")
front_matter = extract_front_matter(post_file)

print(f"File: {post_file}")
print(f"Front matter: {front_matter}")

if front_matter:
    date = front_matter.get('date')
    draft = front_matter.get('draft', False)
    title = front_matter.get('title', 'Untitled')
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Draft: {draft}")
    
    # Parse the date
    if isinstance(date, str):
        post_date = datetime.fromisoformat(date.replace('Z', '+00:00')).date()
    else:
        post_date = date
    
    today = datetime.now(timezone.utc).date()
    print(f"Post date: {post_date}")
    print(f"Today: {today}")
    print(f"Post date <= today: {post_date <= today}")
    print(f"Not draft: {not draft}")
    print(f"Ready to post: {post_date <= today and not draft}")
else:
    print("No front matter found")
