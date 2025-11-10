---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 13: Design Builder Plugin
tags: ["network automation", "nautobot", "design builder", "designs", "plugin"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 13: Design Builder Plugin
## Create and Deploy Network Designs
*Install Design Builder plugin, create designs via Git sync, and deploy them to your network.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 13: Design Builder Plugin](#nautobot-zero-to-hero--part-13-design-builder-plugin)
  - [Create and Deploy Network Designs](#create-and-deploy-network-designs)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Design Builder Plugin](#3-install-design-builder-plugin)
  - [4. Enable Plugin in Configuration](#4-enable-plugin-in-configuration)
  - [5. Create Designs via Git Sync](#5-create-designs-via-git-sync)
  - [6. Review Available Designs](#6-review-available-designs)
  - [7. Deploy Designs](#7-deploy-designs)
  - [8. Verify Design Deployment](#8-verify-design-deployment)
  - [9. Wrap-Up](#9-wrap-up)
  - [10. Series Conclusion](#10-series-conclusion)

---

## 1. Introduction

In this final part of the series, we'll install and configure the Design Builder plugin. This plugin allows you to create network designs (templates for network topologies) and deploy them to your network. Designs can be synced from Git repositories and deployed via Jobs.

We'll:
1. Install the Design Builder plugin
2. Enable it in configuration
3. Create designs via Git sync of jobs
4. Review and manage designs
5. Deploy designs to your network environment

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites

- Completed [Part 12: Floorplan Plugin](/tutorials/nautobot_zero_to_hero/13_nautobot-zero-to-hero-part12/)
- Nautobot is running
- Git repository integration configured
- Understanding of network design concepts

---

## 3. Install Design Builder Plugin

### 3.1 Install via Docker

```bash
# Access the Nautobot container
docker compose exec nautobot bash

# Install the plugin
pip install nautobot-design-builder

# Exit the container
exit

# Restart Nautobot
docker compose restart nautobot
```

### 3.2 Install via Requirements File

Alternatively, add to `local_requirements.txt`:

```bash
echo "nautobot-design-builder" >> local_requirements.txt
```

---

## 4. Enable Plugin in Configuration

### 4.1 Update nautobot_config.py

Add to your `nautobot_config.py`:

```python
PLUGINS = [
    "nautobot_design_builder",
]

PLUGINS_CONFIG = {
    "nautobot_design_builder": {
        # Plugin configuration options
        "enable_design_sync": True,
        "enable_design_deployment": True,
    }
}
```

### 4.2 Restart Nautobot

```bash
docker compose restart nautobot
```

Wait for Nautobot to restart and verify the plugin is loaded.

---

## 5. Create Designs via Git Sync

### 5.1 Prepare Design Repository

The Design Builder plugin can sync designs from a Git repository. Create or use a repository with design definitions:

1. Create a repository structure:
   ```
   designs/
   ├── access-switch-design.yaml
   ├── distribution-switch-design.yaml
   └── router-design.yaml
   ```

2. Example design file format:
   ```yaml
   name: "Access Switch Design"
   description: "Standard access switch configuration"
   device_types:
     - name: "Access Switch"
       role: "access-switch"
       platform: "cisco-ios"
   interfaces:
     - name: "GigabitEthernet0/1"
       type: "1000base-t"
       enabled: true
   vlans:
     - name: "VLAN100"
       vid: 100
   ```

### 5.2 Add Design Repository to Nautobot

1. Navigate to **Apps → Git Repositories**
2. Click **Add**
3. Configure:
   - **Name**: `design-builder-designs`
   - **Source URL**: Your designs repository URL
   - **Branch**: `main`
   - **Secrets Group**: (if private repo)
   - Enable **Design Builder Designs** checkbox
4. Click **Save and Sync Now**

📸 **[Screenshot: Design Repository Configuration]**

### 5.3 Sync Designs

1. After adding the repository, designs will sync automatically
2. Navigate to **Design Builder → Designs**
3. Verify designs are loaded

📸 **[Screenshot: Synced Designs List]**

---

## 6. Review Available Designs

### 6.1 View Designs

1. Navigate to **Design Builder → Designs**
2. Review available designs
3. Click on a design to view details

📸 **[Screenshot: Designs List]**

### 6.2 Design Details

Each design shows:
- **Name and Description**: What the design is for
- **Device Types**: What devices this design applies to
- **Configuration**: Design parameters
- **Deployment Jobs**: Jobs available for deployment

📸 **[Screenshot: Design Details]**

### 6.3 Edit Designs

1. Designs can be edited in the Git repository
2. After editing, sync the repository
3. Changes will be reflected in Nautobot

---

## 7. Deploy Designs

### 7.1 Select Design to Deploy

1. Navigate to **Design Builder → Designs**
2. Select a design
3. Click **Deploy Design**

📸 **[Screenshot: Deploy Design Button]**

### 7.2 Configure Deployment

1. Select deployment parameters:
   - **Site**: Where to deploy
   - **Device**: Target device (if applicable)
   - **Design Parameters**: Customize design values
2. Review deployment preview
3. Click **Deploy**

📸 **[Screenshot: Design Deployment Configuration]**

### 7.3 Run Deployment Job

1. The deployment will run as a Job
2. Monitor job progress
3. Review job output

📸 **[Screenshot: Design Deployment Job]**

---

## 8. Verify Design Deployment

### 8.1 Check Device Configuration

1. Navigate to the device that received the design
2. Verify configuration matches the design
3. Check interfaces, VLANs, and other design elements

📸 **[Screenshot: Device with Deployed Design]**

### 8.2 Verify in Network

1. SSH to the device
2. Verify the design was applied
3. Test connectivity and functionality

```bash
ssh admin@device-name
show running-config
show vlan brief
```

### 8.3 Compare with Design

1. In Nautobot, compare:
   - Design specification
   - Actual device configuration
2. Verify they match

---

## 9. Wrap-Up

Congratulations! You have successfully:
- ✅ Installed the Design Builder plugin
- ✅ Enabled the plugin in configuration
- ✅ Created designs via Git sync
- ✅ Reviewed and managed designs
- ✅ Deployed designs to your network
- ✅ Verified design deployment

You can now create reusable network designs and deploy them consistently!

---

## 10. Series Conclusion

🎉 **Congratulations on completing the Nautobot Zero to Hero series!**

You have built a complete network automation platform with:

### **Foundation**
- ✅ Nautobot installed and configured
- ✅ Demo environment deployed
- ✅ Network lab set up with Containerlab

### **Core Automation**
- ✅ Device discovery and onboarding automated
- ✅ Configuration management with Jobs
- ✅ Golden Config for compliance and remediation
- ✅ Event-driven automation

### **Advanced Features**
- ✅ Visual floor plans
- ✅ Design-based deployments

### **What You Can Do Now**
- Automatically discover and onboard network devices
- Manage device configurations with version control
- Detect and fix configuration drift automatically
- Deploy configurations based on designs
- Visualize your network infrastructure
- React to changes in real-time

### **Next Steps**
- Apply these patterns to your production network
- Customize Jobs and templates for your environment
- Explore additional Nautobot plugins
- Build custom integrations
- Share your automation success stories!

**Happy automating! 🚀**

---

*This concludes the Nautobot Zero to Hero series. Thank you for following along!*

