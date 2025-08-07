---
authors: [bsmeding]
date: 2025-03-17
title: Getting Started with Network Automation, the complete guide!
summary: A brief introduction to network automation, what is possible, and how to start—even if you are not a coder. Start with Ansible and ready-to-use modules for most vendors.
tags: ["network automation", "ansible", "getting started", "nocode", "tutorial"]
---

# Getting Started with Network Automation

I often get the question from Network Engineers: "How / where do I need to start with Network automation?" This blog post provides a comprehensive guide to start with network automation from beginning to expert level.

<!-- more -->

## What Basic Knowledge is Needed

Most automation tools are command-line based, so a basic understanding of Linux is essential. Here's what you need to know:

### 1. Linux Basics
- Navigate directories (`cd`, `ls`, `pwd`)
- Create and edit files (`touch`, `nano`, `vim`)
- Understand file permissions
- Basic shell commands

For a comprehensive guide to Linux basics for network automation, see [Linux Basics for Network Automation](/blog/posts/tools/linux/).

### 2. Development Environment
After basic Linux understanding, you'll need:
- **IDE**: Visual Studio Code, PyCharm, or even Vim/Emacs
- **Version Control**: Git (GitHub, GitLab, Bitbucket, Azure DevOps)
- **YAML Understanding**: Essential for Ansible playbooks

#### Setting Up Visual Studio Code
For network automation, I recommend Visual Studio Code. See [Visual Studio Code for Network Automation](/blog/posts/tools/visual-studio-code/) for detailed setup instructions, including essential extensions and configurations.

#### Installing Ansible in a Virtual Environment
It's best practice to install Ansible in a Python virtual environment to avoid conflicts with system packages:

```bash
# Create a virtual environment
python3 -m venv automation_env

# Activate the virtual environment
source automation_env/bin/activate    # Linux/macOS
# automation_env\Scripts\activate     # Windows

# Install Ansible
pip install ansible

# Verify installation
ansible --version
```

For more detailed Ansible setup instructions, see [Ansible Introduction & Getting Started](/blog/posts/tools/ansible/).

### 3. YAML Syntax Basics
YAML is the foundation of Ansible playbooks. Here's a quick primer:

```yaml
# Basic YAML structure
---
- name: Example playbook
  hosts: network_devices
  gather_facts: false
  
  vars:
    snmp_community: public
    ntp_servers:
      - 192.168.1.1
      - 192.168.1.2
  
  tasks:
    - name: Get device info
      cisco.ios.ios_command:
        commands: show version
```

## Next Steps: Start Creating Your First Automation

First automation should always be small and easy to start. I recommend beginning with Ansible rather than pure Python code, unless you're already familiar with programming.

### Why Start with Ansible?
- **No coding required**: Use existing modules
- **Declarative**: Describe what you want, not how to do it
- **Vendor-agnostic**: Works with Cisco, Arista, Juniper, and more
- **Large community**: Plenty of examples and support

## Automation Steps: Easy to Advanced

Don't try to automate a full device configuration directly. Start small and extend when successful.

### Step 1: Getting Information from Network Devices

Start by creating a playbook to retrieve information from network devices. For testing, you can use:
- Real devices in your network
- Virtual devices with ContainerLab, VMware, VirtualBox, or other virtualization platforms

I recommend VirtualBox for beginners (see my blog post 'getting-started-with-containerlab' for setup instructions).

#### Example: Basic Device Information Gathering

```yaml
---
- name: Gather device information
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Get device version
      cisco.ios.ios_command:
        commands: 
          - show version
          - show running-config | include hostname
      register: device_info
    
    - name: Display device information
      debug:
        msg: "Device: {{ device_info.stdout[1] | regex_search('hostname (.+)') | regex_replace('hostname (.+)', '\\1') }}"
```

#### Inventory Setup

Create an inventory file (`inventory.yml`):

```yaml
all:
  children:
    network_devices:
      children:
        cisco_devices:
          hosts:
            switch01:
              ansible_host: 192.168.1.10
            switch02:
              ansible_host: 192.168.1.11
        arista_devices:
          hosts:
            spine01:
              ansible_host: 192.168.1.20
            spine02:
              ansible_host: 192.168.1.21
```

#### Group Variables

Create `group_vars/cisco_devices.yml`:

```yaml
---
ansible_network_os: ios
ansible_connection: network_cli
ansible_user: admin
ansible_password: "{{ vault_cisco_password }}"
ansible_become: yes
ansible_become_method: enable
ansible_become_password: "{{ vault_cisco_enable }}"
```

### Step 2: Making Configuration Changes

After successfully gathering information, start making configuration changes.

#### Example: Change Hostname

```yaml
---
- name: Change device hostname
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Configure hostname
      cisco.ios.ios_config:
        lines:
          - hostname "{{ inventory_hostname }}"
        save_when: modified
```

#### Example: Arista EOS Configuration

```yaml
---
- name: Configure Arista device
  hosts: arista_devices
  gather_facts: false
  
  tasks:
    - name: Set hostname
      arista.eos.eos_config:
        lines:
          - hostname "{{ inventory_hostname }}"
        save_when: modified
```

### Step 3: Interface Management

Start with simple interface operations.

#### Example: Enable/Disable Interfaces

```yaml
---
- name: Manage interface status
  hosts: network_devices
  gather_facts: false
  
  vars:
    target_interfaces:
      - GigabitEthernet0/1
      - GigabitEthernet0/2
  
  tasks:
    - name: Shutdown specified interfaces
      cisco.ios.ios_config:
        lines:
          - shutdown
        parents: "interface {{ item }}"
      loop: "{{ target_interfaces }}"
      when: inventory_hostname in groups['cisco_devices']
```

### Step 4: Interface Configuration

Move to more complex interface configurations.

#### Example: Configure Interface Settings

```yaml
---
- name: Configure interface settings
  hosts: network_devices
  gather_facts: false
  
  vars:
    interface_configs:
      - interface: GigabitEthernet0/1
        description: "Server 1 Connection"
        vlan: 10
      - interface: GigabitEthernet0/2
        description: "Server 2 Connection"
        vlan: 20
  
  tasks:
    - name: Configure interfaces
      cisco.ios.ios_config:
        lines:
          - description "{{ item.description }}"
          - switchport mode access
          - switchport access vlan {{ item.vlan }}
        parents: "interface {{ item.interface }}"
      loop: "{{ interface_configs }}"
```

### Step 5: Using Jinja2 Templates

Templates allow you to create reusable configuration blocks.

#### Example: SNMP Configuration Template

Create `templates/snmp_config.j2`:

```jinja2
snmp-server community {{ snmp_community }} RO
snmp-server location {{ snmp_location }}
snmp-server contact {{ snmp_contact }}
{% for server in ntp_servers %}
ntp server {{ server }}
{% endfor %}
```

#### Playbook Using Template

```yaml
---
- name: Configure SNMP and NTP
  hosts: network_devices
  gather_facts: false
  
  vars:
    snmp_community: "{{ vault_snmp_community }}"
    snmp_location: "Data Center 1"
    snmp_contact: "network-team@company.com"
    ntp_servers:
      - 192.168.1.1
      - 192.168.1.2
  
  tasks:
    - name: Apply SNMP and NTP configuration
      cisco.ios.ios_config:
        src: "templates/snmp_config.j2"
        save_when: modified
```

### Step 6: Creating Loops

Use loops to process multiple items efficiently.

#### Example: Batch Interface Operations

```yaml
---
- name: Batch interface operations
  hosts: network_devices
  gather_facts: false
  
  vars:
    interfaces_to_disable:
      - GigabitEthernet0/5
      - GigabitEthernet0/6
      - GigabitEthernet0/7
  
  tasks:
    - name: Disable unused interfaces
      cisco.ios.ios_config:
        lines:
          - shutdown
        parents: "interface {{ item }}"
      loop: "{{ interfaces_to_disable }}"
      when: 
        - inventory_hostname in groups['cisco_devices']
        - item in interfaces_to_disable
```

#### Example: Using Group Variables for Interface Selection

Create `group_vars/access_switches.yml`:

```yaml
---
access_ports:
  - GigabitEthernet0/1
  - GigabitEthernet0/2
  - GigabitEthernet0/3
  - GigabitEthernet0/4
```

```yaml
---
- name: Configure access ports
  hosts: access_switches
  gather_facts: false
  
  tasks:
    - name: Configure access port settings
      cisco.ios.ios_config:
        lines:
          - switchport mode access
          - spanning-tree portfast
          - spanning-tree bpduguard enable
        parents: "interface {{ item }}"
      loop: "{{ access_ports }}"
```

### Step 7: Using Host Variables

Host variables allow you to override group variables for specific devices.

#### Example: Host-Specific Configuration

Create `host_vars/switch01.yml`:

```yaml
---
custom_vlans:
  - id: 100
    name: "Management"
  - id: 200
    name: "Voice"
  - id: 300
    name: "Data"
```

Create `templates/vlan_config.j2`:

```jinja2
{% for vlan in custom_vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
{% endfor %}
```

```yaml
---
- name: Configure VLANs per device
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Apply VLAN configuration
      cisco.ios.ios_config:
        src: "templates/vlan_config.j2"
        save_when: modified
      when: custom_vlans is defined
```

### Step 8: Configuration Management

Learn to save, backup, and compare configurations.

#### Example: Save and Backup Configuration

```yaml
---
- name: Backup device configurations
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Get running configuration
      cisco.ios.ios_config:
        retrieve: running
      register: running_config
    
    - name: Save configuration to file
      copy:
        content: "{{ running_config.running }}"
        dest: "backups/{{ inventory_hostname }}_{{ ansible_date_time.iso8601 }}.cfg"
      delegate_to: localhost
```

#### Example: Configuration Diff

```yaml
---
- name: Check configuration changes
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Get configuration diff
      cisco.ios.ios_config:
        lines:
          - hostname "{{ inventory_hostname }}"
        diff_against: running
        diff_ignore_lines:
          - "Building configuration"
          - "Current configuration"
      register: config_diff
    
    - name: Display diff
      debug:
        msg: "{{ config_diff.diff }}"
      when: config_diff.diff is defined
```

### Step 9: Restore Backed Up Configuration

Learn to restore configurations from backups.

#### Example: Restore Configuration

```yaml
---
- name: Restore device configuration
  hosts: network_devices
  gather_facts: false
  
  vars:
    backup_file: "backups/{{ inventory_hostname }}_2024-01-15T10:30:00Z.cfg"
  
  tasks:
    - name: Restore configuration from backup
      cisco.ios.ios_config:
        src: "{{ backup_file }}"
        save_when: modified
      when: backup_file is file
```

## Advanced Topics

Once you're comfortable with the basics, explore these advanced topics:

### 1. Error Handling and Rollback

```yaml
---
- name: Configure with rollback capability
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Backup current configuration
      cisco.ios.ios_config:
        retrieve: running
      register: backup_config
    
    - name: Apply new configuration
      cisco.ios.ios_config:
        lines:
          - hostname "{{ inventory_hostname }}_new"
        save_when: modified
      register: config_result
    
    - name: Rollback on failure
      cisco.ios.ios_config:
        src: "{{ backup_config.running }}"
        save_when: modified
      when: config_result is failed
```

### 2. Conditional Configuration

```yaml
---
- name: Conditional configuration based on device type
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Configure access switch features
      cisco.ios.ios_config:
        lines:
          - spanning-tree mode rapid-pvst
          - spanning-tree extend system-id
        parents: spanning-tree
      when: inventory_hostname in groups['access_switches']
    
    - name: Configure distribution switch features
      cisco.ios.ios_config:
        lines:
          - spanning-tree mode rapid-pvst
          - spanning-tree backbonefast
        parents: spanning-tree
      when: inventory_hostname in groups['distribution_switches']
```

### 3. Integration with Network Management Systems

```yaml
---
- name: Update NMS with device information
  hosts: network_devices
  gather_facts: false
  
  tasks:
    - name: Get device facts
      cisco.ios.ios_facts:
      register: device_facts
    
    - name: Update NMS via API
      uri:
        url: "https://nms.company.com/api/devices/{{ inventory_hostname }}"
        method: PUT
        headers:
          Content-Type: "application/json"
          Authorization: "Bearer {{ vault_nms_token }}"
        body_format: json
        body:
          hostname: "{{ inventory_hostname }}"
          model: "{{ device_facts.ansible_net_model }}"
          serial: "{{ device_facts.ansible_net_serialnum }}"
          version: "{{ device_facts.ansible_net_version }}"
      delegate_to: localhost
```

## Best Practices

1. **Start Small**: Begin with read-only operations
2. **Test in Lab**: Always test in a non-production environment
3. **Version Control**: Use Git for all your automation code
4. **Documentation**: Document your playbooks and variables
5. **Security**: Use Ansible Vault for sensitive information
6. **Backup**: Always backup before making changes
7. **Rollback Plan**: Have a plan to revert changes if needed

## Conclusion

Network automation doesn't have to be overwhelming. Start with simple information gathering, then gradually move to configuration changes. Use templates and variables to make your automation reusable and maintainable.

Remember: **Automation is a journey, not a destination**. Start small, learn from each step, and gradually build your automation capabilities.

For more advanced topics, check out my other blog posts on specific automation techniques and tools.

---

*Happy automating! 🚀*



