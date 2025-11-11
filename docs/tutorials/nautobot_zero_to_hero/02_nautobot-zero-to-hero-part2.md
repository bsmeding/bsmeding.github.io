---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 2: Getting Started with Nautobot
tags: ["network automation", "nautobot", "jobs", "demo environment"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 2: Getting Started with Nautobot
## What Can Nautobot Do?
*Explore Nautobot's capabilities and deploy a demo environment using Jobs.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 2: Getting Started with Nautobot](#nautobot-zero-to-hero--part-2-getting-started-with-nautobot)
  - [What Can Nautobot Do?](#what-can-nautobot-do)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Understanding Nautobot's Capabilities](#3-understanding-nautobots-capabilities)
  - [4. Nautobot Globals - Foundation Data](#4-nautobot-globals---foundation-data)
    - [4.1 Tenant](#41-tenant)
    - [4.2 Location Types](#42-location-types)
    - [4.3 Locations](#43-locations)
    - [4.4 Manufacturers](#44-manufacturers)
    - [4.5 Device Types](#45-device-types)
    - [4.6 Platforms](#46-platforms)
    - [4.7 Tags](#47-tags)
    - [4.8 Roles](#48-roles)
    - [4.9 Status](#49-status)
    - [4.10 IPAM (IP Address Management)](#410-ipam-ip-address-management)
  - [5. Access Jobs from the Repository](#5-access-jobs-from-the-repository)
  - [6. Run the Pre-Flight Job](#6-run-the-pre-flight-job)
  - [7. Verify Demo Environment](#7-verify-demo-environment)
  - [8. Wrap-Up](#8-wrap-up)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction

In this part, we'll explore what Nautobot can do and use Jobs from the [nautobot_zero_to_hero](https://github.com/bsmeding/nautobot_zero_to_hero) repository to quickly set up a demo environment. We'll run the pre-flight job that automatically creates a region, site, and device to get you started.

We'll:

1. Understand Nautobot's core capabilities
2. Learn about Nautobot Globals - the foundation data needed before adding sites and devices
3. Access Jobs from the repository
4. Run the pre-flight job to create initial data
5. Verify the demo environment is set up correctly

> **Estimated Time:** ~1 hour

---

## 2. Prerequisites

- Completed [Part 1: Install Nautobot](/tutorials/nautobot_zero_to_hero/02_nautobot-zero-to-hero-part1/)
- Nautobot is running and accessible
- Access to the nautobot_zero_to_hero repository

---

## 3. Understanding Nautobot's Capabilities

Nautobot is a Network Source of Truth (SSoT) platform that provides:

### **Core Features**
- **Device Inventory Management**: Track all network devices, their locations, and relationships
- **IP Address Management (IPAM)**: Manage IP addresses, prefixes, and VLANs
- **Cable Management**: Document physical and logical connections
- **Configuration Management**: Store and version control device configurations
- **Jobs Framework**: Run custom Python scripts for automation tasks
- **REST and GraphQL APIs**: Integrate with other tools and systems
- **Plugin Ecosystem**: Extend functionality with plugins

### **What Makes Nautobot Powerful**
- **Single Source of Truth**: One place for all network data
- **Git Integration**: Version control for configurations and templates
- **Extensibility**: Custom Jobs, plugins, and integrations
- **API-First Design**: Programmatic access to all data
- **Webhooks**: Event-driven automation

---

## 4. Nautobot Globals - Foundation Data

Before you can add sites and devices to Nautobot, you need to set up the foundational data structures, also known as "Globals." These are the building blocks that define how your network is organized and categorized. Understanding these concepts is crucial for effectively using Nautobot.

> **💡 Tip:** The pre-flight job from the nautobot_zero_to_hero repository will create many of these automatically. However, understanding what they are and how they work will help you customize and extend your Nautobot instance.

### 4.1 Tenant

**Tenants** represent organizations or departments that own or use network resources. They provide logical separation and can be used for multi-tenancy scenarios.

**Use Cases:**
- Separate network resources by business unit
- Track ownership of devices and IP addresses
- Apply tenant-specific policies and access controls

**Navigation:** Organization → Tenants

**Example:**
- Create a tenant named "Engineering" for the engineering department
- Create a tenant named "Sales" for the sales department

---

### 4.2 Location Types

**Location Types** define the hierarchy of physical locations in your network. They create a tree structure that represents your organizational geography.

**Common Location Types:**
- **Country**: Top-level geographic location
- **Region**: Large geographic area (e.g., "North America", "Europe")
- **Site**: Physical location where network equipment resides (e.g., data center, office building)
- **Room**: Specific room within a site (e.g., "Server Room A", "Network Closet")
- **Floor**: Floor level within a building

**Navigation:** Organization → Location Types

**Example Setup:**

1. **Add Location Type: Country**
   - Navigate to **Organization → Location Types**
   - Click **Add**
   - Name: `Country`
   - Description: `Top-level geographic location`
   - Click **Create**

2. **Add Location Type: Region**
   - Name: `Region`
   - Description: `Large geographic area within a country`
   - Parent: `Country` (optional, but recommended for hierarchy)
   - Click **Create**

3. **Add Location Type: Site**
   - Name: `Site`
   - Description: `Physical location with network equipment`
   - Parent: `Region`
   - **Allowed Items**: Enable checkboxes for items that can exist at this level:
     - ✅ Devices
     - ✅ Racks
     - ✅ Power panels
     - ✅ Circuits
     - ✅ Prefixes
     - ✅ VLANs
   - Click **Create**

📸 **[Screenshot: Location Type Configuration with Allowed Items]**

**Why Location Types Matter:**
- They enforce a logical hierarchy for your network locations
- They control what types of objects can be placed at each level
- They enable better organization and filtering of network resources

---

### 4.3 Locations

**Locations** are the actual instances of location types. They represent real places in your network hierarchy.

**Navigation:** Organization → Locations

**Example:**
- Create a location of type "Country" named "United States"
- Create a location of type "Region" named "West Coast" under "United States"
- Create a location of type "Site" named "San Francisco Data Center" under "West Coast"

📸 **[Screenshot: Location Hierarchy Tree]**

---

### 4.4 Manufacturers

**Manufacturers** represent the companies that produce network equipment (e.g., Cisco, Arista, Juniper).

**Navigation:** Devices → Manufacturers

**Why It's Important:**
- Device types are associated with manufacturers
- Helps organize and filter devices by vendor
- Required before creating device types

**Example:**
- Create manufacturer: `Cisco`
- Create manufacturer: `Arista`
- Create manufacturer: `Juniper`

---

### 4.5 Device Types

**Device Types** define the model and specifications of network devices. They include information about:
- Physical dimensions (height in rack units)
- Interfaces and their types
- Power consumption
- Console ports
- Management interfaces

**Navigation:** Devices → Device Types

**Why It's Important:**
- Every device in Nautobot must have a device type
- Device types define what interfaces and components a device has
- They enable proper inventory tracking and automation

**💡 Using the Device Type Library:**

Instead of manually creating device types, you can use the [nautobot_devicetype_library](https://github.com/bsmeding/nautobot_devicetype_library) repository, which contains thousands of pre-defined device types for various manufacturers.

**To use the device type library:**

1. **Add the Repository to Nautobot:**
   - Navigate to **Apps → Git Repositories**
   - Click **Add**
   - Configure:
     - **Name:** `nautobot_devicetype_library`
     - **Source URL:** `https://github.com/bsmeding/nautobot_devicetype_library.git`
     - **Branch:** `main`
     - Enable **Jobs** checkbox
   - Click **Save and Sync Now**

2. **Enable the Device Type Import Job:**
   - Navigate to **Jobs → Jobs**
   - Find the job: `Device Type Import` or `Import Device Types`
   - Click on the job to view details

3. **Run the Job:**
   - Click **Run Job**
   - The job will sync device types from the repository
   - This may take a few minutes depending on the number of device types

📸 **[Screenshot: Device Type Import Job]**

**Benefits:**
- Thousands of device types ready to use
- No manual data entry required
- Regularly updated with new device models
- Includes interface definitions and specifications

---

### 4.6 Platforms

**Platforms** define the operating system and software running on devices. They link device types to automation drivers and capabilities.

**Navigation:** Devices → Platforms

**Key Components:**

1. **Network Driver**: Specifies which Python library to use for device communication
   - Examples: `netmiko`, `napalm`, `scrapli`
   - Used for SSH/Telnet connections

2. **NAPALM Driver**: If using NAPALM for device automation
   - Examples: `ios`, `eos`, `junos`, `nxos`
   - Enables configuration management and data collection

**Example Platform Configuration:**
- **Name:** `Cisco IOS`
- **Manufacturer:** `Cisco`
- **Network Driver:** `netmiko`
- **NAPALM Driver:** `ios`
- **Description:** `Cisco IOS platform for routers and switches`

📸 **[Screenshot: Platform Configuration with Drivers]**

**Why Platforms Matter:**
- They enable automation tools to connect to devices
- They determine which drivers and libraries are used
- They link device types to automation capabilities

---

### 4.7 Tags

**Tags** are flexible labels that can be applied to any object in Nautobot. They enable flexible categorization and filtering.

**Navigation:** Extensibility → Tags

**Use Cases:**
- Mark devices as "production" or "lab"
- Tag IP addresses as "DMZ" or "internal"
- Label circuits as "critical" or "redundant"
- Filter and search across different object types

**Example Tags:**
- `production`
- `lab`
- `critical`
- `redundant`
- `dmz`
- `internal`

📸 **[Screenshot: Tags List]**

---

### 4.8 Roles

**Roles** define the function or purpose of network objects. They provide semantic meaning to devices, IP addresses, VLANs, and other objects.

**Navigation:** Organization → Roles

**Common Device Roles:**
- `core-router`
- `distribution-switch`
- `access-switch`
- `firewall`
- `load-balancer`
- `wireless-controller`

**Common IP Address Roles:**
- `loopback`
- `management`
- `point-to-point`
- `anycast`

**Why Roles Matter:**
- They provide semantic meaning to network objects
- They enable filtering and searching by function
- They help organize and understand network topology

---

### 4.9 Status

**Status** represents the operational state of objects in Nautobot. Every object has a status that indicates whether it's active, planned, decommissioned, etc.

**Navigation:** Extensibility → Statuses

**Common Statuses:**
- `Active`: Object is currently in use
- `Planned`: Object is planned but not yet deployed
- `Staged`: Object is staged for deployment
- `Decommissioning`: Object is being removed
- `Offline`: Object is temporarily offline
- `Failed`: Object has failed

**Why Status Matters:**
- Tracks the lifecycle of network objects
- Enables filtering by operational state
- Helps with capacity planning and inventory management

---

### 4.10 IPAM (IP Address Management)

IPAM components are essential for managing network addressing:

#### **Containers**

**Containers** are large IP address blocks (typically /8, /16, or /12) that contain smaller prefixes.

**Navigation:** IPAM → Prefixes → Add Container

**Example:**
- Container: `10.0.0.0/8` (private RFC 1918 space)
- Container: `172.16.0.0/12` (private RFC 1918 space)

#### **Prefixes**

**Prefixes** are IP address ranges (subnets) that can contain other prefixes or individual IP addresses.

**Navigation:** IPAM → Prefixes

**Example:**
- Prefix: `10.1.0.0/16` (under container `10.0.0.0/8`)
- Prefix: `10.1.1.0/24` (under prefix `10.1.0.0/16`)

**Use Cases:**
- Organize IP address space hierarchically
- Track subnet utilization
- Assign prefixes to sites or tenants

#### **VLANs**

**VLANs** represent virtual LANs in your network. They can be associated with sites and prefixes.

**Navigation:** IPAM → VLANs

**Example:**
- VLAN ID: `100`
- Name: `Production`
- Site: `San Francisco Data Center`
- Prefix: `10.1.1.0/24`

📸 **[Screenshot: VLAN Configuration]**

**Why IPAM Matters:**
- Centralized IP address management
- Prevents IP address conflicts
- Tracks utilization and availability
- Links addressing to network topology

---

## 5. Access Jobs from the Repository

The [nautobot_zero_to_hero](https://github.com/bsmeding/nautobot_zero_to_hero) repository contains pre-built Jobs that help you get started quickly. These Jobs will automatically create the foundation data (Globals) we discussed in the previous section, saving you time and ensuring consistency.

**The Pre-flight Lab Setup Job** in this repository will create:
- Location type hierarchy (Region, Site, Building, Floor, Room)
- A region named "NetDevOps"
- A site named "netdevops.it_lab"
- Manufacturers (Cisco, Arista, Juniper, Nokia)
- Device types for common network devices
- Platforms with proper driver mappings (network driver and NAPALM driver)
- Roles (core-router, distribution-switch, access-switch, etc.)
- Tags and statuses
- Management subnet (172.20.20.0/24) with prefixes
- VLANs for the lab environment
- Sample devices matching the Containerlab topology

Let's set up Jobs in Nautobot:

### 5.1 Add the Repository to Nautobot

1. In Nautobot, navigate to **Apps → Git Repositories**
2. Click **Add** to create a new repository
3. Configure the repository:
   - **Name:** `nautobot_zero_to_hero`
   - **Source URL:** `https://github.com/bsmeding/nautobot_zero_to_hero.git`
   - **Branch:** `main`
   - **Secrets Group:** (leave empty for public repo)
   - Enable **Jobs** checkbox
4. Click **Save and Sync Now**

📸 **[Screenshot: Git Repository Configuration]**

After syncing, the Jobs from the repository will be available in Nautobot.

### 5.2 Verify Jobs are Available

1. Navigate to **Jobs → Jobs**
2. You should see Jobs from the repository, including the pre-flight job

📸 **[Screenshot: Available Jobs List]**

---

## 6. Run the Pre-Flight Job

The **pre-flight job** from the nautobot_zero_to_hero repository will automatically create a complete demo environment, including all the foundation data (Globals) we discussed earlier. This job will:

- Create location types (if needed)
- Create a region
- Create a site
- Create manufacturers
- Create device types
- Create platforms with proper driver mappings
- Create roles and statuses
- Create a device with proper platform and role

This is much faster than manually creating all these objects!

### 6.1 Locate the Pre-Flight Job

1. Navigate to **Jobs → Jobs**
2. Find the job named **"Pre-flight Lab Setup"** (under the "LAB Setup" category)
3. Click on the job name to open it

📸 **[Screenshot: Pre-Flight Job Details]**

### 6.2 Run the Job

1. Click **Run Job** button
2. Review the job parameters (if any)
3. Click **Run Job** to execute

📸 **[Screenshot: Running the Pre-Flight Job]**

The job will run and create all the necessary foundation data. This may take a minute or two.

### 6.3 Review Job Results

After the job completes:
1. View the job result to see what was created
2. Check the logs for any warnings or errors
3. Verify the output shows successful creation of:
   - Location types
   - Region
   - Site
   - Manufacturers
   - Device types
   - Platforms
   - Roles
   - Device

📸 **[Screenshot: Job Result Output]**

---

## 7. Verify Demo Environment

Let's verify that the pre-flight job created all the expected foundation data:

### 7.1 Check Location Types

1. Navigate to **Organization → Location Types**
2. You should see location types created by the job (e.g., Region, Site)

📸 **[Screenshot: Location Types List]**

### 7.2 Check Region

1. Navigate to **Organization → Regions**
2. You should see a region created by the job

📸 **[Screenshot: Regions List]**

### 7.3 Check Site

1. Navigate to **Organization → Sites**
2. You should see a site created by the job
3. Click on the site to view its details and verify it's associated with the region

📸 **[Screenshot: Sites List]**
📸 **[Screenshot: Site Details]**

### 7.4 Check Manufacturers

1. Navigate to **Devices → Manufacturers**
2. You should see manufacturers created by the job (e.g., Cisco, Arista)

📸 **[Screenshot: Manufacturers List]**

### 7.5 Check Device Types

1. Navigate to **Devices → Device Types**
2. You should see device types created by the job

📸 **[Screenshot: Device Types List]**

### 7.6 Check Platforms

1. Navigate to **Devices → Platforms**
2. You should see platforms created by the job with proper driver mappings
3. Click on a platform to verify network driver and NAPALM driver settings

📸 **[Screenshot: Platforms List]**
📸 **[Screenshot: Platform Details with Drivers]**

### 7.7 Check Roles

1. Navigate to **Organization → Roles**
2. You should see roles created by the job (e.g., core-router, access-switch)

📸 **[Screenshot: Roles List]**

### 7.8 Check Device

1. Navigate to **Devices → Devices**
2. You should see a device created by the job
3. Click on the device to view its details:
   - Verify it has a device type
   - Verify it has a platform
   - Verify it has a role
   - Verify it's assigned to the site

📸 **[Screenshot: Devices List]**
📸 **[Screenshot: Device Details]**

---

## 8. Wrap-Up

Congratulations! You have successfully:
- ✅ Explored Nautobot's core capabilities
- ✅ Learned about Nautobot Globals - the foundation data structures
- ✅ Understood the importance of location types, manufacturers, device types, platforms, roles, and statuses
- ✅ Added the nautobot_zero_to_hero repository to Nautobot
- ✅ Synced Jobs from the repository
- ✅ Run the pre-flight job to create initial data
- ✅ Verified the demo environment is set up with all foundation data

You now have a working Nautobot instance with:
- Complete foundation data (Globals) ready for use
- A region and site structure
- Manufacturers, device types, and platforms configured
- A demo device ready for further configuration
- Understanding of how Nautobot organizes network data

This foundation will support all future network automation tasks in the series.

---

## 9. Next Steps

Now that you have Nautobot set up with initial data, proceed to **Part 3: Deploy Network with Containerlab** to:
- Set up a containerlab network topology
- Configure multi-vendor network devices
- Prepare your lab environment for automation

---

*Happy automating! 🚀*
