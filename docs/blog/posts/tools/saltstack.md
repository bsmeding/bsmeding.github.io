---
title: SaltStack Introduction & Getting Started
authors: [bsmeding]
date: 2024-08-17
summary: A brief guide to SaltStack, its automation capabilities, and how to get started.
tags:
  - saltstack
  - automation
  - configuration management
  - devops
---

# SaltStack: Introduction & Getting Started

<img src="https://docs.saltproject.io/salt/user-guide/en/latest/_images/features-of-salt.png" alt="SaltStack Logo" width="200" style="display: block; margin: 0 auto;">

**SaltStack** (Salt) is an open-source automation and configuration management tool designed for fast, scalable, and secure infrastructure automation.
<!-- more -->

## Why Use SaltStack?
- Automate configuration and deployment
- Manage large-scale infrastructure
- Real-time remote execution
- Event-driven automation

## How SaltStack Works
- Uses a master/minion architecture (or masterless mode)
- States define desired system configuration in YAML
- Modules perform actions (e.g., install packages, manage services)

## Quick Start Example
1. **Install Salt (master and minion):**
   ```bash
   sudo apt install salt-master salt-minion
   # or use pip for latest version
   pip install salt
   ```
2. **Start the master and minion services:**
   ```bash
   sudo systemctl start salt-master
   sudo systemctl start salt-minion
   ```
3. **Accept the minion key on the master:**
   ```bash
   sudo salt-key -A
   ```
4. **Write a simple state file (`apache.sls`):**
   ```yaml
   install_apache:
     pkg.installed:
       - name: apache2
   ```
5. **Apply the state to the minion:**
   ```bash
   sudo salt '<minion-id>' state.apply apache
   ```

## Learn More
- [SaltStack Documentation](https://docs.saltproject.io/)
- [Getting Started Guide](https://docs.saltproject.io/en/latest/topics/tutorials/index.html) 