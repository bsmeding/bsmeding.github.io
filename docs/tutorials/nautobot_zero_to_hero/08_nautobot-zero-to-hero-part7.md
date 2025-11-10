---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 7: Deploy Provision Job
tags: ["network automation", "nautobot", "jobs", "provisioning", "deployment"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 7: Deploy Provision Job
## Send Golden Config to Devices
*Create and deploy a Provision job to send golden configurations to network devices.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 7: Deploy Provision Job](#nautobot-zero-to-hero--part-7-deploy-provision-job)
  - [Send Golden Config to Devices](#send-golden-config-to-devices)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Create Provision Job](#3-create-provision-job)
  - [4. Configure Job Parameters](#4-configure-job-parameters)
  - [5. Deploy Configuration to Device](#5-deploy-configuration-to-device)
  - [6. Verify Deployment](#6-verify-deployment)
  - [7. Wrap-Up](#7-wrap-up)
  - [8. Next Steps](#8-next-steps)

---

## 1. Introduction

In this part, we'll create a Provision job that deploys golden configurations to network devices. This job will retrieve the intended configuration from Golden Config and push it to the device.

We'll:
1. Create a Provision job
2. Configure job parameters
3. Deploy the golden configuration to a device
4. Verify the deployment was successful

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites

- Completed [Part 6: Enable Golden Config Plugin](/tutorials/nautobot_zero_to_hero/07_nautobot-zero-to-hero-part6/)
- Golden configurations created for devices
- Devices are reachable via SSH
- Nautobot Jobs framework configured

---

## 3. Create Provision Job

### 3.1 Job Structure

A Provision job typically:
1. Retrieves the intended configuration from Golden Config
2. Connects to the device via SSH/API
3. Pushes the configuration to the device
4. Verifies the deployment
5. Logs the results

### 3.2 Example Provision Job

Create a job file `jobs/provision_device.py`:

```python
from nautobot.extras.jobs import Job, StringVar, ObjectVar
from nautobot.dcim.models import Device
from nautobot_golden_config.models import GoldenConfig
from nautobot_golden_config.utilities import get_golden_config
import requests

class ProvisionDevice(Job):
    class Meta:
        name = "Provision Device with Golden Config"
        description = "Deploy golden configuration to a device"
        field_order = ["device", "dry_run"]

    device = ObjectVar(
        model=Device,
        description="Device to provision",
        required=True
    )
    
    dry_run = StringVar(
        description="Dry run (yes/no)",
        default="no",
        required=False
    )

    def run(self, device, dry_run):
        self.log_info(f"Starting provisioning for {device.name}")
        
        # Get golden configuration
        try:
            golden_config = GoldenConfig.objects.get(device=device)
            intended_config = get_golden_config(golden_config)
            self.log_success(f"Retrieved intended configuration for {device.name}")
        except Exception as e:
            self.log_failure(f"Failed to get golden config: {str(e)}")
            return
        
        # Deploy configuration (example using NAPALM)
        if dry_run.lower() == "yes":
            self.log_info("DRY RUN: Would deploy configuration")
            self.log_info(intended_config)
            return
        
        try:
            # Connect to device and deploy config
            # This is a simplified example - actual implementation depends on device type
            self.log_info(f"Deploying configuration to {device.name}")
            # Add your deployment logic here
            self.log_success(f"Successfully deployed configuration to {device.name}")
        except Exception as e:
            self.log_failure(f"Failed to deploy configuration: {str(e)}")
```

### 3.3 Add Job to Repository

1. Save the job file to your Jobs repository
2. Commit and push to Git
3. Sync the repository in Nautobot

---

## 4. Configure Job Parameters

### 4.1 Review Job in Nautobot

1. Navigate to **Jobs → Jobs**
2. Find your "Provision Device with Golden Config" job
3. Review the job parameters

📸 **[Screenshot: Provision Job Details]**

### 4.2 Test Job Parameters

Before deploying, test the job with dry-run mode to verify:
- Golden config retrieval works
- Configuration format is correct
- Device connectivity is available

---

## 5. Deploy Configuration to Device

### 5.1 Select Device

1. Navigate to **Devices → Devices**
2. Select a device that has a golden configuration
3. Note the device name and platform

### 5.2 Run Provision Job

1. Navigate to **Jobs → Jobs**
2. Find "Provision Device with Golden Config"
3. Click **Run Job**
4. Select parameters:
   - **Device**: Choose your device
   - **Dry Run**: Start with "yes" to test
5. Click **Run Job**

📸 **[Screenshot: Running Provision Job]**

### 5.3 Review Job Output

1. Wait for the job to complete
2. Review the job result
3. Check for any errors or warnings
4. Verify the configuration was retrieved correctly

📸 **[Screenshot: Provision Job Result]**

### 5.4 Deploy for Real

Once dry-run is successful:
1. Run the job again
2. Set **Dry Run** to "no"
3. Execute the deployment
4. Monitor the job output

---

## 6. Verify Deployment

### 6.1 Check Device Configuration

1. SSH to the device
2. Verify the configuration was applied
3. Compare with the intended configuration

```bash
ssh admin@device-name
show running-config
```

### 6.2 Verify in Nautobot

1. Navigate to **Golden Config → Compliance**
2. Run a compliance check on the device
3. Verify the device matches the golden configuration

📸 **[Screenshot: Compliance Check Results]**

### 6.3 Check Job Logs

1. Review the job logs in Nautobot
2. Verify all steps completed successfully
3. Note any warnings or issues

---

## 7. Wrap-Up

Congratulations! You have successfully:
- ✅ Created a Provision job
- ✅ Configured job parameters
- ✅ Deployed golden configuration to a device
- ✅ Verified the deployment was successful

You can now deploy intended configurations to your network devices automatically!

---

## 8. Next Steps

Now that you can deploy configurations, proceed to **Part 8: Separate Golden Config Templates** to:
- Separate Interface configuration into a separate template
- Create Job Hooks for automatic interface updates
- Automate interface configuration changes

---

*Happy automating! 🚀*
