---
authors: [bsmeding]
date: 2025-09-08
title: Nautobot in Action – Part 4
tags: ["network automation", "remediation", "compliance", "nautobot", "configuration management"]
toc: true
layout: single
comments: true
---

# Nautobot in Action – Part 4
## Remediation: Making Devices Compliant
*Automatically fix non-compliant devices and push intended configurations to the network.*

<!-- more -->

---

## Index
- [Nautobot in Action – Part 4](#nautobot-in-action--part-4)
  - [Remediation: Making Devices Compliant](#remediation-making-devices-compliant)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Understanding Remediation Types](#3-understanding-remediation-types)
    - [3.1 Intended Config Remediation](#31-intended-config-remediation)
    - [3.2 Missing Config Remediation](#32-missing-config-remediation)
    - [3.3 Manual Config Remediation](#33-manual-config-remediation)
  - [4. Generate Remediation Configurations](#4-generate-remediation-configurations)
    - [4.1 Intended Config Remediation](#41-intended-config-remediation)
    - [4.2 Missing Config Remediation](#42-missing-config-remediation)
    - [4.3 Manual Config Remediation](#43-manual-config-remediation)
  - [5. Create Multi-Vendor Remediation Job](#5-create-multi-vendor-remediation-job)
    - [5.1 Cisco IOS Remediation](#51-cisco-ios-remediation)
    - [5.2 Arista EOS Remediation](#52-arista-eos-remediation)
    - [5.3 Juniper JunOS Remediation](#53-juniper-junos-remediation)
  - [6. Push Remediation to Devices](#6-push-remediation-to-devices)
    - [6.1 Safe Deployment Strategy](#61-safe-deployment-strategy)
    - [6.2 Rollback Procedures](#62-rollback-procedures)
  - [7. Re-check Compliance After Remediation](#7-re-check-compliance-after-remediation)
    - [7.1 Automated Compliance Verification](#71-automated-compliance-verification)
    - [7.2 Compliance Reporting](#72-compliance-reporting)
  - [8. Advanced Remediation Features](#8-advanced-remediation-features)
    - [8.1 Conditional Remediation](#81-conditional-remediation)
    - [8.2 Batch Remediation](#82-batch-remediation)
  - [9. Wrap-Up](#9-wrap-up)
    - [What We Accomplished](#what-we-accomplished)
    - [Key Takeaways](#key-takeaways)
  - [10. Next Steps](#10-next-steps)

---

## 1. Introduction
In this fourth part of the series, we'll implement remediation workflows to automatically fix non-compliant devices and push intended configurations to the network. This is where our automation truly shines - not just detecting issues, but fixing them automatically.

We'll:
1. Generate different types of remediation configurations
2. Create multi-vendor remediation jobs
3. Push remediation to devices safely
4. Re-check compliance after remediation
5. Implement advanced remediation features

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites
- Completed [Part 1](/blog/posts/2025/2025-08-09-nautobot-zero-to-hero-part1/), [Part 2](/blog/posts/2025/2025-08-16-nautobot-zero-to-hero-part2-draft/), and [Part 3](/blog/posts/2025/2025-08-23-nautobot-zero-to-hero-part3-draft/) of this series
- Golden Config plugin installed and configured
- Devices with compliance issues identified
- Git repository for storing remediation configs

---

## 3. Understanding Remediation Types

Golden Config provides three types of remediation:

### 3.1 Intended Config Remediation
- Replaces the entire device configuration with the intended config
- Use when device has drifted significantly
- Most comprehensive but potentially disruptive

### 3.2 Missing Config Remediation
- Adds only missing configuration elements
- Preserves existing configuration
- Safer for production environments

### 3.3 Manual Config Remediation
- Custom remediation scripts for specific scenarios
- Handles vendor-specific requirements
- Most flexible approach

---

## 4. Generate Remediation Configurations

### 4.1 Intended Config Remediation
```python
# jobs/intended_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device
from nautobot_golden_config.jobs import IntendedConfigJob

class IntendedRemediationJob(IntendedConfigJob):
    class Meta:
        name = "Intended Config Remediation"
        description = "Replace device configs with intended configurations"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        for device in devices:
            try:
                self.generate_intended_config(device)
                self.log_success(f"Generated intended config for {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to generate config for {device.name}: {e}")
```

### 4.2 Missing Config Remediation
```python
# jobs/missing_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class MissingConfigRemediationJob(Job):
    class Meta:
        name = "Missing Config Remediation"
        description = "Add missing configuration elements"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        for device in devices:
            try:
                missing_config = self.get_missing_config(device)
                if missing_config:
                    self.apply_missing_config(device, missing_config)
                    self.log_success(f"Applied missing config to {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to apply missing config to {device.name}: {e}")
```

### 4.3 Manual Config Remediation
```python
# jobs/manual_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class ManualRemediationJob(Job):
    class Meta:
        name = "Manual Config Remediation"
        description = "Custom remediation for specific scenarios"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        for device in devices:
            try:
                custom_config = self.generate_custom_remediation(device)
                if custom_config:
                    self.apply_custom_config(device, custom_config)
                    self.log_success(f"Applied custom remediation to {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to apply custom remediation to {device.name}: {e}")
```

---

## 5. Create Multi-Vendor Remediation Job

### 5.1 Cisco IOS Remediation
```python
# jobs/vendor_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class CiscoIOSRemediationJob(Job):
    class Meta:
        name = "Cisco IOS Remediation"
        description = "Remediate Cisco IOS devices"

    def run(self, data, commit):
        cisco_devices = Device.objects.filter(
            platform__name__icontains="cisco_ios",
            status="active"
        )
        
        for device in cisco_devices:
            try:
                remediation_config = self.generate_cisco_remediation(device)
                self.push_cisco_config(device, remediation_config)
                self.log_success(f"Remediated {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to remediate {device.name}: {e}")
```

### 5.2 Arista EOS Remediation
```python
class AristaEOSRemediationJob(Job):
    class Meta:
        name = "Arista EOS Remediation"
        description = "Remediate Arista EOS devices"

    def run(self, data, commit):
        arista_devices = Device.objects.filter(
            platform__name__icontains="arista_eos",
            status="active"
        )
        
        for device in arista_devices:
            try:
                remediation_config = self.generate_arista_remediation(device)
                self.push_arista_config(device, remediation_config)
                self.log_success(f"Remediated {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to remediate {device.name}: {e}")
```

### 5.3 Juniper JunOS Remediation
```python
class JuniperJunOSRemediationJob(Job):
    class Meta:
        name = "Juniper JunOS Remediation"
        description = "Remediate Juniper JunOS devices"

    def run(self, data, commit):
        juniper_devices = Device.objects.filter(
            platform__name__icontains="juniper_junos",
            status="active"
        )
        
        for device in juniper_devices:
            try:
                remediation_config = self.generate_juniper_remediation(device)
                self.push_juniper_config(device, remediation_config)
                self.log_success(f"Remediated {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to remediate {device.name}: {e}")
```

---

## 6. Push Remediation to Devices

### 6.1 Safe Deployment Strategy
```python
# jobs/safe_deployment.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class SafeRemediationJob(Job):
    class Meta:
        name = "Safe Remediation Deployment"
        description = "Deploy remediation with safety checks"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        
        for device in devices:
            try:
                # Pre-deployment checks
                if not self.pre_deployment_check(device):
                    self.log_warning(f"Skipping {device.name} - failed pre-deployment check")
                    continue
                
                # Backup current config
                self.backup_current_config(device)
                
                # Deploy remediation
                self.deploy_remediation(device)
                
                # Post-deployment verification
                if self.post_deployment_check(device):
                    self.log_success(f"Successfully remediated {device.name}")
                else:
                    self.rollback_device(device)
                    self.log_error(f"Remediation failed for {device.name} - rolled back")
                    
            except Exception as e:
                self.log_error(f"Error during remediation of {device.name}: {e}")
                self.rollback_device(device)
```

### 6.2 Rollback Procedures
```python
def rollback_device(self, device):
    """Rollback device to previous configuration"""
    try:
        previous_config = self.get_previous_config(device)
        self.push_config(device, previous_config)
        self.log_info(f"Rolled back {device.name} to previous configuration")
    except Exception as e:
        self.log_error(f"Failed to rollback {device.name}: {e}")
```

---

## 7. Re-check Compliance After Remediation

### 7.1 Automated Compliance Verification
```python
# jobs/compliance_verification.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class PostRemediationComplianceJob(Job):
    class Meta:
        name = "Post-Remediation Compliance Check"
        description = "Verify compliance after remediation"

    def run(self, data, commit):
        remediated_devices = self.get_recently_remediated_devices()
        compliant_count = 0
        total_count = len(remediated_devices)
        
        for device in remediated_devices:
            try:
                if self.check_compliance(device):
                    compliant_count += 1
                    self.log_success(f"{device.name} is now compliant")
                else:
                    self.log_warning(f"{device.name} is still non-compliant")
            except Exception as e:
                self.log_error(f"Failed to check compliance for {device.name}: {e}")
        
        self.log_info(f"Post-remediation compliance: {compliant_count}/{total_count} devices compliant")
```

### 7.2 Compliance Reporting
```python
def generate_compliance_report(self, devices):
    """Generate detailed compliance report"""
    report = {
        "total_devices": len(devices),
        "compliant_devices": 0,
        "non_compliant_devices": 0,
        "remediation_required": [],
        "compliance_details": {}
    }
    
    for device in devices:
        compliance_status = self.check_compliance(device)
        if compliance_status:
            report["compliant_devices"] += 1
        else:
            report["non_compliant_devices"] += 1
            report["remediation_required"].append(device.name)
        
        report["compliance_details"][device.name] = compliance_status
    
    return report
```

---

## 8. Advanced Remediation Features

### 8.1 Conditional Remediation
```python
# jobs/conditional_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class ConditionalRemediationJob(Job):
    class Meta:
        name = "Conditional Remediation"
        description = "Apply remediation based on conditions"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        
        for device in devices:
            try:
                # Check device conditions
                if self.should_remediate_device(device):
                    remediation_type = self.determine_remediation_type(device)
                    self.apply_conditional_remediation(device, remediation_type)
                    self.log_success(f"Applied conditional remediation to {device.name}")
                else:
                    self.log_info(f"Skipping {device.name} - conditions not met")
            except Exception as e:
                self.log_warning(f"Failed to apply conditional remediation to {device.name}: {e}")
```

### 8.2 Batch Remediation
```python
# jobs/batch_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class BatchRemediationJob(Job):
    class Meta:
        name = "Batch Remediation"
        description = "Remediate multiple devices in batches"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        batch_size = 5  # Process 5 devices at a time
        
        for i in range(0, len(devices), batch_size):
            batch = devices[i:i + batch_size]
            self.log_info(f"Processing batch {i//batch_size + 1}")
            
            for device in batch:
                try:
                    self.remediate_device(device)
                    self.log_success(f"Remediated {device.name}")
                except Exception as e:
                    self.log_warning(f"Failed to remediate {device.name}: {e}")
            
            # Wait between batches
            time.sleep(30)
```

---

## 9. Wrap-Up

### What We Accomplished
- ✅ Generated different types of remediation configurations
- ✅ Created multi-vendor remediation jobs
- ✅ Implemented safe deployment strategies
- ✅ Added rollback procedures
- ✅ Automated compliance verification
- ✅ Built advanced remediation features

### Key Takeaways
- Remediation should always include safety checks and rollback procedures
- Multi-vendor support requires platform-specific handling
- Batch processing helps manage large-scale deployments
- Post-remediation verification is crucial for success
- Conditional remediation provides flexibility for different scenarios

---

## 10. Next Steps

In the next part, we'll implement **event-driven automation** using Job Hooks to automatically respond to network changes and maintain compliance.

**Coming up in Part 5:**
- Job Hooks on interface changes
- Sync admin-state, description, VLANs
- Handle multi-vendor syntax differences
- Real-time network automation

---

*Ready to move to Part 5? Let's continue building our network automation solution! 🚀*
