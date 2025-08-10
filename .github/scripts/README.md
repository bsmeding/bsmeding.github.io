# Auto-post to Bluesky

This script automatically posts to Bluesky when blog posts are published on their scheduled date.

## How it works

1. **Scheduled Check**: The GitHub Action runs every hour to check for new blog posts
2. **Date Detection**: It looks for blog posts with today's date in their front matter
3. **Auto-posting**: If a post is published today and hasn't been posted to Bluesky yet, it automatically posts it
4. **Duplicate Prevention**: It keeps a log of posted content to avoid duplicate posts

## Setup Instructions

### 1. Get Bluesky Credentials

You'll need your Bluesky identifier and password:

1. Go to [Bluesky](https://bsky.app)
2. Get your identifier (usually your handle like `@username.bsky.social`)
3. Use your password (or app password if you have 2FA enabled)

### 2. Add GitHub Secrets

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `BLUESKY_IDENTIFIER`: Your Bluesky identifier (e.g., `@username.bsky.social`)
   - `BLUESKY_PASSWORD`: Your Bluesky password

### 3. Test the Setup

1. The workflow will run automatically every hour
2. You can also trigger it manually:
   - Go to **Actions** tab in your repository
   - Select "Auto-post to Bluesky" workflow
   - Click "Run workflow"

## Blog Post Requirements

For a post to be automatically posted to Bluesky, it must have:

1. **Valid front matter** with a `date` field
2. **Date matching today** (when the script runs)
3. **Not already posted** (checked against the log)

Example front matter:
```yaml
---
authors: [bsmeding]
date: 2025-08-16
title: My Blog Post Title
summary: A brief summary of the post
tags: ["network automation", "ansible"]
---
```

## Post Format

The script formats posts for Bluesky with:
- 📝 Post title
- Summary (if available)
- 🔗 Link to the full post
- Hashtags (if space allows)

## Troubleshooting

### Check the logs
- Go to **Actions** → **Auto-post to Bluesky** → Click on a run
- Check the "Check for newly published posts and post to Bluesky" step

### Common issues
- **Credentials not found**: Make sure you've added the GitHub secrets
- **No posts found**: Check that your blog posts have valid dates in their front matter
- **Already posted**: The script won't post the same content twice

## Manual Override

If you need to post something manually or re-post content:

1. Delete the entry from `.github/scripts/posted_to_bluesky.json`
2. Trigger the workflow manually
3. Or run the script locally with your credentials

## Local Testing

To test the script locally:

```bash
cd bsmeding.github.io
export BLUESKY_IDENTIFIER="your-identifier"
export BLUESKY_PASSWORD="your-password"
python .github/scripts/bluesky_auto_post.py
```
