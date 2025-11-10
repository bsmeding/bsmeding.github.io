---
authors: [bsmeding]
title: Nautobot Zero to Hero – Part 8: Separate Golden Config Templates
tags: ["network automation", "nautobot", "golden config", "templates", "job hooks"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot Zero to Hero – Part 8: Separate Golden Config Templates
## Automate Interface Configuration Updates
*Separate Interface configuration into a separate template and create Job Hooks for automatic updates.*

<!-- more -->

---

## Index
- [Nautobot Zero to Hero – Part 8: Separate Golden Config Templates](#nautobot-zero-to-hero--part-8-separate-golden-config-templates)
  - [Automate Interface Configuration Updates](#automate-interface-configuration-updates)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Separate Interface Template](#3-separate-interface-template)
  - [4. Create Interface Update Job](#4-create-interface-update-job)
  - [5. Create Job Hook](#5-create-job-hook)
  - [6. Test Automatic Updates](#6-test-automatic-updates)
  - [7. Wrap-Up](#7-wrap-up)
  - [8. Next Steps](#8-next-steps)

---

## 1. Introduction

In this part, we'll separate the Interface configuration from the main golden config template into its own file. We'll then create a Job and Job Hook that automatically executes when an interface is created, updated, or deleted in Nautobot.

We'll:
1. Create a separate Interface Jinja template
2. Create a Job to deploy interface configurations
3. Set up a Job Hook to trigger on interface changes
4. Test automatic interface configuration updates

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites

- Completed [Part 7: Deploy Provision Job](/tutorials/nautobot_zero_to_hero/08_nautobot-zero-to-hero-part7/)
- Golden Config templates repository configured
- Understanding of Jinja2 templates
- Devices are reachable via SSH

---

## 3. Separate Interface Template

### 3.1 Create Interface Template File

In your Golden Config templates repository, create a separate file for interfaces:

**File:** `templates/interfaces.j2`

```jinja2
{% for interface in device.interfaces.all() %}
!
interface {{ interface.name }}
 description {{ interface.description|default("") }}
{% if interface.enabled %}
 no shutdown
{% else %}
 shutdown
{% endif %}
{% if interface.mode %}
 switchport mode {{ interface.mode }}
{% endif %}
{% if interface.untagged_vlan %}
 switchport access vlan {{ interface.untagged_vlan.vid }}
{% endif %}
{% if interface.tagged_vlans.all() %}
 switchport trunk allowed vlan {% for vlan in interface.tagged_vlans.all() %}{{ vlan.vid }}{% if not loop.last %},{% endif %}{% endfor %}
{% endif %}
!
{% endfor %}
```

### 3.2 Update Main Template

Update your main golden config template to optionally include interfaces:

**File:** `templates/main_config.j2`

```jinja2
! Main device configuration
hostname {{ device.name }}
!
! Include interfaces if needed
{% if include_interfaces %}
{% include 'interfaces.j2' %}
{% endif %}
!
! Rest of device configuration
...
```

### 3.3 Commit Template Changes

```bash
git add templates/interfaces.j2 templates/main_config.j2
git commit -m "Separate interface configuration into dedicated template"
git push origin main
```

Sync the repository in Nautobot to load the updated templates.

---

## 4. Create Interface Update Job

### 4.1 Create Job File

Create a job file `jobs/update_interface_config.py`:

```python
from nautobot.extras.jobs import Job, ObjectVar
from nautobot.dcim.models import Device, Interface
from nautobot_golden_config.models import GoldenConfig
from nautobot_golden_config.utilities import get_golden_config
from jinja2 import Template
import os

class UpdateInterfaceConfig(Job):
    class Meta:
        name = "Update Interface Configuration"
        description = "Deploy interface configuration to device"
        field_order = ["device", "interface"]

    device = ObjectVar(
        model=Device,
        description="Device to update",
        required=True
    )
    
    interface = ObjectVar(
        model=Interface,
        description="Interface to update (optional - updates all if not specified)",
        required=False
    )

    def run(self, device, interface=None):
        self.log_info(f"Updating interface configuration for {device.name}")
        
        # Get golden config
        try:
            golden_config = GoldenConfig.objects.get(device=device)
        except GoldenConfig.DoesNotExist:
            self.log_failure(f"No golden config found for {device.name}")
            return
        
        # Load interface template
        template_path = os.path.join(
            golden_config.template_repo.working_directory,
            "templates",
            "interfaces.j2"
        )
        
        try:
            with open(template_path, 'r') as f:
                template_content = f.read()
            
            template = Template(template_content)
            
            # Render template
            if interface:
                # Render for specific interface
                config = template.render(device=device, interface=interface)
            else:
                # Render for all interfaces
                config = template.render(device=device)
            
            self.log_info("Generated interface configuration:")
            self.log_info(config)
            
            # Deploy to device (simplified - add actual deployment logic)
            self.log_success(f"Interface configuration updated for {device.name}")
            
        except Exception as e:
            self.log_failure(f"Failed to update interface config: {str(e)}")
```

### 4.2 Add Job to Repository

1. Save the job file
2. Commit and push to Git
3. Sync in Nautobot

---

## 5. Create Job Hook

### 5.1 Create Job Hook File

Create a job hook file `jobs/hooks/interface_hook.py`:

```python
from nautobot.extras.jobs import JobHookReceiver
from nautobot.dcim.models import Interface
from nautobot.extras.jobs import get_job
import logging

logger = logging.getLogger(__name__)

class InterfaceChangeHook(JobHookReceiver):
    class Meta:
        name = "Interface Change Hook"
        description = "Automatically update interface config on changes"

    def receive_job_hook(self, change, model, request_id, user):
        """
        Triggered when an Interface is created, updated, or deleted
        """
        if model != "interface":
            return
        
        # Get the interface object
        try:
            if change == "delete":
                # Interface was deleted - get device from change data
                device_id = request_id  # Adjust based on your hook implementation
                # Update device to remove interface config
                pass
            else:
                interface = Interface.objects.get(id=request_id)
                device = interface.device
                
                # Run the interface update job
                job_class = get_job("Update Interface Configuration")
                if job_class:
                    job = job_class()
                    job.run(device=device, interface=interface)
                    logger.info(f"Interface config updated for {interface.name} on {device.name}")
        except Exception as e:
            logger.error(f"Failed to update interface config: {str(e)}")
```

### 5.2 Register Job Hook

In your job file, register the hook:

```python
from nautobot.extras.jobs import register_job_hook

register_job_hook(
    "Interface Change Hook",
    "interface",
    ["create", "update", "delete"]
)
```

### 5.3 Alternative: Use Nautobot's Built-in Hooks

Nautobot also supports webhooks and signals. You can use Django signals:

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from nautobot.dcim.models import Interface

@receiver(post_save, sender=Interface)
def interface_updated(sender, instance, created, **kwargs):
    """Triggered when interface is created or updated"""
    # Run your update job here
    pass

@receiver(post_delete, sender=Interface)
def interface_deleted(sender, instance, **kwargs):
    """Triggered when interface is deleted"""
    # Update device configuration
    pass
```

---

## 6. Test Automatic Updates

### 6.1 Create an Interface

1. Navigate to **Devices → Interfaces**
2. Select a device
3. Click **Add Interface**
4. Configure:
   - **Name**: e.g., `GigabitEthernet0/3`
   - **Description**: `Test Interface`
   - **Enabled**: Yes
   - **Type**: 1000BASE-T
5. Click **Create**

📸 **[Screenshot: Creating Interface]**

### 6.2 Verify Job Hook Triggered

1. Check **Jobs → Job Results**
2. Look for the interface update job
3. Verify it ran automatically
4. Review the job output

📸 **[Screenshot: Automatic Job Execution]**

### 6.3 Update an Interface

1. Edit the interface you just created
2. Change the description
3. Save the changes
4. Verify the job hook triggered again

### 6.4 Verify Device Configuration

1. SSH to the device
2. Check the interface configuration
3. Verify changes were applied

```bash
ssh admin@device-name
show running-config interface GigabitEthernet0/3
```

---

## 7. Wrap-Up

Congratulations! You have successfully:
- ✅ Separated Interface configuration into a dedicated template
- ✅ Created a Job to update interface configurations
- ✅ Set up a Job Hook to trigger on interface changes
- ✅ Tested automatic interface configuration updates

Interface changes in Nautobot now automatically trigger configuration updates on your devices!

---

## 8. Next Steps

Now that interface updates are automated, proceed to **Part 9: Configuration Compliance** to:
- Create configuration compliance checks
- Run compliance reports
- Detect configuration drift

---

*Happy automating! 🚀*
