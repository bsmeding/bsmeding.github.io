#!/usr/bin/env python3
"""
Test URL generation with front matter title.
"""

import re
import yaml
from pathlib import Path

SITE_URL = "https://netdevops.it"

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

def get_post_url(file_path, front_matter=None):
    """Generate the URL for a blog post."""
    # If we have front matter with a title, use that to generate the URL
    if front_matter and 'title' in front_matter:
        title = front_matter['title']
        # Convert title to URL-friendly slug
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().replace(' ', '-')
        # Remove any special characters except hyphens
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        url = f"{SITE_URL}/blog/{slug}/"
        return url
    
    # Fallback: use filename-based approach
    # Convert file path to URL path
    # Remove docs/ prefix and .md suffix
    relative_path = str(file_path).replace('docs/', '').replace('.md', '')
    
    # Extract the blog post slug from the path
    # Expected format: blog/posts/YYYY/YYYY-MM-DD-title.md
    # We want: /blog/title/
    path_parts = relative_path.split('/')
    
    if len(path_parts) >= 4 and path_parts[0] == 'blog' and path_parts[1] == 'posts':
        # Extract the date and title from the filename
        filename = path_parts[-1]  # YYYY-MM-DD-title.md
        if filename.endswith('.md'):
            filename = filename[:-3]  # Remove .md
        
        # Extract title from YYYY-MM-DD-title format
        if '-' in filename:
            # Split by '-' and skip the first 3 parts (YYYY-MM-DD)
            title_parts = filename.split('-')[3:]
            if title_parts:
                title_slug = '-'.join(title_parts)
                url = f"{SITE_URL}/blog/{title_slug}/"
                return url
    
    # Fallback: use the original path but clean it up
    if not relative_path.startswith('/'):
        relative_path = '/' + relative_path
    url = f"{SITE_URL}{relative_path}"
    url = re.sub(r'(?<!:)//+', '/', url)
    if not url.startswith('https://'):
        url = url.replace('https:/', 'https://', 1)
    return url

# Test the specific file
test_file = "docs/blog/posts/2025/2025-08-10-building-reusable-network-automation-lab-with-containerlab.md"
front_matter = extract_front_matter(test_file)

print(f"Input file: {test_file}")
print(f"Front matter title: {front_matter.get('title', 'No title found')}")
print()

# Test with front matter
url_with_front_matter = get_post_url(test_file, front_matter)
print(f"URL with front matter: {url_with_front_matter}")

# Test without front matter (fallback)
url_without_front_matter = get_post_url(test_file)
print(f"URL without front matter: {url_without_front_matter}")

print()
print(f"Expected URL: https://netdevops.it/blog/building-a-reusable-network-automation-lab-with-containerlab/")
print(f"URLs match (with front matter): {url_with_front_matter == 'https://netdevops.it/blog/building-a-reusable-network-automation-lab-with-containerlab/'}")
print(f"URLs match (without front matter): {url_without_front_matter == 'https://netdevops.it/blog/building-a-reusable-network-automation-lab-with-containerlab/'}")

