---
title: Ansible Tutorial 3: Variables, Modules & Network Fact Gathering
tags:
  - ansible
  - tutorial
  - variables
  - network facts
  - getting started
---

# Ansible Tutorial 3: Variables, Modules & Network Fact Gathering

This tutorial covers how to use variables, advanced modules, and gather facts from network devices with Ansible.

## Ansible Variables
Variables allow you to customize playbooks and reuse code. You can define them in playbooks, inventories, `group_vars/`, or `host_vars/`.

**Example:**
```yaml
vars:
  my_var: value
```

## Cisco IOS Modules
Use modules like `ios_command`, `ios_config`, and `ios_facts` for Cisco devices.

**Example:**
```yaml
- name: Get version from Cisco router
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Show version
      ios_command:
        commands:
          - show version
      register: version_output
    - debug:
        var: version_output.stdout_lines
```

## Using cli_command
`cli_command` is a generic module for sending commands to network devices (multi-vendor).

**Example:**
```yaml
- name: Use cli_command on Cisco
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Show interfaces
      cli_command:
        command: show interfaces
      register: interfaces
    - debug:
        var: interfaces.stdout_lines
```

## Using Enable Mode (become)
Some commands require privileged (enable) mode. Use `become: yes` and set `ansible_become_password`.

**Example:**
```yaml
- name: Use enable mode
  hosts: routers
  gather_facts: no
  connection: network_cli
  become: yes
  vars:
    ansible_become_password: your_enable_password
  tasks:
    - name: Show running config
      ios_command:
        commands:
          - show running-config
      register: config
    - debug:
        var: config.stdout_lines
```

## Passing Credentials
You can pass credentials via variables, `group_vars/`, `host_vars/`, or environment variables.

**Example using environment variables:**
```bash
export ANSIBLE_NET_USERNAME=admin
export ANSIBLE_NET_PASSWORD=yourpass
```

## Gathering Network Facts
Use modules like `ios_facts` to gather detailed information from devices.

**Example:**
```yaml
- name: Gather facts from Cisco IOS
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Get facts
      ios_facts:
      register: facts
    - debug:
        var: facts
```

---

Congratulations! You now have a solid foundation in Ansible for network automation. Explore more advanced topics and real-world playbooks as your next step. 