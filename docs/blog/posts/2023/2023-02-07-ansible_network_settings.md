---
authors: [bsmeding]
toc: true
date: 2023-05-19
layout: single
comments: true
title: Setup Proxmox cluster
tags: ["proxmox", "virtualisation"]
---




# Create cluster


Only hosts thas doesnt have any virtual guests running can be added to a cluster!


## corosync.conf
The config from cluster is saved in the file `/etc/pve/corosync.conf`. When installing a new node sometimes this can be hanging on the corosync service. To solve try to remove on the `master`:

 ```bash
systemctl stop pve-cluster
systemctl stop corosync
pmxcfs -l
rm /etc/pve/corosync.conf
rm -r /etc/corosync/*
killall pmxcfs
systemctl start pve-cluster
```
