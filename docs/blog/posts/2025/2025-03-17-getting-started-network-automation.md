---
authors: [bsmeding]
date: 2025-03-17
title: Getting Started with Network Automation
summary: A brief introduction to network automation, what is possible, and how to start—even if you are not a coder. Start with Ansible and ready-to-use modules for most vendors.
tags: ["network automation", "ansible", "getting started", "nocode", "tutorial"]
---

# Getting Started with Network Automation

Network automation is transforming how we manage and operate networks. Whether you're a beginner or looking to level up your skills, this post will help you get started with the basics, tools, and best practices for automating your network.

<!-- more -->

## What is Possible with Network Automation?
- **Automate repetitive tasks:** Backups, configuration changes, compliance checks, and more.
- **Multi-vendor support:** Manage Cisco, Arista, Juniper, and many other devices from a single tool.
- **Faster deployments:** Roll out new devices or services in minutes, not hours.
- **Consistent changes:** Apply the same configuration everywhere, every time.
- **Self-documenting networks:** Automatically generate inventory and configuration reports.

## Do I Need to Be a Coder?
**Absolutely not!**

You do not need to be a programmer to start with network automation. Many tools are designed for network engineers, not software developers. You can:
- Use simple, human-readable YAML files (no programming required)
- Leverage ready-to-use modules for most network vendors
- Start with copy-paste examples and adapt them to your environment

## Why Start with Ansible?
- **No coding skills required:** Ansible playbooks are written in YAML, which is easy to read and write.
- **Huge module library:** There are modules for Cisco, Arista, Juniper, and many more.
- **Agentless:** No software to install on your network devices—Ansible uses SSH or API connections.
- **Community support:** Tons of examples, documentation, and help available online.
- **Learn more:** See [Ansible: Introduction & Getting Started](../../tools/ansible.md)

## How to Start
1. **Install Ansible:**
   ```bash
   pip install ansible
   # or
   sudo apt install ansible
   ```
2. **Create an inventory file:**
   ```ini
   [routers]
   r1 ansible_host=192.0.2.1 ansible_user=admin ansible_password=yourpass ansible_network_os=ios
   ```
3. **Write your first playbook:**
   ```yaml
   ---
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
4. **Run the playbook:**
   ```bash
   ansible-playbook -i inventory.ini playbook.yml
   ```

## Going Further: Advanced Inventory and Variables
As your automation grows, you’ll want to manage many devices and settings efficiently. Ansible makes this easy with:

### Inventory Files
- Organize devices by groups (e.g., routers, switches, firewalls)
- Use YAML (`inventory.yml`) or INI (`inventory.ini`) formats

### group_vars and host_vars
- Store variables for groups or individual devices in `group_vars/` and `host_vars/` directories
- Example: `group_vars/routers.yml` for all routers, `host_vars/r1.yml` for a specific device

**Example directory structure:**
```
project/
  inventory.yml
  group_vars/
    routers.yml
  host_vars/
    r1.yml
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

This approach makes your automation scalable, maintainable, and easy to update as your network grows.

## Next Steps
- Explore [Ansible Network Getting Started](https://docs.ansible.com/ansible/latest/network/getting_started/index.html)
- Try modules for your vendor (e.g., `ios_command`, `eos_command`, `junos_command`)
- See [Ansible: Introduction & Getting Started](../../tools/ansible.md) for more tips
- Join the community and ask questions—no coding background required!

---

**Remember:** The best way to learn is to start small, experiment, and build confidence. Network automation is for everyone! 