#!/usr/bin/env python3
"""
Test URL generation for the Ansible introduction post.
"""

import re

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
    return "fallback-url"

# Test the specific title
test_title = "Ansible Introduction & Getting Started"
front_matter = {"title": test_title}

url = get_post_url("dummy_file.md", front_matter)

print(f"Title: {test_title}")
print(f"Generated URL: {url}")
print(f"Expected URL: https://netdevops.it/blog/ansible-introduction--getting-started/")
print(f"URLs match: {url == 'https://netdevops.it/blog/ansible-introduction--getting-started/'}")

# Test the transformation steps
print("\nTransformation steps:")
slug = test_title.lower().replace(' ', '-')
print(f"1. Lowercase + spaces to hyphens: {slug}")

slug = slug.replace(':', '-')
print(f"2. Replace colons with dashes: {slug}")

slug = re.sub(r'[^a-z0-9\-]', '', slug)
print(f"3. Remove special chars (including &): {slug}")

# Handle dash patterns - but don't convert double dashes to triple dashes
print(f"4. Keep double dashes as they are: {slug}")

# Remove multiple consecutive hyphens (but preserve intentional dashes)
# First, convert 4+ dashes to triple dashes
slug = re.sub(r'-{4,}', '---', slug)
print(f"5. Convert 4+ dashes to triple: {slug}")

# Then, convert 3 dashes to triple dashes (ensure consistency)
slug = re.sub(r'-{3}', '---', slug)
print(f"6. Convert 3 dashes to triple: {slug}")

# Convert any remaining 4+ dashes to single (shouldn't happen after above)
slug = re.sub(r'-{4,}', '-', slug)
print(f"7. Convert any remaining 4+ dashes: {slug}")

slug = slug.strip('-')
print(f"8. Strip leading/trailing: {slug}")

final_url = f"{SITE_URL}/blog/{slug}/"
print(f"9. Final URL: {final_url}")
