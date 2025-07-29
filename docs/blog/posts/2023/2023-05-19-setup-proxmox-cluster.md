---
authors: [bsmeding]
toc: true
date: 2023-05-19
layout: single
comments: true
title: Setup Proxmox Cluster
summary: How to set up a Proxmox cluster and troubleshoot corosync issues.
tags: ["proxmox", "virtualisation"]
---

# Setup Proxmox Cluster

Proxmox is a powerful open-source virtualization platform. In this post, I'll show you how to set up a basic Proxmox cluster for your home lab or small business.

<!-- more -->

---

## Important Note
Only hosts that do **not** have any virtual guests running can be added to a cluster!

---

## Step 1: Prepare All Nodes
- Ensure all nodes are running the same Proxmox version.
- Set unique hostnames and static IP addresses for each node.
- Make sure `/etc/hosts` is correct on all nodes (add all cluster node IPs and hostnames).

Example `/etc/hosts`:
```ini
192.168.1.101  pve1
192.168.1.102  pve2
192.168.1.103  pve3
```

---

## Step 2: Initialize the Cluster (on the first/master node)
Replace `CLUSTERNAME` with your desired cluster name and `IP` with the master node's IP address:

```bash
pvecm create CLUSTERNAME
```

Check cluster status:
```bash
pvecm status
```

---

## Step 3: Add Additional Nodes to the Cluster
On each additional node, join the cluster using the master node's IP address:

```bash
pvecm add <MASTER_NODE_IP>
```

You will be prompted for the root password of the master node.

Check status on any node:
```bash
pvecm nodes
```

---

## Step 4: Troubleshooting Corosync Issues
If you have issues adding a new node (e.g., corosync service hangs), try the following steps on the master node:

```bash
systemctl stop pve-cluster
systemctl stop corosync
pmxcfs -l
rm /etc/pve/corosync.conf
rm -r /etc/corosync/*
killall pmxcfs
systemctl start pve-cluster
```

---

## Step 5: Verify Cluster Health
On any node, check:
```bash
pvecm status
pvecm nodes
```

---

For more information, see the [Proxmox documentation](https://pve.proxmox.com/wiki/Cluster_Manager).