#!/usr/bin/env python3
"""
Check all URLs in posted_to_bluesky.json and compare with current script output.
"""

import json
import re
from pathlib import Path

SITE_URL = "https://netdevops.it"

def get_post_url(file_path, front_matter=None):
    """Generate the URL for a blog post."""
    # If we have front matter with a title, use that to generate the URL
    if front_matter and 'title' in front_matter:
        title = front_matter['title']
        # Convert title to URL-friendly slug
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().replace(' ', '-')
        # Replace colons with dashes (common in titles)
        slug = slug.replace(':', '-')
        # Remove any special characters except hyphens and dashes
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        # Handle dash patterns - but don't convert double dashes to triple dashes
        # The original logic was wrong - we should preserve double dashes
        # Only convert 4+ dashes to triple dashes
        # Remove multiple consecutive hyphens (but preserve intentional dashes)
        # First, convert 4+ dashes to triple dashes
        slug = re.sub(r'-{4,}', '---', slug)
        # Then, convert 3 dashes to triple dashes (ensure consistency)
        slug = re.sub(r'-{3}', '---', slug)
        # Convert any remaining 4+ dashes to single (shouldn't happen after above)
        slug = re.sub(r'-{4,}', '-', slug)
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

def load_posted_log():
    """Load the log of posts that have already been posted to Bluesky."""
    log_file = Path(".github/scripts/posted_to_bluesky.json")
    if log_file.exists():
        with open(log_file, 'r') as f:
            return json.load(f)
    return {}

def main():
    """Check all URLs in the log file."""
    posted_log = load_posted_log()
    
    print("🔍 Checking URLs in posted_to_bluesky.json...")
    print("=" * 80)
    
    incorrect_urls = []
    correct_urls = []
    
    for post_id, post_data in posted_log.items():
        title = post_data.get('title', 'Unknown Title')
        old_url = post_data.get('url', '')
        
        # Create front matter for the current script
        front_matter = {'title': title}
        
        # Generate new URL using current script logic
        new_url = get_post_url(post_id, front_matter)
        
        # Check if URLs match
        if old_url == new_url:
            correct_urls.append((title, old_url))
            print(f"✅ {title}")
            print(f"   URL: {old_url}")
        else:
            incorrect_urls.append((title, old_url, new_url))
            print(f"❌ {title}")
            print(f"   Old URL: {old_url}")
            print(f"   New URL: {new_url}")
        
        print()
    
    print("=" * 80)
    print(f"📊 Summary:")
    print(f"   ✅ Correct URLs: {len(correct_urls)}")
    print(f"   ❌ Incorrect URLs: {len(incorrect_urls)}")
    print(f"   📄 Total posts: {len(posted_log)}")
    
    if incorrect_urls:
        print("\n🔧 URLs that need to be updated:")
        for title, old_url, new_url in incorrect_urls:
            print(f"   - {title}")
            print(f"     From: {old_url}")
            print(f"     To:   {new_url}")
            print()

if __name__ == "__main__":
    main()

