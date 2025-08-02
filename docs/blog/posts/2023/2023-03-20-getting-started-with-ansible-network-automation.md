---
title: "Getting Started with Ansible Network Automation: A Practical Guide"
authors: [bsmeding]
date: 2023-03-20
summary: Learn how to automate network configurations using Ansible with practical examples, best practices, and real-world use cases.
tags:
  - ansible
  - network automation
  - netdevops
  - automation
  - networking
  - tutorial
---

# Getting Started with Ansible Network Automation: A Practical Guide

**Ansible** has become the de facto standard for network automation, offering a simple yet powerful way to automate network device configurations. This guide will walk you through the fundamentals of using Ansible for network automation, from basic concepts to practical implementations.

<!-- more -->

## Why Ansible for Network Automation?

Ansible offers several advantages for network automation:

- **Agentless**: No software installation required on network devices
- **Declarative**: Describe desired state rather than procedural steps
- **Idempotent**: Safe to run multiple times without side effects
- **Extensible**: Rich ecosystem of modules and collections
- **Human-readable**: YAML-based playbooks are easy to understand

## Prerequisites

Before diving into Ansible network automation, ensure you have:

- Python 3.10+ installed
- Network devices with SSH/API access
- Basic understanding of YAML syntax
- Familiarity with network concepts (VLANs, routing, etc.)

## Installation and Setup

### 1. Install Ansible

```bash
# Using pip (recommended)
pip install ansible

# Using package manager (Ubuntu/Debian)
sudo apt update
sudo apt install ansible

# Using package manager (CentOS/RHEL)
sudo yum install ansible
```

### 2. Install Network Collections

```bash
# Install Cisco IOS collection
ansible-galaxy collection install cisco.ios

# Install Arista EOS collection
ansible-galaxy collection install arista.eos

# Install Juniper JunOS collection
ansible-galaxy collection install junipernetworks.junos
```

### 3. Create Project Structure

```bash
mkdir network-automation
cd network-automation
mkdir {inventory,playbooks,group_vars,host_vars}
```

## Basic Concepts

### Inventory

The inventory file defines your network devices:

```ini
# inventory/hosts
[switches]
switch01 ansible_host=192.168.1.10
switch02 ansible_host=192.168.1.11
switch03 ansible_host=192.168.1.12

[routers]
router01 ansible_host=192.168.1.1
router02 ansible_host=192.168.1.2

[network_devices:children]
switches
routers
```

### Group Variables

Define common variables for device groups:

```yaml
# group_vars/network_devices.yml
ansible_network_os: ios
ansible_connection: network_cli
ansible_user: admin
ansible_password: "{{ vault_network_password }}"
ansible_become: yes
ansible_become_method: enable
ansible_become_password: "{{ vault_enable_password }}"
```

### Host Variables

Define device-specific variables:

```yaml
# host_vars/switch01.yml
device_hostname: SW-CORE-01
management_ip: 192.168.1.10
location: Data Center A
```

## Your First Network Playbook

### Basic VLAN Configuration

```yaml
# playbooks/configure_vlans.yml
---
- name: Configure VLANs on Network Switches
  hosts: switches
  gather_facts: no
  
  vars:
    vlans:
      - id: 10
        name: DATA
        description: Data VLAN
      - id: 20
        name: VOICE
        description: Voice VLAN
      - id: 30
        name: MGMT
        description: Management VLAN

  tasks:
    - name: Configure VLANs
      cisco.ios.vlans:
        config:
          - vlan_id: "{{ item.id }}"
            name: "{{ item.name }}"
            state: present
        state: merged
      loop: "{{ vlans }}"
      register: vlan_result

    - name: Display VLAN configuration results
      debug:
        var: vlan_result
```

### Interface Configuration

```yaml
# playbooks/configure_interfaces.yml
---
- name: Configure Switch Interfaces
  hosts: switches
  gather_facts: no

  tasks:
    - name: Configure access ports
      cisco.ios.interfaces:
        config:
          - name: GigabitEthernet1/0/1
            description: Access Port - PC1
            mode: access
            access:
              vlan: 10
            enabled: true
          - name: GigabitEthernet1/0/2
            description: Access Port - PC2
            mode: access
            access:
              vlan: 20
            enabled: true
        state: merged

    - name: Configure trunk ports
      cisco.ios.interfaces:
        config:
          - name: GigabitEthernet1/0/48
            description: Trunk to Router
            mode: trunk
            trunk:
              allowed_vlans: 10,20,30
              native_vlan: 1
            enabled: true
        state: merged
```

## Advanced Examples

### Backup Configurations

```yaml
# playbooks/backup_configs.yml
---
- name: Backup Network Device Configurations
  hosts: network_devices
  gather_facts: no

  tasks:
    - name: Create backup directory
      file:
        path: "backups/{{ inventory_hostname }}"
        state: directory
      delegate_to: localhost

    - name: Backup running configuration
      cisco.ios.config:
        backup: yes
      register: backup_output

    - name: Copy backup file to local machine
      fetch:
        src: "{{ backup_output.backup_path }}"
        dest: "backups/{{ inventory_hostname }}/"
        flat: yes
      delegate_to: localhost
```

### Configuration Validation

```yaml
# playbooks/validate_config.yml
---
- name: Validate Network Configuration
  hosts: network_devices
  gather_facts: no

  tasks:
    - name: Check interface status
      cisco.ios.interfaces:
        state: gathered
      register: interface_facts

    - name: Validate interface configurations
      assert:
        that:
          - item.enabled == true
          - item.description is defined
        fail_msg: "Interface {{ item.name }} is not properly configured"
        success_msg: "Interface {{ item.name }} is properly configured"
      loop: "{{ interface_facts.gathered }}"
      when: item.name.startswith('GigabitEthernet')
```

## Best Practices

### 1. Use Variables and Templates

```yaml
# group_vars/all.yml
network_config:
  vlans:
    data: 10
    voice: 20
    management: 30
  interfaces:
    access_ports: [1, 2, 3, 4]
    trunk_ports: [48]
```

### 2. Implement Error Handling

```yaml
# playbooks/robust_config.yml
---
- name: Robust Network Configuration
  hosts: switches
  gather_facts: no

  tasks:
    - name: Configure VLANs with error handling
      cisco.ios.vlans:
        config:
          - vlan_id: "{{ item.id }}"
            name: "{{ item.name }}"
        state: merged
      loop: "{{ vlans }}"
      register: vlan_result
      failed_when: vlan_result.failed
      retries: 3
      delay: 10
```

### 3. Use Tags for Selective Execution

```yaml
# playbooks/comprehensive_config.yml
---
- name: Comprehensive Network Configuration
  hosts: switches
  gather_facts: no

  tasks:
    - name: Configure VLANs
      cisco.ios.vlans:
        config: "{{ vlans }}"
        state: merged
      tags: vlans

    - name: Configure interfaces
      cisco.ios.interfaces:
        config: "{{ interfaces }}"
        state: merged
      tags: interfaces

    - name: Configure routing
      cisco.ios.routing:
        config: "{{ routing }}"
        state: merged
      tags: routing
```

## CI/CD Integration

### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - deploy

validate_config:
  stage: validate
  script:
    - ansible-playbook --check playbooks/configure_vlans.yml

test_config:
  stage: test
  script:
    - ansible-playbook --limit test_environment playbooks/configure_vlans.yml

deploy_config:
  stage: deploy
  script:
    - ansible-playbook playbooks/configure_vlans.yml
  when: manual
  only:
    - main
```

### GitHub Actions Workflow

```yaml
# .github/workflows/network-automation.yml
name: Network Automation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install ansible
        ansible-galaxy collection install cisco.ios
    - name: Validate configuration
      run: ansible-playbook --check playbooks/configure_vlans.yml
```

## Monitoring and Validation

### Health Checks

```yaml
# playbooks/health_check.yml
---
- name: Network Health Check
  hosts: network_devices
  gather_facts: no

  tasks:
    - name: Check device connectivity
      cisco.ios.ping:
        dest: "{{ item }}"
        count: 3
      loop: "{{ ping_targets }}"
      register: ping_results

    - name: Check interface status
      cisco.ios.interfaces:
        state: gathered
      register: interface_status

    - name: Generate health report
      template:
        src: templates/health_report.j2
        dest: "reports/{{ inventory_hostname }}_health.html"
      delegate_to: localhost
```

## Troubleshooting Common Issues

### 1. Connection Issues

```bash
# Test connectivity
ansible network_devices -m ping

# Check SSH connection
ssh admin@192.168.1.10

# Verify inventory
ansible-inventory --list
```

### 2. Permission Issues

```yaml
# Ensure proper privilege escalation
ansible_become: yes
ansible_become_method: enable
ansible_become_password: "{{ vault_enable_password }}"
```

### 3. Module Issues

```bash
# Check available modules
ansible-doc -l | grep ios

# Get module documentation
ansible-doc cisco.ios.vlans
```

## Conclusion

Ansible provides a powerful and flexible platform for network automation. By following the practices outlined in this guide, you can build robust, scalable automation solutions that improve network reliability and operational efficiency.

Remember to:
- Start with simple tasks and gradually increase complexity
- Use version control for all playbooks and configurations
- Implement proper testing and validation
- Document your automation workflows
- Continuously improve and refine your processes

## Additional Resources

- [Ansible Network Automation Documentation](https://docs.ansible.com/ansible/latest/network/)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Network Automation Best Practices](https://networktocode.com/blog/)
- [Ansible Network Automation Examples](https://github.com/ansible/ansible-examples)

### Related Tutorials

For more in-depth learning, check out our comprehensive Ansible tutorials:

- [Ansible Tutorial 1: Core Concepts](/tutorials/ansible_tutorial_1_concepts/) - Learn the fundamental concepts of Ansible including playbooks, tasks, and inventory management
- [Ansible Tutorial 2: Working with Modules](/tutorials/ansible_tutorial_2_modules/) - Explore Ansible modules and how to use them effectively for automation
- [Ansible Tutorial 3: Variables and Facts](/tutorials/ansible_tutorial_3_variables_facts/) - Master Ansible variables, facts, and templating for dynamic automation

---

*This guide provides a foundation for Ansible network automation. For more advanced topics, check out our other articles on specific automation scenarios and best practices.* 