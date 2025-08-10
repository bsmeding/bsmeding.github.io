---
authors: [bsmeding]
date: 2025-09-15
title: Nautobot in Action – Part 5
tags: ["network automation", "event-driven", "job hooks", "nautobot", "real-time automation"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot in Action – Part 5
## Event-Driven Automation: Interface Change Jobs
*Automatically respond to network changes and maintain compliance in real-time.*

<!-- more -->

---

## Index
- [Nautobot in Action – Part 5](#nautobot-in-action--part-5)
  - [Event-Driven Automation: Interface Change Jobs](#event-driven-automation-interface-change-jobs)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Understanding Job Hooks](#3-understanding-job-hooks)
    - [3.1 Hook Types](#31-hook-types)
    - [3.2 Hook Configuration](#32-hook-configuration)
  - [4. Interface Change Detection](#4-interface-change-detection)
    - [4.1 Interface Status Changes](#41-interface-status-changes)
    - [4.2 Interface Description Changes](#42-interface-description-changes)
    - [4.3 VLAN Assignment Changes](#43-vlan-assignment-changes)
  - [5. Sync Admin-State Changes](#5-sync-admin-state-changes)
    - [5.1 Multi-Vendor Admin-State Handling](#51-multi-vendor-admin-state-handling)
    - [5.2 Safe State Transitions](#52-safe-state-transitions)
  - [6. Sync Interface Descriptions](#6-sync-interface-descriptions)
    - [6.1 Description Templates](#61-description-templates)
    - [6.2 Auto-Generated Descriptions](#62-auto-generated-descriptions)
  - [7. Sync VLAN Assignments](#7-sync-vlan-assignments)
    - [7.1 VLAN Configuration](#71-vlan-configuration)
    - [7.2 Trunk Port Management](#72-trunk-port-management)
  - [8. Handle Multi-Vendor Syntax](#8-handle-multi-vendor-syntax)
    - [8.1 Cisco IOS Syntax](#81-cisco-ios-syntax)
    - [8.2 Arista EOS Syntax](#82-arista-eos-syntax)
    - [8.3 Juniper JunOS Syntax](#83-juniper-junos-syntax)
  - [9. Real-Time Automation Workflows](#9-real-time-automation-workflows)
    - [9.1 Change Validation](#91-change-validation)
    - [9.2 Automated Remediation](#92-automated-remediation)
  - [10. Wrap-Up](#10-wrap-up)
    - [What We Accomplished](#what-we-accomplished)
    - [Key Takeaways](#key-takeaways)
  - [11. Next Steps](#11-next-steps)

---

## 1. Introduction
In this fifth part of the series, we'll implement event-driven automation using Job Hooks to automatically respond to network changes and maintain compliance in real-time. This is where our automation becomes truly intelligent - responding to changes as they happen.

We'll:
1. Set up Job Hooks for interface changes
2. Sync admin-state, descriptions, and VLANs automatically
3. Handle multi-vendor syntax differences
4. Create real-time automation workflows
5. Implement change validation and remediation

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites
- Completed [Part 1](/blog/posts/2025/2025-08-09-nautobot-zero-to-hero-part1/), [Part 2](/blog/posts/2025/2025-08-16-nautobot-zero-to-hero-part2-draft/), [Part 3](/blog/posts/2025/2025-08-23-nautobot-zero-to-hero-part3-draft/), and [Part 4](/blog/posts/2025/2025-08-30-nautobot-zero-to-hero-part4-draft/) of this series
- Golden Config plugin installed and configured
- Devices with interfaces configured
- Understanding of network interface management

---

## 3. Understanding Job Hooks

Job Hooks in Nautobot allow us to automatically trigger jobs when specific events occur in the system. For interface changes, we can hook into:

- Interface creation
- Interface modification
- Interface deletion
- Status changes
- Configuration changes

### 3.1 Hook Types
```python
# Available hook types for interfaces
HOOK_TYPES = [
    "interface_created",
    "interface_updated", 
    "interface_deleted",
    "interface_status_changed",
    "interface_config_changed"
]
```

### 3.2 Hook Configuration
```python
# jobs/hooks.py
from nautobot.extras.jobs import Job, JobHookReceiver
from nautobot.dcim.models import Interface

class InterfaceChangeHook(JobHookReceiver):
    class Meta:
        name = "Interface Change Hook"
        description = "Automatically respond to interface changes"

    def receive_job_hook(self, change, action, changed_object):
        """Handle interface change events"""
        if action == "interface_updated":
            self.handle_interface_update(changed_object)
        elif action == "interface_status_changed":
            self.handle_status_change(changed_object)
```

---

## 4. Interface Change Detection

### 4.1 Interface Status Changes
```python
# jobs/interface_status_hook.py
from nautobot.extras.jobs import JobHookReceiver
from nautobot.dcim.models import Interface

class InterfaceStatusHook(JobHookReceiver):
    class Meta:
        name = "Interface Status Change Hook"
        description = "Detect and respond to interface status changes"

    def receive_job_hook(self, change, action, changed_object):
        if action == "interface_status_changed":
            interface = changed_object
            device = interface.device
            
            # Log the status change
            self.log_info(f"Interface {interface.name} on {device.name} status changed to {interface.enabled}")
            
            # Trigger appropriate automation
            if interface.enabled:
                self.handle_interface_enabled(interface)
            else:
                self.handle_interface_disabled(interface)

    def handle_interface_enabled(self, interface):
        """Handle interface being enabled"""
        try:
            # Sync admin-state to device
            self.sync_admin_state(interface)
            self.log_success(f"Synced admin-state for {interface.name}")
        except Exception as e:
            self.log_warning(f"Failed to sync admin-state for {interface.name}: {e}")

    def handle_interface_disabled(self, interface):
        """Handle interface being disabled"""
        try:
            # Sync admin-state to device
            self.sync_admin_state(interface)
            self.log_success(f"Synced admin-state for {interface.name}")
        except Exception as e:
            self.log_warning(f"Failed to sync admin-state for {interface.name}: {e}")
```

### 4.2 Interface Description Changes
```python
# jobs/interface_description_hook.py
from nautobot.extras.jobs import JobHookReceiver
from nautobot.dcim.models import Interface

class InterfaceDescriptionHook(JobHookReceiver):
    class Meta:
        name = "Interface Description Change Hook"
        description = "Detect and respond to interface description changes"

    def receive_job_hook(self, change, action, changed_object):
        if action == "interface_updated":
            interface = changed_object
            
            # Check if description changed
            if hasattr(change, 'description') and change.description:
                self.log_info(f"Interface {interface.name} description changed to: {interface.description}")
                self.sync_interface_description(interface)

    def sync_interface_description(self, interface):
        """Sync interface description to device"""
        try:
            device = interface.device
            platform = device.platform.name
            
            if platform == "cisco_ios":
                self.sync_cisco_description(interface)
            elif platform == "arista_eos":
                self.sync_arista_description(interface)
            elif platform == "juniper_junos":
                self.sync_juniper_description(interface)
            
            self.log_success(f"Synced description for {interface.name}")
        except Exception as e:
            self.log_warning(f"Failed to sync description for {interface.name}: {e}")
```

### 4.3 VLAN Assignment Changes
```python
# jobs/interface_vlan_hook.py
from nautobot.extras.jobs import JobHookReceiver
from nautobot.dcim.models import Interface

class InterfaceVLANHook(JobHookReceiver):
    class Meta:
        name = "Interface VLAN Change Hook"
        description = "Detect and respond to interface VLAN assignment changes"

    def receive_job_hook(self, change, action, changed_object):
        if action == "interface_updated":
            interface = changed_object
            
            # Check if VLAN assignments changed
            if hasattr(change, 'untagged_vlan') or hasattr(change, 'tagged_vlans'):
                self.log_info(f"Interface {interface.name} VLAN assignments changed")
                self.sync_vlan_assignments(interface)

    def sync_vlan_assignments(self, interface):
        """Sync VLAN assignments to device"""
        try:
            device = interface.device
            platform = device.platform.name
            
            if platform == "cisco_ios":
                self.sync_cisco_vlans(interface)
            elif platform == "arista_eos":
                self.sync_arista_vlans(interface)
            elif platform == "juniper_junos":
                self.sync_juniper_vlans(interface)
            
            self.log_success(f"Synced VLAN assignments for {interface.name}")
        except Exception as e:
            self.log_warning(f"Failed to sync VLAN assignments for {interface.name}: {e}")
```

---

## 5. Sync Admin-State Changes

### 5.1 Multi-Vendor Admin-State Handling
```python
# jobs/admin_state_sync.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Interface

class AdminStateSyncJob(Job):
    class Meta:
        name = "Admin State Synchronization"
        description = "Sync interface admin-state across vendors"

    def sync_admin_state(self, interface):
        """Sync admin-state based on vendor platform"""
        device = interface.device
        platform = device.platform.name
        
        if platform == "cisco_ios":
            return self.sync_cisco_admin_state(interface)
        elif platform == "arista_eos":
            return self.sync_arista_admin_state(interface)
        elif platform == "juniper_junos":
            return self.sync_juniper_admin_state(interface)
        else:
            self.log_warning(f"Unsupported platform: {platform}")

    def sync_cisco_admin_state(self, interface):
        """Sync admin-state for Cisco IOS"""
        config_commands = []
        
        if interface.enabled:
            config_commands.append(f"interface {interface.name}")
            config_commands.append("no shutdown")
        else:
            config_commands.append(f"interface {interface.name}")
            config_commands.append("shutdown")
        
        return self.push_config(interface.device, config_commands)

    def sync_arista_admin_state(self, interface):
        """Sync admin-state for Arista EOS"""
        config_commands = []
        
        if interface.enabled:
            config_commands.append(f"interface {interface.name}")
            config_commands.append("no shutdown")
        else:
            config_commands.append(f"interface {interface.name}")
            config_commands.append("shutdown")
        
        return self.push_config(interface.device, config_commands)

    def sync_juniper_admin_state(self, interface):
        """Sync admin-state for Juniper JunOS"""
        config_commands = []
        
        if interface.enabled:
            config_commands.append(f"set interfaces {interface.name} disable")
        else:
            config_commands.append(f"delete interfaces {interface.name} disable")
        
        return self.push_config(interface.device, config_commands)
```

### 5.2 Safe State Transitions
```python
def safe_admin_state_transition(self, interface, target_state):
    """Safely transition interface admin-state"""
    try:
        # Pre-transition checks
        if not self.pre_transition_check(interface):
            self.log_warning(f"Pre-transition check failed for {interface.name}")
            return False
        
        # Backup current state
        current_state = self.get_current_admin_state(interface)
        
        # Perform transition
        if target_state:
            self.enable_interface(interface)
        else:
            self.disable_interface(interface)
        
        # Verify transition
        if self.verify_admin_state(interface, target_state):
            self.log_success(f"Successfully transitioned {interface.name} to {target_state}")
            return True
        else:
            # Rollback if verification fails
            self.rollback_admin_state(interface, current_state)
            self.log_error(f"Admin state transition failed for {interface.name}")
            return False
            
    except Exception as e:
        self.log_error(f"Error during admin state transition: {e}")
        return False
```

---

## 6. Sync Interface Descriptions

### 6.1 Description Templates
```python
# jobs/description_sync.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Interface

class DescriptionSyncJob(Job):
    class Meta:
        name = "Interface Description Synchronization"
        description = "Sync interface descriptions using templates"

    def generate_description_template(self, interface):
        """Generate description using template"""
        template_vars = {
            'interface_name': interface.name,
            'device_name': interface.device.name,
            'site_name': interface.device.site.name,
            'role_name': interface.device.role.name,
            'custom_description': interface.description or ''
        }
        
        # Use Jinja2 template for description
        template = """
        {% if custom_description %}
        {{ custom_description }}
        {% else %}
        {{ device_name }} - {{ interface_name }} - {{ site_name }}
        {% endif %}
        """
        
        return self.render_template(template, template_vars)

    def sync_interface_description(self, interface):
        """Sync interface description to device"""
        device = interface.device
        platform = device.platform.name
        
        description = self.generate_description_template(interface)
        
        if platform == "cisco_ios":
            return self.sync_cisco_description(interface, description)
        elif platform == "arista_eos":
            return self.sync_arista_description(interface, description)
        elif platform == "juniper_junos":
            return self.sync_juniper_description(interface, description)
```

### 6.2 Auto-Generated Descriptions
```python
def auto_generate_description(self, interface):
    """Auto-generate description based on interface properties"""
    description_parts = []
    
    # Add device name
    description_parts.append(interface.device.name)
    
    # Add interface name
    description_parts.append(interface.name)
    
    # Add site information
    if interface.device.site:
        description_parts.append(interface.device.site.name)
    
    # Add role information
    if interface.device.role:
        description_parts.append(interface.device.role.name)
    
    # Add VLAN information
    if interface.untagged_vlan:
        description_parts.append(f"VLAN{interface.untagged_vlan.vid}")
    
    if interface.tagged_vlans.exists():
        vlan_list = [f"VLAN{v.vid}" for v in interface.tagged_vlans.all()]
        description_parts.append(f"Trunk: {','.join(vlan_list)}")
    
    return " - ".join(description_parts)
```

---

## 7. Sync VLAN Assignments

### 7.1 VLAN Configuration
```python
# jobs/vlan_sync.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Interface

class VLANSyncJob(Job):
    class Meta:
        name = "VLAN Assignment Synchronization"
        description = "Sync VLAN assignments to devices"

    def sync_vlan_assignments(self, interface):
        """Sync VLAN assignments based on vendor platform"""
        device = interface.device
        platform = device.platform.name
        
        if platform == "cisco_ios":
            return self.sync_cisco_vlans(interface)
        elif platform == "arista_eos":
            return self.sync_arista_vlans(interface)
        elif platform == "juniper_junos":
            return self.sync_juniper_vlans(interface)

    def sync_cisco_vlans(self, interface):
        """Sync VLANs for Cisco IOS"""
        config_commands = [f"interface {interface.name}"]
        
        if interface.untagged_vlan:
            # Access port configuration
            config_commands.append(f"switchport mode access")
            config_commands.append(f"switchport access vlan {interface.untagged_vlan.vid}")
        elif interface.tagged_vlans.exists():
            # Trunk port configuration
            config_commands.append(f"switchport mode trunk")
            vlan_list = [str(v.vid) for v in interface.tagged_vlans.all()]
            config_commands.append(f"switchport trunk allowed vlan {','.join(vlan_list)}")
        else:
            # No VLAN assignment
            config_commands.append(f"no switchport")
        
        return self.push_config(interface.device, config_commands)
```

### 7.2 Trunk Port Management
```python
def manage_trunk_ports(self, interface):
    """Manage trunk port configuration"""
    if not interface.tagged_vlans.exists():
        return
    
    device = interface.device
    platform = device.platform.name
    
    if platform == "cisco_ios":
        return self.manage_cisco_trunk(interface)
    elif platform == "arista_eos":
        return self.manage_arista_trunk(interface)
    elif platform == "juniper_junos":
        return self.manage_juniper_trunk(interface)

def manage_cisco_trunk(self, interface):
    """Manage Cisco trunk port configuration"""
    config_commands = [
        f"interface {interface.name}",
        "switchport mode trunk",
        "switchport trunk encapsulation dot1q"
    ]
    
    # Add allowed VLANs
    vlan_list = [str(v.vid) for v in interface.tagged_vlans.all()]
    config_commands.append(f"switchport trunk allowed vlan {','.join(vlan_list)}")
    
    # Add native VLAN if specified
    if interface.untagged_vlan:
        config_commands.append(f"switchport trunk native vlan {interface.untagged_vlan.vid}")
    
    return self.push_config(interface.device, config_commands)
```

---

## 8. Handle Multi-Vendor Syntax

### 8.1 Cisco IOS Syntax
```python
# jobs/vendor_syntax.py
class CiscoIOSSyntax:
    """Cisco IOS syntax handler"""
    
    @staticmethod
    def interface_config(interface_name):
        return f"interface {interface_name}"
    
    @staticmethod
    def description_config(description):
        return f"description {description}"
    
    @staticmethod
    def admin_state_config(enabled):
        if enabled:
            return "no shutdown"
        else:
            return "shutdown"
    
    @staticmethod
    def access_vlan_config(vlan_id):
        return [
            "switchport mode access",
            f"switchport access vlan {vlan_id}"
        ]
    
    @staticmethod
    def trunk_vlan_config(tagged_vlans, native_vlan=None):
        config = [
            "switchport mode trunk",
            "switchport trunk encapsulation dot1q"
        ]
        
        if tagged_vlans:
            vlan_list = [str(v.vid) for v in tagged_vlans]
            config.append(f"switchport trunk allowed vlan {','.join(vlan_list)}")
        
        if native_vlan:
            config.append(f"switchport trunk native vlan {native_vlan.vid}")
        
        return config
```

### 8.2 Arista EOS Syntax
```python
class AristaEOSSyntax:
    """Arista EOS syntax handler"""
    
    @staticmethod
    def interface_config(interface_name):
        return f"interface {interface_name}"
    
    @staticmethod
    def description_config(description):
        return f"description {description}"
    
    @staticmethod
    def admin_state_config(enabled):
        if enabled:
            return "no shutdown"
        else:
            return "shutdown"
    
    @staticmethod
    def access_vlan_config(vlan_id):
        return [
            "switchport mode access",
            f"switchport access vlan {vlan_id}"
        ]
    
    @staticmethod
    def trunk_vlan_config(tagged_vlans, native_vlan=None):
        config = [
            "switchport mode trunk"
        ]
        
        if tagged_vlans:
            vlan_list = [str(v.vid) for v in tagged_vlans]
            config.append(f"switchport trunk allowed vlan {','.join(vlan_list)}")
        
        if native_vlan:
            config.append(f"switchport trunk native vlan {native_vlan.vid}")
        
        return config
```

### 8.3 Juniper JunOS Syntax
```python
class JuniperJunOSSyntax:
    """Juniper JunOS syntax handler"""
    
    @staticmethod
    def interface_config(interface_name):
        return f"set interfaces {interface_name}"
    
    @staticmethod
    def description_config(description):
        return f"set interfaces {interface_name} description \"{description}\""
    
    @staticmethod
    def admin_state_config(enabled):
        if enabled:
            return f"delete interfaces {interface_name} disable"
        else:
            return f"set interfaces {interface_name} disable"
    
    @staticmethod
    def access_vlan_config(vlan_id):
        return [
            f"set interfaces {interface_name} unit 0 family ethernet-switching vlan members {vlan_id}"
        ]
    
    @staticmethod
    def trunk_vlan_config(tagged_vlans, native_vlan=None):
        config = []
        
        if tagged_vlans:
            vlan_list = [str(v.vid) for v in tagged_vlans]
            config.append(f"set interfaces {interface_name} unit 0 family ethernet-switching vlan members [{','.join(vlan_list)}]")
        
        if native_vlan:
            config.append(f"set interfaces {interface_name} unit 0 family ethernet-switching native-vlan-id {native_vlan.vid}")
        
        return config
```

---

## 9. Real-Time Automation Workflows

### 9.1 Change Validation
```python
# jobs/change_validation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Interface

class ChangeValidationJob(Job):
    class Meta:
        name = "Change Validation"
        description = "Validate interface changes before applying"

    def validate_interface_change(self, interface, change_type):
        """Validate interface change before applying"""
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check if device is manageable
        if not self.is_device_manageable(interface.device):
            validation_results['valid'] = False
            validation_results['errors'].append("Device is not manageable")
        
        # Check if interface exists on device
        if not self.interface_exists_on_device(interface):
            validation_results['valid'] = False
            validation_results['errors'].append("Interface does not exist on device")
        
        # Check for potential conflicts
        if change_type == "vlan_change":
            conflicts = self.check_vlan_conflicts(interface)
            if conflicts:
                validation_results['warnings'].extend(conflicts)
        
        # Check for security implications
        if change_type == "admin_state_change":
            security_checks = self.check_security_implications(interface)
            if security_checks:
                validation_results['warnings'].extend(security_checks)
        
        return validation_results

    def check_vlan_conflicts(self, interface):
        """Check for VLAN configuration conflicts"""
        conflicts = []
        
        # Check for duplicate VLAN assignments
        if interface.untagged_vlan and interface.tagged_vlans.filter(vid=interface.untagged_vlan.vid).exists():
            conflicts.append("Native VLAN is also in tagged VLANs list")
        
        # Check for VLAN existence
        if interface.untagged_vlan and not self.vlan_exists_on_device(interface.device, interface.untagged_vlan):
            conflicts.append(f"Native VLAN {interface.untagged_vlan.vid} does not exist on device")
        
        for vlan in interface.tagged_vlans.all():
            if not self.vlan_exists_on_device(interface.device, vlan):
                conflicts.append(f"Tagged VLAN {vlan.vid} does not exist on device")
        
        return conflicts
```

### 9.2 Automated Remediation
```python
# jobs/automated_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Interface

class AutomatedRemediationJob(Job):
    class Meta:
        name = "Automated Remediation"
        description = "Automatically remediate interface issues"

    def handle_interface_issue(self, interface, issue_type):
        """Handle interface issues automatically"""
        try:
            if issue_type == "admin_state_mismatch":
                self.remediate_admin_state(interface)
            elif issue_type == "description_mismatch":
                self.remediate_description(interface)
            elif issue_type == "vlan_mismatch":
                self.remediate_vlan_assignments(interface)
            elif issue_type == "configuration_drift":
                self.remediate_configuration_drift(interface)
            
            self.log_success(f"Successfully remediated {interface.name}")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to remediate {interface.name}: {e}")
            return False

    def remediate_admin_state(self, interface):
        """Remediate admin state mismatch"""
        current_state = self.get_device_admin_state(interface)
        intended_state = interface.enabled
        
        if current_state != intended_state:
            self.sync_admin_state(interface)

    def remediate_description(self, interface):
        """Remediate description mismatch"""
        current_description = self.get_device_description(interface)
        intended_description = self.generate_description_template(interface)
        
        if current_description != intended_description:
            self.sync_interface_description(interface)

    def remediate_vlan_assignments(self, interface):
        """Remediate VLAN assignment mismatch"""
        current_vlans = self.get_device_vlan_assignments(interface)
        intended_vlans = self.get_intended_vlan_assignments(interface)
        
        if current_vlans != intended_vlans:
            self.sync_vlan_assignments(interface)
```

---

## 10. Wrap-Up

### What We Accomplished
- ✅ Set up Job Hooks for interface changes
- ✅ Implemented admin-state synchronization
- ✅ Created description sync with templates
- ✅ Built VLAN assignment management
- ✅ Handled multi-vendor syntax differences
- ✅ Implemented real-time automation workflows

### Key Takeaways
- Job Hooks enable real-time response to network changes
- Multi-vendor support requires platform-specific syntax handling
- Change validation prevents configuration errors
- Automated remediation maintains compliance
- Event-driven automation reduces manual intervention

---

## 11. Next Steps

In the next part, we'll implement **full device deployment** with Zero-Touch Provisioning (ZTP) and site validation.

**Coming up in Part 6:**
- Push intended configs to startup/running configs
- Integrate with ZTP server
- Validate site cabling (LLDP/CDP) and VLAN/IP assignments
- Force compliance push option
- Generate site compliance report

---

*Ready to move to Part 6? Let's continue building our network automation solution! 🚀*
