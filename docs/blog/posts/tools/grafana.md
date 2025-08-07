---
title: Grafana Introduction & Getting Started
authors: [bsmeding]
date: 2024-10-27
summary: A quick start to Grafana, its dashboarding capabilities, and how to visualize your first metrics.
tags:
  - grafana
  - monitoring
  - observability
  - dashboards
  - devops
---

# Grafana: Introduction & Getting Started

![Grafana Logo](https://grafana.com/static/assets/img/logo_new_transparent_400x100.png){: style="max-width: 300px; display: block; margin: 0 auto;"}

**Grafana** is an open-source analytics and monitoring platform for visualizing time-series data. It is widely used to create dashboards and alerts from data sources like Prometheus, InfluxDB, and more.
<!-- more -->

## Why Use Grafana?
- Visualize metrics from multiple sources
- Build interactive dashboards
- Set up alerts and notifications

## How Grafana Works
- Connects to data sources (Prometheus, InfluxDB, etc.)
- Dashboards are built using a web UI
- Supports plugins and integrations

## Quick Start Example
1. **Run Grafana (Docker):**
   ```bash
   docker run -d -p 3000:3000 grafana/grafana
   ```
2. **Access the UI:**
   - Open `http://localhost:3000` (default login: admin / admin)
3. **Add a data source:**
   - Use the UI to add Prometheus, InfluxDB, etc.
4. **Create a dashboard:**
   - Use the UI to build visualizations

## Learn More
- [Grafana Documentation](https://grafana.com/docs/)
- [Getting Started Guide](https://grafana.com/docs/grafana/latest/getting-started/) 