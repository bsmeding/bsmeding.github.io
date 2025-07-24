---
title: Ansible Introduction & Getting Started
authors: [bsmeding]
date: 2024-08-10
tags:
  - ansible
  - automation
  - configuration management
  - devops
---

# Ansible: Introduction & Getting Started

**Ansible** is an open-source automation tool for configuration management, application deployment, and task automation. It uses simple YAML-based playbooks and requires no agent on managed nodes.

## Why Use Ansible?
- Automate repetitive IT tasks
- Manage infrastructure as code (IaC)
- Orchestrate multi-tier deployments
- Ensure consistency across environments

## How Ansible Works
- Uses SSH (or WinRM for Windows) to connect to hosts
- Playbooks define tasks in YAML
- Modules perform actions (e.g., install packages, copy files)

## Quick Start Example
1. **Install Ansible** (on most Linux/macOS):
   ```bash
   pip install ansible
   # or
   sudo apt install ansible
   ```
2. **Create an inventory file (`hosts`):**
   ```ini
   [web]
   server1.example.com
   server2.example.com
   ```
3. **Write a simple playbook (`site.yml`):**
   ```yaml
   ---
   - name: Ensure Apache is installed
     hosts: web
     become: yes
     tasks:
       - name: Install Apache
         apt:
           name: apache2
           state: present
   ```
4. **Run the playbook:**
   ```bash
   ansible-playbook -i hosts site.yml
   ```

## Learn More
- [Ansible Documentation](https://docs.ansible.com/)
- [Getting Started Guide](https://docs.ansible.com/ansible/latest/getting_started/index.html) 