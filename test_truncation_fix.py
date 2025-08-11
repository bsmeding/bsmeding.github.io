#!/usr/bin/env python3
"""
Test that URLs are not truncated in Bluesky post generation.
"""

from atproto_client.utils.text_builder import TextBuilder

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

# Test cases
test_cases = [
    {
        "title": "Building a Reusable Network Automation Lab with Containerlab",
        "summary": "A comprehensive guide to creating a consistent lab environment for network automation workflows using Containerlab, Docker, and various network OS images.",
        "url": "https://netdevops.it/blog/building-a-reusable-network-automation-lab-with-containerlab/",
        "tags": ["network automation", "containerlab", "lab"]
    },
    {
        "title": "A Very Long Title That Might Cause Truncation Issues When Combined With Other Content",
        "summary": "This is a very long summary that might cause the post to exceed the character limit and potentially truncate the URL, which would break the clickable functionality.",
        "url": "https://netdevops.it/blog/a-very-long-title-that-might-cause-truncation-issues/",
        "tags": ["long title", "truncation", "testing"]
    }
]

print("Testing URL truncation prevention:")
print("=" * 60)

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest Case {i}:")
    print(f"Title: {test_case['title']}")
    print(f"Summary: {test_case['summary'][:50]}...")
    print(f"URL: {test_case['url']}")
    
    post_text, post_facets = create_bluesky_post_with_facets(
        test_case['title'], 
        test_case['summary'], 
        test_case['url'], 
        test_case['tags']
    )
    
    print(f"\nGenerated post ({len(post_text)} characters):")
    print("-" * 40)
    print(post_text)
    print("-" * 40)
    
    # Check if URL is complete
    url_complete = test_case['url'] in post_text
    print(f"URL complete: {url_complete}")
    
    # Check if URL is clickable (has facets)
    url_clickable = len(post_facets) > 0
    print(f"URL clickable: {url_clickable}")
    
    # Check character limit
    within_limit = len(post_text) <= 300
    print(f"Within 300 char limit: {within_limit}")
    
    print()
