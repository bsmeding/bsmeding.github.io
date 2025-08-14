---
authors: [bsmeding]
date: 2025-08-10
title: Building a Reusable Network Automation Lab with Containerlab
tags: ["network automation", "containerlab", "lab", "automation", "network", "automation"]
toc: true
layout: single
comments: true
---

# Building Your Reusable Network Automation Lab with Containerlab

*The standard lab topology used in my Nautobot automation series.*

<!-- more -->

---

## 1. Introduction
A consistent lab environment is essential for learning and testing network automation workflows.  
This guide creates a **reusable Containerlab topology** that you can use for all tutorials in the Nautobot automation series.

**Why Containerlab?**
- Runs entirely in Docker.
- Supports Arista, Nokia, and other network OS images.
- Easy to version control and reproduce.
- Simulates realistic multi-vendor network environments.

---

## 2. Lab Topology Overview

**Devices:**
- **2x Access Switches** (`access1`, `access2`) - Arista vEOS
- **1x Distribution/Core Switch** (`dist1`) - Nokia SR Linux
- **1x Router/WAN Edge** (`rtr1`) - Nokia SR Linux
- **1x Management Host** (`mgmt`) - Linux container
- **1x Nautobot Container** (Docker)
- **1x ZTP Server** (Linux container)

**Logical Layout:**
```
           [rtr1]
             |
          [dist1]
          /     \
     [access1] [access2]
     
     [mgmt] [nautobot] [ztp]
```

**Network Segments:**
- **Data Plane**: access1/2 ↔ dist1 ↔ rtr1
- **Management Plane**: All devices on mgmt-net (172.20.20.0/24)

---

## 3. Installing Containerlab

**Prerequisites:**
- Docker & Docker Compose
- At least 8GB RAM
- Containerlab installed

For detailed installation instructions, see the [ContainerLab Installation Guide](/blog/posts/tools/containerlab.html).

Quick install:
```bash
curl -sL https://get.containerlab.dev | bash
containerlab version
```

---

## 4. Getting Network OS Images

For comprehensive instructions on downloading and importing network OS images, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Free Downloadable Images:**
- **Arista vEOS-lab** - Available from Arista's website
- **Nokia SR Linux** - Available from Nokia's website
- **Juniper vQFX** (optional) - Available from Juniper's website

> ⚠️ Licensing applies. Obtain images legally from vendor websites.

**Quick Download and Import:**
```bash
# Arista vEOS-lab
docker import vEOS-lab-4.28.0F.tar.xz arista/veos:4.28.0F

# Nokia SR Linux (from GitHub Container Registry)
docker pull ghcr.io/nokia/srlinux
```

---

## 5. Containerlab Topology File

Save as `lab-topology.clab.yml`:

```yaml
name: nautobot-lab
topology:
  nodes:
    access1:
      kind: ceos
      image: ceos:4.34.2F
      mgmt_ipv4: 172.20.20.11
    access2:
      kind: ceos
      image: ceos:4.34.2F
      mgmt_ipv4: 172.20.20.12
    dist1:
      kind: srl
      image: ghcr.io/nokia/srlinux
      mgmt_ipv4: 172.20.20.21
    rtr1:
      kind: srl
      image: ghcr.io/nokia/srlinux
      mgmt_ipv4: 172.20.20.22
    ztp:
      kind: linux
      image: alpine
      mgmt_ipv4: 172.20.20.31
    mgmt:
      kind: linux
      image: alpine
      mgmt_ipv4: 172.20.20.32
  links:
    - endpoints: ["access1:eth1", "dist1:ethernet-1/1"]
    - endpoints: ["access2:eth1", "dist1:ethernet-1/2"]
    - endpoints: ["dist1:ethernet-1/3", "rtr1:ethernet-1/1"]

mgmt:
  network: mgmt-net
  ipv4-subnet: 172.20.20.0/24
```

---

## 6. Deploying the Lab

```bash
containerlab deploy -t lab-topology.clab.yml
```

Verify:
```bash
containerlab inspect
```

---

## 7. Configuring Management Access

- Assign management IPs to devices.
- Enable SSH on devices.
- Use NAT/port-forwarding if needed.

**Example (Arista EOS):**
```bash
configure
interface Management1
   ip address 172.20.20.11/24
   no shutdown
exit
management ssh
   no shutdown
exit
```

**Example (Nokia SR Linux):**
```bash
enter candidate
/system network-instance mgmt interface ethernet-1/1
    ipv4 address 172.20.20.12/24
    admin-state enable
commit stay
```

---

## 8. Optional: Nautobot & ZTP Integration

Example `docker-compose.yml`:

```yaml
version: "3.8"
services:
  nautobot:
    # image: networktocode/nautobot:stable
    # image: bsmeding/nautobot:2.1.9-py3.11
    container_name: nautobot
    image: &shared_image bsmeding/nautobot:2.4
    depends_on:
      - postgres
      - redis
    networks:
      - mgmt-net
    ports:
      - "8080:8080"  # Exposes Nautobot on localhost:8080
    environment:
      - NAUTOBOT_DEBUG=True
      - NAUTOBOT_DJANGO_EXTENSIONS_ENABLED=False
      - NAUTOBOT_DJANGO_TOOLBAR_ENABLED=False
      - NAUTOBOT_HIDE_RESTRICTED_UI=True
      - NAUTOBOT_LOG_LEVEL=WARNING
      - NAUTOBOT_METRICS_ENABLED=False
      - NAUTOBOT_NAPALM_TIMEOUT=5
      - NAUTOBOT_MAX_PAGE_SIZE=0
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_ALLOWED_HOSTS=*
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379
      - NAUTOBOT_SUPERUSER_NAME=admin
      - NAUTOBOT_SUPERUSER_PASSWORD=admin
      - NAUTOBOT_SUPERUSER_API_TOKEN=1234567890abcde0987654321
      - NAUTOBOT_CREATE_SUPERUSER=true
      - NAUTOBOT_INSTALLATION_METRICS_ENABLED=false
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_SECURE_HSTS_SECONDS=3600
      - NAUTOBOT_SECURE_SSL_REDIRECT=True
      - NAUTOBOT_SESSION_COOKIE_SECURE=True
      - NAUTOBOT_CSRF_COOKIE_SECURE=True
    volumes:
      - nautobot_config:/opt/nautobot/
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
    container_name: postgres
    command:
      - "-c"
      - "max_connections=1000"
    networks:
      - mgmt-net
    healthcheck:
      test: "pg_isready --username=$$POSTGRES_USER --dbname=$$POSTGRES_DB"
      interval: "10s"
      timeout: "5s"
      retries: 10    
    environment:
      POSTGRES_USER: nautobot
      POSTGRES_PASSWORD: nautobotpassword
      POSTGRES_DB: nautobot
    volumes:
      # - ./mapped_folders/postgres-data:/var/lib/postgresql/data             # Not possible with compose due to folder permissions, use docker volume instead  
      - "postgres_data:/var/lib/postgresql/data"
    restart: unless-stopped

  redis:
    image: redis:6
    container_name: redis
    networks:
      - mgmt-net
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery-beat:
    container_name: nautobot_celery_beat
    image: *shared_image
    command: nautobot-server celery beat
    networks:
      - mgmt-net
    depends_on:
      nautobot:
        condition: "service_healthy"
    networks:
      - mgmt-net
    volumes:
      - nautobot_config:/opt/nautobot/
    environment:
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py

  celery-worker-1:
    image: *shared_image
    container_name: nautobot_celery_worker_1
    command: nautobot-server celery worker --concurrency=4
    depends_on:
      nautobot:
        condition: "service_healthy"
    networks:
      - mgmt-net
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
      - nautobot_config:/opt/nautobot/
    environment:
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py

  ztp:
    image: alpine:latest
    networks:
      - mgmt-net

volumes:
  nautobot_config: {}
  postgres_data: {}
  redis_data: {}

networks:
  mgmt-net:
    external: true
```

---

## 9. Saving & Reusing the Lab

Save `lab-topology.clab.yml` to GitHub.

**Reset Script:**
```bash
#!/bin/bash
containerlab destroy -t lab-topology.clab.yml
containerlab deploy -t lab-topology.clab.yml
```

Make executable:
```bash
chmod +x reset.sh
```

---

## 10. Next Steps

Your lab is ready.  
Continue to **Part 1** of the Nautobot series to start using this lab for inventory, compliance, and automation workflows.
