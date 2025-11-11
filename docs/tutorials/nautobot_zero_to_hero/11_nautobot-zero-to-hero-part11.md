---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 11: Event-Driven Automation
tags: ["network automation", "nautobot", "event-driven", "automation", "job hooks"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 11: Event-Driven Automation
## Automatically Deploy Config When Device Changes
*Set up event-driven automation to automatically deploy full golden config when devices are modified in Nautobot.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 11: Event-Driven Automation](#nautobot-zero-to-hero--part-11-event-driven-automation)
  - [Automatically Deploy Config When Device Changes](#automatically-deploy-config-when-device-changes)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Understand Event-Driven Automation](#3-understand-event-driven-automation)
  - [4. Create Device Change Job](#4-create-device-change-job)
  - [5. Set Up Job Hook](#5-set-up-job-hook)
  - [6. Configure Webhooks](#6-configure-webhooks)
  - [7. Test Event-Driven Automation](#7-test-event-driven-automation)
  - [8. Wrap-Up](#8-wrap-up)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction

In this part, we'll set up event-driven automation that automatically deploys the full golden configuration to a device whenever that device is changed in Nautobot. This ensures that any changes made in Nautobot are immediately reflected on the actual network device.

We'll:

1. Understand event-driven automation concepts
2. Create a job to deploy golden config on device changes
3. Set up Job Hooks to trigger on device modifications
4. Configure webhooks for external integrations
5. Test the event-driven automation

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites

- Completed [Part 10: Configuration Remediation](/tutorials/nautobot_zero_to_hero/11_nautobot-zero-to-hero-part10/)
- Golden Config plugin configured
- Provision job created and tested
- Understanding of Nautobot's event system

---

## 3. Understand Event-Driven Automation

### 3.1 Event Types

Nautobot can trigger automation on various events:
- **Object Changes**: Create, update, delete
- **Webhooks**: HTTP callbacks on events
- **Job Hooks**: Jobs triggered by object changes
- **Signals**: Django signals for model changes

### 3.2 Use Cases

Event-driven automation is useful for:
- Automatically deploying config when device attributes change
- Syncing Nautobot changes to network devices
- Maintaining consistency between SSoT and devices
- Reacting to network changes in real-time

---

## 4. Create Device Change Job

### 4.1 Create Job File

Create `jobs/deploy_on_device_change.py`:

```python
from nautobot.extras.jobs import Job, ObjectVar
from nautobot.dcim.models import Device
from nautobot_golden_config.models import GoldenConfig
from nautobot_golden_config.utilities import get_golden_config
import napalm
import logging

logger = logging.getLogger(__name__)

class DeployOnDeviceChange(Job):
    class Meta:
        name = "Deploy Golden Config on Device Change"
        description = "Automatically deploy golden config when device is modified"
        field_order = ["device"]

    device = ObjectVar(
        model=Device,
        description="Device to deploy config to",
        required=True
    )

    def run(self, device):
        self.log_info(f"Device change detected for {device.name}, deploying golden config")
        
        # Get golden config
        try:
            golden_config = GoldenConfig.objects.get(device=device)
            intended_config = get_golden_config(golden_config)
            self.log_success(f"Retrieved golden config for {device.name}")
        except GoldenConfig.DoesNotExist:
            self.log_warning(f"No golden config found for {device.name}, skipping deployment")
            return
        except Exception as e:
            self.log_failure(f"Failed to get golden config: {str(e)}")
            return
        
        # Deploy to device
        try:
            # Connect to device using NAPALM
            driver = napalm.get_network_driver(device.platform.network_driver)
            
            # Get device credentials (use secrets or config)
            username = device.platform.network_driver_username or "admin"
            password = device.platform.network_driver_password or "admin"
            hostname = device.primary_ip4.address.ip if device.primary_ip4 else device.name
            
            with driver(hostname=hostname, username=username, password=password) as device_conn:
                # Load and commit configuration
                device_conn.load_merge_candidate(config=intended_config)
                diff = device_conn.compare_config()
                
                if diff:
                    self.log_info("Configuration changes:")
                    self.log_info(diff)
                    device_conn.commit_config()
                    self.log_success(f"Golden config deployed to {device.name}")
                else:
                    self.log_info("Device already matches golden config, no changes needed")
                    
        except Exception as e:
            self.log_failure(f"Failed to deploy config to {device.name}: {str(e)}")
            logger.error(f"Deployment error: {str(e)}", exc_info=True)
```

### 4.2 Add Job to Repository

1. Save the job file
2. Commit and push to Git
3. Sync in Nautobot

---

## 5. Set Up Job Hook

### 5.1 Create Job Hook

Create a job hook that triggers on device changes. You can use Django signals:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from nautobot.dcim.models import Device
from nautobot.extras.jobs import get_job
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Device)
def device_changed(sender, instance, created, **kwargs):
    """
    Triggered when a Device is created or updated
    """
    # Only deploy on updates, not initial creation
    if created:
        logger.info(f"Device {instance.name} created, skipping auto-deploy")
        return
    
    # Get the deployment job
    try:
        job_class = get_job("Deploy Golden Config on Device Change")
        if job_class:
            # Run the job asynchronously
            job = job_class()
            job.run(device=instance)
            logger.info(f"Triggered golden config deployment for {instance.name}")
    except Exception as e:
        logger.error(f"Failed to trigger deployment for {instance.name}: {str(e)}")
```

### 5.2 Register Signal Handler

Make sure the signal handler is loaded. Add to your job file or create a separate signals file:

```python
# In your jobs/__init__.py or main job file
from . import deploy_on_device_change
from .signals import device_changed
```

---

## 6. Configure Webhooks

### 6.1 Create Webhook

1. Navigate to **Admin → Webhooks**
2. Click **Add**
3. Configure:
   - **Name**: "Device Change Webhook"
   - **Type Create/Update/Delete**: Enable Update
   - **Object Types**: Select "Device"
   - **HTTP Method**: POST
   - **URL**: Your webhook endpoint
   - **HTTP Headers**: Add authentication if needed
4. Click **Save**

📸 **[Screenshot: Webhook Configuration]**

### 6.2 Webhook Payload

The webhook will send a JSON payload with device information:

```json
{
  "event": "updated",
  "timestamp": "2025-01-01T12:00:00Z",
  "model": "device",
  "username": "admin",
  "request_id": "abc123",
  "data": {
    "id": 1,
    "name": "sw1",
    "device_type": {...},
    ...
  }
}
```

### 6.3 Create Webhook Handler

Create an external service or job to handle webhook calls:

```python
from nautobot.extras.jobs import Job
import requests

class WebhookHandler(Job):
    def receive_webhook(self, request):
        """Handle incoming webhook"""
        if request.data.get('model') == 'device' and request.data.get('event') == 'updated':
            device_id = request.data['data']['id']
            # Trigger deployment job
            pass
```

---

## 7. Test Event-Driven Automation

### 7.1 Modify a Device

1. Navigate to **Devices → Devices**
2. Select a device
3. Make a change (e.g., update description, change site)
4. Click **Update**

📸 **[Screenshot: Updating Device]**

### 7.2 Verify Job Triggered

1. Navigate to **Jobs → Job Results**
2. Look for "Deploy Golden Config on Device Change" job
3. Verify it ran automatically
4. Review the job output

📸 **[Screenshot: Automatic Job Execution]**

### 7.3 Verify Configuration Deployed

1. Check the job result
2. Verify the configuration was deployed
3. SSH to device to confirm changes

```bash
ssh admin@device-name
show running-config
```

### 7.4 Test Multiple Changes

1. Make several changes to a device
2. Verify each change triggers deployment
3. Check that deployments complete successfully

---

## 8. Wrap-Up

Congratulations! You have successfully:
- ✅ Created a job to deploy golden config on device changes
- ✅ Set up Job Hooks to trigger automatically
- ✅ Configured webhooks for external integrations
- ✅ Tested event-driven automation

Your Nautobot changes now automatically sync to your network devices!

---

## 9. Next Steps

Now that event-driven automation is working, proceed to **Part 12: Floorplan Plugin** to:
- Enable and configure the Floorplan plugin
- Create visual floor plans for network sites
- Map devices to physical locations

---

*Happy automating! 🚀*

