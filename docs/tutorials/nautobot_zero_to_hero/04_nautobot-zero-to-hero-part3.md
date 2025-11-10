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

Containerlab is a tool for deploying container-based network topologies. Install it using the official method:

```bash
# Install Containerlab
bash -c "$(curl -sL https://get.containerlab.dev)"

# Verify installation
containerlab version
```

For detailed installation instructions, see the [Containerlab documentation](https://containerlab.dev/install/).

---

## 4. Create Network Topology

The nautobot_zero_to_hero repository includes example Containerlab topologies. Let's use or create a simple multi-vendor topology:

### 4.1 Example Topology File

Create a file named `topology.clab.yml`:

```yaml
name: nautobot-lab

topology:
  nodes:
    r1:
      kind: vr-sros
      image: vrnetlab/vr-sros:20.10.R1
    sw1:
      kind: vr-veos
      image: vrnetlab/vr-veos:latest
    sw2:
      kind: vr-veos
      image: vrnetlab/vr-veos:latest

  links:
    - endpoints: ["r1:eth1", "sw1:eth1"]
    - endpoints: ["sw1:eth2", "sw2:eth1"]
```

This creates a simple topology with:
- One router (Nokia SR OS)
- Two switches (Arista vEOS)

### 4.2 Use Repository Topology

Alternatively, use the topology from the nautobot_zero_to_hero repository:

```bash
cd nautobot_zero_to_hero/containerlab
# Review the topology file
cat topology.clab.yml
```

---

## 5. Deploy the Lab

### 5.1 Deploy the Topology

```bash
# Deploy the lab
containerlab deploy -t topology.clab.yml

# Check status
containerlab inspect -t topology.clab.yml
```

📸 **[Screenshot: Containerlab Deployment]**

### 5.2 Access Device Information

Containerlab will create entries in `/etc/hosts` for easy access:

```bash
# View device hostnames
cat /etc/hosts | grep clab
```

You can also use the `update_hosts.sh` script from the repository:

```bash
./update_hosts.sh
```

---

## 6. Verify Network Connectivity

### 6.1 Test Device Access

```bash
# Test SSH access to devices
ssh admin@clab-nautobot-lab-r1
ssh admin@clab-nautobot-lab-sw1
ssh admin@clab-nautobot-lab-sw2
```

Default credentials are typically:
- Username: `admin`
- Password: `admin` (or check the repository documentation)

### 6.2 Verify Device Configurations

```bash
# Connect to a device and check configuration
ssh admin@clab-nautobot-lab-sw1
show version
show ip interface brief
```

### 6.3 Test Inter-Device Connectivity

From within a device, test connectivity to other devices:

```bash
# From sw1, ping sw2
ping clab-nautobot-lab-sw2
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
