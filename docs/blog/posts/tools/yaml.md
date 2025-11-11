---
title: YAML Introduction & Getting Started
authors: [bsmeding]
date: 2024-12-20
summary: A comprehensive guide to YAML syntax, data types, and best practices for network automation.
tags:
  - yaml
  - network automation
  - configuration management
  - ansible
  - devops
---

# YAML: Introduction & Getting Started

**YAML** (YAML Ain't Markup Language) is a human-readable data serialization standard that's widely used in network automation, configuration management, and DevOps tools. Understanding YAML is essential for working with tools like Ansible, Nautobot, Kubernetes, and many other automation platforms.

<!-- more -->

## Why Use YAML?

- **Human-readable** - Easy to read and write
- **Widely adopted** - Standard for Ansible, Nautobot, Kubernetes
- **Version control friendly** - Works excellently with Git
- **Tool support** - Used by most network automation tools

## YAML Document Structure

### Document Markers

- `---` (three dashes) - Optional, indicates the start of a YAML document
- `...` (three dots) - Optional, indicates the end of a YAML document

### File Extensions

The official recommended extension for YAML files is `.yaml`, but `.yml` is also widely accepted.

**Reference:** [YAML FAQ](https://yaml.org/faq.html)

## Comments

Comments in YAML begin with a hash/sharp `#` sign:

```yaml
# This is a comment
name: value  # This is also a comment
```

## Core Data Types

YAML supports three basic data types:

### 1. Mappings (Key-Value Pairs)

Mappings are unordered key-value pairs, similar to Python dictionaries. Each key must be unique.

```yaml
# Simple mapping
name: John Doe
age: 30
city: New York

# Nested mapping
person:
  name: John Doe
  age: 30
  address:
    street: 123 Main St
    city: New York
```

### 2. Sequences (Lists)

Sequences are ordered lists of items, similar to Python lists.

```yaml
# Simple list
fruits:
  - apple
  - banana
  - orange

# Inline list
fruits: [apple, banana, orange]

# List of mappings
servers:
  - name: web1
    ip: 192.168.1.10
  - name: web2
    ip: 192.168.1.11
```

### 3. Scalars (Simple Values)

Scalars are simple values such as strings, numbers, and Booleans.

```yaml
# Strings
name: "John Doe"
description: 'Single quoted string'
unquoted: Plain string

# Numbers
age: 30
price: 19.99
count: 100

# Booleans (multiple representations)
enabled: true
disabled: false
# Also valid: True, False, TRUE, FALSE, yes, no, Yes, No, YES, NO, on, off
```

## Indentation Rules

YAML relies on indentation to define the hierarchical structure of a document.

### Key Rules:

- **Spaces, not tabs** - YAML does not allow tab characters; only spaces are permitted
- **Consistent indentation** - The ideal is 2 spaces per level (though any consistent spacing works)
- **Alignment matters** - Items at the same level must be aligned
- **Critical for parsing** - Incorrect indentation will cause YAML parser errors

### Example:

```yaml
# Correct indentation (2 spaces)
server:
  name: web1
  ip: 192.168.1.10
  services:
    - http
    - https

# Incorrect - mixing tabs and spaces will cause errors
server:
  name: web1  # ERROR if this line uses tabs
```

### Nested Lists

For nested lists, the 2-space indentation count begins after the dash and space of the parent list item.

```yaml
# Correct nested list indentation
networks:
  - name: production
    subnets:
      - 10.0.1.0/24
      - 10.0.2.0/24
  - name: development
    subnets:
      - 192.168.1.0/24
```

## List and Dictionary Formatting

### Lists

List items must be:

- Preceded by `dash+space` (`- `)
- One item per line
- All start at the same indentation level (aligned)

```yaml
# Correct list formatting
devices:
  - router1
  - router2
  - switch1

# Incorrect - items not aligned
devices:
  - router1
- router2  # ERROR: wrong indentation
```

### Dictionaries (Mappings)

Dictionary entries must:

- Use format: `key: value` (key-colon-space-value)
- All start at the same indentation level (aligned)
- Not require a leading dash

```yaml
# Correct dictionary formatting
device:
  name: router1
  ip: 192.168.1.1
  platform: cisco_ios

# Incorrect - keys not aligned
device:
  name: router1
ip: 192.168.1.1  # ERROR: wrong indentation
```

## Alternative Syntax: Flow Style

Instead of indentation, you can explicitly declare lists and dictionaries using:

- **Square brackets** `[ ]` for lists
- **Curly braces** `{ }` for dictionaries

```yaml
# Flow style lists
fruits: [apple, banana, orange]
numbers: [1, 2, 3, 4, 5]

# Flow style dictionaries
person: {name: John, age: 30, city: New York}

# Mixed style
servers:
  - {name: web1, ip: 192.168.1.10}
  - {name: web2, ip: 192.168.1.11}
```

### Empty Collections

Lists and dictionaries can be empty:

```yaml
empty_list: []
empty_dict: {}

# Or block style
empty_list:
empty_dict:
```

## String Handling

Strings can be:

- **Double-quoted** - Allows escape sequences
- **Single-quoted** - Literal strings (no escaping)
- **Plain (unquoted)** - Simple strings without special characters

```yaml
# Double-quoted strings (escape sequences work)
message: "Hello\nWorld"
path: "C:\\Users\\Name"

# Single-quoted strings (literal, no escaping)
message: 'Hello\nWorld'  # Literal \n, not a newline
name: 'John O''Brien'  # Escaped single quote

# Plain strings (no quotes needed for simple values)
name: John Doe
version: 1.0

# Multi-line strings
description: |
  This is a multi-line string.
  It preserves line breaks.
  All lines are included.

# Folded strings (line breaks become spaces)
description: >
  This is a folded string.
  Line breaks become spaces.
  Good for long paragraphs.
```

**Important:** If a string contains special characters (like colons, dashes, or starts with certain characters), it must be quoted to ensure proper YAML parsing.

## Boolean Values

YAML supports multiple representations for boolean values:

**True values:**
- `true`, `True`, `TRUE`
- `yes`, `Yes`, `YES`
- `on`, `On`, `ON`

**False values:**
- `false`, `False`, `FALSE`
- `no`, `No`, `NO`
- `off`, `Off`, `OFF`

```yaml
# All valid boolean representations
enabled: true
disabled: false
feature1: yes
feature2: no
service: on
maintenance: off
```

## YAML Specifications

There are two main YAML specifications:

### YAML 1.1

- The most widely used version
- Supported by most tools and libraries
- Some inconsistencies with JSON compatibility

### YAML 1.2

- The latest version (released in 2009)
- Full compatibility with JSON
- Improved type system
- Better handling of null values
- Growing adoption in modern tools

**Note:** Most modern tools support YAML 1.2, but many still default to YAML 1.1 for backward compatibility.

### Key Differences

| Feature | YAML 1.1 | YAML 1.2 |
|---------|----------|----------|
| JSON compatibility | Partial | Full |
| Null values | `~`, `null`, `Null`, `NULL` | `null` (JSON-compatible) |
| Boolean values | Multiple formats | `true`/`false` (JSON-compatible) |
| Type system | More permissive | Stricter, JSON-aligned |
| Adoption | Widespread | Growing |

## YAML in Network Automation

YAML is extensively used in network automation tools:

### Ansible

```yaml
---
- name: Configure VLANs
  hosts: switches
  tasks:
    - name: Add VLAN 100
      cisco.ios.ios_vlans:
        config:
          - name: Production
            vlan_id: 100
```

### Nautobot

```yaml
---
device:
  name: router1
  device_type: cisco-iosv
  site: datacenter-1
  platform: cisco-ios
  role: core-router
```

### Kubernetes

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
```

## Common YAML Mistakes

### 1. Using Tabs Instead of Spaces

```yaml
# ❌ WRONG - Using tabs
server:
	name: web1  # Tab character - will cause error
	ip: 192.168.1.10

# ✅ CORRECT - Using spaces
server:
  name: web1  # Spaces - correct
  ip: 192.168.1.10
```

### 2. Incorrect Indentation

```yaml
# ❌ WRONG - Inconsistent indentation
server:
  name: web1
ip: 192.168.1.10  # Wrong indentation level

# ✅ CORRECT - Consistent indentation
server:
  name: web1
  ip: 192.168.1.10
```

### 3. Missing Space After Colon

```yaml
# ❌ WRONG - No space after colon
name:value  # Will cause parsing issues

# ✅ CORRECT - Space after colon
name: value
```

### 4. Incorrect List Formatting

```yaml
# ❌ WRONG - Missing space after dash
devices:
-router1
-router2

# ✅ CORRECT - Space after dash
devices:
  - router1
  - router2
```

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

## Practical Tips

1. **Use 2 spaces for indentation** - This is the most common standard
2. **Validate your YAML** - Use online validators or command-line tools like `yamllint`
3. **Start with examples** - Copy YAML examples from official documentation and adapt them
4. **Use a YAML-aware editor** - Editors like VS Code with YAML extensions provide syntax highlighting and validation
5. **Test incrementally** - Build complex YAML files step by step, testing as you go

### Learning from Examples

If you're new to YAML and Ansible, copy YAML examples from the official Ansible documentation (e.g., `cisco.ios.ios_vlans`) and adapt them to your playbooks. It's the fastest way to learn proper YAML syntax and indentation.

## YAML Validators and Tools

### Online Validators

- [YAML Lint](https://www.yamllint.com/)
- [Online YAML Parser](https://yaml-online-parser.appspot.com/)

### Command-Line Tools

- **yamllint** - Linter for YAML files
- **yq** - YAML processor (like jq for JSON)
- **ansible-lint** - Includes YAML validation for Ansible files

### Editor Extensions

- **VS Code** - YAML extension by Red Hat
- **Vim** - vim-yaml plugin
- **Sublime Text** - YAML syntax highlighting

## Summary

YAML is a powerful and human-readable data format essential for network automation. Key takeaways:

- ✅ Use spaces, not tabs
- ✅ Maintain consistent indentation (2 spaces recommended)
- ✅ Align items at the same level
- ✅ Quote strings with special characters
- ✅ Use dash+space (`- `) for list items
- ✅ Use colon+space (`: `) for key-value pairs

The more YAML documents you read and write, the more comfortable you'll become with its syntax and best practices.

## Additional Resources

- [Official YAML Website](https://yaml.org/)
- [YAML Specification](https://yaml.org/spec/)
- [YAML FAQ](https://yaml.org/faq.html)
- [Ansible YAML Syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
- [YAML Lint Tool](https://github.com/adrienverge/yamllint)

---

*For a more detailed blog post about YAML in network automation, see [What is YAML? A Complete Guide for Network Automation](/blog/posts/2024/2024-12-20-what-is-yaml-network-automation/).*

