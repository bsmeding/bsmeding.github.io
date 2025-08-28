---
authors: [bsmeding]
date: 2025-09-01
title: Nautobot in Action – Part 1
tags: ["network automation", "device onboarding", "nautobot", "discovery"]
toc: true
layout: single
comments: true
draft: true
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
- [Containerlab lab setup](/blog/posts/2025/2025-02-04-building-reusable-network-automation-lab-with-containerlab/)
- [Install Nautobot development environment (Docker, Docker Compose, Nautobot)](/tutorials/install_nautobot_development_in_docker)
- GitHub or GitLab repository (private if external).
- Docker & Docker Compose installed (see Install Nautobot development environment or use Ansible role [bsmeding.docker](/ansible/ansible_role_docker/)).

---

## 3. Deploy Nautobot

**docker-compose.yml**
```yaml
services:
  nautobot:
    container_name: ${NAUTOBOT_CONTAINER_NAME:-customer1-nautobot}
    image: &shared_image bsmeding/nautobot:stable-py3.11
    depends_on:
      - postgres
      - redis
    ports:
      - "${NAUTOBOT_PORT:-8081}:8080"  # Exposes Nautobot on localhost:8081
    environment:
      - NAUTOBOT_DEBUG=True
      - NAUTOBOT_DJANGO_EXTENSIONS_ENABLED=False
      - NAUTOBOT_DJANGO_TOOLBAR_ENABLED=False
      - NAUTOBOT_HIDE_RESTRICTED_UI=True
      - NAUTOBOT_LOG_LEVEL=WARNING
      - NAUTOBOT_METRICS_ENABLED=False
      - NAUTOBOT_NAPALM_TIMEOUT=5
      - NAUTOBOT_MAX_PAGE_SIZE=0
      - NAUTOBOT_DB_HOST=${NAUTOBOT_DB_HOST:-customer1-postgres}
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=${POSTGRES_DB:-nautobot}
      - NAUTOBOT_DB_USER=${POSTGRES_USER:-nautobot}
      - NAUTOBOT_DB_PASSWORD=${POSTGRES_PASSWORD:-nautobotpassword}
      - NAUTOBOT_ALLOWED_HOSTS=*
      - NAUTOBOT_REDIS_HOST=${NAUTOBOT_REDIS_HOST:-customer1-redis}
      - NAUTOBOT_REDIS_PORT=6379
      - NAUTOBOT_SUPERUSER_NAME=${SUPERUSER_NAME:-admin}
      - NAUTOBOT_SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:-admin}
      - NAUTOBOT_SUPERUSER_API_TOKEN=1234567890abcde0987654321
      - NAUTOBOT_CREATE_SUPERUSER=true
      - NAUTOBOT_INSTALLATION_METRICS_ENABLED=false
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py
      - NAUTOBOT_CELERY_BROKER_URL=redis://${NAUTOBOT_REDIS_HOST:-customer1-redis}:6379/0
      - NAUTOBOT_SECURE_HSTS_SECONDS=3600
      - NAUTOBOT_SECURE_SSL_REDIRECT=True
      - NAUTOBOT_SESSION_COOKIE_SECURE=True
      - NAUTOBOT_CSRF_COOKIE_SECURE=True
      - NAUTOBOT_JOBS_ROOT=/opt/nautobot/jobs
    volumes:
      - ./config/nautobot_config.py:/opt/nautobot/nautobot_config.py
      - ./jobs:/opt/nautobot/jobs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
    command: ["nautobot-server", "runserver", "0.0.0.0:8080"]

  postgres:
    image: postgres:13-alpine
    container_name: ${POSTGRES_CONTAINER_NAME:-customer1-postgres}
    command:
      - "-c"
      - "max_connections=1000"
    healthcheck:
      test: "pg_isready --username=$$POSTGRES_USER --dbname=$$POSTGRES_DB"
      interval: "10s"
      timeout: "5s"
      retries: 10    
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-nautobot}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-nautobotpassword}
      POSTGRES_DB: ${POSTGRES_DB:-nautobot}
    volumes:
      - "postgres_data:/var/lib/postgresql/data"
    restart: unless-stopped

  redis:
    image: redis:6
    container_name: ${REDIS_CONTAINER_NAME:-customer1-redis}
    ports:
      - "6380:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery-beat:
    container_name: ${CELERY_BEAT_CONTAINER_NAME:-customer1-nautobot_celery_beat}
    image: *shared_image
    command: nautobot-server celery beat
    depends_on:
      nautobot:
        condition: "service_healthy"
    volumes:
      - ./config/nautobot_config.py:/opt/nautobot/nautobot_config.py
    environment:
      - NAUTOBOT_DB_HOST=${NAUTOBOT_DB_HOST:-customer1-postgres}
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=${POSTGRES_DB:-nautobot}
      - NAUTOBOT_DB_USER=${POSTGRES_USER:-nautobot}
      - NAUTOBOT_DB_PASSWORD=${POSTGRES_PASSWORD:-nautobotpassword}
      - NAUTOBOT_REDIS_HOST=${NAUTOBOT_REDIS_HOST:-customer1-redis}
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://${NAUTOBOT_REDIS_HOST:-customer1-redis}:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py

  celery-worker-1:
    image: *shared_image
    container_name: ${CELERY_WORKER_CONTAINER_NAME:-customer1-nautobot_celery_worker_1}
    command: nautobot-server celery worker --concurrency=4
    depends_on:
      nautobot:
        condition: "service_healthy"
    healthcheck:
      interval: "30s"
      timeout: "10s"
      start_period: "30s"
      retries: 3
      test:
        [
          "CMD",
          "bash",
          "-c",
          "nautobot-server celery inspect ping --destination celery@$$HOSTNAME"  ## $$ because of docker-compose
        ]
    volumes:
      - ./config/nautobot_config.py:/opt/nautobot/nautobot_config.py
      - ./jobs:/opt/nautobot/jobs
    environment:
      - NAUTOBOT_DB_HOST=${NAUTOBOT_DB_HOST:-customer1-postgres}
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=${POSTGRES_DB:-nautobot}
      - NAUTOBOT_DB_USER=${POSTGRES_USER:-nautobot}
      - NAUTOBOT_DB_PASSWORD=${POSTGRES_PASSWORD:-nautobotpassword}
      - NAUTOBOT_REDIS_HOST=${NAUTOBOT_REDIS_HOST:-customer1-redis}
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://${NAUTOBOT_REDIS_HOST:-customer1-redis}:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py
      - NAUTOBOT_JOBS_ROOT=/opt/nautobot/jobs


volumes:
  postgres_data: {}
  redis_data: {}
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
- Nokia SR

### Add Roles
- access-switch
- distribution-switch
- router

### Add Devices
Match your lab topology.

You can also use Design-builder app to pre-flight you Nautobot instance / devices  #TODO! Add 

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
