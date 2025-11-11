---
title: "What is YAML? A Complete Guide for Network Automation"
date: 2024-12-20
author: bsmeding
tags: ["yaml", "network automation", "ansible", "configuration management", "devops", "tutorial"]
toc: true
layout: single
comments: true
---

<!-- more -->

YAML (YAML Ain't Markup Language) has become the de facto standard for configuration files in network automation, DevOps, and infrastructure as code. If you're working with Ansible, Nautobot, Kubernetes, or any modern automation tool, understanding YAML is essential.

In this comprehensive guide, we'll explore what YAML is, how it's used in network automation tools, the differences between YAML specifications, and practical tips for working with YAML effectively.

---

## What is YAML?

YAML is a human-readable data serialization language designed to be both easy to read and easy to write. Unlike JSON or XML, YAML focuses on human readability while maintaining the ability to represent complex data structures.

### Key Characteristics

- **Human-readable** - Easy for humans to read and write
- **Hierarchical** - Uses indentation to represent structure
- **Language-agnostic** - Works with any programming language
- **Expressive** - Supports complex data structures (lists, dictionaries, nested data)
- **Minimal syntax** - Less verbose than XML or JSON

---

## Why YAML in Network Automation?

YAML has become the standard format for network automation tools because:

### 1. **Readability**

Network engineers can easily read and understand YAML files without extensive training:

```yaml
# Ansible playbook - easy to understand
- name: Configure VLANs on switches
  hosts: switches
  tasks:
    - name: Add VLAN 100
      cisco.ios.ios_vlans:
        config:
          - name: Production
            vlan_id: 100
            state: present
```

### 2. **Tool Support**

Most network automation tools use YAML:

- **Ansible** - Playbooks, inventories, variable files
- **Nautobot** - Configuration contexts, device definitions
- **Kubernetes** - Manifests for container orchestration
- **Terraform** - Some configuration formats
- **GitHub Actions / GitLab CI** - Pipeline definitions

### 3. **Version Control Friendly**

YAML files work excellently with Git, making it easy to:
- Track configuration changes
- Review changes in pull requests
- Roll back to previous configurations
- Collaborate on network configurations

---

## YAML Specifications: 1.1 vs 1.2

Understanding the differences between YAML specifications is important for compatibility and avoiding unexpected behavior.

### YAML 1.1 (2005)

**Characteristics:**
- Most widely used version
- Supported by the majority of tools and libraries
- Some inconsistencies with JSON compatibility
- More permissive type system

**Common in:**
- Older tools and libraries
- Python's PyYAML (defaults to 1.1)
- Many Ansible installations

### YAML 1.2 (2009)

**Characteristics:**
- Latest official specification
- **Full JSON compatibility** - Any valid JSON is valid YAML 1.2
- Improved type system
- Better null value handling (`null` instead of `~`, `Null`, etc.)
- Stricter parsing rules

**Common in:**
- Modern tools and libraries
- Kubernetes
- Newer Ansible versions
- Cloud-native tools

### Key Differences

| Feature | YAML 1.1 | YAML 1.2 |
|---------|----------|----------|
| JSON compatibility | Partial | Full |
| Null values | `~`, `null`, `Null`, `NULL` | `null` (JSON-compatible) |
| Boolean values | Multiple formats | `true`/`false` (JSON-compatible) |
| Type system | More permissive | Stricter, JSON-aligned |
| Adoption | Widespread | Growing |

### Example: Null Value Handling

```yaml
# YAML 1.1 - Multiple null representations
value1: ~
value2: null
value3: Null
value4: NULL

# YAML 1.2 - Only null (JSON-compatible)
value1: null
value2: null
```

### Which Version Should You Use?

- **For new projects**: Use YAML 1.2 for better JSON compatibility and future-proofing
- **For existing projects**: Check what your tools support and maintain consistency
- **For Ansible**: Most versions support both, but 1.1 is more common
- **For Kubernetes**: Uses YAML 1.2

---

## YAML Basics for Network Automation

### Document Structure

```yaml
---
# Optional: Document start marker
# YAML content here
name: router-config
version: 1.0
...
# Optional: Document end marker
```

### Core Data Types

#### 1. Mappings (Key-Value Pairs)

```yaml
# Simple mapping
device_name: router1
ip_address: 192.168.1.1
platform: cisco_ios

# Nested mapping
device:
  name: router1
  interfaces:
    - name: GigabitEthernet0/0
      ip: 192.168.1.1
      mask: 255.255.255.0
```

#### 2. Sequences (Lists)

```yaml
# List of devices
devices:
  - router1
  - router2
  - switch1

# List of mappings
vlans:
  - id: 100
    name: Production
  - id: 200
    name: Development
```

#### 3. Scalars (Simple Values)

```yaml
# Strings
hostname: "router1.example.com"
description: 'Core router'

# Numbers
vlan_id: 100
mtu: 1500

# Booleans
enabled: true
shutdown: false
```

### Indentation Rules

**Critical Rules:**
- ✅ **Use spaces, not tabs** - Tabs will cause parser errors
- ✅ **Consistent indentation** - 2 spaces is the standard
- ✅ **Alignment matters** - Items at the same level must align

```yaml
# ✅ CORRECT - 2 spaces, consistent
device:
  name: router1
  interfaces:
    - name: Gi0/0
      ip: 192.168.1.1

# ❌ WRONG - Tabs or inconsistent spacing
device:
	name: router1  # Tab - will cause error
  interfaces:      # Mixed spacing - will cause error
```

---

## YAML in Network Automation Tools

### Ansible Playbooks

Ansible uses YAML for playbooks, inventories, and variable files:

```yaml
---
- name: Configure network devices
  hosts: routers
  gather_facts: no
  tasks:
    - name: Configure hostname
      cisco.ios.ios_config:
        lines:
          - hostname {{ inventory_hostname }}
    
    - name: Configure interfaces
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet0/0
            description: "Uplink to core"
            enabled: true
```

### Nautobot Configuration Contexts

Nautobot uses YAML for configuration contexts:

```yaml
---
# Nautobot Config Context
ntp_servers:
  - 10.0.0.1
  - 10.0.0.2

dns_servers:
  - 8.8.8.8
  - 8.8.4.4

platform_specific:
  cisco_ios:
    management_interface: "Management0"
    cli_commands:
      save_config: "write memory"
```

### Kubernetes Manifests

Kubernetes uses YAML extensively:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### GitHub Actions / GitLab CI

CI/CD pipelines are defined in YAML:

```yaml
# GitHub Actions
name: Network Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Ansible playbook
        run: ansible-playbook site.yml
```

---

## Reading and Parsing YAML

### Command-Line Tools

#### yq (YAML Processor)

Similar to `jq` for JSON, `yq` processes YAML:

```bash
# Install yq
pip install yq

# Read YAML file
yq eval '.device.name' config.yaml

# Modify YAML
yq eval '.device.ip = "192.168.1.2"' -i config.yaml
```

#### yamllint

Validates YAML syntax:

```bash
# Install yamllint
pip install yamllint

# Validate file
yamllint playbook.yml

# Validate with custom rules
yamllint -d '{extends: default, rules: {line-length: {max: 120}}}' playbook.yml
```

### Python Libraries

#### PyYAML

```python
import yaml

# Read YAML file
with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)

# Write YAML file
with open('output.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
```

#### ruamel.yaml

Better for round-trip YAML editing:

```python
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

# Read and modify
with open('config.yaml') as f:
    data = yaml.load(f)

data['device']['ip'] = '192.168.1.2'

# Write back
with open('config.yaml', 'w') as f:
    yaml.dump(data, f)
```

---

## Common YAML Mistakes in Network Automation

### 1. Tab Characters

```yaml
# ❌ WRONG
device:
	name: router1  # Tab character - parser error

# ✅ CORRECT
device:
  name: router1  # Spaces
```

### 2. Inconsistent Indentation

```yaml
# ❌ WRONG
device:
  name: router1
ip: 192.168.1.1  # Wrong indentation level

# ✅ CORRECT
device:
  name: router1
  ip: 192.168.1.1
```

### 3. Missing Space After Colon

```yaml
# ❌ WRONG
name:value  # No space - parsing issues

# ✅ CORRECT
name: value
```

### 4. Incorrect List Formatting

```yaml
# ❌ WRONG
devices:
-router1  # Missing space after dash
-router2

# ✅ CORRECT
devices:
  - router1
  - router2
```

### 5. Unquoted Special Characters

```yaml
# ❌ WRONG - May cause parsing issues
description: Device: Router1 - Core
time: 10:30:00

# ✅ CORRECT - Quote when needed
description: "Device: Router1 - Core"
time: "10:30:00"
```

---

## Best Practices for Network Automation

### 1. Use Consistent Indentation

Always use 2 spaces (the standard):

```yaml
device:
  name: router1
  interfaces:
    - name: Gi0/0
      ip: 192.168.1.1
```

### 2. Validate Before Deployment

Always validate YAML files before using them:

```bash
# Validate Ansible playbook
ansible-playbook --syntax-check playbook.yml

# Validate with yamllint
yamllint playbook.yml
```

### 3. Use Meaningful Comments

```yaml
# Core router configuration
device:
  name: core-router-01
  # Management interface
  mgmt_ip: 10.0.0.1
  # Production VLANs
  vlans:
    - 100
    - 200
```

### 4. Organize Complex Structures

Break down complex configurations:

```yaml
# Instead of one huge file, organize:
# - devices.yaml (device definitions)
# - vlans.yaml (VLAN configurations)
# - interfaces.yaml (interface settings)
```

### 5. Use Templates and Variables

Leverage YAML with templating engines:

```yaml
# Ansible variables
devices:
  - name: "{{ device_name }}"
    ip: "{{ device_ip }}"
    platform: "{{ platform_type }}"
```

---

## Practical Tips

### Learning from Examples

**Best Practice:** Copy YAML examples from official documentation and adapt them.

For example, when learning Ansible:
1. Go to [Ansible Galaxy](https://galaxy.ansible.com/)
2. Find a module like `cisco.ios.ios_vlans`
3. Copy the example YAML
4. Adapt it to your needs

This is the fastest way to learn proper YAML syntax and indentation patterns.

### Use YAML-Aware Editors

- **VS Code** - Install "YAML" extension by Red Hat
- **Vim** - Use vim-yaml plugin
- **Sublime Text** - Built-in YAML syntax highlighting
- **PyCharm** - Excellent YAML support

### Online Validators

- [YAML Lint](https://www.yamllint.com/) - Quick syntax validation
- [Online YAML Parser](https://yaml-online-parser.appspot.com/) - Parse and visualize YAML

---

## YAML vs JSON vs XML

| Feature | YAML | JSON | XML |
|---------|------|------|-----|
| Readability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Verbosity | Low | Medium | High |
| Comments | ✅ Yes | ❌ No | ✅ Yes |
| Data Types | Rich | Limited | Limited |
| Human-friendly | ✅ Yes | ⚠️ Moderate | ❌ No |
| Machine-friendly | ✅ Yes | ✅ Yes | ✅ Yes |

**When to use YAML:**
- Configuration files
- Human-edited data
- Documentation
- Network automation playbooks

**When to use JSON:**
- APIs
- Machine-to-machine communication
- When YAML 1.2 compatibility is needed

---

## Summary

YAML is an essential skill for network automation professionals. Key takeaways:

✅ **YAML is human-readable** - Easy to read and write  
✅ **Widely used** - Standard for Ansible, Nautobot, Kubernetes  
✅ **Two specifications** - YAML 1.1 (common) and YAML 1.2 (modern, JSON-compatible)  
✅ **Indentation matters** - Use spaces (2 spaces standard), not tabs  
✅ **Validate always** - Use yamllint or similar tools  
✅ **Learn from examples** - Copy from official docs and adapt  

The more YAML documents you read and write, the more comfortable you'll become. Start with simple examples, validate your syntax, and gradually work with more complex structures.

---

## Additional Resources

- [Official YAML Website](https://yaml.org/)
- [YAML Specification](https://yaml.org/spec/)
- [YAML FAQ](https://yaml.org/faq.html)
- [Ansible YAML Syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
- [YAML Lint Tool](https://github.com/adrienverge/yamllint)

---

*Happy automating! 🚀*

