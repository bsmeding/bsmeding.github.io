---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 10: Configuration Remediation
tags: ["network automation", "nautobot", "golden config", "remediation", "drift fix"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 10: Configuration Remediation
## Automatically Fix Configuration Drift
*Generate and deploy remediation configurations to fix compliance issues automatically.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 10: Configuration Remediation](#nautobot-zero-to-hero--part-10-configuration-remediation)
  - [Automatically Fix Configuration Drift](#automatically-fix-configuration-drift)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Generate Remediation Configurations](#3-generate-remediation-configurations)
  - [4. Review Remediation Configs](#4-review-remediation-configs)
  - [5. Create Remediation Job](#5-create-remediation-job)
  - [6. Deploy Remediation](#6-deploy-remediation)
  - [7. Verify Remediation](#7-verify-remediation)
  - [8. Automate Remediation Workflow](#8-automate-remediation-workflow)
  - [9. Wrap-Up](#9-wrap-up)
  - [10. Next Steps](#10-next-steps)

---

## 1. Introduction

In this part, we'll use Golden Config to generate remediation configurations that fix compliance issues. We'll create automated workflows to deploy these remediations and verify they resolve the drift.

We'll:

1. Generate remediation configurations from compliance differences
2. Review and validate remediation configs
3. Create a remediation deployment job
4. Deploy remediations to devices
5. Verify compliance is restored
6. Automate the remediation workflow

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites

- Completed [Part 9: Configuration Compliance](/tutorials/nautobot_zero_to_hero/10_nautobot-zero-to-hero-part9/)
- Compliance checks configured and running
- Devices with compliance issues identified
- SSH access to devices for remediation deployment

---

## 3. Generate Remediation Configurations

### 3.1 Access Remediation

1. Navigate to **Golden Config → Remediation**
2. Select a device with compliance issues
3. Click **Generate Remediation**

📸 **[Screenshot: Generate Remediation]**

### 3.2 Remediation Types

Golden Config can generate different types of remediation:

- **Intended Config**: Full intended configuration
- **Missing Config**: Only missing configurations
- **Extra Config**: Configurations that should be removed
- **Manual Remediation**: Custom remediation based on rules

### 3.3 Generate Remediation Config

1. Select remediation type
2. Choose the device
3. Click **Generate**
4. Review the generated configuration

📸 **[Screenshot: Generated Remediation Config]**

---

## 4. Review Remediation Configs

### 4.1 Review Configuration Differences

1. View side-by-side comparison:
   - **Intended**: What should be configured
   - **Actual**: What is currently configured
   - **Remediation**: What needs to be changed

📸 **[Screenshot: Remediation Comparison]**

### 4.2 Validate Remediation

Before deploying, validate:
- Configuration syntax is correct
- Changes are appropriate
- No unintended side effects
- Device can accept the changes

### 4.3 Save Remediation Config

1. Review the remediation configuration
2. Save it for deployment
3. Optionally commit to Git repository

---

## 5. Create Remediation Job

### 5.1 Create Job File

Create `jobs/deploy_remediation.py`:

```python
from nautobot.extras.jobs import Job, ObjectVar, StringVar
from nautobot.dcim.models import Device
from nautobot_golden_config.models import GoldenConfig
from nautobot_golden_config.utilities import get_remediation_config
import napalm

class DeployRemediation(Job):
    class Meta:
        name = "Deploy Remediation Configuration"
        description = "Deploy remediation config to fix compliance issues"
        field_order = ["device", "remediation_type", "dry_run"]

    device = ObjectVar(
        model=Device,
        description="Device to remediate",
        required=True
    )
    
    remediation_type = StringVar(
        description="Remediation type (intended/missing/manual)",
        default="missing",
        required=False
    )
    
    dry_run = StringVar(
        description="Dry run (yes/no)",
        default="no",
        required=False
    )

    def run(self, device, remediation_type, dry_run):
        self.log_info(f"Starting remediation for {device.name}")
        
        # Get golden config
        try:
            golden_config = GoldenConfig.objects.get(device=device)
        except GoldenConfig.DoesNotExist:
            self.log_failure(f"No golden config found for {device.name}")
            return
        
        # Get remediation configuration
        try:
            remediation_config = get_remediation_config(
                golden_config,
                remediation_type=remediation_type
            )
            self.log_success(f"Retrieved remediation config for {device.name}")
        except Exception as e:
            self.log_failure(f"Failed to get remediation config: {str(e)}")
            return
        
        if dry_run.lower() == "yes":
            self.log_info("DRY RUN: Would deploy remediation:")
            self.log_info(remediation_config)
            return
        
        # Deploy remediation
        try:
            # Connect to device using NAPALM
            driver = napalm.get_network_driver(device.platform.network_driver)
            with driver(
                hostname=device.primary_ip4.address.ip,
                username=device.platform.network_driver_username,
                password=device.platform.network_driver_password
            ) as device_conn:
                # Load and commit configuration
                device_conn.load_merge_candidate(config=remediation_config)
                diff = device_conn.compare_config()
                
                if diff:
                    self.log_info("Configuration diff:")
                    self.log_info(diff)
                    device_conn.commit_config()
                    self.log_success(f"Remediation deployed to {device.name}")
                else:
                    self.log_info("No changes needed")
                    
        except Exception as e:
            self.log_failure(f"Failed to deploy remediation: {str(e)}")
```

### 5.2 Add Job to Repository

1. Save the job file
2. Commit and push to Git
3. Sync in Nautobot

---

## 6. Deploy Remediation

### 6.1 Run Remediation Job

1. Navigate to **Jobs → Jobs**
2. Find "Deploy Remediation Configuration"
3. Click **Run Job**
4. Select parameters:
   - **Device**: Choose device with compliance issues
   - **Remediation Type**: Select type (start with "missing")
   - **Dry Run**: Start with "yes" to test
5. Click **Run Job**

📸 **[Screenshot: Running Remediation Job]**

### 6.2 Review Job Output

1. Wait for job to complete
2. Review the configuration diff
3. Verify changes are correct
4. Check for any errors

📸 **[Screenshot: Remediation Job Result]**

### 6.3 Deploy for Real

Once dry-run looks good:
1. Run job again
2. Set **Dry Run** to "no"
3. Execute the remediation
4. Monitor deployment

---

## 7. Verify Remediation

### 7.1 Run Compliance Check

1. After remediation, run compliance check again
2. Verify compliance issues are resolved
3. Check compliance status

📸 **[Screenshot: Post-Remediation Compliance]**

### 7.2 Verify Device Configuration

1. SSH to the device
2. Verify the remediation was applied
3. Check the specific configurations that were changed

```bash
ssh admin@device-name
show running-config
```

### 7.3 Compare Configurations

1. In Nautobot, compare:
   - Intended configuration
   - Actual configuration (after remediation)
2. Verify they match

---

## 8. Automate Remediation Workflow

### 8.1 Create Automated Workflow

Create a job that:
1. Runs compliance check
2. Identifies non-compliant devices
3. Generates remediation configs
4. Deploys remediations
5. Verifies compliance is restored

### 8.2 Schedule Automated Remediation

1. Navigate to **Jobs → Scheduled Jobs**
2. Create scheduled job for automated remediation
3. Configure:
   - **Frequency**: Daily or weekly
   - **Devices**: All or filtered list
   - **Remediation Type**: Choose default type
4. Save schedule

📸 **[Screenshot: Scheduled Remediation Job]**

### 8.3 Set Up Notifications

1. Configure notifications for:
   - Remediation deployments
   - Failed remediations
   - Compliance restored
2. Set up email or webhook notifications

---

## 9. Wrap-Up

Congratulations! You have successfully:
- ✅ Generated remediation configurations
- ✅ Created a remediation deployment job
- ✅ Deployed remediations to devices
- ✅ Verified compliance is restored
- ✅ Automated the remediation workflow

You can now automatically detect and fix configuration drift!

---

## 10. Next Steps

Now that remediation is automated, proceed to **Part 11: Event-Driven Automation** to:
- Automatically deploy full golden config when device changes
- Set up event-driven workflows
- Build reactive automation based on Nautobot changes

---

*Happy automating! 🚀*
