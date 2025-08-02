---
title: "Nautobot: The Ultimate Network Automation Platform for NetDevOps"
authors: [bsmeding]
date: 2024-05-20
summary: Discover how Nautobot serves as a comprehensive network automation platform, providing source of truth, automation workflows, and integration capabilities for modern NetDevOps environments.
tags:
  - nautobot
  - network automation
  - netdevops
  - source of truth
  - automation
  - networking
---

# Nautobot: The Ultimate Network Automation Platform for NetDevOps

**Nautobot** has emerged as a leading network automation platform, providing a comprehensive solution for network source of truth, automation workflows, and integration capabilities. This guide explores how Nautobot serves as the foundation for modern NetDevOps environments.

<!-- more -->

## What is Nautobot?

Nautobot is an open-source network automation platform that provides:

- **Network Source of Truth (SSoT)**: Centralized repository for network data
- **Network Automation**: Built-in automation capabilities and workflows
- **API-First Design**: RESTful API for seamless integration
- **Extensible Architecture**: Plugin system for custom functionality
- **Web Interface**: Intuitive web UI for network management
- **Git Integration**: Version control for network configurations

## Core Features and Capabilities

### 1. Network Source of Truth

Nautobot serves as a centralized repository for all network-related data:

```python
# Example: Network device data model
from nautobot.dcim.models import Device, Site, Rack
from nautobot.ipam.models import IPAddress, Prefix, VLAN

# Device management
device = Device.objects.create(
    name="router-core-01",
    device_type=device_type,
    site=site,
    status=status_active,
    primary_ip4=primary_ip,
    platform=platform_ios
)

# IP address management
ip_address = IPAddress.objects.create(
    address="192.168.1.1/24",
    status=status_active,
    assigned_object=device
)

# VLAN management
vlan = VLAN.objects.create(
    vid=100,
    name="DATA",
    site=site,
    status=status_active
)
```

### 2. RESTful API

Nautobot provides a comprehensive REST API for programmatic access:

```python
# API client example
import requests
import json

class NautobotAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
    
    def get_devices(self):
        """Get all devices"""
        response = requests.get(
            f"{self.base_url}/api/dcim/devices/",
            headers=self.headers
        )
        return response.json()
    
    def create_device(self, device_data):
        """Create a new device"""
        response = requests.post(
            f"{self.base_url}/api/dcim/devices/",
            headers=self.headers,
            json=device_data
        )
        return response.json()
    
    def update_device(self, device_id, device_data):
        """Update an existing device"""
        response = requests.patch(
            f"{self.base_url}/api/dcim/devices/{device_id}/",
            headers=self.headers,
            json=device_data
        )
        return response.json()
    
    def delete_device(self, device_id):
        """Delete a device"""
        response = requests.delete(
            f"{self.base_url}/api/dcim/devices/{device_id}/",
            headers=self.headers
        )
        return response.status_code == 204

# Usage example
api = NautobotAPI("https://nautobot.example.com", "your-token")

# Get all devices
devices = api.get_devices()
print(f"Found {len(devices['results'])} devices")

# Create a new device
new_device = {
    "name": "switch-access-01",
    "device_type": 1,
    "site": 1,
    "status": "active",
    "platform": 1
}
result = api.create_device(new_device)
print(f"Created device: {result['name']}")
```

### 3. Custom Jobs and Automation

Nautobot supports custom jobs for automation workflows:

```python
# Custom job example
from nautobot.core.jobs import Job, StringVar, ObjectVar
from nautobot.dcim.models import Device
from nautobot.ipam.models import IPAddress

class DeviceConfigurationJob(Job):
    """Job to configure network devices"""
    
    class Meta:
        name = "Device Configuration"
        description = "Configure network devices with specified settings"
    
    # Job variables
    device = ObjectVar(
        model=Device,
        description="Device to configure"
    )
    configuration_type = StringVar(
        description="Type of configuration to apply",
        choices=[
            ("vlan", "VLAN Configuration"),
            ("routing", "Routing Configuration"),
            ("security", "Security Configuration")
        ]
    )
    
    def run(self, data, commit):
        device = data['device']
        config_type = data['configuration_type']
        
        self.log_info(f"Starting configuration for {device.name}")
        
        try:
            if config_type == "vlan":
                self.configure_vlans(device)
            elif config_type == "routing":
                self.configure_routing(device)
            elif config_type == "security":
                self.configure_security(device)
            
            self.log_success(f"Configuration completed for {device.name}")
            
        except Exception as e:
            self.log_error(f"Configuration failed for {device.name}: {str(e)}")
            raise
    
    def configure_vlans(self, device):
        """Configure VLANs on device"""
        vlans = device.site.vlans.filter(status='active')
        
        for vlan in vlans:
            self.log_info(f"Configuring VLAN {vlan.vid} - {vlan.name}")
            # Implementation would generate and apply VLAN configuration
    
    def configure_routing(self, device):
        """Configure routing on device"""
        self.log_info("Configuring routing protocols")
        # Implementation would configure routing protocols
    
    def configure_security(self, device):
        """Configure security on device"""
        self.log_info("Configuring security settings")
        # Implementation would configure security policies
```

## Integration with Network Automation Tools

### Ansible Integration

```yaml
# Ansible inventory plugin for Nautobot
# inventory/nautobot.yml
plugin: nautobot
api_token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
query_filters:
  - status: active
group_by:
  - site
  - rack
  - device_type
```

```yaml
# Ansible playbook using Nautobot data
---
- name: Configure Network Devices from Nautobot
  hosts: all
  gather_facts: no
  
  vars:
    nautobot_url: "https://nautobot.example.com"
    nautobot_token: "{{ vault_nautobot_token }}"
  
  tasks:
    - name: Get device information from Nautobot
      uri:
        url: "{{ nautobot_url }}/api/dcim/devices/?name={{ inventory_hostname }}"
        method: GET
        headers:
          Authorization: "Token {{ nautobot_token }}"
          Content-Type: "application/json"
      register: device_info
      delegate_to: localhost
    
    - name: Set device facts
      set_fact:
        device_data: "{{ device_info.json.results[0] }}"
        primary_ip: "{{ device_data.primary_ip4.address | default('') }}"
        site_name: "{{ device_data.site.name }}"
        device_type: "{{ device_data.device_type.model }}"
    
    - name: Configure device based on Nautobot data
      cisco.ios.config:
        lines: "{{ item }}"
        parents: "{{ item.parents | default([]) }}"
      loop: "{{ lookup('template', 'configs/' + device_type + '.j2') | from_yaml }}"
      when: device_data.status == 'active'
```

### Terraform Integration

```hcl
# Terraform provider for Nautobot
terraform {
  required_providers {
    nautobot = {
      source = "nautobot/nautobot"
      version = "~> 1.0"
    }
  }
}

provider "nautobot" {
  url   = "https://nautobot.example.com"
  token = var.nautobot_token
}

# Create a site
resource "nautobot_site" "main" {
  name = "Main Data Center"
  slug = "main-dc"
  status = "active"
}

# Create a device
resource "nautobot_device" "router" {
  name = "router-core-01"
  device_type_id = data.nautobot_device_type.router.id
  site_id = nautobot_site.main.id
  status = "active"
  platform_id = data.nautobot_platform.ios.id
}

# Create IP addresses
resource "nautobot_ip_address" "primary" {
  address = "192.168.1.1/24"
  status = "active"
  assigned_object_type = "dcim.device"
  assigned_object_id = nautobot_device.router.id
}

# Data sources
data "nautobot_device_type" "router" {
  model = "ISR4321"
}

data "nautobot_platform" "ios" {
  name = "Cisco IOS"
}
```

## Advanced Automation Workflows

### Network Provisioning Workflow

```python
# Network provisioning workflow
from nautobot.core.jobs import Job, ObjectVar, StringVar
from nautobot.dcim.models import Device, Site, Rack
from nautobot.ipam.models import IPAddress, Prefix, VLAN

class NetworkProvisioningJob(Job):
    """Automated network provisioning workflow"""
    
    class Meta:
        name = "Network Provisioning"
        description = "Provision new network infrastructure"
    
    site = ObjectVar(
        model=Site,
        description="Site for new infrastructure"
    )
    device_type = StringVar(
        description="Type of device to provision",
        choices=[
            ("router", "Router"),
            ("switch", "Switch"),
            ("firewall", "Firewall")
        ]
    )
    quantity = StringVar(
        description="Number of devices to provision",
        default="1"
    )
    
    def run(self, data, commit):
        site = data['site']
        device_type = data['device_type']
        quantity = int(data['quantity'])
        
        self.log_info(f"Starting provisioning of {quantity} {device_type}(s) at {site.name}")
        
        try:
            # Allocate IP addresses
            ip_addresses = self.allocate_ip_addresses(site, quantity)
            
            # Create devices
            devices = self.create_devices(site, device_type, quantity, ip_addresses)
            
            # Configure devices
            self.configure_devices(devices)
            
            # Update documentation
            self.update_documentation(devices)
            
            self.log_success(f"Successfully provisioned {quantity} {device_type}(s)")
            
        except Exception as e:
            self.log_error(f"Provisioning failed: {str(e)}")
            raise
    
    def allocate_ip_addresses(self, site, quantity):
        """Allocate IP addresses for new devices"""
        ip_addresses = []
        
        # Find available prefix
        prefix = Prefix.objects.filter(
            site=site,
            status='active',
            prefix='192.168.1.0/24'
        ).first()
        
        if not prefix:
            raise Exception("No available prefix found")
        
        # Find available IP addresses
        used_ips = set(IPAddress.objects.filter(
            address__net_contained_or_equal=prefix.prefix
        ).values_list('address', flat=True))
        
        for i in range(quantity):
            for j in range(2, 255):
                candidate_ip = f"192.168.1.{j}/24"
                if candidate_ip not in used_ips:
                    ip_address = IPAddress.objects.create(
                        address=candidate_ip,
                        status='reserved'
                    )
                    ip_addresses.append(ip_address)
                    break
        
        return ip_addresses
    
    def create_devices(self, site, device_type, quantity, ip_addresses):
        """Create device records"""
        devices = []
        
        for i in range(quantity):
            device_name = f"{device_type}-{site.slug}-{i+1:02d}"
            
            device = Device.objects.create(
                name=device_name,
                site=site,
                device_type_id=self.get_device_type_id(device_type),
                status='planned',
                primary_ip4=ip_addresses[i] if i < len(ip_addresses) else None
            )
            
            devices.append(device)
            self.log_info(f"Created device: {device_name}")
        
        return devices
    
    def configure_devices(self, devices):
        """Configure devices via automation"""
        for device in devices:
            self.log_info(f"Configuring {device.name}")
            # Implementation would trigger Ansible playbook or other automation
    
    def update_documentation(self, devices):
        """Update network documentation"""
        self.log_info("Updating network documentation")
        # Implementation would update documentation systems
```

### Network Monitoring Integration

```python
# Network monitoring integration
from nautobot.core.jobs import Job
from nautobot.dcim.models import Device
import requests
import json

class NetworkMonitoringJob(Job):
    """Network monitoring and health check job"""
    
    class Meta:
        name = "Network Monitoring"
        description = "Monitor network device health and status"
    
    def run(self, data, commit):
        self.log_info("Starting network monitoring")
        
        # Get all active devices
        devices = Device.objects.filter(status='active')
        
        for device in devices:
            try:
                health_status = self.check_device_health(device)
                self.update_device_status(device, health_status)
                
            except Exception as e:
                self.log_error(f"Error monitoring {device.name}: {str(e)}")
    
    def check_device_health(self, device):
        """Check device health via SNMP or API"""
        if not device.primary_ip4:
            return {'status': 'unknown', 'error': 'No primary IP'}
        
        ip_address = str(device.primary_ip4.address.ip)
        
        try:
            # Check device reachability
            response = requests.get(
                f"http://{ip_address}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                return {'status': 'healthy', 'response_time': response.elapsed.total_seconds()}
            else:
                return {'status': 'unhealthy', 'error': f"HTTP {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {'status': 'unreachable', 'error': str(e)}
    
    def update_device_status(self, device, health_status):
        """Update device status in Nautobot"""
        if health_status['status'] == 'healthy':
            self.log_info(f"{device.name}: Healthy")
        elif health_status['status'] == 'unhealthy':
            self.log_warning(f"{device.name}: Unhealthy - {health_status.get('error', 'Unknown error')}")
        else:
            self.log_error(f"{device.name}: Unreachable - {health_status.get('error', 'Unknown error')}")
```

## Custom Plugins and Extensions

### Custom Device Type Plugin

```python
# Custom device type plugin
from nautobot.core.api import ValidatedModelSerializer
from nautobot.core.models import BaseModel
from django.db import models

class CustomDeviceType(BaseModel):
    """Custom device type with additional fields"""
    
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    power_consumption = models.IntegerField(help_text="Power consumption in watts")
    rack_units = models.IntegerField(help_text="Rack units required")
    
    class Meta:
        ordering = ['manufacturer', 'model']

class CustomDeviceTypeSerializer(ValidatedModelSerializer):
    """API serializer for custom device type"""
    
    class Meta:
        model = CustomDeviceType
        fields = [
            'id', 'name', 'manufacturer', 'model',
            'power_consumption', 'rack_units', 'created', 'last_updated'
        ]
```

### Custom Automation Plugin

```python
# Custom automation plugin
from nautobot.core.jobs import Job, ObjectVar
from nautobot.dcim.models import Device

class CustomAutomationJob(Job):
    """Custom automation job"""
    
    class Meta:
        name = "Custom Automation"
        description = "Custom network automation workflow"
    
    device = ObjectVar(
        model=Device,
        description="Device to automate"
    )
    
    def run(self, data, commit):
        device = data['device']
        
        self.log_info(f"Running custom automation on {device.name}")
        
        # Custom automation logic here
        result = self.execute_custom_automation(device)
        
        if result['success']:
            self.log_success(f"Custom automation completed for {device.name}")
        else:
            self.log_error(f"Custom automation failed for {device.name}: {result['error']}")
    
    def execute_custom_automation(self, device):
        """Execute custom automation logic"""
        # Implementation would contain custom automation logic
        return {'success': True, 'message': 'Automation completed'}
```

## Best Practices for Nautobot Implementation

### 1. Data Modeling

```python
# Best practices for data modeling
from nautobot.dcim.models import Device, Site, Rack
from nautobot.ipam.models import IPAddress, Prefix, VLAN

class NetworkDataManager:
    """Network data management best practices"""
    
    @staticmethod
    def create_device_with_validation(name, site, device_type):
        """Create device with proper validation"""
        # Check for duplicate names
        if Device.objects.filter(name=name).exists():
            raise ValueError(f"Device {name} already exists")
        
        # Validate site exists
        if not Site.objects.filter(id=site.id).exists():
            raise ValueError("Invalid site")
        
        # Create device
        device = Device.objects.create(
            name=name,
            site=site,
            device_type=device_type,
            status='active'
        )
        
        return device
    
    @staticmethod
    def allocate_ip_address(device, prefix):
        """Allocate IP address for device"""
        # Find available IP in prefix
        used_ips = set(IPAddress.objects.filter(
            address__net_contained_or_equal=prefix
        ).values_list('address', flat=True))
        
        for i in range(2, 255):
            candidate_ip = f"{prefix.network_address + i}/24"
            if candidate_ip not in used_ips:
                ip_address = IPAddress.objects.create(
                    address=candidate_ip,
                    status='active',
                    assigned_object=device
                )
                return ip_address
        
        raise ValueError("No available IP addresses in prefix")
```

### 2. API Usage

```python
# Best practices for API usage
import requests
from typing import Dict, List, Optional

class NautobotAPIClient:
    """Nautobot API client with best practices"""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        })
    
    def get_devices(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get devices with pagination support"""
        url = f"{self.base_url}/api/dcim/devices/"
        params = filters or {}
        
        all_results = []
        
        while url:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            all_results.extend(data['results'])
            
            url = data.get('next')
            params = {}  # Clear params for subsequent requests
        
        return all_results
    
    def create_device(self, device_data: Dict) -> Dict:
        """Create device with validation"""
        # Validate required fields
        required_fields = ['name', 'device_type', 'site']
        for field in required_fields:
            if field not in device_data:
                raise ValueError(f"Missing required field: {field}")
        
        response = self.session.post(
            f"{self.base_url}/api/dcim/devices/",
            json=device_data
        )
        response.raise_for_status()
        
        return response.json()
    
    def update_device(self, device_id: int, device_data: Dict) -> Dict:
        """Update device with validation"""
        response = self.session.patch(
            f"{self.base_url}/api/dcim/devices/{device_id}/",
            json=device_data
        )
        response.raise_for_status()
        
        return response.json()
```

### 3. Job Development

```python
# Best practices for job development
from nautobot.core.jobs import Job, ObjectVar, StringVar
from nautobot.dcim.models import Device
import logging

class BestPracticeJob(Job):
    """Job with best practices implementation"""
    
    class Meta:
        name = "Best Practice Job"
        description = "Example job with best practices"
    
    device = ObjectVar(
        model=Device,
        description="Target device"
    )
    action = StringVar(
        description="Action to perform",
        choices=[
            ("backup", "Backup Configuration"),
            ("deploy", "Deploy Configuration"),
            ("verify", "Verify Configuration")
        ]
    )
    
    def run(self, data, commit):
        device = data['device']
        action = data['action']
        
        # Set up logging
        logger = logging.getLogger(__name__)
        
        try:
            self.log_info(f"Starting {action} for {device.name}")
            
            # Execute action
            if action == "backup":
                result = self.backup_configuration(device)
            elif action == "deploy":
                result = self.deploy_configuration(device)
            elif action == "verify":
                result = self.verify_configuration(device)
            
            # Log results
            if result['success']:
                self.log_success(f"{action} completed successfully for {device.name}")
                logger.info(f"Job completed: {action} for {device.name}")
            else:
                self.log_error(f"{action} failed for {device.name}: {result['error']}")
                logger.error(f"Job failed: {action} for {device.name} - {result['error']}")
            
        except Exception as e:
            error_msg = f"Unexpected error during {action}: {str(e)}"
            self.log_error(error_msg)
            logger.exception(error_msg)
            raise
    
    def backup_configuration(self, device):
        """Backup device configuration"""
        # Implementation
        return {'success': True, 'backup_file': f"{device.name}_config.txt"}
    
    def deploy_configuration(self, device):
        """Deploy configuration to device"""
        # Implementation
        return {'success': True, 'deployed': True}
    
    def verify_configuration(self, device):
        """Verify device configuration"""
        # Implementation
        return {'success': True, 'verified': True}
```

## Conclusion

Nautobot provides a comprehensive platform for network automation in NetDevOps environments. By implementing the patterns and best practices outlined in this guide, organizations can achieve:

- **Centralized Network Management**: Single source of truth for network data
- **Automated Workflows**: Streamlined network operations
- **Integration Capabilities**: Seamless integration with existing tools
- **Scalability**: Support for large-scale network environments
- **Extensibility**: Custom plugins and automation capabilities

Key takeaways:
- Start with proper data modeling and validation
- Implement comprehensive API usage patterns
- Develop robust automation jobs and workflows
- Follow security and access control best practices
- Continuously monitor and optimize performance

## Additional Resources

- [Nautobot Documentation](https://nautobot.readthedocs.io/)
- [Nautobot API Reference](https://nautobot.readthedocs.io/en/stable/api/)
- [Nautobot Plugin Development](https://nautobot.readthedocs.io/en/stable/plugins/)
- [Network Automation Best Practices](https://networktocode.com/blog/)

---

*This guide provides a comprehensive overview of Nautobot as a network automation platform. For more advanced topics, check out our other articles on specific Nautobot features and integration patterns.* 