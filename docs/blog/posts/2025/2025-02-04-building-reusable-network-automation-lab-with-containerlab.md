---
authors: [bsmeding]
date: 2025-02-04
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

```bash
curl -sL https://get.containerlab.dev | bash
containerlab version
```

---

## 4. Getting Network OS Images

**Free Downloadable Images:**
- **Arista vEOS-lab** - Available from Arista's website
- **Nokia SR Linux** - Available from Nokia's website
- **Juniper vQFX** (optional) - Available from Juniper's website

> ⚠️ Licensing applies. Obtain images legally from vendor websites.

**Download and Import:**
```bash
# Arista vEOS-lab
docker import vEOS-lab-4.28.0F.tar.xz arista/veos:4.28.0F

# Nokia SR Linux
docker import srlinux-22.11.1.tar.xz nokia/srlinux:22.11.1
```

---

## 5. Containerlab Topology File

Save as `lab-topology.clab.yml`:

```yaml
name: nautobot-lab
topology:
  nodes:
    access1:
      kind: vr-veos
      image: arista/veos:4.28.0F
    access2:
      kind: vr-veos
      image: arista/veos:4.28.0F
    dist1:
      kind: nokia_srlinux
      image: nokia/srlinux:22.11.1
    rtr1:
      kind: nokia_srlinux
      image: nokia/srlinux:22.11.1
    ztp:
      kind: linux
      image: alpine:latest
    mgmt:
      kind: linux
      image: alpine:latest
  links:
    - endpoints: ["access1:eth1", "dist1:ethernet-1/1"]
    - endpoints: ["access2:eth1", "dist1:ethernet-1/2"]
    - endpoints: ["dist1:ethernet-1/3", "rtr1:ethernet-1/1"]
mgmt:
  network: mgmt-net
  ipv4_subnet: 172.20.20.0/24
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
    image: networktocode/nautobot:latest
    ports:
      - "8080:8080"
    networks:
      - mgmt-net
  ztp:
    image: alpine:latest
    networks:
      - mgmt-net
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
