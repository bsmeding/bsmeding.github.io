---
authors: [bsmeding]
date: 2025-08-10
title: Building a Reusable Network Automation Lab with Containerlab
tags: ["network automation", "containerlab", "lab", "automation", "network", "automation"]
toc: true
layout: single
comments: true
---

# Building Your Reusable Network Automation Lab with Containerlab

*The standard lab topology used in my Nautobot automation series.*

<!-- more -->

---

## 1. Introduction
A consistent lab environment is essential for learning and testing network automation workflows.  
This guide creates a **reusable Containerlab topology** that you can use for all tutorials in the Nautobot automation series.

**Why Containerlab?**
- Runs entirely in Docker.
- Supports Arista EOS images.
- Easy to version control and reproduce.
- Simulates realistic enterprise network environments with Cisco-like syntax.

---

## 2. Lab Topology Overview

**Devices:**
- **2x Access Switches** (`access1`, `access2`) - Arista cEOS-lab
- **1x Distribution/Core Switch** (`dist1`) - Arista cEOS-lab
- **1x Router/WAN Edge** (`rtr1`) - Arista cEOS-lab
- **1x Management Host** (`mgmt`) - Linux container
- **1x Workstation Host** (`workstation1`) - Linux container
- **1x Nautobot Container** (Docker)
- **1x ZTP Server** (Linux container)

**Logical Layout:**
```
           [rtr1]
             |
          [dist1]
          /     \
     [access1] [access2]
     
     [mgmt] [nautobot] [ztp]
          [workstation1]
```

**Network Segments:**
- **Data Plane**: access1/2 ↔ dist1 ↔ rtr1
- **Management Plane**: All devices on mgmt-net (172.20.20.0/24)

---

## 3. Installing Containerlab

**Prerequisites:**
- Docker & Docker Compose
- At least 8GB RAM
- Containerlab installed

For detailed installation instructions, see the [ContainerLab Installation Guide](/blog/posts/tools/containerlab.html).

Quick install:
```bash
curl -sL https://get.containerlab.dev | bash
containerlab version
```

---

## 4. Getting Network OS Images

For comprehensive instructions on downloading and importing network OS images, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started/).

**Free Downloadable Images:**
- **Arista cEOS-lab** - Available from Arista's website

> ⚠️ Licensing applies. Obtain images legally from vendor websites.

**Quick Download and Import:**
```bash
# Arista cEOS-lab
docker import cEOS-lab-4.34.2F.tar.xz arista/ceos:4.34.2F
```

---

## 5. Containerlab Topology File

Save as `lab-topology.clab.yml`:

```yaml

name: nautobot-lab
topology:
  nodes:
    access1:
      kind: arista_ceos
      image: arista/ceos:4.34.2F
    access2:
      kind: arista_ceos
      image: arista/ceos:4.34.2F
    dist1:
      kind: arista_ceos
      image: arista/ceos:4.34.2F
    rtr1:
      kind: arista_ceos
      image: arista/ceos:4.34.2F
    ztp:
      kind: linux
      image: alpine
    mgmt:
      kind: linux
      image: alpine
    workstation1:
      kind: linux
      image: alpine
  links:
    - endpoints: ["access1:eth1", "dist1:eth1"]
    - endpoints: ["access2:eth1", "dist1:eth2"]
    - endpoints: ["dist1:eth3", "rtr1:eth1"]

mgmt:
  network: mgmt-net
  ipv4-subnet: 172.20.20.0/24
```
In current versions it is not possible anymore to set static ip addresses from the `yaml`, Containerlab will automatically create an ansible-inventory if needed with the IP addresses assigned


---

## 6. Deploying the Lab

```bash
containerlab deploy -t lab-topology.clab.yml
```

Verify:
```bash
containerlab inspect
```

---

## 6.1 Bootstrap Configs (Arista EOS and Alpine Linux)

Use the following startup configs exactly as in the Zero to Hero repo. Source: [bootstrap configs](https://github.com/bsmeding/nautobot_zero_to_hero/tree/main/containerlab/bootstrap).

Place these as startup-configs via the containerlab node `startup-config` option or apply after first boot.

**access1.cfg (Arista EOS)**
```bash
!
! Bootstrap configuration for access1 (Arista EOS)
! Management interface and SSH configuration
! Hostname is incorrect
! PROBLEM: Ethernet2 is in wrong VLAN (999) - breaks connectivity to workstation1!
!
hostname nonamedswitch
!
interface Management0
   ip address 172.20.20.11/24
   no shutdown
   description "Management interface"
!
! Data interfaces
interface Ethernet1
   no shutdown
   description "Uplink to dist1"
   switchport mode trunk
   switchport trunk allowed vlan 10
!
interface Ethernet2
   shutdown
   description "Connected to workstation1 - DISABLED"
   switchport mode access
   switchport access vlan 10
   ! PROBLEM: Interface is SHUTDOWN! Needs to be enabled
!
interface Ethernet3
   shutdown
   description "Available for connections"
!
! Define VLANs
vlan 10
   name Data_VLAN
!
! Enable SSH
management ssh
   no shutdown
!
! Enable API for automation
management api http-commands
   no shutdown
   protocol http
   protocol https port 443
!
! Basic security
username admin privilege 15 secret admin
!
! Save configuration
write memory
!
```

**access2.cfg (Arista EOS)**
```bash
!
! Bootstrap configuration for access2 (Arista EOS)
! Management interface and SSH configuration
!
interface Management0
   ip address 172.20.20.12/24
   no shutdown
   description "Management interface"
!
! Data interfaces
interface Ethernet1
   no shutdown
   description "Data interface - connected to dist1"
   switchport mode trunk
   switchport trunk allowed vlan all
!
interface Ethernet2
   no shutdown
   description "Data interface - available for connections"
   switchport mode access
   switchport access vlan 20
!
interface Ethernet3
   no shutdown
   description "Data interface - available for connections"
   switchport mode access
   switchport access vlan 30
!
! Enable SSH
management ssh
   no shutdown
!
! Enable API for automation
management api http-commands
   no shutdown
   protocol http
   protocol https port 443
!
! Basic security
username admin privilege 15 secret admin
!
! Enable logging
logging host 172.20.20.1
!
! Enable routing to host
ip routing
ip route 0.0.0.0 0.0.0.0 Management0 172.20.20.1
!
! Save configuration
write memory
!
```

**dist1.cfg (Arista cEOS)**
```bash
!
! Bootstrap configuration for dist1 (Arista cEOS)
! Distribution switch configuration
!
hostname dist1
!
! Configure VLANs
vlan 10
   name DATA_VLAN
!
! Management interface
interface Management0
   description Management Interface
   ip address 172.20.20.13/24
   no shutdown
!
! Data interfaces - Layer 2 switchports
interface Ethernet1
   description Connected to access1
   switchport mode trunk
   switchport trunk allowed vlan 10
   no shutdown
!
interface Ethernet2
   description Connected to access2
   switchport mode trunk
   switchport trunk allowed vlan 10
   no shutdown
!
interface Ethernet3
   description Connected to rtr1
   switchport mode trunk
   switchport trunk allowed vlan 10
   no shutdown
!
! Enable gNMI
management api gnmi
   transport grpc default
      port 6030
!
! Enable NETCONF
management api netconf
   transport ssh default
!
! Admin user configuration
username admin privilege 15 secret admin
!
! Enable eAPI (REST API)
management api http-commands
   no shutdown
   protocol https
!
end
```

**rtr1.cfg (Arista cEOS)**
```bash
!
! Bootstrap configuration for rtr1 (Arista cEOS)
! Router configuration
! PROBLEM: Ethernet2 is shutdown - breaks connectivity to mgmt!
!
hostname rtr1
!
! Configure VLANs
vlan 10
   name DATA_VLAN
!
! Management interface
interface Management0
   description Management Interface
   ip address 172.20.20.14/24
   no shutdown
!
! Data interfaces - Layer 2 switchports
interface Ethernet1
   description Uplink to dist1
   switchport mode trunk
   switchport trunk allowed vlan 10
   no shutdown
!
interface Ethernet2
   shutdown
   description Connected to mgmt server - DISABLED
   switchport mode access
   switchport access vlan 10
   ! PROBLEM: Interface is SHUTDOWN! Needs to be enabled
!
interface Ethernet3
   description Available for connections
   shutdown
!
! Enable gNMI
management api gnmi
   transport grpc default
      port 6030
!
! Enable NETCONF
management api netconf
   transport ssh default
!
! Admin user configuration
username admin privilege 15 secret admin
!
! Enable eAPI (REST API)
management api http-commands
   no shutdown
   protocol https
!
end
```

**mgmt.cfg (Alpine Linux)**
```bash
# Bootstrap configuration for mgmt (Alpine Linux)
# Management server configuration

# Configure management interface (eth0)
cat > /etc/network/interfaces << EOF
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 172.20.20.16
    netmask 255.255.255.0
    gateway 172.20.20.1

auto eth1
iface eth1 inet static
    address 10.0.0.16
    netmask 255.255.255.0
EOF

# Configure data interface (eth1)
# eth1 will be used for management server connections

# Set root password
echo "root:admin" | chpasswd

# Enable SSH with root login and password authentication
apk add --no-cache openssh
ssh-keygen -A
sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
rc-update add sshd default

# Install network management tools
apk add --no-cache curl wget net-tools tcpdump nmap iperf3

# Install Python and pip for automation (commented out for faster startup)
# apk add python3 py3-pip
# pip3 install requests paramiko napalm

# Create management directory structure
mkdir -p /opt/management/{scripts,configs,logs}

# Add lab devices to /etc/hosts for easy access
cat >> /etc/hosts << HOSTS_EOF
# Lab devices
172.20.20.11    access1.lab access1
172.20.20.12    access2.lab access2
172.20.20.13    dist1.lab dist1
172.20.20.14    rtr1.lab rtr1
172.20.20.15    workstation1.lab workstation1
172.20.20.16    mgmt.lab mgmt management
HOSTS_EOF

# Set up basic logging
echo "Management server initialized at $(date)" > /var/log/management.log

# Enable network interfaces
ifup eth0
ifup eth1

echo "Management server bootstrap completed"

# Start SSH daemon in background (without -D flag)
/usr/sbin/sshd

# Script completes here, allowing containerlab deployment to finish
echo "Bootstrap script finished"
```

**workstation1.cfg (Alpine Linux)**
```bash
# Bootstrap configuration for workstation1 (Alpine Linux)
# Workstation for network testing and demonstrations

# Configure management interface (eth0)
cat > /etc/network/interfaces << EOF
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 172.20.20.15
    netmask 255.255.255.0
    gateway 172.20.20.1

auto eth1
iface eth1 inet static
    address 10.0.0.15
    netmask 255.255.255.0
EOF

# Install network testing tools
apk add --no-cache openssh iproute2 ethtool curl iputils bash tcpdump iperf3 mtr

# Set root password
echo "root:admin" | chpasswd

# Enable SSH with root login and password authentication
ssh-keygen -A
sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
rc-update add sshd default

# Create workspace directory
mkdir -p /home/workspace

# Add lab devices to /etc/hosts for easy access
cat >> /etc/hosts << HOSTS_EOF
# Lab devices
172.20.20.11    access1.lab access1
172.20.20.12    access2.lab access2
172.20.20.13    dist1.lab dist1
172.20.20.14    rtr1.lab rtr1
172.20.20.15    workstation1.lab workstation1
172.20.20.16    mgmt.lab mgmt management
HOSTS_EOF

# Set up basic logging
echo "Workstation1 initialized at $(date)" > /var/log/workstation.log

# Enable network interfaces
ifup eth0
ifup eth1

echo "Workstation1 bootstrap completed - Ready for network automation demos"

# Start SSH daemon in background (without -D flag)
/usr/sbin/sshd

# Script completes here, allowing containerlab deployment to finish
echo "Bootstrap script finished"
```

---

## 7. Configuring Management Access

- Assign management IPs to devices.
- Enable SSH on devices.
- Use NAT/port-forwarding if needed.

**Example (Arista EOS):**
```bash
configure
interface Management0
   ip address 172.20.20.11/24
   no shutdown
exit
management ssh
   no shutdown
exit
```

---

## 8. Optional: Nautobot & ZTP Integration

Example `docker-compose.yml`:

```yaml
version: "3.8"
services:
  nautobot:
    # image: networktocode/nautobot:stable
    # image: bsmeding/nautobot:2.1.9-py3.11
    container_name: nautobot
    image: &shared_image bsmeding/nautobot:2.4
    depends_on:
      - postgres
      - redis
    networks:
      - mgmt-net
    ports:
      - "8080:8080"  # Exposes Nautobot on localhost:8080
    environment:
      - NAUTOBOT_DEBUG=True
      - NAUTOBOT_DJANGO_EXTENSIONS_ENABLED=False
      - NAUTOBOT_DJANGO_TOOLBAR_ENABLED=False
      - NAUTOBOT_HIDE_RESTRICTED_UI=True
      - NAUTOBOT_LOG_LEVEL=WARNING
      - NAUTOBOT_METRICS_ENABLED=False
      - NAUTOBOT_NAPALM_TIMEOUT=5
      - NAUTOBOT_MAX_PAGE_SIZE=0
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_ALLOWED_HOSTS=*
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379
      - NAUTOBOT_SUPERUSER_NAME=admin
      - NAUTOBOT_SUPERUSER_PASSWORD=admin
      - NAUTOBOT_SUPERUSER_API_TOKEN=1234567890abcde0987654321
      - NAUTOBOT_CREATE_SUPERUSER=true
      - NAUTOBOT_INSTALLATION_METRICS_ENABLED=false
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_SECURE_HSTS_SECONDS=3600
      - NAUTOBOT_SECURE_SSL_REDIRECT=True
      - NAUTOBOT_SESSION_COOKIE_SECURE=True
      - NAUTOBOT_CSRF_COOKIE_SECURE=True
    volumes:
      - nautobot_config:/opt/nautobot/
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
    command: ["nautobot-server", "runserver", "0.0.0.0:8080"]



  postgres:
    image: postgres:13-alpine
    container_name: postgres
    command:
      - "-c"
      - "max_connections=1000"
    networks:
      - mgmt-net
    healthcheck:
      test: "pg_isready --username=$$POSTGRES_USER --dbname=$$POSTGRES_DB"
      interval: "10s"
      timeout: "5s"
      retries: 10    
    environment:
      POSTGRES_USER: nautobot
      POSTGRES_PASSWORD: nautobotpassword
      POSTGRES_DB: nautobot
    volumes:
      # - ./mapped_folders/postgres-data:/var/lib/postgresql/data             # Not possible with compose due to folder permissions, use docker volume instead  
      - "postgres_data:/var/lib/postgresql/data"
    restart: unless-stopped

  redis:
    image: redis:6
    container_name: redis
    networks:
      - mgmt-net
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery-beat:
    container_name: nautobot_celery_beat
    image: *shared_image
    command: nautobot-server celery beat
    networks:
      - mgmt-net
    depends_on:
      nautobot:
        condition: "service_healthy"
    networks:
      - mgmt-net
    volumes:
      - nautobot_config:/opt/nautobot/
    environment:
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py

  celery-worker-1:
    image: *shared_image
    container_name: nautobot_celery_worker_1
    command: nautobot-server celery worker --concurrency=4
    depends_on:
      nautobot:
        condition: "service_healthy"
    networks:
      - mgmt-net
    healthcheck:
      interval: "30s"
      timeout: "10s"
      start_period: "30s"
      retries: 3
      test:
        [
          "CMD",
          "bash",
          "-c",
          "nautobot-server celery inspect ping --destination celery@$$HOSTNAME"  ## $$ because of docker-compose
        ]
    volumes:
      - nautobot_config:/opt/nautobot/
    environment:
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py

  ztp:
    image: alpine:latest
    networks:
      - mgmt-net

volumes:
  nautobot_config: {}
  postgres_data: {}
  redis_data: {}

networks:
  mgmt-net:
    external: true
```

---

## 9. Saving & Reusing the Lab

Save `lab-topology.clab.yml` to GitHub.

**Reset Script:**
```bash
#!/bin/bash
containerlab destroy -t lab-topology.clab.yml
containerlab deploy -t lab-topology.clab.yml
```

Make executable:
```bash
chmod +x reset.sh
```

---

## 10. Next Steps

Your lab is ready.  
Continue to **Part 1** of the Nautobot series to start using this lab for inventory, compliance, and automation workflows.
