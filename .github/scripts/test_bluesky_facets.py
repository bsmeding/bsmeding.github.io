#!/usr/bin/env python3
"""
Test script to verify Bluesky link facets functionality.
"""

from atproto_client.utils.text_builder import TextBuilder

def test_link_facets():
    """Test creating a post with link facets."""
    tb = TextBuilder()
    
    # Add some text
    tb.text("New blog post online!: Building a Reusable Network Automation Lab with Containerlab\n\n")
    
    # Add a summary
    tb.text("A comprehensive guide to creating a consistent lab environment for network automation workflows.\n\n")
    
    # Add the URL as a clickable link
    url = "https://netdevops.it/blog/building-a-reusable-network-automation-lab-with-containerlab/"
    tb.link(url, url)
    
    # Get the text and facets
    post_text = tb.build_text()
    post_facets = tb.build_facets()
    
    print("Generated post text:")
    print("=" * 50)
    print(post_text)
    print()
    print("Generated facets:")
    print("=" * 50)
    for facet in post_facets:
        print(f"Index: {facet.index}")
        print(f"Features: {facet.features}")
        print()
    
    print(f"Text length: {len(post_text)} characters")
    print(f"Number of facets: {len(post_facets)}")

if __name__ == "__main__":
    test_link_facets()
