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
  - [4. Access Jobs from the Repository](#4-access-jobs-from-the-repository)
  - [5. Run the Pre-Flight Job](#5-run-the-pre-flight-job)
  - [6. Verify Demo Environment](#6-verify-demo-environment)
  - [7. Wrap-Up](#7-wrap-up)
  - [8. Next Steps](#8-next-steps)

---

## 1. Introduction

In this part, we'll explore what Nautobot can do and use Jobs from the [nautobot_zero_to_hero](https://github.com/bsmeding/nautobot_zero_to_hero) repository to quickly set up a demo environment. We'll run the pre-flight job that automatically creates a region, site, and device to get you started.

We'll:
1. Understand Nautobot's core capabilities
2. Access Jobs from the repository
3. Run the pre-flight job to create initial data
4. Verify the demo environment is set up correctly

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

## 4. Access Jobs from the Repository

The nautobot_zero_to_hero repository contains pre-built Jobs that help you get started quickly. Let's set up Jobs in Nautobot:

### 4.1 Add the Repository to Nautobot

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

### 4.2 Verify Jobs are Available

1. Navigate to **Jobs → Jobs**
2. You should see Jobs from the repository, including the pre-flight job

📸 **[Screenshot: Available Jobs List]**

---

## 5. Run the Pre-Flight Job

The pre-flight job creates initial data structures in Nautobot:
- A region
- A site
- A device with proper platform and role

### 5.1 Locate the Pre-Flight Job

1. Navigate to **Jobs → Jobs**
2. Find the job named something like "Pre-Flight Setup" or "Create Demo Environment"
3. Click on the job name to open it

📸 **[Screenshot: Pre-Flight Job Details]**

### 5.2 Run the Job

1. Click **Run Job** button
2. Review the job parameters (if any)
3. Click **Run Job** to execute

📸 **[Screenshot: Running the Pre-Flight Job]**

### 5.3 Review Job Results

After the job completes:
1. View the job result to see what was created
2. Check the logs for any warnings or errors
3. Verify the output shows successful creation

📸 **[Screenshot: Job Result Output]**

---

## 6. Verify Demo Environment

Let's verify that the pre-flight job created the expected data:

### 6.1 Check Region

1. Navigate to **Organization → Regions**
2. You should see a region created by the job

📸 **[Screenshot: Regions List]**

### 6.2 Check Site

1. Navigate to **Organization → Sites**
2. You should see a site created by the job

📸 **[Screenshot: Sites List]**

### 6.3 Check Device

1. Navigate to **Devices → Devices**
2. You should see a device created by the job
3. Click on the device to view its details

📸 **[Screenshot: Devices List]**
📸 **[Screenshot: Device Details]**

---

## 7. Wrap-Up

Congratulations! You have successfully:
- ✅ Explored Nautobot's core capabilities
- ✅ Added the nautobot_zero_to_hero repository to Nautobot
- ✅ Synced Jobs from the repository
- ✅ Run the pre-flight job to create initial data
- ✅ Verified the demo environment is set up

You now have a working Nautobot instance with initial data structures ready for further configuration.

---

## 8. Next Steps

Now that you have Nautobot set up with initial data, proceed to **Part 3: Deploy Network with Containerlab** to:
- Set up a containerlab network topology
- Configure multi-vendor network devices
- Prepare your lab environment for automation

---

*Happy automating! 🚀*
