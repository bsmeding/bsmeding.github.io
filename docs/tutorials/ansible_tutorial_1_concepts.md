---
title: Ansible Tutorial 1: Concepts & Terminology
tags:
  - ansible
  - tutorial
  - concepts
  - getting started
---

# Ansible Tutorial 1: Understand Ansible Concepts & Terminology

This tutorial introduces the core concepts and terminology of Ansible. It is the first step for anyone new to network automation or configuration management.

## Ansible Overview
Ansible is an open-source automation tool for configuration management, application deployment, and task automation. It uses simple YAML files (playbooks) and does not require agents on managed nodes.

## Introduction to YAML
YAML (YAML Ain't Markup Language) is a human-readable data format used for Ansible playbooks and inventories.

**Example YAML:**
```yaml
key: value
list:
  - item1
  - item2
```

---

## Inventory
The inventory defines the hosts and groups Ansible manages. It is the foundation of all automation in Ansible.

### Inventory File Formats
- **INI format:** Simple, easy to start with, good for small environments.
- **YAML format:** More powerful, supports nested groups and variables, recommended for larger or more complex environments.

**Example inventory (INI):**
```ini
[routers]
r1 ansible_host=192.0.2.1 ansible_user=admin ansible_password=yourpass ansible_network_os=ios
r2 ansible_host=192.0.2.2 ansible_user=admin ansible_password=yourpass ansible_network_os=ios

[switches]
s1 ansible_host=192.0.2.10 ansible_user=admin ansible_password=yourpass ansible_network_os=eos
```

**Example inventory (YAML):**
```yaml
all:
  children:
    routers:
      hosts:
        r1:
          ansible_host: 192.0.2.1
          ansible_user: admin
          ansible_password: yourpass
          ansible_network_os: ios
        r2:
          ansible_host: 192.0.2.2
          ansible_user: admin
          ansible_password: yourpass
          ansible_network_os: ios
    switches:
      hosts:
        s1:
          ansible_host: 192.0.2.10
          ansible_user: admin
          ansible_password: yourpass
          ansible_network_os: eos
```

### Host and Group Variables in Inventory
- You can define variables for all hosts, groups, or individual hosts directly in the inventory file or in separate `group_vars/` and `host_vars/` directories.
- Common variables include:
  - `ansible_host`: The IP or DNS name to connect to
  - `ansible_user`: The SSH username
  - `ansible_password`: The SSH password
  - `ansible_network_os`: The network platform (e.g., ios, eos, junos)
  - `ansible_become`: Whether to use privilege escalation (e.g., enable mode)

**Best Practice:**
- Use `group_vars/` and `host_vars/` for sensitive data and to keep your inventory clean and maintainable.

**Example directory structure:**
```
project/
  inventory.yml
  group_vars/
    routers.yml
    switches.yml
  host_vars/
    r1.yml
    s1.yml
  playbook.yml
```

**Example `group_vars/routers.yml`:**
```yaml
ansible_user: admin
ansible_password: yourpass
ansible_network_os: ios
```

**Example `host_vars/r1.yml`:**
```yaml
ansible_host: 192.0.2.1
```

### Inventory Best Practices
- Use descriptive group names (e.g., routers, switches, firewalls)
- Store credentials and sensitive data in `group_vars/` or use Ansible Vault for encryption
- Use YAML inventory for complex environments
- Document your inventory structure for your team

---

## Ansible Playbook Structure
A playbook is a YAML file describing automation tasks.

**Example playbook:**
```yaml
---
- name: Example Playbook
  hosts: routers
  gather_facts: no
  tasks:
    - name: Ping device
      ansible.builtin.ping:
```

---

## Host and Group Variables
Variables can be set for groups or individual hosts using `group_vars/` and `host_vars/` directories.

**Example `group_vars/routers.yml`:**
```yaml
ansible_user: admin
ansible_password: yourpass
ansible_network_os: ios
```

**Example `host_vars/r1.yml`:**
```yaml
ansible_host: 192.0.2.1
```

---

## Ansible Facts
Facts are variables automatically discovered about hosts. For network devices, use modules like `cisco.ios.ios_facts` or `arista.eos.eos_facts`.

**Example:**
```yaml
- name: Gather facts from Cisco IOS
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Get facts
      cisco.ios.ios_facts:
      register: facts
    - debug:
        var: facts
```

---

Continue to [Tutorial 2: Ansible Modules](ansible_tutorial_2_modules.md) 