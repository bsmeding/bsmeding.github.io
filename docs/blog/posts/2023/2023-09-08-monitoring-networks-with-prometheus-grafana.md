---
title: "Monitoring Networks with Prometheus and Grafana: A Complete Guide"
authors: [bsmeding]
date: 2023-09-08
summary: Learn how to implement comprehensive network monitoring using Prometheus and Grafana, from basic setup to advanced dashboards and alerting.
tags:
  - monitoring
  - prometheus
  - grafana
  - netdevops
  - observability
  - networking
---

# Monitoring Networks with Prometheus and Grafana: A Complete Guide

**Network monitoring** is a critical component of NetDevOps, providing visibility into network performance, health, and availability. This guide explores how to implement comprehensive network monitoring using **Prometheus** and **Grafana**, from basic setup to advanced dashboards and alerting.

<!-- more -->

## Why Prometheus and Grafana for Network Monitoring?

Prometheus and Grafana form a powerful combination for network monitoring:

- **Prometheus**: Time-series database with powerful querying capabilities
- **Grafana**: Rich visualization and dashboard platform
- **Scalability**: Handle large-scale network monitoring
- **Flexibility**: Support for custom metrics and integrations
- **Open Source**: Cost-effective and community-driven

## Understanding the Monitoring Stack

### Prometheus Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Prometheus    │    │   Node Exporter │    │   Network       │
│   Server        │◄───┤   (on hosts)    │◄───┤   Devices       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Grafana       │    │   Alertmanager  │    │   Custom        │
│   Dashboards    │    │   (Alerts)      │    │   Exporters     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Installation and Setup

### 1. Install Prometheus

```bash
# Download Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvf prometheus-*.tar.gz
cd prometheus-*

# Create systemd service
sudo tee /etc/systemd/system/prometheus.service << EOF
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus \
  --config.file /etc/prometheus/prometheus.yml \
  --storage.tsdb.path /var/lib/prometheus/ \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090

[Install]
WantedBy=default.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
```

### 2. Install Grafana

```bash
# Add Grafana repository
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Install Grafana
sudo apt update
sudo apt install grafana

# Start Grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

### 3. Install Node Exporter

```bash
# Download Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvf node_exporter-*.tar.gz
cd node_exporter-*

# Create systemd service
sudo tee /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=default.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
```

## Configuration

### Prometheus Configuration

```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'network_devices'
    static_configs:
      - targets: ['192.168.1.1:9100', '192.168.1.2:9100']
    scrape_interval: 30s

  - job_name: 'snmp_exporter'
    static_configs:
      - targets: ['192.168.1.1', '192.168.1.2']
    metrics_path: /snmp
    params:
      module: [if_mib]
    scrape_interval: 30s
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9116
```

### SNMP Exporter Configuration

```yaml
# /etc/snmp_exporter/snmp.yml
modules:
  if_mib:
    walk:
      - 1.3.6.1.2.1.2.2.1.1  # ifIndex
      - 1.3.6.1.2.1.2.2.1.2  # ifDescr
      - 1.3.6.1.2.1.2.2.1.3  # ifType
      - 1.3.6.1.2.1.2.2.1.4  # ifMtu
      - 1.3.6.1.2.1.2.2.1.5  # ifSpeed
      - 1.3.6.1.2.1.2.2.1.6  # ifPhysAddress
      - 1.3.6.1.2.1.2.2.1.7  # ifAdminStatus
      - 1.3.6.1.2.1.2.2.1.8  # ifOperStatus
      - 1.3.6.1.2.1.2.2.1.10 # ifInOctets
      - 1.3.6.1.2.1.2.2.1.16 # ifOutOctets
      - 1.3.6.1.2.1.2.2.1.14 # ifInErrors
      - 1.3.6.1.2.1.2.2.1.20 # ifOutErrors
    version: 2
    auth:
      community: public
    retries: 3
    timeout: 10s
    interval: 30s
```

## Network-Specific Monitoring

### Interface Monitoring

```yaml
# Custom network metrics exporter
#!/usr/bin/env python3
import time
import subprocess
import re
from prometheus_client import start_http_server, Gauge

# Define metrics
interface_up = Gauge('interface_up', 'Interface operational status', ['interface'])
interface_speed = Gauge('interface_speed', 'Interface speed in Mbps', ['interface'])
interface_errors = Gauge('interface_errors', 'Interface error count', ['interface', 'type'])

def get_interface_stats():
    try:
        # Get interface statistics using ip command
        result = subprocess.run(['ip', '-s', 'link'], capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if ':' in line and not line.startswith(' '):
                # Parse interface name
                interface_match = re.search(r'(\d+):\s+(\w+):', line)
                if interface_match:
                    interface = interface_match.group(2)
                    
                    # Get interface status
                    status_result = subprocess.run(['ip', 'link', 'show', interface], 
                                                 capture_output=True, text=True)
                    if 'UP' in status_result.stdout:
                        interface_up.labels(interface=interface).set(1)
                    else:
                        interface_up.labels(interface=interface).set(0)
                        
    except Exception as e:
        print(f"Error getting interface stats: {e}")

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        get_interface_stats()
        time.sleep(15)
```

### Bandwidth Monitoring

```python
# bandwidth_monitor.py
import psutil
import time
from prometheus_client import start_http_server, Gauge

# Define metrics
bytes_sent = Gauge('network_bytes_sent', 'Bytes sent per interface', ['interface'])
bytes_recv = Gauge('network_bytes_recv', 'Bytes received per interface', ['interface'])
packets_sent = Gauge('network_packets_sent', 'Packets sent per interface', ['interface'])
packets_recv = Gauge('network_packets_recv', 'Packets received per interface', ['interface'])

def collect_network_metrics():
    net_io = psutil.net_io_counters(pernic=True)
    
    for interface, stats in net_io.items():
        bytes_sent.labels(interface=interface).set(stats.bytes_sent)
        bytes_recv.labels(interface=interface).set(stats.bytes_recv)
        packets_sent.labels(interface=interface).set(stats.packets_sent)
        packets_recv.labels(interface=interface).set(stats.packets_recv)

if __name__ == '__main__':
    start_http_server(8001)
    while True:
        collect_network_metrics()
        time.sleep(15)
```

## Grafana Dashboards

### Network Overview Dashboard

```json
{
  "dashboard": {
    "title": "Network Overview",
    "panels": [
      {
        "title": "Interface Status",
        "type": "stat",
        "targets": [
          {
            "expr": "interface_up",
            "legendFormat": "{{interface}}"
          }
        ]
      },
      {
        "title": "Bandwidth Utilization",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(ifInOctets[5m]) * 8 / 1000000",
            "legendFormat": "{{instance}} - In (Mbps)"
          },
          {
            "expr": "rate(ifOutOctets[5m]) * 8 / 1000000",
            "legendFormat": "{{instance}} - Out (Mbps)"
          }
        ]
      },
      {
        "title": "Interface Errors",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(ifInErrors[5m])",
            "legendFormat": "{{instance}} - In Errors"
          },
          {
            "expr": "rate(ifOutErrors[5m])",
            "legendFormat": "{{instance}} - Out Errors"
          }
        ]
      }
    ]
  }
}
```

### Custom Network Dashboard

```json
{
  "dashboard": {
    "title": "Network Performance",
    "panels": [
      {
        "title": "Network Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile latency"
          }
        ]
      },
      {
        "title": "Packet Loss",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(icmp_packet_loss_total[5m])",
            "legendFormat": "Packet loss rate"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "netstat_tcp_established",
            "legendFormat": "TCP connections"
          }
        ]
      }
    ]
  }
}
```

## Alerting Configuration

### Alert Rules

```yaml
# /etc/prometheus/alert_rules.yml
groups:
  - name: network_alerts
    rules:
      - alert: InterfaceDown
        expr: interface_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Interface {{ $labels.interface }} is down"
          description: "Interface {{ $labels.interface }} has been down for more than 1 minute"

      - alert: HighBandwidthUsage
        expr: rate(ifInOctets[5m]) * 8 / 1000000 > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High bandwidth usage on {{ $labels.instance }}"
          description: "Interface {{ $labels.interface }} is using more than 100 Mbps"

      - alert: InterfaceErrors
        expr: rate(ifInErrors[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Interface {{ $labels.interface }} has error rate > 0.1 errors/sec"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is above 500ms"
```

### Alertmanager Configuration

```yaml
# /etc/alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alertmanager@example.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://127.0.0.1:5001/'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
```

## Advanced Monitoring Scenarios

### Docker Container Monitoring

```yaml
# docker-compose.yml for monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
```

### Custom Network Metrics

```python
# custom_network_exporter.py
import subprocess
import time
from prometheus_client import start_http_server, Gauge, Counter

# Define custom metrics
network_connections = Gauge('network_connections_total', 'Total network connections', ['protocol', 'state'])
network_bandwidth = Gauge('network_bandwidth_bytes', 'Network bandwidth in bytes', ['interface', 'direction'])
network_packet_loss = Counter('network_packet_loss_total', 'Total packet loss', ['destination'])

def get_network_connections():
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
        lines = result.stdout.split('\n')[1:]  # Skip header
        
        tcp_established = 0
        tcp_listen = 0
        udp_listen = 0
        
        for line in lines:
            if 'tcp' in line and 'ESTAB' in line:
                tcp_established += 1
            elif 'tcp' in line and 'LISTEN' in line:
                tcp_listen += 1
            elif 'udp' in line and 'UNCONN' in line:
                udp_listen += 1
        
        network_connections.labels(protocol='tcp', state='established').set(tcp_established)
        network_connections.labels(protocol='tcp', state='listen').set(tcp_listen)
        network_connections.labels(protocol='udp', state='listen').set(udp_listen)
        
    except Exception as e:
        print(f"Error getting network connections: {e}")

def ping_test():
    destinations = ['8.8.8.8', '1.1.1.1', 'google.com']
    
    for dest in destinations:
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', dest], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                network_packet_loss.labels(destination=dest).inc()
        except Exception as e:
            print(f"Error pinging {dest}: {e}")

if __name__ == '__main__':
    start_http_server(8002)
    while True:
        get_network_connections()
        ping_test()
        time.sleep(30)
```

## Performance Optimization

### Prometheus Configuration Optimization

```yaml
# Optimized prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: 'network-monitor'

storage:
  tsdb:
    retention.time: 15d
    retention.size: 50GB

scrape_configs:
  - job_name: 'network_devices'
    scrape_interval: 30s
    scrape_timeout: 10s
    static_configs:
      - targets: ['192.168.1.1:9100', '192.168.1.2:9100']
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: '.*'
        action: keep
```

### Grafana Performance Tuning

```ini
# /etc/grafana/grafana.ini
[server]
http_port = 3000
protocol = http

[database]
type = sqlite3
path = /var/lib/grafana/grafana.db

[session]
provider = file

[security]
admin_user = admin
admin_password = admin

[users]
allow_sign_up = false

[server]
root_url = http://localhost:3000/

[log]
mode = console
level = info
```

## Troubleshooting

### Common Issues and Solutions

1. **Prometheus not scraping targets**
```bash
# Check target status
curl http://localhost:9090/api/v1/targets

# Check configuration
promtool check config /etc/prometheus/prometheus.yml
```

2. **Grafana not connecting to Prometheus**
```bash
# Test Prometheus connection
curl http://localhost:9090/api/v1/query?query=up

# Check Grafana logs
sudo journalctl -u grafana-server -f
```

3. **High memory usage**
```yaml
# Optimize retention and scrape intervals
global:
  scrape_interval: 30s  # Increase from 15s

storage:
  tsdb:
    retention.time: 7d  # Reduce from 15d
```

## Conclusion

Prometheus and Grafana provide a powerful foundation for network monitoring in NetDevOps environments. By implementing the configurations and best practices outlined in this guide, you can achieve comprehensive visibility into your network infrastructure.

Key takeaways:
- Start with basic monitoring and gradually add complexity
- Use custom exporters for network-specific metrics
- Implement proper alerting and notification
- Optimize performance for large-scale deployments
- Regular maintenance and updates are essential

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [SNMP Exporter](https://github.com/prometheus/snmp_exporter)
- [Network Monitoring Best Practices](https://networktocode.com/blog/)

---

*This guide provides a comprehensive overview of network monitoring with Prometheus and Grafana. For more advanced topics, check out our other articles on specific monitoring scenarios and best practices.* 