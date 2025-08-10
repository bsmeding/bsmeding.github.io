# Preview System for Draft Blog Posts

This document explains how to use the preview system for testing draft blog posts before publishing them to the main site.

## Overview

The preview system allows you to:
- Create draft blog posts with `draft: true` in the front matter
- Test them on a separate preview site
- Get feedback before publishing
- Automatically build and deploy previews via GitHub Actions

## Quick Start

### 1. Create a Draft Post

Create a new blog post with `draft: true` in the front matter:

```yaml
---
authors: [bsmeding]
date: 2025-08-16
title: My New Post (Draft)
tags: ["network automation", "nautobot"]
toc: true
layout: single
comments: true
draft: true  # This marks it as a draft
---
```

### 2. Set Up Preview Branch

```bash
# Navigate to the repository root
cd bsmeding.github.io

# Create and switch to preview branch
./scripts/preview-branch.sh create
```

### 3. Add Your Draft Posts

Add your draft posts to the `docs/blog/posts/` directory and commit them:

```bash
git add .
git commit -m "Add draft posts"
git push origin preview
```

### 4. View Preview

The preview will be automatically built and deployed to:
- **Preview Branch**: https://bsmeding.github.io/bsmeding.github.io/preview/
- **Pull Requests**: https://bsmeding.github.io/bsmeding.github.io/pr-{PR_NUMBER}/

## Workflow Commands

### Create Preview Branch
```bash
./scripts/preview-branch.sh create
```
Creates a new `preview` branch from `main` and pushes it to remote.

### Update Preview
```bash
./scripts/preview-branch.sh update
```
Updates the preview branch with latest changes from main and commits any local changes.

### Publish Drafts
```bash
./scripts/preview-branch.sh publish
```
Removes the `draft: true` flag from all draft posts and merges them to main.

### Check Status
```bash
./scripts/preview-branch.sh status
```
Shows current branch status, uncommitted changes, and draft files.

### Clean Up
```bash
./scripts/preview-branch.sh cleanup
```
Deletes the preview branch after publishing.

## GitHub Actions Workflow

The preview system uses GitHub Actions to automatically build and deploy previews:

### Triggers
- **Push to `preview` branch**: Builds and deploys to `/preview/`
- **Pull Request to `main` or `preview`**: Builds and deploys to `/pr-{PR_NUMBER}/`

### Workflow Steps
1. **Checkout**: Gets the latest code
2. **Setup Python**: Installs Python 3.11
3. **Cache Dependencies**: Caches pip dependencies for faster builds
4. **Install Dependencies**: Installs requirements from `requirements.txt`
5. **Build Site**: Runs `mkdocs build`
6. **Deploy**: Deploys to GitHub Pages with appropriate directory

## File Structure

```
bsmeding.github.io/
├── .github/
│   └── workflows/
│       └── preview.yml          # GitHub Actions workflow
├── scripts/
│   └── preview-branch.sh        # Preview management script
├── docs/
│   ├── blog/
│   │   └── posts/
│   │       └── 2025/
│   │           ├── *draft*.md   # Draft posts
│   │           └── *.md         # Published posts
│   └── PREVIEW_SYSTEM.md        # This documentation
└── mkdocs.yml                   # Site configuration
```

## Draft Post Guidelines

### Front Matter Requirements
```yaml
---
authors: [bsmeding]
date: YYYY-MM-DD
title: "Post Title (Draft)"  # Include (Draft) in title
tags: ["tag1", "tag2"]
toc: true
layout: single
comments: true
draft: true  # Required for draft posts
---
```

### Content Guidelines
- Use `<!-- more -->` tag to separate excerpt
- Include proper navigation links
- Test all code examples
- Ensure proper formatting and structure

### Publishing Process
1. **Review**: Test the preview thoroughly
2. **Feedback**: Get feedback from team/community
3. **Finalize**: Make any necessary changes
4. **Publish**: Run `./scripts/preview-branch.sh publish`
5. **Cleanup**: Run `./scripts/preview-branch.sh cleanup`

## Troubleshooting

### Preview Not Building
- Check GitHub Actions tab for build errors
- Verify all dependencies are in `requirements.txt`
- Ensure proper YAML syntax in front matter

### Draft Posts Not Showing
- Verify `draft: true` is in front matter
- Check that posts are in correct directory structure
- Ensure proper file naming convention

### Script Errors
- Make sure you're in the repository root
- Verify script has execute permissions: `chmod +x scripts/preview-branch.sh`
- Check that you're on the correct branch

## Best Practices

1. **Always test drafts** before publishing
2. **Use descriptive commit messages** for draft changes
3. **Keep preview branch updated** with main branch changes
4. **Clean up preview branch** after publishing
5. **Test all links and code examples** in preview
6. **Get feedback** from team members before publishing

## Support

If you encounter issues with the preview system:
1. Check the GitHub Actions logs
2. Review this documentation
3. Check the script help: `./scripts/preview-branch.sh help`
4. Create an issue in the repository

---

*Happy drafting! 🚀*
