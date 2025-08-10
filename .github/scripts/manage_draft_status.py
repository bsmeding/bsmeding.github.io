#!/usr/bin/env python3
"""
Automatically manage draft status for blog posts based on publication dates.
This script removes draft: true from posts when their publication date arrives.
"""

import os
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path

# Configuration
BLOG_POSTS_DIR = "docs/blog/posts"

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

def update_draft_status(file_path, front_matter):
    """Update the draft status in a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if draft: true exists
    if 'draft: true' in content:
        # Remove draft: true
        content = re.sub(r'\n\s*draft:\s*true\s*\n', '\n', content)
        content = re.sub(r'\n\s*draft:\s*true\s*$', '', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Main function to manage draft status."""
    print("🔍 Checking for posts ready to publish...")
    
    # Get today's date
    today = datetime.now(timezone.utc).date()
    print(f"📅 Today's date: {today}")
    
    # Find all markdown files in the blog posts directory
    blog_dir = Path(BLOG_POSTS_DIR)
    if not blog_dir.exists():
        print(f"❌ Blog directory not found: {blog_dir}")
        return
    
    published_count = 0
    
    for md_file in blog_dir.rglob("*.md"):
        # Extract front matter
        front_matter = extract_front_matter(md_file)
        if not front_matter:
            continue
        
        # Check if it's a blog post with a date and draft status
        if 'date' not in front_matter or not front_matter.get('draft', False):
            continue
        
        # Parse the date
        try:
            if isinstance(front_matter['date'], str):
                post_date = datetime.fromisoformat(front_matter['date'].replace('Z', '+00:00')).date()
            else:
                post_date = front_matter['date']
        except (ValueError, AttributeError):
            continue
        
        title = front_matter.get('title', 'Untitled')
        print(f"📄 Found draft post: {title} (date: {post_date})")
        
        # Check if it's time to publish
        if post_date <= today:
            print(f"  ✅ Publishing today!")
            if update_draft_status(md_file, front_matter):
                published_count += 1
                print(f"  ✅ Removed draft status")
            else:
                print(f"  ⚠️ Could not update draft status")
        else:
            print(f"  ⏳ Will be published on {post_date}")
    
    print(f"📊 Summary: Published {published_count} posts today")

if __name__ == "__main__":
    main()
