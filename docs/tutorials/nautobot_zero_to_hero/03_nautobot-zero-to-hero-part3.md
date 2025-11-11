---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 3: Deploy Network with Containerlab
tags: ["network automation", "containerlab", "lab environment", "network topology"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 3: Deploy Network with Containerlab
## Set Up Your Network Lab Environment
*Deploy a multi-vendor network topology using Containerlab for hands-on practice.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 3: Deploy Network with Containerlab](#nautobot-zero-to-hero--part-3-deploy-network-with-containerlab)
  - [Set Up Your Network Lab Environment](#set-up-your-network-lab-environment)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Install Containerlab](#3-install-containerlab)
  - [4. Create Network Topology](#4-create-network-topology)
  - [5. Deploy the Lab](#5-deploy-the-lab)
  - [6. Verify Network Connectivity](#6-verify-network-connectivity)
  - [7. Wrap-Up](#7-wrap-up)
  - [8. Next Steps](#8-next-steps)

---

## 1. Introduction

In this part, we'll deploy a network lab environment using Containerlab. This will provide us with real network devices that we can use for automation practice throughout the series.

We'll:

1. Install Containerlab
2. Create a network topology file
3. Deploy the lab network
4. Verify connectivity between devices

> **Estimated Time:** ~1 hour

---

## 2. Prerequisites

- Completed [Part 2: Getting Started with Nautobot](/tutorials/nautobot_zero_to_hero/03_nautobot-zero-to-hero-part2/)
- Linux system with Docker installed (or use the same VM as Nautobot)
- Sufficient resources: 4GB+ RAM, 20GB+ disk space
- Basic understanding of network topologies

---

## 3. Install Containerlab

Containerlab is a tool for deploying container-based network topologies.

> **💡 Already Installed?** If you followed Part 1 and used the `install.sh` script from the [nautobot_zero_to_hero](https://github.com/bsmeding/nautobot_zero_to_hero) repository, Containerlab is already installed. You can skip to section 4.

### 3.1 Check if Containerlab is Installed

First, verify if Containerlab is already installed:

```bash
# Check if Containerlab is installed
containerlab version
```

If the command succeeds and shows a version number, Containerlab is already installed. You can proceed to section 4.

### 3.2 Install Containerlab (if needed)

If Containerlab is not installed, install it using the official method:

```bash
# Install Containerlab
bash -c "$(curl -sL https://get.containerlab.dev)"

# Verify installation
containerlab version
```

For detailed installation instructions, see the [Containerlab documentation](https://containerlab.dev/install/).

---

## 4. Create Network Topology

The nautobot_zero_to_hero repository includes a complete Containerlab topology file that matches the lab environment used throughout the series. This topology includes multiple Arista cEOS devices that will be used for automation practice.

### 4.1 Use Repository Topology

The repository includes a ready-to-use topology file:

```bash
cd nautobot_zero_to_hero/containerlab
# Review the topology file
cat nautobot-lab.clab.yml
```

This topology includes:
- **access1** - Arista cEOS access switch (172.20.20.11)
- **access2** - Arista cEOS access switch (172.20.20.12)
- **dist1** - Arista cEOS distribution switch (172.20.20.13)
- **rtr1** - Arista cEOS router (172.20.20.14)
- **workstation1** - Linux workstation (172.20.20.15)
- **mgmt** - Management server (172.20.20.16)

All devices are pre-configured with:
- Management IP addresses in the 172.20.20.0/24 subnet
- Bootstrap configurations
- SSH access (admin/admin)
- NAPALM support enabled

### 4.2 Verify Topology File

The topology file is located at `containerlab/nautobot-lab.clab.yml`. You can review it to understand the network structure before deploying.

---

## 5. Deploy the Lab

### 5.1 Deploy the Topology

```bash
# Navigate to containerlab directory
cd nautobot_zero_to_hero/containerlab

# Deploy the lab (requires sudo for network namespace creation)
sudo containerlab deploy -t nautobot-lab.clab.yml

# Check status
sudo containerlab inspect -t nautobot-lab.clab.yml
```

> **Note:** Containerlab requires `sudo` privileges to create network namespaces and configure networking.

### 5.2 Verify Lab Status

```bash
# Show all lab nodes
sudo containerlab show -t nautobot-lab.clab.yml

# Check if all nodes are running
sudo containerlab inspect -t nautobot-lab.clab.yml
```

📸 **[Screenshot: Containerlab Deployment]**

### 5.3 Access Device Information

If you ran `install.sh` from Part 1, your `/etc/hosts` file should already be updated with friendly hostnames. Otherwise, you can update it manually:

**Option 1: Use the update script (if not already done):**
```bash
cd nautobot_zero_to_hero
sudo bash update_hosts.sh
```

**Option 2: Manual /etc/hosts update:**
```bash
# Add these entries to /etc/hosts
172.20.20.11  access1.lab access1
172.20.20.12  access2.lab access2
172.20.20.13  dist1.lab dist1
172.20.20.14  rtr1.lab rtr1
172.20.20.15  workstation1.lab workstation1
172.20.20.16  mgmt.lab mgmt
127.0.0.1     nautobotlab.dev
```

After updating `/etc/hosts`, you can access devices using friendly names:
```bash
ssh admin@access1
ssh admin@dist1.lab
ping rtr1
```

---

## 6. Verify Network Connectivity

### 6.1 Test Device Access

```bash
# Test SSH access to devices (using friendly hostnames from /etc/hosts)
ssh admin@access1
ssh admin@access2
ssh admin@dist1
ssh admin@rtr1
```

Default credentials for all devices:
- **Username:** `admin`
- **Password:** `admin`

You can also use the Containerlab-generated hostnames:
```bash
ssh admin@clab-nautobot-lab-access1
ssh admin@clab-nautobot-lab-dist1
```

### 6.2 Verify Device Configurations

```bash
# Connect to an access switch and check configuration
ssh admin@access1
show version
show ip interface brief
show running-config
```

### 6.3 Test Inter-Device Connectivity

From within a device, test connectivity to other devices:

```bash
# From access1, ping other devices
ssh admin@access1
ping 172.20.20.12  # access2
ping 172.20.20.13  # dist1
ping 172.20.20.14  # rtr1
```

### 6.4 Verify Management Network

All devices should be reachable from your host machine:

```bash
# Ping all devices from your host
ping -c 2 access1
ping -c 2 access2
ping -c 2 dist1
ping -c 2 rtr1
ping -c 2 workstation1
ping -c 2 mgmt
```

---

## 7. Wrap-Up

Congratulations! You have successfully:
- ✅ Installed Containerlab
- ✅ Created a network topology
- ✅ Deployed the lab network
- ✅ Verified device connectivity

You now have a working network lab environment that you can use for automation practice throughout the series.

---

## 8. Next Steps

Now that your network lab is deployed, proceed to **Part 4: Device Discovery & Onboarding** to:
- Install and configure the Device Onboarding plugin
- Automatically discover devices from Containerlab
- Onboard devices into Nautobot

---

*Happy automating! 🚀*
