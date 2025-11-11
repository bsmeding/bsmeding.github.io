---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 6: Enable Golden Config Plugin
tags: ["network automation", "nautobot", "golden config", "compliance", "plugin"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 6: Enable Golden Config Plugin
## Create Golden Configurations for Your Devices
*Install Golden Config plugin, fork required repositories, and create golden configurations.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 6: Enable Golden Config Plugin](#nautobot-zero-to-hero--part-6-enable-golden-config-plugin)
  - [Create Golden Configurations for Your Devices](#create-golden-configurations-for-your-devices)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Golden Config Plugin](#3-install-golden-config-plugin)
  - [4. Fork Required Repositories](#4-fork-required-repositories)
  - [5. Add Repositories to Nautobot](#5-add-repositories-to-nautobot)
  - [6. Configure Golden Config](#6-configure-golden-config)
  - [7. Create Golden Configurations](#7-create-golden-configurations)
  - [8. Wrap-Up](#8-wrap-up)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction

In this part, we'll install and configure the Golden Config plugin, which enables configuration compliance and remediation. We'll fork the required repositories and set up golden configurations for our devices.

We'll:

1. Install the Golden Config plugin
2. Fork three required repositories (backups, jinja templates, intended config)
3. Add the forked repositories to Nautobot
4. Configure Golden Config settings
5. Create golden configurations for devices

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites

- Completed [Part 5: Add Device Config from Jobs](/tutorials/nautobot_zero_to_hero/06_nautobot-zero-to-hero-part5/)
- GitHub account (for forking repositories)
- Devices are onboarded in Nautobot
- Git repository access configured in Nautobot

---

## 3. Install Golden Config Plugin

### 3.1 Install via Docker

```bash
# Access the Nautobot container
docker compose exec nautobot bash

# Install the plugin
pip install nautobot-golden-config

# Exit the container
exit

# Restart Nautobot
docker compose restart nautobot
```

### 3.2 Enable Plugin in nautobot_config.py

Add to your `nautobot_config.py`:

```python
PLUGINS = [
    "nautobot_golden_config",
]

PLUGINS_CONFIG = {
    "nautobot_golden_config": {
        "per_feature_bar_width": 0.3,
        "per_feature_width": 13,
        "per_feature_height": 4,
        "enable_backup": True,
        "enable_compliance": True,
        "enable_intended": True,
        "enable_sot_agg": True,
    }
}
```

Restart Nautobot after making changes.

---

## 4. Fork Required Repositories

Golden Config requires three Git repositories. Fork these repositories to your GitHub account:

### 4.1 Fork Backups Repository

1. Go to [https://github.com/bsmeding/nzth_demo_backups](https://github.com/bsmeding/nzth_demo_backups)
2. Click **Fork** button
3. Fork to your account
4. Note your forked repository URL: `https://github.com/YOUR_USERNAME/nzth_demo_backups.git`

### 4.2 Fork Jinja Templates Repository

1. Go to [https://github.com/bsmeding/nzth_demo_jinja_templates](https://github.com/bsmeding/nzth_demo_jinja_templates)
2. Click **Fork** button
3. Fork to your account
4. Note your forked repository URL: `https://github.com/YOUR_USERNAME/nzth_demo_jinja_templates.git`

### 4.3 Fork Intended Config Repository

1. Go to [https://github.com/bsmeding/nzth_demo_intended_config](https://github.com/bsmeding/nzth_demo_intended_config)
2. Click **Fork** button
3. Fork to your account
4. Note your forked repository URL: `https://github.com/YOUR_USERNAME/nzth_demo_intended_config.git`

---

## 5. Add Repositories to Nautobot

### 5.1 Add Backups Repository

1. Navigate to **Apps → Git Repositories**
2. Click **Add**
3. Configure:
   - **Name:** `golden-config-backups`
   - **Source URL:** Your forked backups repository URL
   - **Branch:** `main`
   - **Secrets Group:** (if using private repo, create secrets group)
   - Enable **Golden Config Backups** checkbox
4. Click **Save and Sync Now**

### 5.2 Add Jinja Templates Repository

1. Click **Add** again
2. Configure:
   - **Name:** `golden-config-templates`
   - **Source URL:** Your forked jinja templates repository URL
   - **Branch:** `main`
   - **Secrets Group:** (if needed)
   - Enable **Golden Config Templates** checkbox
3. Click **Save and Sync Now**

### 5.3 Add Intended Config Repository

1. Click **Add** again
2. Configure:
   - **Name:** `golden-config-intended`
   - **Source URL:** Your forked intended config repository URL
   - **Branch:** `main`
   - **Secrets Group:** (if needed)
   - Enable **Golden Config Intended** checkbox
3. Click **Save and Sync Now**

📸 **[Screenshot: All Three Repositories Added]**

---

## 6. Configure Golden Config

### 6.1 Access Golden Config

1. Navigate to **Golden Config** in the main menu
2. You should see Golden Config options

📸 **[Screenshot: Golden Config Menu]**

### 6.2 Configure Compliance Rules

1. Navigate to **Golden Config → Compliance Rules**
2. Review default rules or create custom rules
3. Configure rules for your device types

### 6.3 Configure Compliance Features

1. Navigate to **Golden Config → Compliance Features**
2. Enable features you want to check:
   - Interface configurations
   - VLAN configurations
   - Routing configurations
   - etc.

---

## 7. Create Golden Configurations

### 7.1 Generate Intended Configuration

1. Navigate to **Golden Config → Intended Configs**
2. Select a device
3. Click **Generate Intended Config**
4. Review the generated configuration

📸 **[Screenshot: Generated Intended Config]**

### 7.2 Create Golden Config for Device

1. Navigate to **Golden Config → Golden Configurations**
2. Click **Add**
3. Select:
   - **Device**: Choose your device
   - **Backup Repository**: Select your backups repo
   - **Template Repository**: Select your templates repo
   - **Intended Repository**: Select your intended config repo
4. Click **Save**

### 7.3 Generate Golden Config

1. Click on your created Golden Config
2. Click **Generate Config**
3. Review the generated configuration
4. Verify it's stored in the intended config repository

📸 **[Screenshot: Golden Configuration Details]**

---

## 8. Wrap-Up

Congratulations! You have successfully:
- ✅ Installed the Golden Config plugin
- ✅ Forked all three required repositories
- ✅ Added repositories to Nautobot
- ✅ Configured Golden Config settings
- ✅ Created golden configurations for devices

You now have Golden Config set up and ready for compliance checking and remediation!

---

## 9. Next Steps

Now that Golden Config is configured, proceed to **Part 7: Deploy Provision Job** to:
- Create a Provision job to send golden-config to devices
- Deploy intended configurations to network devices
- Verify configuration deployment

---

*Happy automating! 🚀*
