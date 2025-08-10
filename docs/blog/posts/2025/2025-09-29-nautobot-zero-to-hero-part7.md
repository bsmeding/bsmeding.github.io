---
authors: [bsmeding]
date: 2025-09-29
title: Nautobot in Action – Part 7
tags: ["network automation", "api", "integrations", "infoblox", "ise", "nautobot", "graphql"]
toc: true
layout: single
comments: true
draft: true
---

# Nautobot in Action – Part 7
## API Integrations
*Integrate Nautobot Jobs with Infoblox, ISE, and other external tools using REST and GraphQL.*

<!-- more -->

---

## Index
- [Nautobot in Action – Part 7](#nautobot-in-action--part-7)
  - [API Integrations](#api-integrations)
  - [Index](#index)
  - [1. Introduction](#1-introduction)
  - [2. Prerequisites](#2-prerequisites)
  - [3. REST API Integration](#3-rest-api-integration)
    - [3.1 Basic REST Client](#31-basic-rest-client)
    - [3.2 Authentication Handling](#32-authentication-handling)
  - [4. GraphQL Integration](#4-graphql-integration)
    - [4.1 GraphQL Client](#41-graphql-client)
    - [4.2 Nautobot GraphQL Queries](#42-nautobot-graphql-queries)
  - [5. Infoblox Integration](#5-infoblox-integration)
    - [5.1 IP Address Management](#51-ip-address-management)
  - [6. Cisco ISE Integration](#6-cisco-ise-integration)
    - [6.1 Network Access Control](#61-network-access-control)
  - [7. Other Tool Integrations](#7-other-tool-integrations)
    - [7.1 Monitoring Integration](#71-monitoring-integration)
    - [7.2 Configuration Management Integration](#72-configuration-management-integration)
  - [8. Wrap-Up](#8-wrap-up)
    - [What We Accomplished](#what-we-accomplished)
    - [Key Takeaways](#key-takeaways)

---

## 1. Introduction
In this advanced part, we'll explore API integrations to connect Nautobot with external tools like Infoblox, Cisco ISE, and other network management systems.

> **Estimated Time:** ~1.5 hours

---

## 2. Prerequisites
- Completed Parts 1-6 of this series
- Access to external APIs (Infoblox, ISE, etc.)
- Understanding of REST and GraphQL APIs

---

## 3. REST API Integration

### 3.1 Basic REST Client
```python
# jobs/api_integrations.py
import requests
from nautobot.extras.jobs import Job

class RESTAPIIntegrationJob(Job):
    class Meta:
        name = "REST API Integration"
        description = "Integrate with external REST APIs"

    def make_rest_call(self, url, method="GET", data=None, headers=None):
        """Make REST API call with error handling"""
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log_error(f"REST API call failed: {e}")
            return None
```

### 3.2 Authentication Handling
```python
def get_auth_token(self, auth_url, credentials):
    """Get authentication token for API access"""
    try:
        response = requests.post(auth_url, json=credentials)
        response.raise_for_status()
        return response.json().get('token')
    except requests.exceptions.RequestException as e:
        self.log_error(f"Authentication failed: {e}")
        return None
```

---

## 4. GraphQL Integration

### 4.1 GraphQL Client
```python
import requests

class GraphQLIntegrationJob(Job):
    class Meta:
        name = "GraphQL Integration"
        description = "Integrate with GraphQL APIs"

    def make_graphql_query(self, url, query, variables=None):
        """Execute GraphQL query"""
        try:
            response = requests.post(
                url,
                json={
                    'query': query,
                    'variables': variables or {}
                },
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log_error(f"GraphQL query failed: {e}")
            return None
```

### 4.2 Nautobot GraphQL Queries
```python
def query_nautobot_devices(self):
    """Query Nautobot devices via GraphQL"""
    query = """
    query {
        devices {
            name
            platform {
                name
            }
            site {
                name
            }
            interfaces {
                name
                enabled
                description
            }
        }
    }
    """
    
    return self.make_graphql_query(
        "http://nautobot/graphql/",
        query
    )
```

---

## 5. Infoblox Integration

### 5.1 IP Address Management
```python
class InfobloxIntegrationJob(Job):
    class Meta:
        name = "Infoblox Integration"
        description = "Integrate with Infoblox IPAM"

    def sync_ip_assignments(self):
        """Sync IP assignments between Nautobot and Infoblox"""
        # Get IP assignments from Infoblox
        infoblox_ips = self.get_infoblox_ip_assignments()
        
        # Get IP assignments from Nautobot
        nautobot_ips = self.get_nautobot_ip_assignments()
        
        # Compare and sync differences
        for device_name, ip_info in infoblox_ips.items():
            if device_name not in nautobot_ips:
                self.create_nautobot_ip_assignment(device_name, ip_info)

    def get_infoblox_ip_assignments(self):
        """Get IP assignments from Infoblox"""
        url = f"{self.infoblox_url}/wapi/v2.11/ipv4address"
        headers = {'Authorization': f'Basic {self.infoblox_auth}'}
        
        response = self.make_rest_call(url, headers=headers)
        return self.parse_infoblox_response(response)
```

---

## 6. Cisco ISE Integration

### 6.1 Network Access Control
```python
class CiscoISEIntegrationJob(Job):
    class Meta:
        name = "Cisco ISE Integration"
        description = "Integrate with Cisco ISE"

    def sync_device_authentication(self):
        """Sync device authentication status with ISE"""
        # Get authentication status from ISE
        ise_devices = self.get_ise_device_status()
        
        # Update Nautobot device status
        for device_name, auth_status in ise_devices.items():
            self.update_device_auth_status(device_name, auth_status)

    def get_ise_device_status(self):
        """Get device authentication status from ISE"""
        url = f"{self.ise_url}/api/v1/endpoint"
        headers = {'Authorization': f'Bearer {self.ise_token}'}
        
        response = self.make_rest_call(url, headers=headers)
        return self.parse_ise_response(response)
```

---

## 7. Other Tool Integrations

### 7.1 Monitoring Integration
```python
class MonitoringIntegrationJob(Job):
    class Meta:
        name = "Monitoring Integration"
        description = "Integrate with monitoring systems"

    def sync_device_status(self):
        """Sync device status with monitoring systems"""
        # Get device status from monitoring
        monitoring_status = self.get_monitoring_status()
        
        # Update Nautobot device status
        for device_name, status in monitoring_status.items():
            self.update_device_status(device_name, status)
```

### 7.2 Configuration Management Integration
```python
class ConfigManagementIntegrationJob(Job):
    class Meta:
        name = "Config Management Integration"
        description = "Integrate with configuration management tools"

    def sync_configurations(self):
        """Sync configurations with external CM tools"""
        # Get configurations from external tool
        external_configs = self.get_external_configs()
        
        # Compare with Nautobot intended configs
        for device_name, config in external_configs.items():
            self.compare_and_sync_config(device_name, config)
```

---

## 8. Wrap-Up

### What We Accomplished
- ✅ Implemented REST API integration
- ✅ Created GraphQL client for Nautobot
- ✅ Integrated with Infoblox IPAM
- ✅ Connected with Cisco ISE
- ✅ Built monitoring system integration

### Key Takeaways
- API integrations enable ecosystem connectivity
- GraphQL provides efficient data querying
- Authentication handling is crucial for security
- Error handling ensures reliability
- Integration enables end-to-end automation

---

*Ready for GitOps-style change management in Part 8! 🚀*
