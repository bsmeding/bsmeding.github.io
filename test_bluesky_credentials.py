#!/usr/bin/env python3
"""
Test Bluesky credentials
"""

import os
from atproto import Client

def test_bluesky_credentials():
    identifier = os.environ.get('BLUESKY_IDENTIFIER')
    password = os.environ.get('BLUESKY_PASSWORD')
    
    if not identifier or not password:
        print("❌ Credentials not found in environment")
        print(f"Identifier: {'SET' if identifier else 'NOT SET'}")
        print(f"Password: {'SET' if password else 'NOT SET'}")
        return False
    
    print(f"🔍 Testing credentials...")
    print(f"Identifier: {identifier}")
    print(f"Password: {'*' * len(password)} (length: {len(password)})")
    
    try:
        client = Client()
        client.login(identifier, password)
        print("✅ Login successful!")
        
        # Test posting
        response = client.send_post(text="🧪 Test post from GitHub Actions")
        print(f"✅ Test post successful: {response.uri}")
        
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

if __name__ == "__main__":
    test_bluesky_credentials()
