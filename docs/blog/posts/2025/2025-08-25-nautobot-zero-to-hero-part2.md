---
authors: [bsmeding]
date: 2025-08-25
title: Nautobot in Action – Part 2
tags: ["network automation", "device onboarding", "nautobot", "discovery"]
toc: true
layout: single
comments: true
---

# Nautobot in Action – Part 2
## Onboarding Brownfield Devices with the Device Onboarding App
*Automatically discover and onboard existing network devices into Nautobot.*

<!-- more -->

---

## Index
- [Nautobot in Action – Part 2](#nautobot-in-action--part-2)
  - [Onboarding Brownfield Devices with the Device Onboarding App](#onboarding-brownfield-devices-with-the-device-onboarding-app)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Device Onboarding App](#3-install-device-onboarding-app)
    - [3.1 Install the Plugin](#31-install-the-plugin)
    - [3.2 Add to Configuration](#32-add-to-configuration)
    - [3.3 Restart Nautobot](#33-restart-nautobot)
  - [4. Configure Device Discovery](#4-configure-device-discovery)
    - [4.1 Access Device Onboarding](#41-access-device-onboarding)
    - [4.2 Discovery Configuration](#42-discovery-configuration)
  - [5. Run Device Discovery](#5-run-device-discovery)
    - [5.1 Start Discovery Job](#51-start-discovery-job)
    - [5.2 Discovery Process](#52-discovery-process)
  - [6. Review and Import Devices](#6-review-and-import-devices)
    - [6.1 Review Discovered Devices](#61-review-discovered-devices)
    - [6.2 Import Devices](#62-import-devices)
  - [7. Store Discovered Configs in Git](#7-store-discovered-configs-in-git)
    - [7.1 Create Backup Job](#71-create-backup-job)
    - [7.2 Store in Git Repository](#72-store-in-git-repository)
  - [8. Validation and Testing](#8-validation-and-testing)
    - [8.1 Verify Device Import](#81-verify-device-import)
    - [8.2 Test Configuration Access](#82-test-configuration-access)
  - [9. Wrap-Up](#9-wrap-up)
    - [What We Accomplished](#what-we-accomplished)
    - [Key Takeaways](#key-takeaways)
  - [10. Next Steps](#10-next-steps)

---

## 1. Introduction
In this second part of the series, we'll use the Device Onboarding app to automatically discover and onboard existing network devices into Nautobot. This is essential for brownfield environments where you already have devices in production.

We'll:
1. Install and configure the Device Onboarding app
2. Set up device discovery parameters
3. Run discovery against our lab devices
4. Review and import discovered devices
5. Store discovered configurations in Git

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites
- Completed [Part 1](/blog/posts/2025/2025-08-09-nautobot-zero-to-hero-part1/) of this series
- Containerlab lab running with network devices
- Git repository configured in Nautobot
- Basic understanding of network device management

---

## 3. Install Device Onboarding App

### 3.1 Install the Plugin
```bash
# In your Nautobot container
pip install nautobot-device-onboarding
```

### 3.2 Add to Configuration
Add to your `nautobot_config.py`:
```python
PLUGINS = [
    "nautobot_device_onboarding",
]

PLUGINS_CONFIG = {
    "nautobot_device_onboarding": {
        "default_platform": "cisco_ios",
        "default_site": "HQ",
        "default_role": "switch",
        "default_status": "active",
    }
}
```

### 3.3 Restart Nautobot
```bash
docker compose restart nautobot
```

---

## 4. Configure Device Discovery

### 4.1 Access Device Onboarding
1. Navigate to **Plugins > Device Onboarding**
2. Click **Add Device Onboarding**

### 4.2 Discovery Configuration
```yaml
# Example discovery configuration
discovery_type: "ip_addresses"
ip_addresses: "192.168.1.10-20"
platform: "cisco_ios"
site: "HQ"
role: "switch"
status: "active"
```

---

## 5. Run Device Discovery

### 5.1 Start Discovery Job
1. Fill in the discovery form
2. Click **Submit**
3. Monitor the job progress

### 5.2 Discovery Process
The app will:
- Connect to each IP address
- Gather device information
- Extract interface details
- Collect current configuration

---

## 6. Review and Import Devices

### 6.1 Review Discovered Devices
1. Check the discovery results
2. Verify device information
3. Review interface details

### 6.2 Import Devices
1. Select devices to import
2. Choose import options
3. Execute import job

---

## 7. Store Discovered Configs in Git

### 7.1 Create Backup Job
```python
# Example backup job for discovered devices
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class BackupDiscoveredDevices(Job):
    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        for device in devices:
            # Backup configuration
            self.log_info(f"Backing up {device.name}")
```

### 7.2 Store in Git Repository
- Configurations are automatically stored
- Version controlled in Git
- Available for compliance checking

---

## 8. Validation and Testing

### 8.1 Verify Device Import
- Check device count in Nautobot
- Verify interface information
- Confirm platform assignments

### 8.2 Test Configuration Access
- Access device configurations
- Verify Git integration
- Test template rendering

---

## 9. Wrap-Up

### What We Accomplished
- ✅ Installed Device Onboarding app
- ✅ Discovered existing network devices
- ✅ Imported devices with proper metadata
- ✅ Stored configurations in Git
- ✅ Validated the onboarding process

### Key Takeaways
- Device onboarding automates the discovery process
- Proper configuration ensures accurate device import
- Git integration provides version control for configs
- Validation is crucial for production environments

---

## 10. Next Steps

In the next part, we'll implement **Golden Config** for intended configurations and compliance checking. This will build upon our device inventory and stored configurations.

**Coming up in Part 3:**
- Install Golden Config plugin
- Configure backup jobs
- Store intended configs in Git
- Run compliance reports and detect drift

---

*Ready to move to Part 3? Let's continue building our network automation solution! 🚀*
