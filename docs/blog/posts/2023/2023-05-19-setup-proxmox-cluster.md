---
authors: [bsmeding]
toc: true
date: 2023-05-19
layout: single
comments: true
title: Setup Proxmox Cluster
tags: ["proxmox", "virtualisation"]
---

# Setup Proxmox Cluster

A quick guide to setting up a Proxmox cluster and troubleshooting corosync issues.

---

## Important Note
Only hosts that do **not** have any virtual guests running can be added to a cluster!

---

## Cluster Configuration
The cluster configuration is saved in `/etc/pve/corosync.conf`.

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

For more information, see the [Proxmox documentation](https://pve.proxmox.com/wiki/Cluster_Manager).