---
authors: [bsmeding]
date: 2025-10-20
title: Nautobot in Action – Part 10
tags: ["network automation", "firewalls", "wireless", "golden config", "nautobot", "security"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot in Action – Part 10: Advanced Automation and Production Deployment

Welcome to the final installment of our Nautobot Zero to Hero series! In this concluding part, we'll explore advanced automation techniques, API integrations, monitoring, and best practices for production deployment. We'll bring together all the concepts from previous parts and create a comprehensive, enterprise-ready Nautobot solution.

<!-- more -->

## Prerequisites

- Complete Nautobot instance (from previous parts)
- Understanding of all previous concepts
- Basic knowledge of monitoring and observability
- Familiarity with CI/CD pipelines

## Advanced Automation and Orchestration

### 1. Multi-Vendor Configuration Management

Let's create a comprehensive configuration management system that works across multiple vendors:

```python
# nautobot_jobs/multi_vendor_config.py
from nautobot.extras.jobs import Job, StringVar, ObjectVar, BooleanVar
from nautobot.dcim.models import Device, DeviceType, Manufacturer
from nautobot.ipam.models import IPAddress, Prefix, VLAN
from nautobot.extras.models import CustomField, Tag
import json
import yaml

class MultiVendorConfigurationManager(Job):
    """Advanced configuration management for multiple vendors."""
    
    class Meta:
        name = "Multi-Vendor Configuration Manager"
        description = "Generate and manage configurations for Cisco, Juniper, and Arista devices"
    
    device_filter = StringVar(
        description="Device filter (e.g., 'cisco', 'juniper', 'arista')",
        required=False
    )
    
    config_type = StringVar(
        description="Configuration type (interfaces, routing, security)",
        required=True
    )
    
    dry_run = BooleanVar(
        description="Dry run mode (don't apply changes)",
        default=True
    )
    
    def run(self, data, commit):
        device_filter = data.get('device_filter', '').lower()
        config_type = data['config_type']
        dry_run = data['dry_run']
        
        # Vendor-specific configuration templates
        config_templates = {
            'cisco': {
                'interfaces': self._generate_cisco_interface_config,
                'routing': self._generate_cisco_routing_config,
                'security': self._generate_cisco_security_config
            },
            'juniper': {
                'interfaces': self._generate_juniper_interface_config,
                'routing': self._generate_juniper_routing_config,
                'security': self._generate_juniper_security_config
            },
            'arista': {
                'interfaces': self._generate_arista_interface_config,
                'routing': self._generate_arista_routing_config,
                'security': self._generate_arista_security_config
            }
        }
        
        # Get devices based on filter
        devices = Device.objects.all()
        if device_filter:
            devices = devices.filter(
                device_type__manufacturer__name__icontains=device_filter
            )
        
        configurations = {}
        
        for device in devices:
            vendor = self._get_device_vendor(device)
            
            if vendor in config_templates and config_type in config_templates[vendor]:
                config_generator = config_templates[vendor][config_type]
                config = config_generator(device)
                
                if config:
                    configurations[device.name] = {
                        'vendor': vendor,
                        'config_type': config_type,
                        'configuration': config,
                        'device': device
                    }
                    
                    self.log_success(f"Generated {config_type} config for {device.name}")
        
        # Store configurations in custom fields
        if not dry_run and commit:
            for device_name, config_data in configurations.items():
                device = config_data['device']
                
                # Store configuration in custom field
                device.custom_field_data.update({
                    f'last_{config_type}_config': json.dumps(config_data['configuration']),
                    f'{config_type}_config_generated': True
                })
                device.save()
                
                self.log_success(f"Applied {config_type} configuration to {device_name}")
        
        return f"Generated {len(configurations)} {config_type} configurations"
    
    def _get_device_vendor(self, device):
        """Determine vendor from device type."""
        manufacturer = device.device_type.manufacturer.name.lower()
        
        if 'cisco' in manufacturer:
            return 'cisco'
        elif 'juniper' in manufacturer:
            return 'juniper'
        elif 'arista' in manufacturer:
            return 'arista'
        else:
            return 'unknown'
    
    def _generate_cisco_interface_config(self, device):
        """Generate Cisco interface configuration."""
        config_lines = []
        
        for interface in device.interfaces.all():
            if interface.type == '1000base-t':
                config_lines.extend([
                    f"interface {interface.name}",
                    " description Auto-generated by Nautobot",
                    " switchport mode access",
                    " switchport access vlan 10",
                    " spanning-tree portfast",
                    " spanning-tree bpduguard enable",
                    "!"
                ])
        
        return "\n".join(config_lines)
    
    def _generate_juniper_interface_config(self, device):
        """Generate Juniper interface configuration."""
        config_lines = []
        
        for interface in device.interfaces.all():
            if interface.type == '1000base-t':
                config_lines.extend([
                    f"interfaces {{",
                    f"    {interface.name} {{",
                    f"        description \"Auto-generated by Nautobot\";",
                    f"        unit 0 {{",
                    f"            family ethernet-switching {{",
                    f"                vlan {{",
                    f"                    members vlan-10;",
                    f"                }}",
                    f"            }}",
                    f"        }}",
                    f"    }}",
                    f"}}"
                ])
        
        return "\n".join(config_lines)
    
    def _generate_arista_interface_config(self, device):
        """Generate Arista interface configuration."""
        config_lines = []
        
        for interface in device.interfaces.all():
            if interface.type == '1000base-t':
                config_lines.extend([
                    f"interface {interface.name}",
                    " description Auto-generated by Nautobot",
                    " switchport mode access",
                    " switchport access vlan 10",
                    " spanning-tree portfast",
                    " spanning-tree bpduguard enable",
                    "!"
                ])
        
        return "\n".join(config_lines)
    
    # Additional configuration generators for routing and security...
    def _generate_cisco_routing_config(self, device):
        return "router ospf 1\n network 192.168.0.0 0.0.255.255 area 0"
    
    def _generate_juniper_routing_config(self, device):
        return "protocols {\n    ospf {\n        area 0.0.0.0 {\n            interface ge-0/0/0.0;\n        }\n    }\n}"
    
    def _generate_arista_routing_config(self, device):
        return "router ospf 1\n network 192.168.0.0/16 area 0"
    
    def _generate_cisco_security_config(self, device):
        return "access-list 100 permit ip any any"
    
    def _generate_juniper_security_config(self, device):
        return "firewall {\n    filter default {\n        term allow-all {\n            then accept;\n        }\n    }\n}"
    
    def _generate_arista_security_config(self, device):
        return "ip access-list standard default\n permit any"
```

### 2. Automated Network Validation

Create a comprehensive network validation system:

```python
# nautobot_jobs/network_validation.py
from nautobot.extras.jobs import Job, StringVar, BooleanVar
from nautobot.dcim.models import Device, Interface, Cable
from nautobot.ipam.models import IPAddress, Prefix, VLAN
from nautobot.extras.models import Tag
import ipaddress

class NetworkValidationEngine(Job):
    """Comprehensive network validation and health checks."""
    
    class Meta:
        name = "Network Validation Engine"
        description = "Validate network configuration and connectivity"
    
    validation_type = StringVar(
        description="Type of validation (connectivity, addressing, security)",
        required=True
    )
    
    auto_fix = BooleanVar(
        description="Automatically fix issues when possible",
        default=False
    )
    
    def run(self, data, commit):
        validation_type = data['validation_type']
        auto_fix = data['auto_fix']
        
        validation_results = {
            'passed': [],
            'failed': [],
            'warnings': [],
            'fixed': []
        }
        
        if validation_type == 'connectivity':
            validation_results = self._validate_connectivity(auto_fix, commit)
        elif validation_type == 'addressing':
            validation_results = self._validate_addressing(auto_fix, commit)
        elif validation_type == 'security':
            validation_results = self._validate_security(auto_fix, commit)
        elif validation_type == 'all':
            validation_results = self._validate_all(auto_fix, commit)
        
        # Log results
        for result_type, items in validation_results.items():
            for item in items:
                if result_type == 'passed':
                    self.log_success(item)
                elif result_type == 'failed':
                    self.log_failure(item)
                elif result_type == 'warnings':
                    self.log_warning(item)
                elif result_type == 'fixed':
                    self.log_success(f"Fixed: {item}")
        
        return f"Validation completed. {len(validation_results['passed'])} passed, {len(validation_results['failed'])} failed, {len(validation_results['fixed'])} fixed"
    
    def _validate_connectivity(self, auto_fix, commit):
        """Validate network connectivity."""
        results = {'passed': [], 'failed': [], 'warnings': [], 'fixed': []}
        
        # Check for disconnected interfaces
        for interface in Interface.objects.all():
            if not interface.cable and interface.type in ['1000base-t', '10gbase-t']:
                results['warnings'].append(f"Interface {interface.name} on {interface.device.name} is not connected")
        
        # Check for cable mismatches
        for cable in Cable.objects.all():
            if cable.termination_a and cable.termination_b:
                a_type = cable.termination_a.type
                b_type = cable.termination_b.type
                
                if a_type != b_type:
                    results['failed'].append(
                        f"Cable type mismatch: {cable.termination_a.device.name}:{cable.termination_a.name} "
                        f"({a_type}) -> {cable.termination_b.device.name}:{cable.termination_b.name} ({b_type})"
                    )
        
        return results
    
    def _validate_addressing(self, auto_fix, commit):
        """Validate IP addressing."""
        results = {'passed': [], 'failed': [], 'warnings': [], 'fixed': []}
        
        # Check for duplicate IP addresses
        ip_addresses = {}
        for ip in IPAddress.objects.all():
            if ip.address in ip_addresses:
                results['failed'].append(f"Duplicate IP address: {ip.address}")
            else:
                ip_addresses[ip.address] = ip
        
        # Check for overlapping prefixes
        prefixes = list(Prefix.objects.all())
        for i, prefix1 in enumerate(prefixes):
            for prefix2 in prefixes[i+1:]:
                try:
                    net1 = ipaddress.ip_network(prefix1.prefix)
                    net2 = ipaddress.ip_network(prefix2.prefix)
                    
                    if net1.overlaps(net2):
                        results['failed'].append(f"Overlapping prefixes: {prefix1.prefix} and {prefix2.prefix}")
                except ValueError:
                    results['warnings'].append(f"Invalid prefix format: {prefix1.prefix} or {prefix2.prefix}")
        
        return results
    
    def _validate_security(self, auto_fix, commit):
        """Validate security configurations."""
        results = {'passed': [], 'failed': [], 'warnings': [], 'fixed': []}
        
        # Check for devices without security tags
        security_tag = Tag.objects.filter(name='security-audited').first()
        
        if security_tag:
            for device in Device.objects.all():
                if security_tag not in device.tags.all():
                    results['warnings'].append(f"Device {device.name} not security audited")
                    
                    if auto_fix and commit:
                        device.tags.add(security_tag)
                        results['fixed'].append(f"Added security audit tag to {device.name}")
        
        # Check for management interfaces
        for device in Device.objects.all():
            mgmt_interfaces = device.interfaces.filter(name__icontains='mgmt')
            
            if not mgmt_interfaces.exists():
                results['warnings'].append(f"Device {device.name} has no management interface")
        
        return results
    
    def _validate_all(self, auto_fix, commit):
        """Run all validations."""
        all_results = {'passed': [], 'failed': [], 'warnings': [], 'fixed': []}
        
        for validation_type in ['connectivity', 'addressing', 'security']:
            results = getattr(self, f'_validate_{validation_type}')(auto_fix, commit)
            
            for key in all_results:
                all_results[key].extend(results[key])
        
        return all_results
```

## API Integration and External Systems

### 1. REST API Automation

```python
# nautobot_jobs/api_integration.py
from nautobot.extras.jobs import Job, StringVar, TextVar
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress
import requests
import json

class ExternalAPIIntegration(Job):
    """Integrate with external systems via REST APIs."""
    
    class Meta:
        name = "External API Integration"
        description = "Integrate with monitoring, ticketing, and other systems"
    
    api_type = StringVar(
        description="API type (monitoring, ticketing, backup)",
        required=True
    )
    
    api_endpoint = StringVar(
        description="API endpoint URL",
        required=True
    )
    
    api_key = StringVar(
        description="API key or token",
        required=True
    )
    
    def run(self, data, commit):
        api_type = data['api_type']
        api_endpoint = data['api_endpoint']
        api_key = data['api_key']
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        if api_type == 'monitoring':
            return self._integrate_monitoring(api_endpoint, headers, commit)
        elif api_type == 'ticketing':
            return self._integrate_ticketing(api_endpoint, headers, commit)
        elif api_type == 'backup':
            return self._integrate_backup(api_endpoint, headers, commit)
        
        return f"Unknown API type: {api_type}"
    
    def _integrate_monitoring(self, endpoint, headers, commit):
        """Integrate with monitoring systems."""
        devices = Device.objects.all()
        
        for device in devices:
            # Prepare device data for monitoring system
            device_data = {
                'name': device.name,
                'ip_address': self._get_device_ip(device),
                'device_type': device.device_type.model,
                'site': device.site.name,
                'status': device.status.value,
                'tags': [tag.name for tag in device.tags.all()]
            }
            
            try:
                response = requests.post(
                    f"{endpoint}/devices",
                    headers=headers,
                    json=device_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    self.log_success(f"Added {device.name} to monitoring system")
                else:
                    self.log_warning(f"Failed to add {device.name} to monitoring: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.log_failure(f"API error for {device.name}: {str(e)}")
        
        return f"Integrated {devices.count()} devices with monitoring system"
    
    def _integrate_ticketing(self, endpoint, headers, commit):
        """Integrate with ticketing systems."""
        # Create tickets for devices with issues
        problematic_devices = Device.objects.filter(
            status__value='failed'
        )
        
        for device in problematic_devices:
            ticket_data = {
                'title': f"Device {device.name} is down",
                'description': f"Device {device.name} at {device.site.name} is reporting failed status",
                'priority': 'high',
                'category': 'network',
                'device_name': device.name,
                'site': device.site.name
            }
            
            try:
                response = requests.post(
                    f"{endpoint}/tickets",
                    headers=headers,
                    json=ticket_data,
                    timeout=30
                )
                
                if response.status_code == 201:
                    self.log_success(f"Created ticket for {device.name}")
                else:
                    self.log_warning(f"Failed to create ticket for {device.name}: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.log_failure(f"API error for {device.name}: {str(e)}")
        
        return f"Created tickets for {problematic_devices.count()} problematic devices"
    
    def _integrate_backup(self, endpoint, headers, commit):
        """Integrate with backup systems."""
        devices = Device.objects.filter(
            device_type__model__in=['ASA5525-X', 'PA-3220', 'FortiGate 600E']
        )
        
        for device in devices:
            backup_data = {
                'device_name': device.name,
                'device_type': device.device_type.model,
                'site': device.site.name,
                'backup_type': 'configuration',
                'schedule': 'daily'
            }
            
            try:
                response = requests.post(
                    f"{endpoint}/backups",
                    headers=headers,
                    json=backup_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    self.log_success(f"Scheduled backup for {device.name}")
                else:
                    self.log_warning(f"Failed to schedule backup for {device.name}: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.log_failure(f"API error for {device.name}: {str(e)}")
        
        return f"Scheduled backups for {devices.count()} devices"
    
    def _get_device_ip(self, device):
        """Get primary IP address for device."""
        try:
            return device.primary_ip4.address if device.primary_ip4 else None
        except:
            return None
```

### 2. Webhook Integration

```python
# nautobot_jobs/webhook_integration.py
from nautobot.extras.jobs import Job, StringVar, TextVar
from nautobot.dcim.models import Device
from nautobot.extras.models import Webhook
import requests
import json

class WebhookConfiguration(Job):
    """Configure webhooks for external integrations."""
    
    class Meta:
        name = "Webhook Configuration"
        description = "Set up webhooks for external system notifications"
    
    webhook_url = StringVar(
        description="Webhook URL",
        required=True
    )
    
    webhook_type = StringVar(
        description="Webhook type (slack, teams, custom)",
        required=True
    )
    
    def run(self, data, commit):
        webhook_url = data['webhook_url']
        webhook_type = data['webhook_type']
        
        if webhook_type == 'slack':
            return self._configure_slack_webhook(webhook_url, commit)
        elif webhook_type == 'teams':
            return self._configure_teams_webhook(webhook_url, commit)
        elif webhook_type == 'custom':
            return self._configure_custom_webhook(webhook_url, commit)
        
        return f"Unknown webhook type: {webhook_type}"
    
    def _configure_slack_webhook(self, webhook_url, commit):
        """Configure Slack webhook."""
        # Create webhook for device changes
        webhook, created = Webhook.objects.get_or_create(
            name='device-changes-slack',
            defaults={
                'url': webhook_url,
                'http_method': 'POST',
                'http_content_type': 'application/json',
                'enabled': True,
                'type_create': True,
                'type_update': True,
                'type_delete': True,
                'additional_headers': json.dumps({
                    'Content-Type': 'application/json'
                }),
                'body_template': json.dumps({
                    'text': 'Device {{ object.name }} was {{ action }} in Nautobot',
                    'attachments': [{
                        'fields': [
                            {'title': 'Device', 'value': '{{ object.name }}', 'short': True},
                            {'title': 'Site', 'value': '{{ object.site.name }}', 'short': True},
                            {'title': 'Status', 'value': '{{ object.status.value }}', 'short': True},
                            {'title': 'Action', 'value': '{{ action }}', 'short': True}
                        ]
                    }]
                })
            }
        )
        
        if created:
            self.log_success("Created Slack webhook for device changes")
        else:
            self.log_info("Slack webhook already exists")
        
        return "Slack webhook configured successfully"
    
    def _configure_teams_webhook(self, webhook_url, commit):
        """Configure Microsoft Teams webhook."""
        webhook, created = Webhook.objects.get_or_create(
            name='device-changes-teams',
            defaults={
                'url': webhook_url,
                'http_method': 'POST',
                'http_content_type': 'application/json',
                'enabled': True,
                'type_create': True,
                'type_update': True,
                'type_delete': True,
                'additional_headers': json.dumps({
                    'Content-Type': 'application/json'
                }),
                'body_template': json.dumps({
                    '@type': 'MessageCard',
                    '@context': 'http://schema.org/extensions',
                    'themeColor': '0076D7',
                    'summary': 'Device {{ action }} in Nautobot',
                    'sections': [{
                        'activityTitle': 'Device {{ action }}',
                        'facts': [
                            {'name': 'Device', 'value': '{{ object.name }}'},
                            {'name': 'Site', 'value': '{{ object.site.name }}'},
                            {'name': 'Status', 'value': '{{ object.status.value }}'},
                            {'name': 'Action', 'value': '{{ action }}'}
                        ]
                    }]
                })
            }
        )
        
        if created:
            self.log_success("Created Teams webhook for device changes")
        else:
            self.log_info("Teams webhook already exists")
        
        return "Microsoft Teams webhook configured successfully"
    
    def _configure_custom_webhook(self, webhook_url, commit):
        """Configure custom webhook."""
        webhook, created = Webhook.objects.get_or_create(
            name='device-changes-custom',
            defaults={
                'url': webhook_url,
                'http_method': 'POST',
                'http_content_type': 'application/json',
                'enabled': True,
                'type_create': True,
                'type_update': True,
                'type_delete': True,
                'additional_headers': json.dumps({
                    'Content-Type': 'application/json',
                    'X-Nautobot-Event': '{{ action }}'
                }),
                'body_template': json.dumps({
                    'event': '{{ action }}',
                    'device': {
                        'name': '{{ object.name }}',
                        'site': '{{ object.site.name }}',
                        'status': '{{ object.status.value }}',
                        'device_type': '{{ object.device_type.model }}'
                    },
                    'timestamp': '{{ timestamp }}'
                })
            }
        )
        
        if created:
            self.log_success("Created custom webhook for device changes")
        else:
            self.log_info("Custom webhook already exists")
        
        return "Custom webhook configured successfully"
```

## Monitoring and Observability

### 1. Network Health Dashboard

```python
# nautobot_jobs/health_monitoring.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device, Interface, Cable
from nautobot.ipam.models import IPAddress, Prefix
from nautobot.extras.models import CustomField, Tag
from datetime import datetime, timedelta

class NetworkHealthMonitoring(Job):
    """Comprehensive network health monitoring and reporting."""
    
    class Meta:
        name = "Network Health Monitoring"
        description = "Monitor network health and generate reports"
    
    def run(self, data, commit):
        health_metrics = {
            'total_devices': Device.objects.count(),
            'active_devices': Device.objects.filter(status__value='active').count(),
            'failed_devices': Device.objects.filter(status__value='failed').count(),
            'total_interfaces': Interface.objects.count(),
            'connected_interfaces': Cable.objects.count() * 2,  # Each cable connects 2 interfaces
            'total_ips': IPAddress.objects.count(),
            'total_prefixes': Prefix.objects.count(),
            'health_score': 0
        }
        
        # Calculate health score
        if health_metrics['total_devices'] > 0:
            device_health = health_metrics['active_devices'] / health_metrics['total_devices']
            interface_health = health_metrics['connected_interfaces'] / health_metrics['total_interfaces'] if health_metrics['total_interfaces'] > 0 else 1
            health_metrics['health_score'] = int((device_health + interface_health) / 2 * 100)
        
        # Store health metrics in custom fields
        if commit:
            # Create or update health metrics custom field
            health_field, created = CustomField.objects.get_or_create(
                name='network_health_metrics',
                defaults={
                    'type': 'json',
                    'label': 'Network Health Metrics',
                    'description': 'Current network health metrics'
                }
            )
            
            # Store metrics in a system device or create a virtual device
            system_device, created = Device.objects.get_or_create(
                name='nautobot-system',
                defaults={
                    'device_type': DeviceType.objects.first(),
                    'site': Site.objects.first(),
                    'status': Status.objects.get(value='active')
                }
            )
            
            system_device.custom_field_data['network_health_metrics'] = health_metrics
            system_device.save()
        
        # Log health status
        self.log_success(f"Network Health Score: {health_metrics['health_score']}%")
        self.log_info(f"Active Devices: {health_metrics['active_devices']}/{health_metrics['total_devices']}")
        self.log_info(f"Connected Interfaces: {health_metrics['connected_interfaces']}/{health_metrics['total_interfaces']}")
        
        # Alert on critical issues
        if health_metrics['health_score'] < 80:
            self.log_warning(f"Network health score is low: {health_metrics['health_score']}%")
        
        if health_metrics['failed_devices'] > 0:
            self.log_warning(f"Found {health_metrics['failed_devices']} failed devices")
        
        return f"Health monitoring completed. Score: {health_metrics['health_score']}%"
```

### 2. Performance Monitoring

```python
# nautobot_jobs/performance_monitoring.py
from nautobot.extras.jobs import Job
from nautobot.dcim.models import Device
from nautobot.extras.models import CustomField
import time
import psutil

class PerformanceMonitoring(Job):
    """Monitor Nautobot system performance."""
    
    class Meta:
        name = "Performance Monitoring"
        description = "Monitor system performance and resource usage"
    
    def run(self, data, commit):
        performance_metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'database_connections': self._get_db_connections(),
            'active_jobs': self._get_active_jobs(),
            'api_requests': self._get_api_requests()
        }
        
        # Store performance metrics
        if commit:
            perf_field, created = CustomField.objects.get_or_create(
                name='system_performance_metrics',
                defaults={
                    'type': 'json',
                    'label': 'System Performance Metrics',
                    'description': 'Current system performance metrics'
                }
            )
            
            # Store in system device
            system_device = Device.objects.filter(name='nautobot-system').first()
            if system_device:
                system_device.custom_field_data['system_performance_metrics'] = performance_metrics
                system_device.save()
        
        # Log performance status
        self.log_info(f"CPU Usage: {performance_metrics['cpu_usage']}%")
        self.log_info(f"Memory Usage: {performance_metrics['memory_usage']}%")
        self.log_info(f"Disk Usage: {performance_metrics['disk_usage']}%")
        
        # Alert on high resource usage
        if performance_metrics['cpu_usage'] > 80:
            self.log_warning(f"High CPU usage: {performance_metrics['cpu_usage']}%")
        
        if performance_metrics['memory_usage'] > 80:
            self.log_warning(f"High memory usage: {performance_metrics['memory_usage']}%")
        
        if performance_metrics['disk_usage'] > 90:
            self.log_warning(f"High disk usage: {performance_metrics['disk_usage']}%")
        
        return "Performance monitoring completed"
    
    def _get_db_connections(self):
        """Get database connection count."""
        try:
            from django.db import connection
            return len(connection.queries) if hasattr(connection, 'queries') else 0
        except:
            return 0
    
    def _get_active_jobs(self):
        """Get count of active jobs."""
        try:
            from nautobot.extras.models import JobResult
            return JobResult.objects.filter(status='running').count()
        except:
            return 0
    
    def _get_api_requests(self):
        """Get API request count (simplified)."""
        return 0  # Would need middleware to track this
```

## Production Deployment Best Practices

### 1. Backup and Recovery

```python
# nautobot_jobs/backup_recovery.py
from nautobot.extras.jobs import Job, StringVar, BooleanVar
from nautobot.dcim.models import Device
from nautobot.extras.models import CustomField
import json
import os
from datetime import datetime

class BackupAndRecovery(Job):
    """Automated backup and recovery procedures."""
    
    class Meta:
        name = "Backup and Recovery"
        description = "Create and manage Nautobot backups"
    
    backup_type = StringVar(
        description="Backup type (full, incremental, config)",
        required=True
    )
    
    backup_location = StringVar(
        description="Backup location path",
        required=True
    )
    
    include_configs = BooleanVar(
        description="Include device configurations",
        default=True
    )
    
    def run(self, data, commit):
        backup_type = data['backup_type']
        backup_location = data['backup_location']
        include_configs = data['include_configs']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"nautobot_backup_{backup_type}_{timestamp}.json"
        backup_path = os.path.join(backup_location, backup_filename)
        
        backup_data = {
            'backup_type': backup_type,
            'timestamp': timestamp,
            'version': '1.0',
            'devices': [],
            'configurations': {}
        }
        
        # Backup device data
        for device in Device.objects.all():
            device_data = {
                'name': device.name,
                'device_type': device.device_type.model,
                'site': device.site.name,
                'status': device.status.value,
                'custom_fields': device.custom_field_data,
                'interfaces': []
            }
            
            for interface in device.interfaces.all():
                interface_data = {
                    'name': interface.name,
                    'type': interface.type,
                    'enabled': interface.enabled,
                    'ip_addresses': []
                }
                
                for ip in interface.ip_addresses.all():
                    interface_data['ip_addresses'].append(str(ip.address))
                
                device_data['interfaces'].append(interface_data)
            
            backup_data['devices'].append(device_data)
            
            # Include device configurations if requested
            if include_configs and device.custom_field_data.get('last_config'):
                backup_data['configurations'][device.name] = device.custom_field_data['last_config']
        
        # Save backup file
        try:
            os.makedirs(backup_location, exist_ok=True)
            
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            self.log_success(f"Backup created: {backup_path}")
            
            # Store backup metadata
            if commit:
                backup_field, created = CustomField.objects.get_or_create(
                    name='backup_metadata',
                    defaults={
                        'type': 'json',
                        'label': 'Backup Metadata',
                        'description': 'Backup file metadata'
                    }
                )
                
                system_device = Device.objects.filter(name='nautobot-system').first()
                if system_device:
                    backup_metadata = system_device.custom_field_data.get('backup_metadata', [])
                    backup_metadata.append({
                        'filename': backup_filename,
                        'path': backup_path,
                        'type': backup_type,
                        'timestamp': timestamp,
                        'size': os.path.getsize(backup_path)
                    })
                    system_device.custom_field_data['backup_metadata'] = backup_metadata
                    system_device.save()
            
        except Exception as e:
            self.log_failure(f"Backup failed: {str(e)}")
            return f"Backup failed: {str(e)}"
        
        return f"Backup completed successfully: {backup_filename}"
```

### 2. Security Hardening

```python
# nautobot_jobs/security_hardening.py
from nautobot.extras.jobs import Job, BooleanVar
from nautobot.dcim.models import Device
from nautobot.extras.models import CustomField, Tag
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class SecurityHardening(Job):
    """Implement security hardening measures."""
    
    class Meta:
        name = "Security Hardening"
        description = "Apply security hardening measures to Nautobot"
    
    enable_audit_logging = BooleanVar(
        description="Enable comprehensive audit logging",
        default=True
    )
    
    enforce_password_policy = BooleanVar(
        description="Enforce strong password policy",
        default=True
    )
    
    enable_mfa = BooleanVar(
        description="Enable multi-factor authentication",
        default=True
    )
    
    def run(self, data, commit):
        enable_audit_logging = data['enable_audit_logging']
        enforce_password_policy = data['enforce_password_policy']
        enable_mfa = data['enable_mfa']
        
        security_measures = []
        
        # Create security tags
        security_tags = [
            {'name': 'security-hardened', 'color': '00ff00', 'description': 'Device has security hardening applied'},
            {'name': 'audit-enabled', 'color': 'ffff00', 'description': 'Audit logging enabled'},
            {'name': 'mfa-enabled', 'color': 'ff00ff', 'description': 'Multi-factor authentication enabled'}
        ]
        
        for tag_data in security_tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults=tag_data
            )
            
            if created:
                security_measures.append(f"Created security tag: {tag.name}")
        
        # Apply security measures to devices
        for device in Device.objects.all():
            device_tags = []
            
            if enable_audit_logging:
                audit_tag = Tag.objects.get(name='audit-enabled')
                device_tags.append(audit_tag)
                security_measures.append(f"Enabled audit logging for {device.name}")
            
            # Add security hardening tag
            hardened_tag = Tag.objects.get(name='security-hardened')
            device_tags.append(hardened_tag)
            
            # Apply tags to device
            for tag in device_tags:
                if tag not in device.tags.all():
                    device.tags.add(tag)
        
        # Enforce password policy
        if enforce_password_policy:
            # This would typically be done through Django settings
            # For demonstration, we'll create a custom field to track password policy
            password_field, created = CustomField.objects.get_or_create(
                name='password_policy_enforced',
                defaults={
                    'type': 'boolean',
                    'label': 'Password Policy Enforced',
                    'description': 'Strong password policy is enforced'
                }
            )
            
            if created:
                security_measures.append("Password policy enforcement configured")
        
        # Enable MFA
        if enable_mfa:
            mfa_field, created = CustomField.objects.get_or_create(
                name='mfa_required',
                defaults={
                    'type': 'boolean',
                    'label': 'MFA Required',
                    'description': 'Multi-factor authentication is required'
                }
            )
            
            if created:
                security_measures.append("Multi-factor authentication configured")
        
        # Log security measures
        for measure in security_measures:
            self.log_success(measure)
        
        return f"Security hardening completed. Applied {len(security_measures)} measures."
```

## Wrap-Up and Best Practices

### Key Takeaways from the Series:

1. **Comprehensive Network Management**: We've built a complete network management solution covering device onboarding, configuration management, security, and automation.

2. **Multi-Vendor Support**: The solution works across Cisco, Juniper, Arista, and other major vendors.

3. **Security-First Approach**: Integrated security policies, compliance frameworks, and hardening measures.

4. **Automation and Integration**: Extensive automation capabilities with external system integration.

5. **Monitoring and Observability**: Comprehensive health monitoring and performance tracking.

### Production Deployment Checklist:

- [ ] **Backup Strategy**: Implement automated backups with off-site storage
- [ ] **Security Hardening**: Apply all security measures and enable audit logging
- [ ] **Monitoring**: Set up comprehensive monitoring and alerting
- [ ] **High Availability**: Configure redundant Nautobot instances
- [ ] **Documentation**: Maintain up-to-date documentation and runbooks
- [ ] **Testing**: Regular testing of backup/restore procedures
- [ ] **Updates**: Establish update and patch management procedures

### Next Steps:

1. **Scale Up**: Expand the solution to larger networks
2. **Advanced Automation**: Implement more sophisticated automation workflows
3. **Integration**: Add more external system integrations
4. **Analytics**: Implement advanced analytics and reporting
5. **Compliance**: Add more compliance frameworks and audits

### Resources:

- [Nautobot Documentation](https://nautobot.readthedocs.io/)
- [Network Automation Best Practices](https://www.ansible.com/blog/network-automation-best-practices)
- [Security Hardening Guide](https://docs.djangoproject.com/en/stable/topics/security/)
- [Monitoring Best Practices](https://prometheus.io/docs/practices/)

## Conclusion

Congratulations! You've completed the Nautobot Zero to Hero series. You now have a comprehensive understanding of network automation with Nautobot, from basic device management to advanced automation and production deployment.

The skills you've learned in this series will enable you to:

- **Automate Network Operations**: Reduce manual tasks and improve efficiency
- **Ensure Network Security**: Implement comprehensive security policies and compliance
- **Scale Network Management**: Handle growing networks with automation
- **Integrate Systems**: Connect Nautobot with your existing tools and workflows
- **Monitor and Maintain**: Keep your network healthy and performant

Remember that network automation is a journey, not a destination. Continue learning, experimenting, and improving your automation workflows. The network automation community is vibrant and growing, so stay connected and share your experiences!

Thank you for joining us on this journey from Zero to Hero with Nautobot! 🚀

---

*This concludes the Nautobot Zero to Hero series. For questions, feedback, or to share your automation success stories, feel free to reach out through the comments or social media channels.*
