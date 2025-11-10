---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 12: Floorplan Plugin
tags: ["network automation", "nautobot", "floorplan", "visualization", "plugin"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 12: Floorplan Plugin
## Visualize Your Network with Floor Plans
*Enable and use the Floorplan plugin to create visual representations of your network sites.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 12: Floorplan Plugin](#nautobot-zero-to-hero--part-12-floorplan-plugin)
  - [Visualize Your Network with Floor Plans](#visualize-your-network-with-floor-plans)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Floorplan Plugin](#3-install-floorplan-plugin)
  - [4. Enable Plugin in Configuration](#4-enable-plugin-in-configuration)
  - [5. Create Floor Plans](#5-create-floor-plans)
  - [6. Map Devices to Locations](#6-map-devices-to-locations)
  - [7. Use Floor Plans](#7-use-floor-plans)
  - [8. Wrap-Up](#8-wrap-up)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction

In this part, we'll install and configure the Floorplan plugin, which allows you to create visual floor plans for your network sites and map devices to physical locations. This provides a visual representation of where devices are located.

We'll:
1. Install the Floorplan plugin
2. Enable it in nautobot_config.py
3. Create floor plans for your sites
4. Map devices to locations on the floor plan
5. Use floor plans for visualization and management

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites

- Completed [Part 11: Event-Driven Automation](/tutorials/nautobot_zero_to_hero/12_nautobot-zero-to-hero-part11/)
- Nautobot is running
- Sites and devices are configured
- Basic understanding of site layouts

---

## 3. Install Floorplan Plugin

### 3.1 Install via Docker

```bash
# Access the Nautobot container
docker compose exec nautobot bash

# Install the plugin
pip install nautobot-floor-plan

# Exit the container
exit

# Restart Nautobot
docker compose restart nautobot
```

### 3.2 Install via Requirements File

Alternatively, add to `local_requirements.txt`:

```bash
echo "nautobot-floor-plan" >> local_requirements.txt
```

Update docker-compose.yml to install from requirements file.

---

## 4. Enable Plugin in Configuration

### 4.1 Update nautobot_config.py

Add to your `nautobot_config.py`:

```python
PLUGINS = [
    "nautobot_floor_plan",
]

PLUGINS_CONFIG = {
    "nautobot_floor_plan": {
        # Plugin configuration options
    }
}
```

### 4.2 Restart Nautobot

```bash
docker compose restart nautobot
```

Wait for Nautobot to restart and verify the plugin is loaded.

---

## 5. Create Floor Plans

### 5.1 Access Floor Plans

1. Navigate to **Floor Plans** in the main menu
2. You should see the Floor Plans interface

📸 **[Screenshot: Floor Plans Menu]**

### 5.2 Create a Floor Plan

1. Click **Add** to create a new floor plan
2. Configure:
   - **Name**: e.g., "Data Center Floor 1"
   - **Site**: Select the site
   - **Location**: (Optional) Specific location within site
   - **Image**: Upload a floor plan image (PNG, JPG, SVG)
   - **Width/Height**: Set dimensions in meters or feet
3. Click **Save**

📸 **[Screenshot: Creating Floor Plan]**

### 5.3 Upload Floor Plan Image

1. Prepare a floor plan image:
   - Use building blueprints
   - Create a simple diagram
   - Use any image showing the layout
2. Upload the image when creating the floor plan
3. Set the scale/dimensions

---

## 6. Map Devices to Locations

### 6.1 Add Device to Floor Plan

1. Open your floor plan
2. Click **Add Device** or use the device placement tool
3. Select a device from the list
4. Click on the floor plan image where the device is located
5. The device will be placed at that location

📸 **[Screenshot: Placing Device on Floor Plan]**

### 6.2 Position Devices

1. Drag devices to their correct locations
2. Adjust positions as needed
3. Add labels or annotations if desired

### 6.3 Configure Device Display

1. Right-click on a device on the floor plan
2. Configure:
   - **Label**: Custom label
   - **Color**: Device color
   - **Icon**: Device icon
   - **Size**: Display size
3. Save changes

---

## 7. Use Floor Plans

### 7.1 View Floor Plans

1. Navigate to **Floor Plans**
2. Select a floor plan to view
3. See all devices mapped to their locations

📸 **[Screenshot: Floor Plan View]**

### 7.2 Navigate from Device

1. Go to a device detail page
2. Look for floor plan information
3. Click to view the device on the floor plan

### 7.3 Search and Filter

1. Use search to find devices on floor plans
2. Filter by device type, role, or status
3. Highlight specific devices

### 7.4 Export Floor Plans

1. Export floor plans as images
2. Share with team members
3. Use in documentation

---

## 8. Wrap-Up

Congratulations! You have successfully:
- ✅ Installed the Floorplan plugin
- ✅ Enabled the plugin in configuration
- ✅ Created floor plans for your sites
- ✅ Mapped devices to physical locations
- ✅ Used floor plans for visualization

You now have visual representations of your network infrastructure!

---

## 9. Next Steps

Now that floor plans are set up, proceed to **Part 13: Design Builder Plugin** (the final part!) to:
- Install and configure the Design Builder plugin
- Create designs via Git sync of jobs
- Deploy designs to your network environment

---

*Happy automating! 🚀*

