---
authors: [bsmeding]
date: 2025-04-12
title: pyATS Testing Tutorial
tags: ["pyats", "genie", "network automation", "testing", "cisco"]
summary: Learn how to get started with Cisco pyATS and Genie for automated network testing, validation, and health checks.
---

# pyATS Testing Tutorial

pyATS (Python Automated Test System) is a powerful, open-source Python framework originally developed by Cisco for network testing and validation. With the Genie library, pyATS can parse, learn, and compare network device states, making it a must-have tool for network engineers and automation professionals. In this tutorial, you'll learn how to install pyATS, create a testbed, run your first test, and use Genie for network state validation.

<!-- more -->

## What is pyATS and Genie?

- **pyATS** stands for Python Automated Test System. It is a modular, Python-based test automation framework used for network validation, health checks, and regression testing. While it was developed by Cisco, it works with many network platforms.
- **Genie** is a library that extends pyATS with network knowledge—parsers, "learn" features, and diffing capabilities.
- Together, they allow you to automate network testing, parse CLI output, and compare network states before and after changes.

> pyATS is used by Cisco internally for millions of tests per month and is now open source for everyone.

## Installation

It's best to use a Python virtual environment for pyATS projects:

```bash
# Create and activate a virtual environment
mkdir pyats-demo
cd pyats-demo
python3 -m venv .
source bin/activate

# Install pyATS and Genie (full extras)
pip install "pyats[full]"
```

Check your installation:
```bash
pyats version check
```

## Creating a Testbed File

A testbed file describes your network devices for pyATS. You can create one interactively:

```bash
genie create testbed interactive --output testbed1.yml
```

You'll be prompted for device names, IPs, credentials, and connection details. The result is a YAML file like:

```yaml
devices:
  csr1:
    os: iosxe
    type: router
    connections:
      cli:
        protocol: ssh
        ip: 192.168.1.10
    credentials:
      default:
        username: admin
        password: mypassword
```

You can add more devices by editing the YAML file.

## Running Your First pyATS/Genie Test

Let's use Genie to "learn" OSPF state from your devices:

```bash
genie learn ospf --testbed-file testbed1.yml --output ospf1
```

- This command connects to all devices in your testbed and collects OSPF state, saving the results in the `ospf1` folder.
- You can repeat this after making changes (e.g., disabling an interface) and save to a new folder:

```bash
genie learn ospf --testbed-file testbed1.yml --output ospf2
```

## Comparing Network States with pyATS Diff

To see what changed between two states:

```bash
pyats diff ospf1 ospf2
```

- This will show you exactly what changed in OSPF between the two runs—great for troubleshooting and validation!

## Use Cases for pyATS

- **Network Health Checks:** Automate regular checks for interface status, routing, CPU/memory, etc.
- **Pre/Post Change Validation:** Capture network state before and after upgrades or config changes, and compare.
- **Automated Testing:** Integrate with CI/CD pipelines for continuous network validation.
- **Parsing CLI Output:** Use Genie parsers to turn CLI output into structured data for further analysis.

## Example: Health Check Automation

You can schedule pyATS/Genie scripts to run at intervals, collecting and comparing network state, and alerting on changes or anomalies.

## Key Resources

- [Roger Perkin: pyATS Genie Tutorial](https://www.rogerperkin.co.uk/network-automation/pyats/pyats-genie-tutorial/)
- [Cisco pyATS Getting Started Guide](https://developer.cisco.com/docs/pyats-getting-started/)
- [DevNet Academy pyATS Start Guide](https://docs.devnet-academy.com/docs/pyats_start_guide_v22.1/)
- [Dave Brown: pyATS Getting Started](https://davebrownblog.com/2025/03/04/pyats-getting-started/)
- [Cisco pyATS Documentation](https://pubhub.devnetcloud.com/media/pyats/docs/overview/introduction.html)
- [Genie Parsers List](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers)

## Conclusion

pyATS and Genie are essential tools for network engineers looking to automate testing, validation, and troubleshooting. With simple YAML testbeds, powerful "learn" and diff features, and a Pythonic workflow, you can bring your network automation to the next level.

For more network automation tutorials, check out the [NetDevOps blog](/blog/index/) and [tools index](/tools/). 

## Bonus: Generate a pyATS Testbed from Nautobot

You can automate the creation of your pyATS testbed file by extracting device data directly from Nautobot. The script below connects to Nautobot using environment variables for the URL, API token, and site name, and outputs a testbed YAML file for use with pyATS.

**Usage:**
```bash
export NAUTOBOT_URL=https://nautobot.example.com/api/
export NAUTOBOT_TOKEN=yourtoken
export NAUTOBOT_SITE=ams-dc1
python3 nautobot_to_pyats_testbed.py > testbed.yml
```

**Script:**
```python
#!/usr/bin/env python3
"""
Script to extract devices from a Nautobot site and generate a pyATS testbed YAML file.

Environment variables required:
- NAUTOBOT_URL: Nautobot API base URL (e.g., https://nautobot.example.com/api/)
- NAUTOBOT_TOKEN: Nautobot API token
- NAUTOBOT_SITE: Name or slug of the site to extract devices from

Usage:
  export NAUTOBOT_URL=https://nautobot.example.com/api/
  export NAUTOBOT_TOKEN=yourtoken
  export NAUTOBOT_SITE=ams-dc1
  python3 nautobot_to_pyats_testbed.py > testbed.yml
"""
import os
import sys
import requests
import yaml

NAUTOBOT_URL = os.environ.get("NAUTOBOT_URL")
NAUTOBOT_TOKEN = os.environ.get("NAUTOBOT_TOKEN")
NAUTOBOT_SITE = os.environ.get("NAUTOBOT_SITE")

if not (NAUTOBOT_URL and NAUTOBOT_TOKEN and NAUTOBOT_SITE):
    print("Error: Please set NAUTOBOT_URL, NAUTOBOT_TOKEN, and NAUTOBOT_SITE environment variables.", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Token {NAUTOBOT_TOKEN}",
    "Accept": "application/json",
}

# Fetch devices from the specified site
def get_devices(site):
    url = f"{NAUTOBOT_URL.rstrip('/')}/dcim/devices/?site={site}&limit=1000"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get("results", [])

# Fetch primary IP for a device (if available)
def get_primary_ip(device):
    ip = device.get("primary_ip4") or device.get("primary_ip")
    if ip and ip.get("address"):
        return ip["address"].split("/")[0]
    return None

# Build pyATS testbed structure
def build_testbed(devices):
    testbed = {"devices": {}}
    for dev in devices:
        name = dev["name"]
        os_type = dev.get("platform", {}).get("slug", "iosxe")
        mgmt_ip = get_primary_ip(dev)
        if not mgmt_ip:
            continue  # skip devices without management IP
        testbed["devices"][name] = {
            "os": os_type,
            "type": dev.get("device_type", {}).get("model", "router"),
            "connections": {
                "cli": {
                    "protocol": "ssh",
                    "ip": mgmt_ip
                }
            },
            "credentials": {
                "default": {
                    "username": "<username>",
                    "password": "<password>"
                }
            }
        }
    return testbed

if __name__ == "__main__":
    devices = get_devices(NAUTOBOT_SITE)
    if not devices:
        print(f"No devices found for site '{NAUTOBOT_SITE}'.", file=sys.stderr)
        sys.exit(1)
    testbed = build_testbed(devices)
    yaml.dump(testbed, sys.stdout, default_flow_style=False, sort_keys=False)
``` 