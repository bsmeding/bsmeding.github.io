#!/usr/bin/env python3
"""
Auto-post to Bluesky when blog posts are published.
This script checks for blog posts that were published today and posts them to Bluesky.
"""

import os
import re
import yaml
import requests
from datetime import datetime, timezone
from pathlib import Path
from atproto import Client
import json

# Configuration
BLOG_POSTS_DIR = "docs/blog/posts"
POSTED_LOG_FILE = ".github/scripts/posted_to_bluesky.json"
SITE_URL = "https://netdevops.it"

def load_posted_log():
    """Load the log of posts that have already been posted to Bluesky."""
    log_file = Path(POSTED_LOG_FILE)
    if log_file.exists():
        with open(log_file, 'r') as f:
            return json.load(f)
    return {}

def save_posted_log(log):
    """Save the log of posted posts."""
    log_file = Path(POSTED_LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)

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

def get_post_url(file_path):
    """Generate the URL for a blog post."""
    # Remove docs/ prefix and .md suffix
    relative_path = str(file_path).replace('docs/', '').replace('.md', '')
    return f"{SITE_URL}/{relative_path}"

def format_bluesky_post(title, summary, url, tags):
    """Format a blog post for Bluesky."""
    # Bluesky has a 300 character limit
    max_length = 300
    
    # Create the post content
    post_content = f"📝 {title}\n\n"
    
    if summary:
        post_content += f"{summary}\n\n"
    
    post_content += f"🔗 {url}"
    
    # Add tags if there's space
    if tags and len(post_content) < max_length - 20:
        tag_text = " ".join([f"#{tag.replace('-', '')}" for tag in tags[:3]])
        if len(post_content + f"\n\n{tag_text}") <= max_length:
            post_content += f"\n\n{tag_text}"
    
    # Truncate if too long
    if len(post_content) > max_length:
        post_content = post_content[:max_length-3] + "..."
    
    return post_content

def post_to_bluesky(content):
    """Post content to Bluesky using the atproto library."""
    identifier = os.environ.get('BLUESKY_IDENTIFIER')
    password = os.environ.get('BLUESKY_PASSWORD')
    
    if not identifier or not password:
        print("❌ Bluesky credentials not found in environment variables")
        return False
    
    try:
        client = Client()
        client.login(identifier, password)
        
        # Post to Bluesky
        response = client.send_post(text=content)
        print(f"✅ Posted to Bluesky: {response.uri}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to post to Bluesky: {e}")
        return False

def main():
    """Main function to check for new posts and post them to Bluesky."""
    print("🔍 Checking for newly published blog posts...")
    
    # Load the log of already posted content
    posted_log = load_posted_log()
    
    # Get today's date
    today = datetime.now(timezone.utc).date()
    
    # Find all markdown files in the blog posts directory
    blog_dir = Path(BLOG_POSTS_DIR)
    if not blog_dir.exists():
        print(f"❌ Blog directory not found: {blog_dir}")
        return
    
    new_posts = []
    
    for md_file in blog_dir.rglob("*.md"):
        # Skip the log file itself
        if "posted_to_bluesky" in str(md_file):
            continue
            
        # Extract front matter
        front_matter = extract_front_matter(md_file)
        if not front_matter:
            continue
        
        # Check if it's a blog post with a date
        if 'date' not in front_matter:
            continue
        
        # Parse the date
        try:
            if isinstance(front_matter['date'], str):
                post_date = datetime.fromisoformat(front_matter['date'].replace('Z', '+00:00')).date()
            else:
                post_date = front_matter['date'].date()
        except (ValueError, AttributeError):
            continue
        
        # Check if it's published today and not already posted
        if post_date == today:
            post_id = str(md_file)
            if post_id not in posted_log:
                new_posts.append({
                    'file': md_file,
                    'front_matter': front_matter,
                    'post_id': post_id
                })
    
    if not new_posts:
        print("✅ No new posts to publish today")
        return
    
    print(f"📝 Found {len(new_posts)} new posts to publish:")
    
    for post in new_posts:
        title = post['front_matter'].get('title', 'Untitled')
        summary = post['front_matter'].get('summary', '')
        tags = post['front_matter'].get('tags', [])
        url = get_post_url(post['file'])
        
        print(f"  - {title}")
        
        # Format the post for Bluesky
        bluesky_content = format_bluesky_post(title, summary, url, tags)
        
        # Post to Bluesky
        if post_to_bluesky(bluesky_content):
            # Mark as posted
            posted_log[post['post_id']] = {
                'posted_at': datetime.now(timezone.utc).isoformat(),
                'title': title,
                'url': url
            }
        else:
            print(f"  ❌ Failed to post: {title}")
    
    # Save the updated log
    save_posted_log(posted_log)
    print("✅ Posted log updated")

if __name__ == "__main__":
    main()
