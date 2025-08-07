---
title: InfluxDB Introduction & Getting Started
authors: [bsmeding]
date: 2024-11-03
summary: A beginner's guide to InfluxDB, its time-series database features, and how to store and query your first metrics.
tags:
  - influxdb
  - monitoring
  - time-series
  - devops
---

# InfluxDB: Introduction & Getting Started

![InfluxDB Logo](https://www.influxdata.com/wp-content/uploads/2021/05/InfluxDB-logo.png?w=300&h=auto){: style="max-width: 300px; display: block; margin: 0 auto;"}

**InfluxDB** is an open-source time-series database designed for storing and analyzing high volumes of time-stamped data, such as metrics and events.
<!-- more -->

## Why Use InfluxDB?
- Store and query time-series data efficiently
- Integrate with Grafana, Telegraf, and other tools
- Ideal for IoT, monitoring, and analytics

## How InfluxDB Works
- Data is written and queried using InfluxQL or Flux
- Supports retention policies and continuous queries
- Integrates with visualization and monitoring tools

## Quick Start Example
1. **Run InfluxDB (Docker):**
   ```bash
   docker run -d -p 8086:8086 influxdb:latest
   ```
2. **Access the UI:**
   - Open `http://localhost:8086` in your browser
3. **Write data (CLI):**
   ```bash
   docker exec -it <container_id> influx
   CREATE DATABASE mydb
   INSERT cpu,host=server01 usage=0.5
   SELECT * FROM cpu
   ```

## Learn More
- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/)
- [Getting Started Guide](https://docs.influxdata.com/influxdb/latest/get-started/) 