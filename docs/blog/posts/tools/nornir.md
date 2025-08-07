---
title: Nornir Introduction & Getting Started
authors: [bsmeding]
date: 2024-08-24
summary: An introduction to Nornir, a Python automation framework for network engineers, with a quick start example.
tags:
  - nornir
  - network automation
  - python
  - devops
---

# Nornir: Introduction & Getting Started

![Nornir Logo](https://nornir.readthedocs.io/en/latest/_static/nornir-logo.png?w=300&h=auto){: style="max-width: 300px; display: block; margin: 0 auto;"}

**Nornir** is a pure Python automation framework for network engineers. It provides inventory management, task execution, and plugin support for network automation workflows.
<!-- more -->

## Why Use Nornir?
- Automate network device configuration and validation
- Use Python for full programmability
- Integrate with other Python libraries and tools

## How Nornir Works
- Inventory is defined in YAML or Python
- Tasks are Python functions (or plugins)
- Results are returned as Python objects for further processing

## Quick Start Example
1. **Install Nornir:**
   ```bash
   pip install nornir
   ```
2. **Create a simple inventory (`inventory/hosts.yaml`):**
   ```yaml
   r1:
     hostname: 192.0.2.1
     username: admin
     password: admin
   ```
3. **Write a basic script (`main.py`):**
   ```python
   from nornir import InitNornir
   from nornir.core.task import Task, Result

   def hello_world(task: Task) -> Result:
       return Result(host=task.host, result=f"Hello from {task.host.name}")

   nr = InitNornir()
   result = nr.run(task=hello_world)
   print(result)
   ```
4. **Run the script:**
   ```bash
   python main.py
   ```

## Learn More
- [Nornir Documentation](https://nornir.readthedocs.io/)
- [Getting Started Guide](https://nornir.readthedocs.io/en/latest/tutorials/getting_started.html) 