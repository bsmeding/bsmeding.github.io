---
authors: [bsmeding]
toc: true
date: 2023-02-07
layout: single
comments: true
title: Ansible - Network Settings
tags: ["ansible", "network-cli"]
---

# Ansible - Network Settings

A quick guide to Ansible network settings and how to use them for network automation tasks.

---

## Overview

Ansible provides modules and connection plugins for automating network devices. You can use the `network_cli` connection for most network platforms (Cisco, Arista, Juniper, etc.).

---

## Example: Using network_cli

```yaml
- name: Run show version on Cisco IOS
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Show version
      ios_command:
        commands:
          - show version
      register: version_output

    - name: Display output
      debug:
        var: version_output.stdout_lines
```

---

## Tips
- Use `ansible_network_os` in your inventory to specify the platform (e.g., `ios`, `eos`, `junos`).
- Use `ansible_user` and `ansible_password` for authentication.
- For more, see the [Ansible Network Guide](https://docs.ansible.com/ansible/latest/network/index.html).
