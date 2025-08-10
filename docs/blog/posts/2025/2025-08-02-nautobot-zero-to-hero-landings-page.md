---
authors: [bsmeding]
date: 2025-08-02
title: Nautobot in Action – Global Series Index
tags: ["graphql", "network automation", "api", "jinja2", "opsmill", "nautobot"]
toc: true
layout: single
comments: true
---

# Nautobot in Action – Global Series Index

*A comprehensive guide to building a complete network automation solution with Nautobot, from zero to production-ready deployment.*

<!-- more -->

---

## Series Overview

This series takes you from a basic Nautobot installation to a fully automated network environment. You'll learn how to use Nautobot as your Single Source of Truth (SSoT), implement configuration management, ensure compliance, and build event-driven automation workflows.

**What You'll Learn:**
- Deploy and configure Nautobot with Git integration
- Onboard existing network devices automatically
- Implement Golden Config for compliance and drift detection
- Build remediation workflows for non-compliant devices
- Create event-driven automation for network changes
- Deploy new devices with Zero-Touch Provisioning (ZTP)
- Integrate with external tools via APIs

**Prerequisites:**
- Basic understanding of networking concepts
- Familiarity with Docker and Git
- A lab environment (Containerlab recommended)

**Estimated Time:** 8-12 hours across all parts

---

## Core Series

### 1. **Part 1 – Nautobot as Your Single Source of Truth (SSoT)**
*Publishing: August 18, 2025*

- Deploy Nautobot
- Connect to Git repository
- Create base inventory
- Add first Jinja2 template
- Create and run first Nautobot Job

**Estimated Time:** ~2 hours

### 2. **Part 2 – Onboarding Brownfield Devices with the Device Onboarding App**
*Publishing: August 25, 2025*

- Install and configure Device Onboarding app
- Discover existing devices
- Auto-create devices with platforms, roles, and interfaces
- Store discovered configs in Git

**Estimated Time:** ~1.5 hours

### 3. **Part 3 – Golden Config for Intended Configs & Compliance**
*Publishing: September 1, 2025*

- Install Golden Config plugin
- Configure backup jobs
- Store intended configs in Git
- Run compliance reports and detect drift

**Estimated Time:** ~2 hours

### 4. **Part 4 – Remediation: Making Devices Compliant**
*Publishing: September 8, 2025*

- Generate remediation configs (intended, missing, manual)
- Create a multi-vendor remediation Job
- Push remediation to devices and re-check compliance

**Estimated Time:** ~2 hours

### 5. **Part 5 – Event-Driven Automation: Interface Change Jobs**
*Publishing: September 15, 2025*

- Job Hooks on interface changes
- Sync admin-state, description, VLANs
- Handle multi-vendor syntax differences

**Estimated Time:** ~1.5 hours

### 6. **Part 6 – Full Device Deployment, ZTP & Site Validation**
*Publishing: September 22, 2025*

- Push intended configs to startup/running configs
- Integrate with ZTP server
- Validate site cabling (LLDP/CDP) and VLAN/IP assignments
- Force compliance push option
- Generate site compliance report

**Estimated Time:** ~2 hours

---

## Optional / Advanced Parts

### 7. **Part 7 – API Integrations**
*Publishing: September 29, 2025*

- Integrating Nautobot Jobs with Infoblox, ISE, and other tools
- Using REST and GraphQL queries

**Estimated Time:** ~1.5 hours

### 8. **Part 8 – GitOps-Style Change Management**
*Publishing: October 6, 2025*

- PR → Review → Automated Deployment
- Using Golden Config in a GitOps pipeline

**Estimated Time:** ~1.5 hours

### 9. **Part 9 – Multi-Vendor Compliance Pipelines**
*Publishing: October 13, 2025*

- Advanced Golden Config with vendor-specific templates
- Compliance across Cisco, Arista, Juniper

**Estimated Time:** ~2 hours

### 10. **Part 10 – Golden Config for Firewalls and Wireless Controllers**
*Publishing: October 20, 2025*

- Handling non-switch/router devices
- Backups, intended configs, and compliance for firewalls and WLCs

**Estimated Time:** ~1.5 hours

---

## Lab Setup Reference

### **Containerlab Lab Deployment**
*[Available: [Building a Reusable Network Automation Lab with Containerlab](/blog/posts/2025/2025-02-04-building-reusable-network-automation-lab-with-containerlab/)]*

- Build a reusable multi-vendor lab with Containerlab
- Topology file, device images, and Nautobot + ZTP integration
- This lab is used for all parts of the series

**Estimated Time:** ~1 hour

---

## Getting Started

1. **Set up your lab environment** using the Containerlab guide above
2. **Start with Part 1** to deploy Nautobot and create your first inventory
3. **Follow each part sequentially** as they build upon each other
4. **Complete the core series** (Parts 1-6) for a production-ready setup
5. **Explore advanced topics** (Parts 7-10) for additional integrations

---

## Support & Community

- **Questions?** Leave a comment on any post
- **Found an issue?** Report it in the comments
- **Want to contribute?** Submit a pull request to the [GitHub repository](https://github.com/bsmeding/bsmeding.github.io)

---

*Happy automating! 🚀*
