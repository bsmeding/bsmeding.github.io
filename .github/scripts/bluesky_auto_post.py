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
from atproto import Client, models
from atproto_client.utils.text_builder import TextBuilder
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

def format_bluesky_post(title, summary, url, tags):
    """Format a blog post for Bluesky with proper link facets."""
    # Bluesky has a 300 character limit
    max_length = 300
    
    # Create the post content
    post_content = f"New blog post online!: {title}\n\n"
    
    if summary:
        # Truncate summary if too long
        max_summary_length = max_length - len(post_content) - len(url) - 20  # Reserve space for tags and URL
        if len(summary) > max_summary_length:
            summary = summary[:max_summary_length-3] + "..."
        post_content += f"{summary}\n\n"
    
    # Add tags if there's space (limit to 3 tags)
    if tags and len(post_content) < max_length - len(url) - 30:
        tag_text = " ".join([f"#{tag.replace('-', '').replace(' ', '')}" for tag in tags[:3]])
        if len(post_content + f"{tag_text}\n\n") <= max_length - len(url) - 5:
            post_content += f"{tag_text}\n\n"
    
    # Add URL on its own line for better clickability
    post_content += f"{url}"
    
    # Truncate if too long
    if len(post_content) > max_length:
        # Try to truncate summary first
        if summary and len(summary) > 20:
            # Calculate how much to truncate
            excess = len(post_content) - max_length
            new_summary = summary[:-excess-3] + "..."
            post_content = f"New blog post online!: {title}\n\n{new_summary}\n\n{url}"
        else:
            # If no summary or can't truncate further, truncate title
            post_content = post_content[:max_length-3] + "..."
    
    return post_content

def create_bluesky_post_with_facets(title, summary, url, tags):
    """Create a Bluesky post with proper link facets for clickable URLs."""
    # Bluesky has a 300 character limit
    max_length = 300
    
    # Reserve space for the URL (always keep it complete)
    url_length = len(url)
    available_length = max_length - url_length - 10  # Reserve 10 chars for formatting
    
    # Build the text content
    tb = TextBuilder()
    
    # Add title (truncate if necessary)
    title_text = f"New blog post online!: {title}\n\n"
    if len(title_text) > available_length:
        # Truncate title to fit
        max_title_length = available_length - 10  # Reserve space for summary
        truncated_title = title[:max_title_length-3] + "..."
        title_text = f"New blog post online!: {truncated_title}\n\n"
    
    tb.text(title_text)
    available_length -= len(title_text)
    
    # Add summary if available and there's space
    if summary and available_length > 20:
        # Truncate summary if too long
        if len(summary) > available_length - 10:  # Reserve space for tags
            summary = summary[:available_length-13] + "..."
        tb.text(f"{summary}\n\n")
        available_length -= len(summary) + 2  # +2 for \n\n
    
    # Add tags if there's space (limit to 3 tags)
    if tags and available_length > 15:
        tag_text = " ".join([f"#{tag.replace('-', '').replace(' ', '')}" for tag in tags[:3]])
        if len(tag_text) <= available_length - 5:
            tb.text(f"{tag_text}\n\n")
            available_length -= len(tag_text) + 2  # +2 for \n\n
    
    # Add the URL as a clickable link (always complete)
    tb.link(url, url)
    
    # Get the text and facets
    post_text = tb.build_text()
    post_facets = tb.build_facets()
    
    # Verify the URL is complete in the final text
    if url not in post_text:
        # If URL was truncated, rebuild with minimal content
        tb = TextBuilder()
        tb.text(f"New blog post online!: {title[:50]}...\n\n")
        tb.link(url, url)
        post_text = tb.build_text()
        post_facets = tb.build_facets()
    
    return post_text, post_facets

def post_to_bluesky(content, facets=None):
    """Post content to Bluesky using the atproto library."""
    identifier = os.environ.get('BLUESKY_IDENTIFIER')
    password = os.environ.get('BLUESKY_PASSWORD')
    
    if not identifier or not password:
        print("❌ Bluesky credentials not found in environment variables")
        print("🔍 Would post this content:")
        print("---")
        print(content)
        if facets:
            print("With facets:", facets)
        print("---")
        return False
    
    try:
        client = Client()
        client.login(identifier, password)
        
        # Post to Bluesky with facets if provided
        if facets:
            response = client.send_post(text=content, facets=facets)
        else:
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
    print(f"📅 Today's date: {today}")
    
    # Find all markdown files in the blog posts directory
    blog_dir = Path(BLOG_POSTS_DIR)
    if not blog_dir.exists():
        print(f"❌ Blog directory not found: {blog_dir}")
        return
    
    new_posts = []
    found_posts = 0
    
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
        
        found_posts += 1
        
        # Parse the date
        try:
            if isinstance(front_matter['date'], str):
                post_date = datetime.fromisoformat(front_matter['date'].replace('Z', '+00:00')).date()
            else:
                post_date = front_matter['date']
        except (ValueError, AttributeError):
            continue
        
        title = front_matter.get('title', 'Untitled')
        print(f"📄 Found post: {title} (date: {post_date}, draft: {front_matter.get('draft', False)})")
        
        # Check if it's published today or in the past and not already posted
        if post_date <= today:
            # Use the file path as post ID to match existing log format
            post_id = str(md_file)
            print(f"  🔍 Checking post ID: {post_id}")
            
            # Check if this post is already in the log
            if post_id not in posted_log:
                # Check if it's not a draft
                if not front_matter.get('draft', False):
                    new_posts.append({
                        'file': md_file,
                        'front_matter': front_matter,
                        'post_id': post_id
                    })
                    print(f"  ✅ Added to posting queue")
                else:
                    print(f"  📝 Draft post (skipping)")
            else:
                print(f"  ⏭️ Already posted on {posted_log[post_id].get('posted_at', 'unknown date')}")
        else:
            print(f"  ⏳ Future post (will be published on {post_date})")
    
    print(f"📊 Summary: Found {found_posts} posts, {len(new_posts)} ready to post")
    
    if not new_posts:
        print("✅ No new posts to publish today")
        return
    
    print(f"📝 Found {len(new_posts)} new posts to publish:")
    
    for post in new_posts:
        title = post['front_matter'].get('title', 'Untitled')
        summary = post['front_matter'].get('summary', '')
        tags = post['front_matter'].get('tags', [])
        url = get_post_url(post['file'], post['front_matter'])
        
        print(f"  - {title}")
        print(f"    URL: {url}")
        
        # Format the post for Bluesky with proper link facets for clickable URLs
        bluesky_content, bluesky_facets = create_bluesky_post_with_facets(title, summary, url, tags)
        
        # Post to Bluesky
        if post_to_bluesky(bluesky_content, bluesky_facets):
            # Mark as posted with current timestamp
            posted_log[post['post_id']] = {
                'posted_at': datetime.now(timezone.utc).isoformat(),
                'title': title,
                'url': url
            }
            # Save the log immediately after each successful post
            save_posted_log(posted_log)
            print(f"  ✅ Posted and logged: {title}")
        else:
            print(f"  ❌ Failed to post: {title}")
    
    print("✅ All posts processed")

if __name__ == "__main__":
    main()
