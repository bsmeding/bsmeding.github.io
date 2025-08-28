---
authors: [bsmeding]
date: 2025-10-13
title: Nautobot in Action – Part 6
tags: ["network automation", "deployment", "nautobot", "validation"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot in Action – Part 6
## Full Device Deployment, ZTP & Site Validation
*Deploy new devices with Zero-Touch Provisioning and validate site configurations.*

<!-- more -->

---

## Index
- [Nautobot in Action – Part 6](#nautobot-in-action--part-6)
  - [Full Device Deployment, ZTP \& Site Validation](#full-device-deployment-ztp--site-validation)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Push Intended Configs to Devices](#3-push-intended-configs-to-devices)
    - [3.1 Full Configuration Deployment](#31-full-configuration-deployment)
    - [3.2 Multi-Vendor Deployment](#32-multi-vendor-deployment)
  - [4. Zero-Touch Provisioning (ZTP) Integration](#4-zero-touch-provisioning-ztp-integration)
    - [4.1 ZTP Server Integration](#41-ztp-server-integration)
    - [4.2 ZTP Template Generation](#42-ztp-template-generation)
  - [5. Site Validation](#5-site-validation)
    - [5.1 LLDP/CDP Validation](#51-lldpcdp-validation)
    - [5.2 VLAN and IP Validation](#52-vlan-and-ip-validation)
  - [6. Force Compliance Push](#6-force-compliance-push)
    - [6.1 Force Compliance Job](#61-force-compliance-job)
    - [6.2 Emergency Remediation](#62-emergency-remediation)
  - [7. Site Compliance Reporting](#7-site-compliance-reporting)
    - [7.1 Comprehensive Site Report](#71-comprehensive-site-report)
    - [7.2 Report Distribution](#72-report-distribution)
  - [8. Wrap-Up](#8-wrap-up)
    - [What We Accomplished](#what-we-accomplished)
    - [Key Takeaways](#key-takeaways)
  - [9. Next Steps](#9-next-steps)

---

## 1. Introduction
In this final part of the core series, we'll implement full device deployment with Zero-Touch Provisioning (ZTP) and comprehensive site validation. This brings our automation solution to production readiness.

We'll:
1. Push intended configs to startup/running configs
2. Integrate with ZTP server
3. Validate site cabling (LLDP/CDP) and VLAN/IP assignments
4. Implement force compliance push option
5. Generate site compliance reports

> **Estimated Time:** ~2 hours

---

## 2. Prerequisites
- Completed Parts 1-5 of this series
- Golden Config plugin configured
- ZTP server available
- Network devices with LLDP/CDP enabled

---

## 3. Push Intended Configs to Devices

### 3.1 Full Configuration Deployment
```python
# jobs/full_deployment.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class FullDeviceDeploymentJob(Job):
    class Meta:
        name = "Full Device Deployment"
        description = "Deploy complete intended configurations to devices"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        
        for device in devices:
            try:
                # Generate intended config
                intended_config = self.generate_intended_config(device)
                
                # Push to running config
                self.push_running_config(device, intended_config)
                
                # Push to startup config
                self.push_startup_config(device, intended_config)
                
                self.log_success(f"Successfully deployed full config to {device.name}")
                
            except Exception as e:
                self.log_error(f"Failed to deploy config to {device.name}: {e}")
```

### 3.2 Multi-Vendor Deployment
```python
def push_running_config(self, device, config):
    """Push configuration to running config"""
    platform = device.platform.name
    
    if platform == "cisco_ios":
        return self.push_cisco_running_config(device, config)
    elif platform == "arista_eos":
        return self.push_arista_running_config(device, config)
    elif platform == "juniper_junos":
        return self.push_juniper_running_config(device, config)

def push_startup_config(self, device, config):
    """Push configuration to startup config"""
    platform = device.platform.name
    
    if platform == "cisco_ios":
        return self.push_cisco_startup_config(device, config)
    elif platform == "arista_eos":
        return self.push_arista_startup_config(device, config)
    elif platform == "juniper_junos":
        return self.push_juniper_startup_config(device, config)
```

---

## 4. Zero-Touch Provisioning (ZTP) Integration

### 4.1 ZTP Server Integration
```python
# jobs/ztp_integration.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class ZTPIntegrationJob(Job):
    class Meta:
        name = "ZTP Integration"
        description = "Integrate with Zero-Touch Provisioning server"

    def run(self, data, commit):
        # Configure ZTP server
        self.configure_ztp_server()
        
        # Register devices for ZTP
        devices = Device.objects.filter(status="planned")
        for device in devices:
            self.register_device_for_ztp(device)
        
        # Monitor ZTP progress
        self.monitor_ztp_progress()

def configure_ztp_server(self):
    """Configure ZTP server settings"""
    ztp_config = {
        "server_url": "http://ztp-server:8080",
        "config_template_path": "/templates/ztp/",
        "dhcp_server": "192.168.1.1",
        "tftp_server": "192.168.1.10"
    }
    
    # Apply ZTP configuration
    self.apply_ztp_configuration(ztp_config)
```

### 4.2 ZTP Template Generation
```python
def generate_ztp_template(self, device):
    """Generate ZTP template for device"""
    template_vars = {
        'device_name': device.name,
        'management_ip': device.primary_ip4.address.ip,
        'gateway': device.primary_ip4.address.network.gateway,
        'site_name': device.site.name,
        'role_name': device.role.name
    }
    
    # Generate platform-specific ZTP template
    platform = device.platform.name
    if platform == "cisco_ios":
        return self.generate_cisco_ztp_template(template_vars)
    elif platform == "arista_eos":
        return self.generate_arista_ztp_template(template_vars)
    elif platform == "juniper_junos":
        return self.generate_juniper_ztp_template(template_vars)
```

---

## 5. Site Validation

### 5.1 LLDP/CDP Validation
```python
# jobs/site_validation.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device, Site

class SiteValidationJob(Job):
    class Meta:
        name = "Site Validation"
        description = "Validate site cabling and configurations"

    def run(self, data, commit):
        sites = Site.objects.all()
        
        for site in sites:
            self.validate_site_cabling(site)
            self.validate_vlan_assignments(site)
            self.validate_ip_assignments(site)

def validate_site_cabling(self, site):
    """Validate site cabling using LLDP/CDP"""
    devices = Device.objects.filter(site=site, status="active")
    
    for device in devices:
        try:
            # Collect LLDP/CDP information
            lldp_neighbors = self.collect_lldp_neighbors(device)
            cdp_neighbors = self.collect_cdp_neighbors(device)
            
            # Validate against Nautobot topology
            self.validate_topology_consistency(device, lldp_neighbors, cdp_neighbors)
            
        except Exception as e:
            self.log_warning(f"Failed to validate cabling for {device.name}: {e}")
```

### 5.2 VLAN and IP Validation
```python
def validate_vlan_assignments(self, site):
    """Validate VLAN assignments across site"""
    devices = Device.objects.filter(site=site, status="active")
    
    for device in devices:
        try:
            # Check VLAN consistency
            intended_vlans = self.get_intended_vlans(device)
            actual_vlans = self.get_actual_vlans(device)
            
            if intended_vlans != actual_vlans:
                self.log_warning(f"VLAN mismatch on {device.name}")
                self.remediate_vlan_assignments(device)
                
        except Exception as e:
            self.log_warning(f"Failed to validate VLANs for {device.name}: {e}")

def validate_ip_assignments(self, site):
    """Validate IP assignments across site"""
    devices = Device.objects.filter(site=site, status="active")
    
    for device in devices:
        try:
            # Check IP consistency
            intended_ips = self.get_intended_ips(device)
            actual_ips = self.get_actual_ips(device)
            
            if intended_ips != actual_ips:
                self.log_warning(f"IP mismatch on {device.name}")
                self.remediate_ip_assignments(device)
                
        except Exception as e:
            self.log_warning(f"Failed to validate IPs for {device.name}: {e}")
```

---

## 6. Force Compliance Push

### 6.1 Force Compliance Job
```python
# jobs/force_compliance.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device

class ForceComplianceJob(Job):
    class Meta:
        name = "Force Compliance Push"
        description = "Force push compliance configurations to devices"

    def run(self, data, commit):
        devices = Device.objects.filter(status="active")
        
        for device in devices:
            try:
                # Force compliance check
                if not self.check_compliance(device):
                    self.log_warning(f"Device {device.name} is non-compliant, forcing remediation")
                    
                    # Generate remediation config
                    remediation_config = self.generate_remediation_config(device)
                    
                    # Force push to device
                    self.force_push_config(device, remediation_config)
                    
                    # Verify compliance after push
                    if self.check_compliance(device):
                        self.log_success(f"Successfully forced compliance for {device.name}")
                    else:
                        self.log_error(f"Force compliance failed for {device.name}")
                        
            except Exception as e:
                self.log_error(f"Error during force compliance for {device.name}: {e}")
```

### 6.2 Emergency Remediation
```python
def emergency_remediation(self, device):
    """Emergency remediation for critical devices"""
    try:
        # Backup current configuration
        self.backup_current_config(device)
        
        # Generate emergency config
        emergency_config = self.generate_emergency_config(device)
        
        # Force push emergency config
        self.force_push_config(device, emergency_config)
        
        # Verify device is operational
        if self.verify_device_operational(device):
            self.log_success(f"Emergency remediation successful for {device.name}")
            return True
        else:
            self.log_error(f"Emergency remediation failed for {device.name}")
            return False
            
    except Exception as e:
        self.log_error(f"Emergency remediation error for {device.name}: {e}")
        return False
```

---

## 7. Site Compliance Reporting

### 7.1 Comprehensive Site Report
```python
# jobs/site_compliance_report.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Site

class SiteComplianceReportJob(Job):
    class Meta:
        name = "Site Compliance Report"
        description = "Generate comprehensive site compliance reports"

    def run(self, data, commit):
        sites = Site.objects.all()
        
        for site in sites:
            report = self.generate_site_report(site)
            self.save_report(site, report)
            self.send_report_notification(site, report)

def generate_site_report(self, site):
    """Generate comprehensive site compliance report"""
    devices = Device.objects.filter(site=site, status="active")
    
    report = {
        "site_name": site.name,
        "total_devices": len(devices),
        "compliant_devices": 0,
        "non_compliant_devices": 0,
        "device_details": {},
        "cabling_issues": [],
        "vlan_issues": [],
        "ip_issues": [],
        "overall_compliance": 0.0
    }
    
    for device in devices:
        device_status = self.check_device_compliance(device)
        report["device_details"][device.name] = device_status
        
        if device_status["compliant"]:
            report["compliant_devices"] += 1
        else:
            report["non_compliant_devices"] += 1
    
    # Calculate overall compliance percentage
    if report["total_devices"] > 0:
        report["overall_compliance"] = (report["compliant_devices"] / report["total_devices"]) * 100
    
    return report
```

### 7.2 Report Distribution
```python
def send_report_notification(self, site, report):
    """Send compliance report notifications"""
    if report["overall_compliance"] < 90:
        # Send alert for low compliance
        self.send_alert_notification(site, report)
    
    # Send regular report
    self.send_regular_report(site, report)

def send_alert_notification(self, site, report):
    """Send alert for compliance issues"""
    alert_message = f"""
    ALERT: Site {site.name} Compliance Issues
    
    Overall Compliance: {report['overall_compliance']:.1f}%
    Non-compliant devices: {report['non_compliant_devices']}
    
    Please review and remediate compliance issues.
    """
    
    # Send via email, Slack, etc.
    self.send_notification(alert_message)
```

---

## 8. Wrap-Up

### What We Accomplished
- ✅ Implemented full device deployment
- ✅ Integrated with ZTP server
- ✅ Created comprehensive site validation
- ✅ Built force compliance push capability
- ✅ Generated detailed site compliance reports
- ✅ Achieved production-ready automation

### Key Takeaways
- Full deployment requires both running and startup config management
- ZTP integration enables automated device onboarding
- Site validation ensures network consistency
- Force compliance provides emergency remediation options
- Comprehensive reporting enables proactive management

---

## 9. Next Steps

Congratulations! You've completed the core Nautobot automation series. You now have a production-ready network automation solution.

**Optional Advanced Topics (Parts 7-10):**
- Part 7: API Integrations with external tools
- Part 8: GitOps-style change management
- Part 9: Multi-vendor compliance pipelines
- Part 10: Golden Config for firewalls and wireless controllers

---

*You've successfully built a complete network automation solution! 🚀*
