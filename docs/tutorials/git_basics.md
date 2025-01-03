# Getting Started with Git: The Basics

If you’re diving into network automation or development, learning Git is essential. Git is a version control system that helps you track changes, collaborate with others, and manage code efficiently. Whether you’re working solo or as part of a team, Git keeps your projects organized and your work history intact.

In this guide, we’ll cover the basics of Git to get you started.

---

## What is Git?

Git is a distributed version control system. It allows multiple people to work on the same project simultaneously without overwriting each other’s changes. It also keeps a detailed history of every change, so you can roll back to a previous state if needed.

---

## Why Use Git?

- **Version Tracking**: Never lose your work and easily revert to earlier versions.
- **Collaboration**: Work with others on the same codebase without conflicts.
- **Branching**: Experiment with new features or fixes without affecting the main project.
- **Backup**: Store your code on platforms like GitHub, GitLab, or Bitbucket for safekeeping.

---

## Installing Git

Before using Git, you need to install it. You can download it from the [official Git website](https://git-scm.com/), or use a package manager like:

- **Windows**: `choco install git`
- **macOS**: `brew install git`
- **Linux**: 
  - Ubuntu/Debian: `sudo apt install git`
  - CentOS/RedHat: `sudo yum install git`

---

## Setting Up Git

Once installed, set up your Git identity so your commits are properly attributed:

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

To verify your settings:

```bash
git config --list
```

---

## Basic Git Workflow

Here’s how a typical Git workflow looks:

### 1. Create a Repository

A repository is where Git tracks your project. Navigate to your project folder and initialize Git:

```bash
git init
```

This creates a hidden `.git` folder to store version history.

---

### 2. Add Files to Git

To start tracking files, use the `git add` command:

```bash
git add filename
```

To track all files in the directory:

```bash
git add .
```

---

### 3. Commit Changes

Once files are staged with `git add`, commit them to save your changes:

```bash
git commit -m "Initial commit"
```

Use a clear and descriptive message to explain your changes.

---

### 4. View Status and Logs

Check the status of your repository:

```bash
git status
```

View the commit history:

```bash
git log
```

---

### 5. Create a Branch

Branches let you work on features without affecting the main codebase:

```bash
git branch feature-branch
git checkout feature-branch
```

To create and switch to a branch in one command:

```bash
git checkout -b feature-branch
```

---

### 6. Merge Changes

When your work is complete, merge the branch into the main branch:

```bash
git checkout main
git merge feature-branch
```

Resolve any conflicts, if necessary, and finalize the merge.

---

## Wrapping Up

Git is a powerful tool that can simplify your workflow and improve collaboration. By mastering the basics, you’ll be well on your way to managing your projects effectively. In future posts, we’ll dive deeper into more advanced Git features.

Ready to get started? Try creating your first repository and experiment with these commands!