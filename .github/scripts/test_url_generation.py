#!/usr/bin/env python3
"""
Test script to verify URL generation for blog posts.
"""

import re
from pathlib import Path

SITE_URL = "https://netdevops.it"

def get_post_url(file_path):
    """Generate the URL for a blog post."""
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

# Test cases
test_cases = [
    "docs/blog/posts/2025/2025-08-10-building-reusable-network-automation-lab-with-containerlab.md",
    "docs/blog/posts/2024/2024-12-25-some-other-post.md",
    "docs/blog/posts/2025/2025-01-15-another-example-post.md",
]

print("Testing URL generation:")
print("=" * 50)

for test_path in test_cases:
    url = get_post_url(test_path)
    print(f"Input:  {test_path}")
    print(f"Output: {url}")
    print()

print("Expected results:")
print("- https://netdevops.it/blog/building-reusable-network-automation-lab-with-containerlab/")
print("- https://netdevops.it/blog/some-other-post/")
print("- https://netdevops.it/blog/another-example-post/")
