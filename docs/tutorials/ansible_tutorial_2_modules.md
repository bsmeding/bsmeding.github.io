---
title: Ansible Tutorial 2: Modules & Your First Playbook
tags:
  - ansible
  - tutorial
  - modules
  - getting started
---

# Ansible Tutorial 2: Modules & Your First Playbook

This tutorial covers the basics of using Ansible modules, the difference between built-in and community modules, and how to find and use modules for your network devices.

## What is a Module?
A module is a reusable, single-purpose unit of work in Ansible (e.g., install a package, run a command, configure a device).

## Using Modules
Modules are used in playbooks as tasks.

**Example:**
```yaml
- name: Ping all devices
  hosts: all
  gather_facts: no
  tasks:
    - name: Ping
      ansible.builtin.ping:
```

## Built-in vs. Community Modules
- **Built-in modules:** Included with Ansible (e.g., `ansible.builtin.ping`, `ansible.builtin.copy`, `cisco.ios.ios_command`)
- **Community modules:** Provided by the community, often via Ansible Galaxy collections (e.g., `cisco.ios.ios_config`)

## Module Index & How to Search
- [Ansible Module Index](https://docs.ansible.com/ansible/latest/collections/index_module.html)
- Use `ansible-doc -l` to list available modules
- Use `ansible-doc <module_name>` for documentation

## Vendor Modules
Always try to use vendor-specific modules (e.g., `cisco.ios.ios_command` for Cisco, `arista.eos.eos_command` for Arista) for best results.

## Your First Playbook with a Vendor Module
```yaml
---
- name: Get running config from Cisco router
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Get running config
      cisco.ios.ios_command:
        commands:
          - show running-config
      register: config
    - debug:
        var: config.stdout_lines
```

---

Continue to [Tutorial 3: Variables, Modules, and Network Fact Gathering](ansible_tutorial_3_variables_facts.md) 