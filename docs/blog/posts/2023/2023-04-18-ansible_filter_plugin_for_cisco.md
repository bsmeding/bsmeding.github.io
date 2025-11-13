---
authors: [bsmeding]
toc: true
date: 2023-04-18
layout: single
comments: true
title: Ansible - Filter plugins for Cisco networking
summary: Learn how to create and use custom Ansible filter plugins to simplify Cisco IOS configuration tasks, with practical examples and extended filter functions.
tags: ["ansible", "cisco", "ios", "filter-plugins", "network-automation"]
---

# Ansible - Filter plugins for Cisco networking

When automating Cisco network devices with Ansible, you often need to transform data into formats that match Cisco IOS configuration syntax. Custom filter plugins allow you to create reusable functions that simplify these transformations directly in your playbooks and templates.

<!-- more -->

## What are Filter Plugins?

Filter plugins in Ansible are Python functions that transform data. They're similar to Jinja2 filters but are written in Python and can be used in playbooks, templates, and anywhere Ansible processes variables. For network automation, custom filters can:

- Convert data formats (e.g., CIDR to netmask)
- Format interface names consistently
- Generate VLAN range configurations
- Validate network configurations
- Transform data structures for Cisco IOS syntax

## Project Structure

To use custom filter plugins in your Ansible project, create the following directory structure:

```
project/
├── filter_plugins/
│   └── ios_filters.py
├── playbooks/
│   └── configure_network.yml
├── inventory.yml
└── ansible.cfg
```

The `filter_plugins/` directory should be at the same level as your playbooks, or you can specify a custom path in `ansible.cfg`:

```ini
[defaults]
filter_plugins = ./filter_plugins
```

## Creating the Filter Plugin

Let's create a comprehensive filter plugin file with useful functions for Cisco IOS automation:

```python
#!/usr/bin/python3
"""
Ansible filter plugins for Cisco IOS configuration.
Place this file in filter_plugins/ios_filters.py
"""

import re
import ipaddress
import inspect
from ansible.errors import AnsibleError

MAX_LINE_LENGTH = 80


def vlan_ranges(num_list):
    """
    Convert a list of VLAN numbers into range notation.
    
    Input: [1, 2, 3, 5, 7, 8, 9]
    Output: ['1-3', '5', '7-9']
    
    Usage in playbook:
      {{ [1,2,3,5,7,8,9] | vlan_ranges }}
    """
    def get_range_string(range_begin, prev):
        if range_begin == prev:
            return str(range_begin)
        return f"{range_begin}-{prev}"

    result = []
    num_list = sorted(num_list)
    range_begin = int(num_list[0])
    prev = range_begin
    for element in num_list[1:]:
        elem = int(element)
        if elem != prev + 1:
            result.append(get_range_string(range_begin, prev))
            range_begin = elem
        prev = elem

    result.append(get_range_string(range_begin, prev))
    return result


def vlan_ranges_to_config(range_list, max_length=MAX_LINE_LENGTH):
    """
    Split VLAN ranges into multiple lines that fit within max_length.
    
    Input: ['1-3', '5', '7-9'], max_length=10
    Output: ['1-3,5', '7-9']
    
    Usage in playbook:
      {{ vlan_list | vlan_ranges | vlan_ranges_to_config(80) }}
    """
    result = []
    indices = [0]
    prev_length = len(range_list[0])
    for i in range(1, len(range_list)):
        length = len(range_list[i])
        if prev_length + length + 1 > max_length:  # +1 for ','
            indices.append(i)
            prev_length = length
        else:
            prev_length += length + 1

    indices.append(len(range_list))
    for j in range(0, len(indices) - 1):
        result.append(','.join(range_list[indices[j]:indices[j+1]]))
    return result


def get_interface_id(name):
    """
    Extract the interface ID from a full interface name.
    
    Input: 'GigabitEthernet1/1/2'
    Output: '1/1/2'
    
    Usage in playbook:
      {{ 'GigabitEthernet1/1/2' | get_interface_id }}
    """
    re_match = re.search(r'([0-9]+[\/0-9]*)', name)
    if re_match:
        return re_match.group(0)
    return name


def get_interface_id_and_range(name):
    """
    Extract interface ID and range from interface range notation.
    
    Input: 'gi 1/1-10'
    Output: ('1/1', 1, 10)
    
    Usage in playbook:
      {{ 'gi 1/1-10' | get_interface_id_and_range }}
    """
    re_match = re.search(r'([0-9]+(/[0-9]+))/([0-9]+)-([0-9]+)', name)
    if re_match:
        return re_match.group(1), int(re_match.group(3)), int(re_match.group(4))
    return None, None, None


def get_ip_prefix(cidr):
    """
    Extract the prefix length from a CIDR notation.
    
    Input: '10.0.0.1/25'
    Output: '25'
    
    Usage in playbook:
      {{ '10.0.0.1/25' | get_ip_prefix }}
    """
    match = re.search(r'/([0-9]{1,2})', cidr)
    if match:
        return match.group(1)
    return None


def prefix_to_netmask(prefix):
    """
    Convert prefix length to subnet mask.
    
    Input: 25
    Output: '255.255.255.128'
    
    Usage in playbook:
      {{ 25 | prefix_to_netmask }}
    """
    try:
        prefix = int(prefix)
        ip_addr = ipaddress.ip_network(f"0.0.0.0/{prefix}")
        return str(ip_addr.netmask)
    except (ValueError, ipaddress.AddressValueError):
        return None


def interface_in_range(interface, irange):
    """
    Check if an interface is within a specified range.
    
    Input:
      interface: '1/2/6'
      irange: '1/1/0-1/3/0'
    Output: True
    
    Usage in playbook:
      {{ '1/2/6' | interface_in_range('1/1/0-1/3/0') }}
    """
    bounds = irange.split('-')
    if len(bounds) != 2:
        raise AnsibleError(f"[{inspect.currentframe()}] Invalid interface range.")
    
    left_bound = bounds[0].split('/')
    right_bound = bounds[1].split('/')
    if len(left_bound) != len(right_bound):
        raise AnsibleError(f"[{inspect.currentframe()}] Invalid interface range.")
    
    interface_parts = interface.split('/')
    if len(left_bound) != len(interface_parts):
        raise AnsibleError(f"[{inspect.currentframe()}] Interface and range "
                          "bounds have an unequal number of '/' characters.")

    left = False
    right = False
    for i, (mini, maxi) in zip(interface_parts, zip(left_bound, right_bound)):
        if (i < mini and not left) or (i > maxi and not right):
            return False
        if i > mini:
            left = True
        if i < maxi:
            right = True
        if left and right:
            return True
    return True


def normalize_interface_name(name):
    """
    Normalize interface names to Cisco standard format.
    
    Input: 'gi1/0/1', 'GigabitEthernet1/0/1', 'gig1/0/1'
    Output: 'GigabitEthernet1/0/1'
    
    Usage in playbook:
      {{ 'gi1/0/1' | normalize_interface_name }}
    """
    # Common abbreviations mapping
    abbrev_map = {
        'gi': 'GigabitEthernet',
        'te': 'TenGigabitEthernet',
        'fa': 'FastEthernet',
        'et': 'Ethernet',
        'se': 'Serial',
        'lo': 'Loopback',
        'vl': 'Vlan',
        'po': 'Port-channel',
        'tu': 'Tunnel'
    }
    
    # Extract prefix and number
    match = re.match(r'^([a-zA-Z]+)(.*)$', name)
    if not match:
        return name
    
    prefix = match.group(1).lower()
    number = match.group(2)
    
    # Check if it's already full name
    if prefix in [v.lower() for v in abbrev_map.values()]:
        return name.capitalize() if prefix.islower() else name
    
    # Convert abbreviation
    if prefix in abbrev_map:
        return abbrev_map[prefix] + number
    
    return name


def cidr_to_network(cidr):
    """
    Extract network address from CIDR notation.
    
    Input: '10.0.0.1/24'
    Output: '10.0.0.0'
    
    Usage in playbook:
      {{ '10.0.0.1/24' | cidr_to_network }}
    """
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return str(network.network_address)
    except (ValueError, ipaddress.AddressValueError):
        return None


def expand_vlan_range(vlan_range):
    """
    Expand a VLAN range string into a list of VLAN numbers.
    
    Input: '1-3,5,7-9'
    Output: [1, 2, 3, 5, 7, 8, 9]
    
    Usage in playbook:
      {{ '1-3,5,7-9' | expand_vlan_range }}
    """
    result = []
    parts = vlan_range.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            result.extend(range(int(start), int(end) + 1))
        else:
            result.append(int(part))
    return sorted(result)


def format_ios_acl_rule(rule_dict):
    """
    Format a dictionary into Cisco IOS ACL rule syntax.
    
    Input:
      {
        'action': 'permit',
        'protocol': 'tcp',
        'source': '10.0.0.0/24',
        'destination': '192.168.1.0/24',
        'destination_port': 80
      }
    Output: 'permit tcp 10.0.0.0 0.0.0.255 192.168.1.0 0.0.0.255 eq 80'
    
    Usage in playbook:
      {{ acl_rule | format_ios_acl_rule }}
    """
    action = rule_dict.get('action', 'permit')
    protocol = rule_dict.get('protocol', 'ip')
    source = rule_dict.get('source', 'any')
    destination = rule_dict.get('destination', 'any')
    
    # Convert CIDR to network and wildcard
    def cidr_to_wildcard(cidr):
        if cidr == 'any':
            return 'any'
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            wildcard = str(network.hostmask)
            return f"{network.network_address} {wildcard}"
        except:
            return cidr
    
    rule = f"{action} {protocol} {cidr_to_wildcard(source)} {cidr_to_wildcard(destination)}"
    
    # Add port if specified
    if 'destination_port' in rule_dict:
        rule += f" eq {rule_dict['destination_port']}"
    elif 'source_port' in rule_dict:
        rule += f" eq {rule_dict['source_port']}"
    
    return rule


def split_interface_range(interface_range):
    """
    Split an interface range into individual interfaces.
    
    Input: 'GigabitEthernet1/0/1-10'
    Output: ['GigabitEthernet1/0/1', 'GigabitEthernet1/0/2', ..., 'GigabitEthernet1/0/10']
    
    Usage in playbook:
      {{ 'GigabitEthernet1/0/1-10' | split_interface_range }}
    """
    match = re.match(r'^(.+?)(\d+)-(\d+)$', interface_range)
    if not match:
        return [interface_range]
    
    prefix = match.group(1)
    start = int(match.group(2))
    end = int(match.group(3))
    
    return [f"{prefix}{i}" for i in range(start, end + 1)]


def validate_ip_address(ip):
    """
    Validate if a string is a valid IP address.
    
    Input: '192.168.1.1'
    Output: True
    
    Usage in playbook:
      {{ '192.168.1.1' | validate_ip_address }}
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except (ValueError, ipaddress.AddressValueError):
        return False


def validate_cidr(cidr):
    """
    Validate if a string is a valid CIDR notation.
    
    Input: '192.168.1.0/24'
    Output: True
    
    Usage in playbook:
      {{ '192.168.1.0/24' | validate_cidr }}
    """
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except (ValueError, ipaddress.AddressValueError):
        return False


class FilterModule():
    """
    Ansible filter plugin class.
    """
    def filters(self):
        """
        Return dictionary of filter functions.
        """
        return {
            'vlan_ranges': vlan_ranges,
            'vlan_ranges_to_config': vlan_ranges_to_config,
            'get_interface_id': get_interface_id,
            'get_interface_id_and_range': get_interface_id_and_range,
            'get_ip_prefix': get_ip_prefix,
            'prefix_to_netmask': prefix_to_netmask,
            'interface_in_range': interface_in_range,
            'normalize_interface_name': normalize_interface_name,
            'cidr_to_network': cidr_to_network,
            'expand_vlan_range': expand_vlan_range,
            'format_ios_acl_rule': format_ios_acl_rule,
            'split_interface_range': split_interface_range,
            'validate_ip_address': validate_ip_address,
            'validate_cidr': validate_cidr
        }
```

## Using Filters in Playbooks

Now let's see how to use these filters in your Ansible playbooks:

### Example 1: VLAN Configuration with Ranges

```yaml
---
- name: Configure VLANs with range formatting
  hosts: switches
  gather_facts: no
  connection: network_cli

  vars:
    vlan_list: [1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 20, 21, 22, 30, 31, 32, 33, 34, 35]

  tasks:
    - name: Generate VLAN ranges
      set_fact:
        vlan_ranges: "{{ vlan_list | vlan_ranges }}"

    - name: Split ranges into config lines
      set_fact:
        vlan_config_lines: "{{ vlan_ranges | vlan_ranges_to_config(80) }}"

    - name: Display formatted VLAN ranges
      debug:
        msg: "VLAN ranges: {{ vlan_config_lines }}"

    - name: Configure VLANs using ranges
      cisco.ios.vlans:
        config:
          - vlan_id: "{{ item | int }}"
            name: "VLAN{{ item }}"
        state: merged
      loop: "{{ vlan_list }}"
```

### Example 2: Interface Configuration with Normalization

```yaml
---
- name: Configure interfaces with normalized names
  hosts: switches
  gather_facts: no
  connection: network_cli

  vars:
    interfaces:
      - name: gi1/0/1
        description: Access Port 1
        vlan: 10
      - name: GigabitEthernet1/0/2
        description: Access Port 2
        vlan: 20
      - name: te1/1/1
        description: Trunk Port
        mode: trunk

  tasks:
    - name: Configure interfaces
      cisco.ios.interfaces:
        config:
          - name: "{{ item.name | normalize_interface_name }}"
            description: "{{ item.description }}"
            mode: "{{ item.mode | default('access') }}"
            {% if item.vlan is defined %}
            access:
              vlan: "{{ item.vlan }}"
            {% endif %}
        state: merged
      loop: "{{ interfaces }}"
```

### Example 3: IP Address Configuration with CIDR Conversion

```yaml
---
- name: Configure IP addresses with CIDR to netmask conversion
  hosts: routers
  gather_facts: no
  connection: network_cli

  vars:
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.0.1/24
      - name: GigabitEthernet0/1
        ip: 192.168.1.1/25

  tasks:
    - name: Configure interface IP addresses
      cisco.ios.interfaces:
        config:
          - name: "{{ item.name }}"
            ipv4:
              - address: "{{ item.ip | cidr_to_network }} {{ item.ip | get_ip_prefix | prefix_to_netmask }}"
        state: merged
      loop: "{{ interfaces }}"
```

### Example 4: ACL Configuration

```yaml
---
- name: Configure ACLs using filter formatting
  hosts: routers
  gather_facts: no
  connection: network_cli

  vars:
    acl_rules:
      - action: permit
        protocol: tcp
        source: 10.0.0.0/24
        destination: 192.168.1.0/24
        destination_port: 80
      - action: deny
        protocol: ip
        source: any
        destination: 192.168.1.100/32

  tasks:
    - name: Generate ACL configuration
      set_fact:
        acl_config: "{{ acl_rules | map('format_ios_acl_rule') | list }}"

    - name: Display ACL rules
      debug:
        msg: "{{ item }}"
      loop: "{{ acl_config }}"

    - name: Apply ACL configuration
      cisco.ios.acls:
        config:
          - acls:
              - name: WEB_ACCESS
                aces:
                  - sequence: "{{ item.0 }}"
                    grant: "{{ item.1.action }}"
                    protocol: "{{ item.1.protocol }}"
                    source:
                      address: "{{ item.1.source | cidr_to_network }}"
                      wildcard_bits: "{{ item.1.source | get_ip_prefix | prefix_to_netmask }}"
                    destination:
                      address: "{{ item.1.destination | cidr_to_network }}"
                      wildcard_bits: "{{ item.1.destination | get_ip_prefix | prefix_to_netmask }}"
        state: merged
      loop: "{{ acl_rules | enumerate | list }}"
      loop_control:
        label: "{{ item.1.action }} {{ item.1.protocol }}"
```

### Example 5: Interface Range Processing

```yaml
---
- name: Configure multiple interfaces using ranges
  hosts: switches
  gather_facts: no
  connection: network_cli

  vars:
    interface_ranges:
      - GigabitEthernet1/0/1-10
      - GigabitEthernet1/0/20-25

  tasks:
    - name: Expand interface ranges
      set_fact:
        expanded_interfaces: "{{ expanded_interfaces | default([]) + [item | split_interface_range] | flatten }}"
      loop: "{{ interface_ranges }}"

    - name: Configure all interfaces
      cisco.ios.interfaces:
        config:
          - name: "{{ item }}"
            description: "Auto-configured port"
            mode: access
            access:
              vlan: 10
        state: merged
      loop: "{{ expanded_interfaces }}"
```

### Example 6: Validation Before Configuration

```yaml
---
- name: Validate and configure network settings
  hosts: routers
  gather_facts: no
  connection: network_cli

  vars:
    network_config:
      management_ip: 192.168.1.1/24
      gateway: 192.168.1.254
      dns_servers:
        - 8.8.8.8
        - 8.8.4.4

  tasks:
    - name: Validate IP addresses
      assert:
        that:
          - "management_ip | get_ip_prefix | int <= 32"
          - "gateway | validate_ip_address"
          - "item | validate_ip_address"
        fail_msg: "Invalid IP address configuration"
      loop: "{{ network_config.dns_servers }}"
      loop_control:
        label: "{{ item }}"

    - name: Validate CIDR notation
      assert:
        that:
          - "network_config.management_ip | validate_cidr"
        fail_msg: "Invalid CIDR notation for management IP"

    - name: Configure validated settings
      debug:
        msg: "Configuration validated successfully"
```

## Using Filters in Jinja2 Templates

You can also use these filters in Jinja2 templates:

```jinja2
! VLAN Configuration
{% for vlan_range in vlan_list | vlan_ranges | vlan_ranges_to_config(80) %}
vlan {{ vlan_range }}
{% endfor %}

! Interface Configuration
{% for interface in interfaces %}
interface {{ interface.name | normalize_interface_name }}
 description {{ interface.description }}
 ip address {{ interface.ip | cidr_to_network }} {{ interface.ip | get_ip_prefix | prefix_to_netmask }}
{% endfor %}

! ACL Configuration
ip access-list extended WEB_ACCESS
{% for rule in acl_rules %}
 {{ rule | format_ios_acl_rule }}
{% endfor %}
```

## Testing Your Filters

You can test your filters using Ansible's `debug` module or by creating a simple test playbook:

```yaml
---
- name: Test filter plugins
  hosts: localhost
  gather_facts: no
  connection: local

  tasks:
    - name: Test vlan_ranges
      debug:
        msg: "{{ [1,2,3,5,7,8,9] | vlan_ranges }}"
      # Expected: ['1-3', '5', '7-9']

    - name: Test normalize_interface_name
      debug:
        msg: "{{ 'gi1/0/1' | normalize_interface_name }}"
      # Expected: 'GigabitEthernet1/0/1'

    - name: Test prefix_to_netmask
      debug:
        msg: "{{ 24 | prefix_to_netmask }}"
      # Expected: '255.255.255.0'

    - name: Test cidr_to_network
      debug:
        msg: "{{ '10.0.0.1/24' | cidr_to_network }}"
      # Expected: '10.0.0.0'
```

## Best Practices

1. **Error Handling**: Always validate input data before processing. Use `validate_ip_address` and `validate_cidr` filters before configuring network settings.

2. **Reusability**: Create filters that can be used across multiple playbooks and templates.

3. **Documentation**: Document each filter with clear input/output examples and usage notes.

4. **Testing**: Test filters thoroughly with various input formats before using in production.

5. **Performance**: For large datasets, consider the performance impact of filter operations, especially when processing thousands of interfaces or VLANs.

6. **Version Control**: Keep your filter plugins in version control and share them across projects using Ansible collections.

## Creating an Ansible Collection

To share your filter plugins across multiple projects, consider creating an Ansible collection:

```yaml
# galaxy.yml
namespace: your_namespace
name: cisco_filters
version: 1.0.0
readme: README.md
authors:
  - Your Name
description: Custom filter plugins for Cisco IOS automation
```

Place your filter plugins in `plugins/filter/` directory within the collection structure.

## Conclusion

Custom filter plugins are powerful tools for simplifying Cisco IOS configuration tasks in Ansible. They allow you to:

- Transform data into Cisco-specific formats
- Normalize interface names and configurations
- Validate network configurations before deployment
- Generate complex configurations from simple data structures

By creating reusable filter plugins, you can make your Ansible playbooks more readable, maintainable, and less error-prone. Start with the filters provided in this guide and extend them based on your specific needs.

## Additional Resources

- [Ansible Filter Plugin Documentation](https://docs.ansible.com/ansible/latest/plugins/filter.html)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Python ipaddress Module](https://docs.python.org/3/library/ipaddress.html)

---

*This guide provides a comprehensive foundation for creating and using custom filter plugins with Cisco network automation. Extend these examples based on your specific requirements and network environment.*
