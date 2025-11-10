---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 9: Configuration Compliance
tags: ["network automation", "nautobot", "golden config", "compliance", "drift detection"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 9: Configuration Compliance
## Detect Configuration Drift with Golden Config
*Set up configuration compliance checks to detect and monitor configuration drift.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 9: Configuration Compliance](#nautobot-zero-to-hero--part-9-configuration-compliance)
  - [Detect Configuration Drift with Golden Config](#detect-configuration-drift-with-golden-config)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Configure Compliance Rules](#3-configure-compliance-rules)
  - [4. Configure Compliance Features](#4-configure-compliance-features)
  - [5. Run Compliance Checks](#5-run-compliance-checks)
  - [6. Review Compliance Reports](#6-review-compliance-reports)
  - [7. Monitor Compliance Status](#7-monitor-compliance-status)
  - [8. Wrap-Up](#8-wrap-up)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction

In this part, we'll set up configuration compliance checking using the Golden Config plugin. This will allow us to detect configuration drift by comparing actual device configurations against our golden (intended) configurations.

We'll:
1. Configure compliance rules
2. Set up compliance features to check
3. Run compliance checks on devices
4. Review compliance reports
5. Monitor compliance status over time

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites

- Completed [Part 8: Separate Golden Config Templates](/tutorials/nautobot_zero_to_hero/09_nautobot-zero-to-hero-part8/)
- Golden Config plugin installed and configured
- Golden configurations created for devices
- Device backups configured and working

---

## 3. Configure Compliance Rules

### 3.1 Access Compliance Rules

1. Navigate to **Golden Config → Compliance Rules**
2. Review existing rules or create new ones

📸 **[Screenshot: Compliance Rules List]**

### 3.2 Create Compliance Rule

1. Click **Add** to create a new rule
2. Configure the rule:
   - **Name**: e.g., "Interface Description Compliance"
   - **Platform**: Select platform(s) or leave blank for all
   - **Feature**: Select what to check (e.g., "Interfaces")
   - **Config Compliance**: Define the compliance logic
3. Click **Save**

### 3.3 Example Compliance Rules

Common compliance rules include:
- **Interface Compliance**: Check interface descriptions, VLANs, admin state
- **VLAN Compliance**: Verify VLAN configurations match intended
- **Routing Compliance**: Check routing protocol configurations
- **Security Compliance**: Verify security-related configurations

---

## 4. Configure Compliance Features

### 4.1 Access Compliance Features

1. Navigate to **Golden Config → Compliance Features**
2. Review available features

📸 **[Screenshot: Compliance Features List]**

### 4.2 Enable Compliance Features

Enable the features you want to check:
- **Interfaces**: Interface configurations
- **VLANs**: VLAN assignments and configurations
- **IP Addresses**: IP address assignments
- **Routing**: Routing protocol configurations
- **ACLs**: Access control lists
- **SNMP**: SNMP configurations

### 4.3 Configure Feature Settings

For each feature, configure:
- **Required**: Whether the feature must be present
- **Compliance Rules**: Which rules apply to this feature
- **Severity**: How critical non-compliance is

---

## 5. Run Compliance Checks

### 5.1 Manual Compliance Check

1. Navigate to **Golden Config → Compliance**
2. Select a device
3. Click **Run Compliance Check**
4. Wait for the check to complete

📸 **[Screenshot: Running Compliance Check]**

### 5.2 Batch Compliance Check

1. Navigate to **Golden Config → Compliance**
2. Select multiple devices
3. Click **Run Compliance Check** (batch mode)
4. Monitor progress

### 5.3 Scheduled Compliance Checks

1. Navigate to **Jobs → Scheduled Jobs**
2. Create a scheduled job for compliance checks
3. Configure:
   - **Job**: Select compliance check job
   - **Schedule**: Set frequency (daily, weekly, etc.)
   - **Devices**: Select devices or use filter
4. Save the schedule

📸 **[Screenshot: Scheduled Compliance Job]**

---

## 6. Review Compliance Reports

### 6.1 View Compliance Results

1. Navigate to **Golden Config → Compliance**
2. View compliance status for each device
3. Click on a device to see detailed results

📸 **[Screenshot: Compliance Status Dashboard]**

### 6.2 Analyze Compliance Issues

For each non-compliant device:
1. Review what's different
2. See side-by-side comparison (intended vs actual)
3. Identify specific configuration differences

📸 **[Screenshot: Compliance Comparison View]**

### 6.3 Export Compliance Reports

1. Navigate to **Golden Config → Compliance Reports**
2. Generate reports for:
   - Individual devices
   - All devices
   - Specific compliance features
3. Export in various formats (CSV, PDF, etc.)

📸 **[Screenshot: Compliance Report Export]**

---

## 7. Monitor Compliance Status

### 7.1 Compliance Dashboard

1. Navigate to **Golden Config → Compliance Dashboard**
2. View overall compliance metrics:
   - Total devices
   - Compliant devices
   - Non-compliant devices
   - Compliance percentage

📸 **[Screenshot: Compliance Dashboard]**

### 7.2 Compliance Trends

1. View compliance trends over time
2. Identify devices with recurring compliance issues
3. Track improvements after remediation

### 7.3 Set Up Alerts

1. Configure alerts for:
   - New compliance violations
   - Devices falling out of compliance
   - Critical compliance issues
2. Set notification methods (email, webhook, etc.)

---

## 8. Wrap-Up

Congratulations! You have successfully:
- ✅ Configured compliance rules
- ✅ Set up compliance features to check
- ✅ Run compliance checks on devices
- ✅ Reviewed compliance reports
- ✅ Set up compliance monitoring and alerts

You can now detect configuration drift and ensure your devices stay compliant with your intended configurations!

---

## 9. Next Steps

Now that compliance checking is set up, proceed to **Part 10: Configuration Remediation** to:
- Generate remediation configurations
- Create automated remediation workflows
- Fix configuration drift automatically

---

*Happy automating! 🚀*
