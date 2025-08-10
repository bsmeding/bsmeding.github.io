---
authors: [bsmeding]
date: 2025-08-09
title: Nautobot in Action – Part 1
tags: ["network automation", "device onboarding", "nautobot", "discovery"]
toc: true
layout: single
comments: true
---

# Nautobot in Action – Part 1
## Nautobot as Your Single Source of Truth (SSoT)
*From zero to a Git-integrated Nautobot environment.*
<!-- more -->

---

## Index
- [Nautobot in Action – Part 1](#nautobot-in-action--part-1)
  - [Nautobot as Your Single Source of Truth (SSoT)](#nautobot-as-your-single-source-of-truth-ssot)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Deploy Nautobot](#3-deploy-nautobot)
  - [4. Create Git Repository](#4-create-git-repository)
    - [Security Note](#security-note)
    - [4.1 Create the Repository](#41-create-the-repository)
    - [4.2 Create Repo Structure](#42-create-repo-structure)
    - [4.3 Create a Personal Access Token (PAT)](#43-create-a-personal-access-token-pat)
    - [4.4 Store Token in Nautobot](#44-store-token-in-nautobot)
  - [5. Create Base Inventory](#5-create-base-inventory)
    - [Create Location](#create-location)
    - [Add Platforms](#add-platforms)
    - [Add Roles](#add-roles)
    - [Add Devices](#add-devices)
  - [6. Store First Template in Git](#6-store-first-template-in-git)
  - [7. Test Template Rendering in Nautobot](#7-test-template-rendering-in-nautobot)
  - [8. Validation Script](#8-validation-script)
  - [9. Wrap-Up](#9-wrap-up)
  - [10. Next Steps](#10-next-steps)

---

## 1. Introduction
In this first part of the series, we’ll set up Nautobot as the **Single Source of Truth (SSoT)** for our lab network.

We’ll:
1. Deploy Nautobot.
2. Connect it to our Git repository.
3. Create the base inventory (sites, devices, platforms, roles).
4. Store our first Jinja2 template in Git.

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites
- Containerlab lab from the separate setup blog.
- GitHub or GitLab repository (private if external).
- Docker & Docker Compose installed.

---

## 3. Deploy Nautobot

**docker-compose.yml**
```yaml
version: "3.8"
services:
  nautobot:
    image: networktocode/nautobot:latest
    ports:
      - "8080:8080"
    environment:
      - NAUTOBOT_CREATE_SUPERUSER=true
      - NAUTOBOT_SUPERUSER_USERNAME=admin
      - NAUTOBOT_SUPERUSER_PASSWORD=admin
      - NAUTOBOT_SUPERUSER_EMAIL=admin@example.com
    volumes:
      - nautobot_data:/opt/nautobot
volumes:
  nautobot_data:
```

Run:
```bash
docker compose up -d
```

Access: [http://localhost:8080](http://localhost:8080)  
User: `admin` / Pass: `admin`

📸 **[Screenshot: Nautobot Login Page Placeholder]**

---

## 4. Create Git Repository

### Security Note
If you are not using internally hosted Git, create the repository as **private** to avoid exposing sensitive data.

### 4.1 Create the Repository
1. On GitHub/GitLab: **New Repository**
2. Name: `nautobot-configs`
3. Visibility: **Private**

### 4.2 Create Repo Structure
```bash
git clone git@github.com:yourusername/nautobot-configs.git
cd nautobot-configs
mkdir templates backups jobs compliance
git add .
git commit -m "Initial repo structure"
git push origin main
```

### 4.3 Create a Personal Access Token (PAT)
- **GitHub:** Settings → Developer settings → Personal access tokens → Tokens (classic) → `repo` scope.
- **GitLab:** User Settings → Access Tokens → `read_repository` scope.

### 4.4 Store Token in Nautobot
In Nautobot → Apps → Git Repositories → Add:
- Name: `nautobot-configs`
- URL: `https://github.com/yourusername/nautobot-configs.git`
- Branch: `main`
- Username: your Git username
- Token: PAT
- Enable:
  - Templates
  - Jobs
  - Config Contexts
  - Golden Config Templates

📸 **[Screenshot: Git Repo Sync Success Placeholder]**

---

## 5. Create Base Inventory

### Create Location
- Organization → Locations → Add → Name: `Lab-Site`

📸 **[Screenshot: New Location Placeholder]**

### Add Platforms
- Cisco IOS XE
- Arista EOS

### Add Roles
- access-switch
- distribution-switch
- router

### Add Devices
Match your lab topology.

---

## 6. Store First Template in Git
`templates/interface_basic.j2`:
```jinja2
!
interface {{ interface_name }}
 description {{ description }}
 {% if enabled %}
 no shutdown
 {% else %}
 shutdown
 {% endif %}
!
```

Commit:
```bash
git add templates/interface_basic.j2
git commit -m "Add basic interface template"
git push origin main
```

---

## 7. Test Template Rendering in Nautobot
Render the template in:
- Config Contexts
- Golden Config Intended Config

📸 **[Screenshot: Rendered Template Placeholder]**

---

## 8. Validation Script
`jobs/list_devices.py`:
```python
from nautobot.extras.jobs import Job, register_jobs
from nautobot.dcim.models import Device

class ListDevices(Job):
    class Meta:
        name = "List All Devices"
        description = "Prints all devices in the inventory."

    def run(self):
        for device in Device.objects.all():
            self.log_info(f"{device.name} ({device.role}) - {device.platform}")

register_jobs(ListDevices)
```

Commit:
```bash
git add jobs/list_devices.py
git commit -m "Add List Devices job"
git push origin main
```

📸 **[Screenshot: Job in Nautobot Placeholder]**

---

## 9. Wrap-Up
You have:
- Deployed Nautobot
- Linked it to Git
- Created base inventory
- Added a Jinja2 template
- Created your first job

---

## 10. Next Steps
Go to **Part 2** – Onboarding Brownfield Devices with the Device Onboarding App.
