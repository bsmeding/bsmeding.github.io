---
authors: [bsmeding]
toc: true
date: 2023-02-07
layout: single
comments: true
title: Ansible - Network Settings
summary: A quick guide to Ansible network settings and using network_cli for automation.
tags: ["ansible", "network-cli"]
---

# Ansible - Network Settings

A quick guide to Ansible network settings and how to use them for network automation tasks.

<!-- more -->
---

## Overview

Ansible provides modules and connection plugins for automating network devices. You can use the `network_cli` connection for most network platforms (Cisco, Arista, Juniper, etc.).

---

## Step 1: Inventory Setup (Copy-Paste Example)

Create an inventory file (e.g., `inventory.yml`):

```yaml
all:
  children:
    routers:
      hosts:
        r1:
          ansible_host: 192.0.2.11
          ansible_user: admin
          ansible_password: Cisco123
          ansible_network_os: ios
        r2:
          ansible_host: 192.0.2.12
          ansible_user: admin
          ansible_password: Arista123
          ansible_network_os: eos
```

---

## Step 2: ansible.cfg for Network Automation

Create an `ansible.cfg` in your project directory:

```ini
[defaults]
inventory = ./inventory.yml
host_key_checking = False
retry_files_enabled = False

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
```

- `host_key_checking = False` disables SSH host key checking (useful for labs).
- `ssh_args` enables SSH connection reuse for speed.

---

## Step 3: Example Playbook - Get Facts and Validate Connection

```yaml
---
- name: Validate network device connection and get facts
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Validate device connection
      ping:

    - name: Get device facts
      ios_facts:
      when: ansible_network_os == 'ios'
      register: iosfacts

    - name: Show facts
      debug:
        var: iosfacts
```

For Arista, use `eos_facts:` instead of `ios_facts:`.

---

## Step 4: Example - Run a Command and Validate Output

```yaml
---
- name: Run show version and validate output
  hosts: routers
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Run show version
      ios_command:
        commands:
          - show version
      register: version_output
      when: ansible_network_os == 'ios'

    - name: Validate output contains IOS
      assert:
        that:
          - "'IOS' in version_output.stdout[0]"
      when: ansible_network_os == 'ios'
```

---

## When to Use network_cli (and When Not)

- **Use `network_cli`** for most network devices (Cisco IOS, NX-OS, Arista EOS, Juniper, etc.) that support SSH CLI access.
- **Do NOT use `network_cli`** for:
  - Devices that only support API/NETCONF/REST (use `httpapi`, `netconf`, or `restconf` connection plugins instead).
  - Linux servers (use the default `ssh` connection).

---

## SSH Settings for Network Devices

- Ensure SSH is enabled on all network devices.
- Use strong passwords or SSH keys.
- For lab/dev, you can disable host key checking (see `ansible.cfg` above).
- If using SSH keys, add:
  ```yaml
  ansible_ssh_private_key_file: /path/to/key
  ```
  to your host/group vars.

---

## Related Articles

- [Getting Started with Ansible Network Automation](/blog/posts/2023/2023-03-20-getting-started-with-ansible-network-automation/) - Learn the fundamentals of Ansible network automation with practical examples
- [Ansible Filter Plugins for Cisco Networking](/blog/posts/2023/2023-04-18-ansible_filter_plugin_for_cisco/) - Create custom filter plugins to simplify Cisco IOS configuration tasks

## More Resources
- [Ansible Network Guide](https://docs.ansible.com/ansible/latest/network/index.html)
- [Ansible network_cli connection](https://docs.ansible.com/ansible/latest/plugins/connection/network_cli.html)
- [Ansible ios_facts module](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_facts_module.html)
