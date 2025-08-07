---
title: Ansible Introduction & Getting Started
authors: [bsmeding]
date: 2024-08-10
summary: A quick introduction to Ansible, its use cases, and how to get started with automation.
tags:
  - ansible
  - automation
  - configuration management
  - devops
---

# Ansible: Introduction & Getting Started

![Ansible AWX (former Tower/AAP)](https://docs.ansible.com/ansible-tower/3.4.1/html/userguide/_images/jobs-show-job-std-output-hover.png){: style="max-width: 300px; display: block; margin: 0 auto;"}

**Ansible** is an open-source automation tool for configuration management, application deployment, and task automation. It uses simple YAML-based playbooks and requires no agent on managed nodes.
<!-- more -->

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

---

## Step-by-Step Ansible Tutorials
If you want a structured, beginner-friendly path, check out the Ansible tutorial series:
- [Tutorial 1: Concepts & Terminology](../../tutorials/ansible_tutorial_1_concepts.md)
- [Tutorial 2: Modules & Your First Playbook](../../tutorials/ansible_tutorial_2_modules.md)
- [Tutorial 3: Variables, Modules & Network Fact Gathering](../../tutorials/ansible_tutorial_3_variables_facts.md) 