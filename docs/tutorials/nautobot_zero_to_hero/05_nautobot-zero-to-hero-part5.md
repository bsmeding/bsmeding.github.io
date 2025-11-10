---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 5: Add Device Config from Jobs
tags: ["network automation", "nautobot", "jobs", "configuration management"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 5: Add Device Config from Jobs
## Sync Device Configurations with Custom Jobs
*Use Jobs from the nzth_demo_jobs repository to manage device configurations.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 5: Add Device Config from Jobs](#nautobot-zero-to-hero--part-5-add-device-config-from-jobs)
  - [Sync Device Configurations with Custom Jobs](#sync-device-configurations-with-custom-jobs)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Add nzth_demo_jobs Repository](#3-add-nzth_demo_jobs-repository)
  - [4. Review Available Jobs](#4-review-available-jobs)
  - [5. Run Configuration Collection Job](#5-run-configuration-collection-job)
  - [6. Verify Configuration Storage](#6-verify-configuration-storage)
  - [7. Wrap-Up](#7-wrap-up)
  - [8. Next Steps](#8-next-steps)

---

## 1. Introduction

In this part, we'll sync with the [nzth_demo_jobs](https://github.com/bsmeding/nzth_demo_jobs) repository to access pre-built Jobs for managing device configurations. These Jobs will help us collect, store, and manage device configurations in Nautobot.

We'll:
1. Add the nzth_demo_jobs repository to Nautobot
2. Review available Jobs
3. Run Jobs to collect device configurations
4. Verify configurations are stored correctly

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites

- Completed [Part 4: Device Discovery & Onboarding](/tutorials/nautobot_zero_to_hero/05_nautobot-zero-to-hero-part4/)
- Devices are onboarded in Nautobot
- Devices are reachable via SSH
- Nautobot has Git repository integration configured

---

## 3. Add nzth_demo_jobs Repository

### 3.1 Add Repository to Nautobot

1. Navigate to **Apps → Git Repositories**
2. Click **Add** to create a new repository
3. Configure the repository:
   - **Name:** `nzth_demo_jobs`
   - **Source URL:** `https://github.com/bsmeding/nzth_demo_jobs.git`
   - **Branch:** `main`
   - **Secrets Group:** (leave empty for public repo)
   - Enable **Jobs** checkbox
4. Click **Save and Sync Now**

📸 **[Screenshot: Git Repository Configuration]**

### 3.2 Verify Sync

After syncing, verify the Jobs are available:
1. Navigate to **Jobs → Jobs**
2. You should see Jobs from the nzth_demo_jobs repository

📸 **[Screenshot: Available Jobs from Repository]**

---

## 4. Review Available Jobs

The nzth_demo_jobs repository contains various Jobs for configuration management. Common Jobs include:

### 4.1 Configuration Collection Jobs

- **Collect Running Config**: Retrieves running configuration from devices
- **Collect Startup Config**: Retrieves startup configuration from devices
- **Sync Config to Git**: Stores configurations in Git repositories

### 4.2 Configuration Management Jobs

- **Compare Configs**: Compares running vs startup configurations
- **Validate Config**: Validates device configurations
- **Deploy Config**: Deploys configurations to devices

### 4.3 Review Job Details

Click on a Job to view its details:
- **Description**: What the Job does
- **Parameters**: Required inputs
- **Code**: Review the Job code if needed

📸 **[Screenshot: Job Details]**

---

## 5. Run Configuration Collection Job

### 5.1 Select a Device

1. Navigate to **Devices → Devices**
2. Select a device you want to collect configuration from
3. Note the device name and ensure it's reachable

### 5.2 Run Collection Job

1. Navigate to **Jobs → Jobs**
2. Find a configuration collection Job (e.g., "Collect Running Config")
3. Click **Run Job**
4. Select parameters:
   - **Device**: Choose your device
   - **Credentials**: Select or enter SSH credentials
   - **Output Format**: Choose how to store the config
5. Click **Run Job**

📸 **[Screenshot: Running Configuration Collection Job]**

### 5.3 Review Job Results

After the Job completes:
1. View the job result
2. Check the output for the collected configuration
3. Verify any errors or warnings

📸 **[Screenshot: Job Result with Configuration]**

---

## 6. Verify Configuration Storage

### 6.1 Check Device Configurations

1. Navigate to **Devices → Devices**
2. Click on your device
3. Look for configuration-related fields or tabs
4. Verify the configuration is stored

### 6.2 Check Git Repository

If the Job stores configs in Git:
1. Navigate to **Apps → Git Repositories**
2. Check the repository that stores configurations
3. Verify files were created/updated

### 6.3 Review Configuration Content

1. Access the stored configuration
2. Verify it matches the device's actual configuration
3. Check formatting and completeness

📸 **[Screenshot: Stored Configuration]**

---

## 7. Wrap-Up

Congratulations! You have successfully:
- ✅ Added the nzth_demo_jobs repository to Nautobot
- ✅ Synced Jobs from the repository
- ✅ Reviewed available configuration management Jobs
- ✅ Run Jobs to collect device configurations
- ✅ Verified configurations are stored correctly

You now have Jobs available to manage device configurations throughout the series!

---

## 8. Next Steps

Now that you can collect device configurations, proceed to **Part 6: Enable Golden Config Plugin** to:
- Install and configure the Golden Config plugin
- Fork required repositories
- Create golden configurations for devices

---

*Happy automating! 🚀*
