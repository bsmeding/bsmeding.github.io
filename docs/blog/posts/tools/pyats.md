---
title: pyATS Introduction & Getting Started
authors: [bsmeding]
date: 2024-09-22
summary: A introduction and getting-started to use pyATS for network testing
tags:
  - pyats
  - network testing
  - validation
  - automation
  - devops
---

# pyATS: Introduction & Getting Started

![pyATS Logo](https://developer.cisco.com/pyats/assets/images/pyats-logo.png){: style="max-width: 300px; display: block; margin: 0 auto;"}

**pyATS** (Python Automated Test System) is an open-source network testing and validation framework developed by Cisco. It enables engineers to automate network testing, validation, and verification tasks.
<!-- more -->

## Why Use pyATS?
- Automate network device testing and validation
- Perform pre- and post-change checks
- Integrate with CI/CD pipelines for continuous network validation
- Use Genie for parsing and model-driven testing

## How pyATS Works
- Uses Python scripts and YAML testbeds to define network topologies
- Test scripts (jobs) automate device connections, command execution, and result validation
- Genie library provides parsers and test harnesses

## Quick Start Example
1. **Install pyATS and Genie:**
   ```bash
   pip install pyats[full]
   pip install genie
   ```
2. **Create a testbed YAML file (`testbed.yaml`):**
   ```yaml
   devices:
     r1:
       os: iosxe
       type: router
       connections:
         cli:
           protocol: ssh
           ip: 192.0.2.1
       credentials:
         default:
           username: admin
           password: admin
   ```
3. **Write a simple test script (`test.py`):**
   ```python
   from pyats.topology import loader

   testbed = loader.load('testbed.yaml')
   device = testbed.devices['r1']
   device.connect()
   output = device.execute('show version')
   print(output)
   device.disconnect()
   ```
4. **Run the script:**
   ```bash
   python test.py
   ```

## Learn More
- [pyATS Documentation](https://developer.cisco.com/docs/pyats/)
- [Getting Started Guide](https://developer.cisco.com/docs/pyats/#!getting-started/overview) 