---
authors: [bsmeding]
date: 2025-09-15
title: Nautobot in Action – Part 3
tags: ["network automation", "golden config", "nautobot", "compliance"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot in Action – Part 3
## Golden Config for Intended Configs & Compliance
*Implement configuration management and compliance checking with Golden Config.*

<!-- more -->

---

## Index
- [Nautobot in Action – Part 3](#nautobot-in-action--part-3)
  - [Golden Config for Intended Configs \& Compliance](#golden-config-for-intended-configs--compliance)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Golden Config Plugin](#3-install-golden-config-plugin)
    - [3.1 Install the Plugin](#31-install-the-plugin)
    - [3.2 Add to Configuration](#32-add-to-configuration)
    - [3.3 Restart Nautobot](#33-restart-nautobot)
  - [4. Configure Golden Config](#4-configure-golden-config)
    - [4.1 Access Golden Config](#41-access-golden-config)
    - [4.2 Git Repository Configuration](#42-git-repository-configuration)
  - [5. Create Intended Config Templates](#5-create-intended-config-templates)
    - [5.1 Basic Switch Template](#51-basic-switch-template)
    - [5.2 Router Template](#52-router-template)
  - [6. Set Up Backup Jobs](#6-set-up-backup-jobs)
    - [6.1 Create Backup Job](#61-create-backup-job)
    - [6.2 Schedule Backup Jobs](#62-schedule-backup-jobs)
  - [7. Generate Intended Configurations](#7-generate-intended-configurations)
    - [7.1 Create Intended Config Job](#71-create-intended-config-job)
    - [7.2 Run Intended Config Generation](#72-run-intended-config-generation)
  - [8. Run Compliance Reports](#8-run-compliance-reports)
    - [8.1 Create Compliance Job](#81-create-compliance-job)
    - [8.2 Run Compliance Check](#82-run-compliance-check)
  - [9. Detect Configuration Drift](#9-detect-configuration-drift)
    - [9.1 Drift Analysis](#91-drift-analysis)
    - [9.2 Drift Remediation](#92-drift-remediation)
  - [10. Wrap-Up](#10-wrap-up)
    - [What We Accomplished](#what-we-accomplished)
    - [Key Takeaways](#key-takeaways)
  - [11. Next Steps](#11-next-steps)

---

## 1. Introduction
In this third part of the series, we'll implement Golden Config to manage intended configurations and ensure compliance across our network devices. This is a crucial step in maintaining network consistency and detecting unauthorized changes.

We'll:
1. Install and configure the Golden Config plugin
2. Create intended configuration templates
3. Set up automated backup jobs
4. Generate intended configurations
5. Run compliance reports and detect drift

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites
- Completed [Part 1](/blog/posts/2025/2025-08-09-nautobot-zero-to-hero-part1/) and [Part 2](/blog/posts/2025/2025-08-16-nautobot-zero-to-hero-part2-draft/) of this series
- Devices imported into Nautobot
- Git repository configured and working
- Basic understanding of Jinja2 templating

---

## 3. Install Golden Config Plugin

### 3.1 Install the Plugin
```bash
# In your Nautobot container
pip install nautobot-golden-config
```

### 3.2 Add to Configuration
Add to your `nautobot_config.py`:
```python
PLUGINS = [
    "naautobot_golden_config",
]

PLUGINS_CONFIG = {
    "nautobot_golden_config": {
        "enable_backup": True,
        "enable_compliance": True,
        "enable_intended": True,
        "enable_sotagg": True,
        "sot_agg_transposer": "nautobot_golden_config.transposers.SoTaggTransposer",
        "default_delimiter": ".",
        "default_merge_behavior": "replace",
    }
}
```

### 3.3 Restart Nautobot
```bash
docker compose restart nautobot
```

---

## 4. Configure Golden Config

### 4.1 Access Golden Config
1. Navigate to **Plugins > Golden Config**
2. Configure the following sections:
   - **Backup Jobs**
   - **Intended Jobs**
   - **Compliance Jobs**

### 4.2 Git Repository Configuration
```yaml
# Example Git configuration
git_repo: "https://github.com/yourusername/nautobot-configs.git"
git_username: "your-username"
git_password: "your-token"
git_branch: "main"
```

---

## 5. Create Intended Config Templates

### 5.1 Basic Switch Template
```jinja2
{# templates/switch_base.j2 #}
hostname {{ device.name }}
!
interface Loopback0
 description Management Loopback
 ip address {{ device.primary_ip4.address.ip }} {{ device.primary_ip4.address.netmask }}
!
{% for interface in device.interfaces.all %}
interface {{ interface.name }}
 description {{ interface.description|default('') }}
 {% if interface.enabled %}
  no shutdown
 {% else %}
  shutdown
 {% endif %}
{% endfor %}
!
end
```

### 5.2 Router Template
```jinja2
{# templates/router_base.j2 #}
hostname {{ device.name }}
!
interface Loopback0
 description Management Loopback
 ip address {{ device.primary_ip4.address.ip }} {{ device.primary_ip4.address.netmask }}
!
{% for interface in device.interfaces.all %}
interface {{ interface.name }}
 description {{ interface.description|default('') }}
 {% if interface.enabled %}
  no shutdown
 {% else %}
  shutdown
 {% endif %}
{% endfor %}
!
router ospf 1
 network {{ device.primary_ip4.address.network }} {{ device.primary_ip4.address.wildcard }}
!
end
```

---

## 6. Set Up Backup Jobs

### 6.1 Create Backup Job
```python
# jobs/backup_jobs.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device
from nautobot_golden_config.jobs import BackupConfigJob

class NetworkBackupJob(BackupConfigJob):
    class Meta:
        name = "Network Device Backup"
        description = "Backup configurations for all network devices"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        for device in devices:
            try:
                self.backup_device(device)
                self.log_success(f"Backed up {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to backup {device.name}: {e}")
```

### 6.2 Schedule Backup Jobs
1. Navigate to **Jobs > Scheduled Jobs**
2. Create a new scheduled job
3. Set frequency (daily recommended)
4. Assign to appropriate devices

---

## 7. Generate Intended Configurations

### 7.1 Create Intended Config Job
```python
# jobs/intended_jobs.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device
from nautobot_golden_config.jobs import IntendedConfigJob

class GenerateIntendedConfigs(IntendedConfigJob):
    class Meta:
        name = "Generate Intended Configurations"
        description = "Generate intended configurations for all devices"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        for device in devices:
            try:
                self.generate_intended_config(device)
                self.log_success(f"Generated intended config for {device.name}")
            except Exception as e:
                self.log_warning(f"Failed to generate config for {device.name}: {e}")
```

### 7.2 Run Intended Config Generation
1. Navigate to **Jobs > Generate Intended Configurations**
2. Select target devices
3. Choose template mapping
4. Execute the job

---

## 8. Run Compliance Reports

### 8.1 Create Compliance Job
```python
# jobs/compliance_jobs.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device
from nautobot_golden_config.jobs import ComplianceJob

class NetworkComplianceJob(ComplianceJob):
    class Meta:
        name = "Network Compliance Check"
        description = "Check compliance across all network devices"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        compliant_count = 0
        total_count = len(devices)
        
        for device in devices:
            try:
                if self.check_compliance(device):
                    compliant_count += 1
                    self.log_success(f"{device.name} is compliant")
                else:
                    self.log_warning(f"{device.name} is non-compliant")
            except Exception as e:
                self.log_error(f"Failed to check compliance for {device.name}: {e}")
        
        self.log_info(f"Compliance Summary: {compliant_count}/{total_count} devices compliant")
```

### 8.2 Run Compliance Check
1. Navigate to **Jobs > Network Compliance Check**
2. Select devices to check
3. Execute the compliance job
4. Review results and reports

---

## 9. Detect Configuration Drift

### 9.1 Drift Analysis
Golden Config provides several ways to detect drift:

1. **Visual Diff**: Compare intended vs actual configurations
2. **Compliance Reports**: Automated compliance checking
3. **Drift Alerts**: Email notifications for non-compliant devices

### 9.2 Drift Remediation
```python
# jobs/drift_remediation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class DriftRemediationJob(Job):
    class Meta:
        name = "Drift Remediation"
        description = "Remediate configuration drift"

    def run(self, data, commit):
        non_compliant_devices = self.get_non_compliant_devices()
        for device in non_compliant_devices:
            self.remediate_device(device)
```

---

## 10. Wrap-Up

### What We Accomplished
- ✅ Installed Golden Config plugin
- ✅ Created intended configuration templates
- ✅ Set up automated backup jobs
- ✅ Generated intended configurations
- ✅ Implemented compliance checking
- ✅ Detected configuration drift

### Key Takeaways
- Golden Config provides comprehensive configuration management
- Automated backups ensure configuration history
- Compliance checking detects unauthorized changes
- Template-based intended configs ensure consistency
- Drift detection enables proactive network management

---

## 11. Next Steps

In the next part, we'll implement **remediation workflows** to automatically fix non-compliant devices and push intended configurations to the network.

**Coming up in Part 4:**
- Generate remediation configurations
- Create multi-vendor remediation jobs
- Push remediation to devices
- Re-check compliance after remediation

---

*Ready to move to Part 4? Let's continue building our network automation solution! 🚀*
