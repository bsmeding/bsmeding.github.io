---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 4: Device Discovery & Onboarding
tags: ["network automation", "nautobot", "device onboarding", "discovery", "plugin"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 4: Device Discovery & Onboarding
## Automatically Discover and Onboard Network Devices
*Use the Device Onboarding plugin to automatically discover and add devices from your Containerlab network.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 4: Device Discovery & Onboarding](#nautobot-zero-to-hero--part-4-device-discovery--onboarding)
  - [Automatically Discover and Onboard Network Devices](#automatically-discover-and-onboard-network-devices)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Device Onboarding Plugin](#3-install-device-onboarding-plugin)
  - [4. Enable Plugin in nautobot_config.py](#4-enable-plugin-in-nautobot_configpy)
  - [5. Configure Device Onboarding](#5-configure-device-onboarding)
  - [6. Discover Devices from Containerlab](#6-discover-devices-from-containerlab)
  - [7. Verify Onboarded Devices](#7-verify-onboarded-devices)
  - [8. Wrap-Up](#8-wrap-up)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction

In this part, we'll use the Device Onboarding plugin to automatically discover and onboard devices from your Containerlab network. This eliminates the need to manually create each device in Nautobot.

We'll:
1. Install the Device Onboarding plugin
2. Enable it in nautobot_config.py
3. Configure the plugin settings
4. Discover and onboard devices from Containerlab
5. Verify devices are properly created with platforms, roles, and interfaces

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites

- Completed [Part 3: Deploy Network with Containerlab](/tutorials/nautobot_zero_to_hero/03_nautobot-zero-to-hero-part3/)
- Nautobot is running and accessible
- Containerlab network is deployed and devices are reachable
- SSH access to Containerlab devices

> **💡 Starting Fresh?** If you're starting from Part 4, you can clone the [nautobot_zero_to_hero](https://github.com/bsmeding/nautobot_zero_to_hero) repository and follow the setup from Parts 1-3:
> ```bash
> git clone https://github.com/bsmeding/nautobot_zero_to_hero.git
> cd nautobot_zero_to_hero
> bash install.sh
> docker compose up -d
> ```
> Then complete Parts 1-3 before proceeding with Part 4.

---

## 3. Install Device Onboarding Plugin

The Device Onboarding plugin is available from the Nautobot plugin ecosystem. Install it using pip:

### 3.1 Install via Docker

If you're using Docker, add the plugin to your requirements file or install it directly:

```bash
# Access the Nautobot container
docker compose exec nautobot bash

# Install the plugin
pip install nautobot-device-onboarding

# Exit the container
exit

# Restart Nautobot to load the plugin
docker compose restart nautobot
```

### 3.2 Install via Requirements File

Alternatively, add it to a `local_requirements.txt` file and mount it:

```bash
# Create requirements file
echo "nautobot-device-onboarding" > local_requirements.txt

# Update docker-compose.yml to mount and install
# Add volume: ./local_requirements.txt:/opt/nautobot/local_requirements.txt
# Add environment variable: NAUTOBOT_INSTALL_PLUGINS=true
```

---

## 4. Enable Plugin in nautobot_config.py

Edit your `nautobot_config.py` file to enable the plugin:

### 4.1 Locate Configuration File

```bash
# Find your nautobot_config.py
# Usually in ./config/nautobot_config.py or mounted volume
```

### 4.2 Add Plugin to PLUGINS List

```python
PLUGINS = [
    "nautobot_device_onboarding",
]

# Plugin configuration
PLUGINS_CONFIG = {
    "nautobot_device_onboarding": {
        "create_platform_if_missing": True,
        "create_manufacturer_if_missing": True,
        "create_device_type_if_missing": True,
        "create_device_role_if_missing": True,
        "default_device_role": "network",
        "default_device_role_color": "2196F3",
        "default_platform": None,
        "default_site": None,
        "default_device_status": "active",
        "default_interface_mac": None,
        "default_interface_type": "1000base-t",
        "default_interface_mgmt_only": False,
        "default_interface_enabled": True,
        "onboarding_extensions_map": {},
        "object_match_strategy": "loose",
        "skip_device_type_on_update": False,
        "skip_manufacturer_on_update": False,
        "skip_platform_on_update": False,
    }
}
```

### 4.3 Restart Nautobot

```bash
docker compose restart nautobot
```

Wait for Nautobot to fully restart, then verify the plugin is loaded.

---

## 5. Configure Device Onboarding

### 5.1 Access Device Onboarding

1. Navigate to **Apps → Device Onboarding** in Nautobot
2. You should see the Device Onboarding interface

📸 **[Screenshot: Device Onboarding Interface]**

### 5.2 Configure Default Settings

Review and adjust the default settings:
- **Default Site**: Select your lab site
- **Default Device Role**: Choose or create a role (e.g., "switch", "router")
- **Default Platform**: Set if you have a preferred platform
- **Create Missing Objects**: Enable to auto-create platforms, roles, etc.

---

## 6. Discover Devices from Containerlab

### 6.1 Prepare Device Information

Gather information about your Containerlab devices:
- IP addresses or hostnames
- SSH credentials
- Device types (Cisco, Arista, etc.)

### 6.2 Onboard a Device

1. Navigate to **Apps → Device Onboarding → Onboard Device**
2. Enter device information:
   - **IP Address or Hostname**: e.g., `clab-nautobot-lab-sw1`
   - **Site**: Select your lab site
   - **Device Role**: Select or let it auto-create
   - **Platform**: Select or let it auto-discover
   - **Username**: SSH username (e.g., `admin`)
   - **Password**: SSH password (e.g., `admin`)
   - **Secret**: (Optional) Use a Nautobot secret for credentials
3. Click **Onboard**

📸 **[Screenshot: Onboarding Form]**

### 6.3 Review Onboarding Results

After onboarding:
1. Check the job result for any errors
2. Review what was created (device, interfaces, etc.)
3. Verify the device appears in the Devices list

📸 **[Screenshot: Onboarding Job Result]**

### 6.4 Onboard Remaining Devices

Repeat the process for all devices in your Containerlab topology:
- `clab-nautobot-lab-r1`
- `clab-nautobot-lab-sw1`
- `clab-nautobot-lab-sw2`
- etc.

---

## 7. Verify Onboarded Devices

### 7.1 Check Devices List

1. Navigate to **Devices → Devices**
2. Verify all onboarded devices are listed
3. Check that each device has:
   - Correct platform
   - Correct role
   - Correct site
   - Interfaces populated

📸 **[Screenshot: Devices List with Onboarded Devices]**

### 7.2 Verify Device Details

Click on a device to view its details:
- **Interfaces**: Should be populated from device discovery
- **Platform**: Should match the device type
- **Role**: Should be set correctly
- **Status**: Should be "Active"

📸 **[Screenshot: Device Details with Interfaces]**

### 7.3 Verify Interfaces

1. Navigate to **Devices → Interfaces**
2. Filter by your onboarded devices
3. Verify interfaces are correctly discovered and mapped

📸 **[Screenshot: Interfaces List]**

---

## 8. Wrap-Up

Congratulations! You have successfully:
- ✅ Installed the Device Onboarding plugin
- ✅ Enabled the plugin in nautobot_config.py
- ✅ Configured device onboarding settings
- ✅ Discovered and onboarded devices from Containerlab
- ✅ Verified devices are properly created with all details

You now have all your network devices automatically discovered and managed in Nautobot!

---

## 9. Next Steps

Now that devices are onboarded, proceed to **Part 5: Add Device Config from Jobs** to:
- Sync with the nzth_demo_jobs repository
- Create custom Jobs to manage device configurations
- Automate configuration collection and storage

---

*Happy automating! 🚀*
