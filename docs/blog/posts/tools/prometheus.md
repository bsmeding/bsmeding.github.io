---
title: Prometheus Introduction & Getting Started
authors: [bsmeding]
date: 2024-10-20
summary: A hands-on introduction to Prometheus, its monitoring features, and how to collect your first metrics.
tags:
  - prometheus
  - monitoring
  - observability
  - devops
---

# Prometheus: Introduction & Getting Started

**Prometheus** is an open-source monitoring and alerting toolkit designed for reliability and scalability. It is widely used for collecting metrics and powering observability in cloud-native environments.

<!-- more -->

## Why Use Prometheus?
- Collect and store time-series metrics
- Powerful query language (PromQL)
- Integrates with Grafana and alerting systems

## How Prometheus Works
- Scrapes metrics from targets via HTTP endpoints
- Stores data in a time-series database
- Supports service discovery and dynamic environments

## Quick Start Example
1. **Run Prometheus (Docker):**
   ```bash
   docker run -d -p 9090:9090 prom/prometheus
   ```
2. **Access the UI:**
   - Open `http://localhost:9090` in your browser
3. **Add a scrape target (edit `prometheus.yml`):**
   ```yaml
   scrape_configs:
     - job_name: 'example'
       static_configs:
         - targets: ['localhost:9090']
   ```
4. **Reload Prometheus config:**
   - Use the UI or send a SIGHUP to the container

## Learn More
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Getting Started Guide](https://prometheus.io/docs/introduction/first_steps/) 