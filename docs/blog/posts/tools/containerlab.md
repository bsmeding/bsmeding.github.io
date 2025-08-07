---
title: "ContainerLab"
tags: ["containerlab", "network automation", "lab environment", "docker", "networking", "testing"]
date: 2024-06-11
summary: ContainerLab is a powerful tool for creating and managing container-based network labs. Learn how to set up a complete lab environment with free vendor images for network automation testing.
---

# ContainerLab

![ContainerLab Logo](https://camo.githubusercontent.com/223ecd49b5a869d166bd6b86752960600ccb5fb10b8b5bc278e51ba06550690e/68747470733a2f2f6769746c61622e636f6d2f72646f64696e2f706963732f2d2f77696b69732f75706c6f6164732f30316663646332313265653163376465373065663564326138643130393034342f696d6167652e706e67){: style="max-width: 300px; display: block; margin: 0 auto;"}

[ContainerLab](https://containerlab.dev/) is a **container-based network lab orchestrator** that allows you to create and manage network topologies using containerized network operating systems. It's perfect for network automation testing, learning, and development without the overhead of traditional virtualization.
<!-- more -->

## What is ContainerLab?

ContainerLab is an open-source tool that enables you to:
- **Deploy network topologies** using containerized network operating systems
- **Test network automation** with real network devices
- **Create reproducible lab environments** for learning and development
- **Run multiple vendor images** in a single lab topology
- **Integrate with automation tools** like Ansible, Nornir, and Terraform

## Key Features
- **Multi-vendor Support**: Cisco, Arista, Nokia, Juniper, and more
- **Docker-based**: Lightweight and fast deployment
- **Topology Management**: YAML-based topology definitions
- **CLI Interface**: Easy-to-use command-line tools
- **Integration Ready**: Works with popular automation tools
- **Free Images**: Support for vendor images that can be used freely

## Installation Guide

### Prerequisites
- **Linux** (Ubuntu 20.04+, CentOS 8+, or similar)
- **Docker** installed and running
- **Docker Compose** (optional, for advanced setups)
- **Git** for cloning repositories

### Step 1: Install Docker

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

#### CentOS/RHEL
```bash
# Install required packages
sudo yum install -y yum-utils

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
```

### Step 2: Install ContainerLab

#### Method 1: Using the Official Install Script (Recommended)
```bash
# Download and run the installation script
bash -c "$(curl -sL https://get.containerlab.dev)"

# Verify installation
containerlab version
```

#### Method 2: Manual Installation
```bash
# Download the latest release
VERSION=$(curl -s https://api.github.com/repos/srl-labs/containerlab/releases/latest | grep 'tag_name' | cut -d\" -f4)
wget https://github.com/srl-labs/containerlab/releases/download/${VERSION}/containerlab_${VERSION}_Linux_amd64.tar.gz

# Extract and install
sudo tar -xzf containerlab_${VERSION}_Linux_amd64.tar.gz -C /usr/local/bin containerlab
sudo chmod +x /usr/local/bin/containerlab

# Verify installation
containerlab version
```

### Step 3: Install Additional Tools (Optional)

#### Install Docker Compose
```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

#### Install Network Tools
```bash
# Install additional networking tools
sudo apt install -y bridge-utils iproute2 net-tools tcpdump

# Or for CentOS/RHEL
sudo yum install -y bridge-utils iproute net-tools tcpdump
```

### Step 4: Docker Compose Installation (Alternative Method)

For those who prefer using Docker Compose for ContainerLab deployment, here's a complete setup:

#### Docker Compose Setup
Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  containerlab:
    image: ghcr.io/srl-labs/containerlab:latest
    container_name: containerlab
    privileged: true
    network_mode: host
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./labs:/labs
      - ./configs:/configs
      - ./images:/images
    environment:
      - CLAB_HOST=0.0.0.0
      - CLAB_PORT=8080
    restart: unless-stopped
    command: ["sleep", "infinity"]

  # Optional: Web UI for ContainerLab
  containerlab-ui:
    image: ghcr.io/srl-labs/containerlab-ui:latest
    container_name: containerlab-ui
    ports:
      - "3000:3000"
    environment:
      - CLAB_API_URL=http://localhost:8080
    depends_on:
      - containerlab
    restart: unless-stopped

  # Optional: Grafana for lab monitoring
  grafana:
    image: grafana/grafana:latest
    container_name: containerlab-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

  # Optional: Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:latest
    container_name: containerlab-prometheus
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
    restart: unless-stopped

volumes:
  grafana_data:
  prometheus_data:
```

#### Prometheus Configuration
Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'containerlab'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics

  - job_name: 'network-devices'
    static_configs:
      - targets: ['192.168.1.10:9100', '192.168.1.11:9100']
    scrape_interval: 30s
```

#### Directory Structure
```bash
# Create the directory structure
mkdir -p containerlab-setup/{labs,configs,images}
cd containerlab-setup

# Copy the docker-compose.yml and prometheus.yml files
# Then start the services
docker-compose up -d

# Access ContainerLab
docker exec -it containerlab containerlab version

# Deploy a lab
docker exec -it containerlab containerlab deploy -t /labs/lab.yml
```

#### Using ContainerLab with Docker Compose
```bash
# Deploy a lab
docker exec -it containerlab containerlab deploy -t /labs/my-lab.yml

# List running labs
docker exec -it containerlab containerlab list

# Access a device
docker exec -it containerlab containerlab exec -t /labs/my-lab.yml --label clab-node-name=ceos1

# Destroy a lab
docker exec -it containerlab containerlab destroy -t /labs/my-lab.yml
```

### Step 5: Ansible Role Deployment (Coming Soon)

**Note**: An Ansible role for automated ContainerLab deployment will be created and made available. This role will include:

- Automated Docker installation
- ContainerLab installation and configuration
- Pre-configured lab topologies
- Integration with existing automation workflows
- Support for multiple deployment scenarios

The Ansible role will be published to the [bsmeding.containerlab](https://github.com/bsmeding/ansible-role-containerlab) repository and will be available through Ansible Galaxy.

## Getting Started with Free Vendor Images

### Available Free Images

#### 1. **Arista cEOS (Cloud Edition)**
- **License**: Free for lab use
- **Download**: Available from Arista website
- **Features**: Full EOS functionality, REST API, eAPI

#### 2. **Nokia SR Linux**
- **License**: Free for lab use
- **Download**: Available from Nokia website
- **Features**: Full SR Linux functionality, gNMI, gRPC

#### 3. **Cisco XE (Subscription Required)**
- **License**: Requires Cisco subscription
- **Download**: Available through Cisco DevNet
- **Features**: Full IOS XE functionality, RESTCONF, NETCONF

#### 4. **Juniper vMX (Subscription Required)**
- **License**: Requires Juniper subscription
- **Download**: Available through Juniper website
- **Features**: Full Junos functionality, NETCONF, REST API

### Downloading Free Images

#### Arista cEOS
```bash
# Create directory for images
mkdir -p ~/containerlab-images
cd ~/containerlab-images

# Download Arista cEOS (you'll need to register on Arista website)
# Visit: https://www.arista.com/en/support/software-download
# Download: cEOS-lab-4.28.0F.tar.xz

# Extract the image
tar -xJf cEOS-lab-4.28.0F.tar.xz

# Import into Docker
docker import cEOS-lab-4.28.0F.tar.xz ceos:4.28.0F
```

#### Nokia SR Linux
```bash
# Download Nokia SR Linux (you'll need to register on Nokia website)
# Visit: https://www.nokia.com/networks/solutions/sr-linux/
# Download: srlinux-22.11.1.tar.xz

# Extract the image
tar -xJf srlinux-22.11.1.tar.xz

# Import into Docker
docker import srlinux-22.11.1.tar.xz srlinux:22.11.1
```

### Creating Your First Lab

#### Basic Topology File
Create a file named `lab.yml`:

```yaml
name: my-first-lab
topology:
  nodes:
    # Arista cEOS switch
    ceos1:
      kind: ceos
      image: ceos:4.28.0F
      mgmt_ipv4: 192.168.1.10
    
    ceos2:
      kind: ceos
      image: ceos:4.28.0F
      mgmt_ipv4: 192.168.1.11
    
    # Nokia SR Linux router
    srl1:
      kind: srl
      image: srlinux:22.11.1
      mgmt_ipv4: 192.168.1.20
    
    # Linux host for testing
    host1:
      kind: linux
      image: alpine:latest
      mgmt_ipv4: 192.168.1.100

  links:
    - endpoints: ["ceos1:eth1", "srl1:eth1"]
    - endpoints: ["ceos2:eth1", "srl1:eth2"]
    - endpoints: ["host1:eth1", "ceos1:eth2"]
```

#### Deploy the Lab
```bash
# Deploy the lab
containerlab deploy -t lab.yml

# Check lab status
containerlab inspect -t lab.yml

# List running containers
containerlab list
```

#### Access Devices
```bash
# Access Arista cEOS
containerlab exec -t lab.yml --label clab-node-name=ceos1

# Access Nokia SR Linux
containerlab exec -t lab.yml --label clab-node-name=srl1

# Access Linux host
containerlab exec -t lab.yml --label clab-node-name=host1
```

## Advanced Lab Examples

### Multi-Vendor Lab with Automation

#### Complex Topology
```yaml
name: automation-lab
topology:
  nodes:
    # Core switches
    core1:
      kind: ceos
      image: ceos:4.28.0F
      mgmt_ipv4: 192.168.1.10
      startup-config: configs/core1.cfg
    
    core2:
      kind: ceos
      image: ceos:4.28.0F
      mgmt_ipv4: 192.168.1.11
      startup-config: configs/core2.cfg
    
    # Distribution switches
    dist1:
      kind: ceos
      image: ceos:4.28.0F
      mgmt_ipv4: 192.168.1.20
      startup-config: configs/dist1.cfg
    
    dist2:
      kind: ceos
      image: ceos:4.28.0F
      mgmt_ipv4: 192.168.1.21
      startup-config: configs/dist2.cfg
    
    # Edge router
    edge1:
      kind: srl
      image: srlinux:22.11.1
      mgmt_ipv4: 192.168.1.30
      startup-config: configs/edge1.cfg
    
    # Management server
    mgmt:
      kind: linux
      image: ubuntu:20.04
      mgmt_ipv4: 192.168.1.100
      exec:
        - cmd: "apt update && apt install -y ansible python3-pip"
        - cmd: "pip3 install napalm netmiko"
    
    # Test hosts
    host1:
      kind: linux
      image: alpine:latest
      mgmt_ipv4: 192.168.1.101
    
    host2:
      kind: linux
      image: alpine:latest
      mgmt_ipv4: 192.168.1.102

  links:
    # Core to distribution
    - endpoints: ["core1:eth1", "dist1:eth1"]
    - endpoints: ["core1:eth2", "dist2:eth1"]
    - endpoints: ["core2:eth1", "dist1:eth2"]
    - endpoints: ["core2:eth2", "dist2:eth2"]
    
    # Distribution to edge
    - endpoints: ["dist1:eth3", "edge1:eth1"]
    - endpoints: ["dist2:eth3", "edge1:eth2"]
    
    # Hosts to distribution
    - endpoints: ["host1:eth1", "dist1:eth4"]
    - endpoints: ["host2:eth1", "dist2:eth4"]
    
    # Management to core
    - endpoints: ["mgmt:eth1", "core1:eth3"]
```

#### Configuration Files
Create configuration files in a `configs/` directory:

```bash
# Create configs directory
mkdir -p configs

# Core1 configuration
cat > configs/core1.cfg << 'EOF'
!
hostname core1
!
interface Ethernet1
   description Link to dist1
   no switchport
   ip address 10.1.1.1/30
!
interface Ethernet2
   description Link to dist2
   no switchport
   ip address 10.1.2.1/30
!
interface Ethernet3
   description Management
   no switchport
   ip address 192.168.1.10/24
!
router ospf 1
   network 10.1.1.0/30 area 0
   network 10.1.2.0/30 area 0
!
EOF

# Dist1 configuration
cat > configs/dist1.cfg << 'EOF'
!
hostname dist1
!
interface Ethernet1
   description Link to core1
   no switchport
   ip address 10.1.1.2/30
!
interface Ethernet2
   description Link to core2
   no switchport
   ip address 10.1.3.1/30
!
interface Ethernet3
   description Link to edge1
   no switchport
   ip address 10.2.1.1/30
!
interface Ethernet4
   description Link to host1
   switchport mode access
   switchport access vlan 10
!
vlan 10
   name DATA
!
router ospf 1
   network 10.1.1.0/30 area 0
   network 10.1.3.0/30 area 0
   network 10.2.1.0/30 area 0
!
EOF
```

### Ansible Integration

#### Inventory File
Create `inventory.yml`:

```yaml
all:
  children:
    network_devices:
      children:
        arista:
          hosts:
            core1:
              ansible_host: 192.168.1.10
              ansible_network_os: eos
              ansible_connection: network_cli
              ansible_user: admin
              ansible_password: admin
            core2:
              ansible_host: 192.168.1.11
              ansible_network_os: eos
              ansible_connection: network_cli
              ansible_user: admin
              ansible_password: admin
            dist1:
              ansible_host: 192.168.1.20
              ansible_network_os: eos
              ansible_connection: network_cli
              ansible_user: admin
              ansible_password: admin
            dist2:
              ansible_host: 192.168.1.21
              ansible_network_os: eos
              ansible_connection: network_cli
              ansible_user: admin
              ansible_password: admin
        nokia:
          hosts:
            edge1:
              ansible_host: 192.168.1.30
              ansible_network_os: srl
              ansible_connection: network_cli
              ansible_user: admin
              ansible_password: admin
    linux_hosts:
      hosts:
        mgmt:
          ansible_host: 192.168.1.100
          ansible_user: root
        host1:
          ansible_host: 192.168.1.101
          ansible_user: root
        host2:
          ansible_host: 192.168.1.102
          ansible_user: root
```

#### Ansible Playbook
Create `playbook.yml`:

```yaml
---
- name: Configure Network Devices
  hosts: network_devices
  gather_facts: no
  
  tasks:
    - name: Gather device facts
      network_facts:
      
    - name: Display device facts
      debug:
        var: ansible_net_version
        
    - name: Configure hostname
      network_config:
        lines:
          - hostname "{{ inventory_hostname }}"
          
    - name: Configure interfaces
      network_config:
        lines:
          - description "Configured by Ansible"
        parents: "{{ item }}"
      loop:
        - "interface Ethernet1"
        - "interface Ethernet2"
        - "interface Ethernet3"
        
    - name: Save running config
      network_config:
        save_when: modified
```

## Working with Different Vendor Images

### Cisco Images (Subscription Required)

#### Cisco XE
```bash
# Download Cisco XE (requires Cisco DevNet account)
# Visit: https://developer.cisco.com/site/ios-xe/
# Download: ios-xe-17.03.01a.tar.xz

# Extract and import
tar -xJf ios-xe-17.03.01a.tar.xz
docker import ios-xe-17.03.01a.tar.xz cisco_xe:17.03.01a
```

#### Cisco Topology Example
```yaml
name: cisco-lab
topology:
  nodes:
    cisco1:
      kind: cisco_xe
      image: cisco_xe:17.03.01a
      mgmt_ipv4: 192.168.1.10
      startup-config: configs/cisco1.cfg
    
    cisco2:
      kind: cisco_xe
      image: cisco_xe:17.03.01a
      mgmt_ipv4: 192.168.1.11
      startup-config: configs/cisco2.cfg

  links:
    - endpoints: ["cisco1:eth1", "cisco2:eth1"]
```

### Juniper Images (Subscription Required)

#### Juniper vMX
```bash
# Download Juniper vMX (requires Juniper account)
# Visit: https://www.juniper.net/us/en/dm/downloads/
# Download: vmx-20.4R1.12.tgz

# Extract and import
tar -xzf vmx-20.4R1.12.tgz
docker import vmx-20.4R1.12.tar.xz juniper_vmx:20.4R1.12
```

## Lab Management Commands

### Basic Commands
```bash
# Deploy a lab
containerlab deploy -t lab.yml

# Destroy a lab
containerlab destroy -t lab.yml

# List running labs
containerlab list

# Inspect lab topology
containerlab inspect -t lab.yml

# Execute commands on nodes
containerlab exec -t lab.yml --label clab-node-name=node1 -- cmd

# Get lab topology graph
containerlab graph -t lab.yml

# Save lab state
containerlab save -t lab.yml

# Load lab state
containerlab load -t lab.yml
```

### Advanced Commands
```bash
# Deploy with specific nodes
containerlab deploy -t lab.yml --nodes node1,node2

# Deploy with custom topology
containerlab deploy --topo custom-topo.yml

# Get detailed node information
containerlab inspect -t lab.yml --all

# Execute interactive shell
containerlab exec -t lab.yml --label clab-node-name=node1

# Get lab logs
containerlab logs -t lab.yml

# Export lab configuration
containerlab export -t lab.yml --format yaml
```

## Integration with Automation Tools

### Nornir Integration
```python
# nornir_inventory.py
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get

# Initialize Nornir
nr = InitNornir(
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yml",
            "group_file": "inventory/groups.yml",
            "defaults_file": "inventory/defaults.yml",
        }
    }
)

# Get facts from all devices
result = nr.run(task=napalm_get, getters=["facts", "interfaces"])

# Print results
for host, task_result in result.items():
    print(f"{host}: {task_result[0].result}")
```

### Terraform Integration
```hcl
# main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Deploy ContainerLab using external data source
data "external" "containerlab" {
  program = ["containerlab", "deploy", "-t", "lab.yml", "--format", "json"]
}

# Use lab information in Terraform
resource "null_resource" "configure_network" {
  depends_on = [data.external.containerlab]
  
  provisioner "local-exec" {
    command = "ansible-playbook -i inventory.yml playbook.yml"
  }
}
```

### Ansible Role Integration (Coming Soon)

A dedicated Ansible role for ContainerLab deployment will be available, providing:

#### Role Features
- **Automated Installation**: Complete ContainerLab setup with Docker
- **Lab Management**: Deploy, destroy, and manage lab topologies
- **Image Management**: Automated vendor image downloads and imports
- **Configuration Templates**: Pre-built lab configurations
- **Integration**: Seamless integration with existing Ansible workflows

#### Example Playbook Usage
```yaml
---
- name: Deploy ContainerLab Environment
  hosts: lab_servers
  roles:
    - role: bsmeding.containerlab
      containerlab_version: "0.52.0"
      containerlab_images:
        - name: ceos
          version: "4.28.0F"
          source: "arista"
        - name: srlinux
          version: "22.11.1"
          source: "nokia"
      containerlab_labs:
        - name: "basic-lab"
          topology_file: "labs/basic-lab.yml"
          auto_deploy: true
      containerlab_monitoring:
        enable_grafana: true
        enable_prometheus: true
        grafana_port: 3001
        prometheus_port: 9090
```

#### Role Variables
```yaml
# containerlab.yml
containerlab_version: "0.52.0"
containerlab_install_method: "script"  # script, docker, or manual
containerlab_docker_compose: false
containerlab_web_ui: false
containerlab_monitoring:
  enable_grafana: false
  enable_prometheus: false
  grafana_port: 3001
  prometheus_port: 9090

# Lab configurations
containerlab_labs: []
containerlab_images: []

# Network settings
containerlab_network:
  mgmt_subnet: "192.168.1.0/24"
  data_subnet: "10.0.0.0/8"
```

The role will be available at: `bsmeding.containerlab`

## Troubleshooting

### Common Issues

#### Docker Permission Issues
```bash
# If you get permission errors
sudo usermod -aG docker $USER
newgrp docker
```

#### Image Import Issues
```bash
# Check available images
docker images

# Remove corrupted images
docker rmi image_name:tag

# Re-import images
docker import image.tar.xz image_name:tag
```

#### Network Connectivity Issues
```bash
# Check Docker networks
docker network ls

# Inspect network
docker network inspect containerlab

# Check container connectivity
containerlab exec -t lab.yml --label clab-node-name=node1 -- ping 8.8.8.8
```

#### Performance Issues
```bash
# Check system resources
docker stats

# Limit container resources
# Add to topology file:
nodes:
  node1:
    kind: ceos
    image: ceos:4.28.0F
    mgmt_ipv4: 192.168.1.10
    cpu_limit: 1
    memory_limit: 1G
```

## Best Practices

### 1. **Image Management**
- Keep images organized in a dedicated directory
- Use version tags for images
- Document image sources and licenses
- Regularly update images for security patches

### 2. **Topology Design**
- Use descriptive node names
- Document link purposes
- Use consistent IP addressing schemes
- Keep topologies modular and reusable

### 3. **Configuration Management**
- Store configurations in version control
- Use templates for common configurations
- Document configuration changes
- Test configurations before deployment

### 4. **Automation Integration**
- Use consistent naming conventions
- Implement proper error handling
- Document automation workflows
- Test automation scripts regularly

### 5. **Resource Management**
- Monitor system resources
- Clean up unused labs
- Use resource limits for containers
- Implement lab lifecycle management

## Resources

### Official Documentation
- [ContainerLab Documentation](https://containerlab.dev/)
- [ContainerLab GitHub](https://github.com/srl-labs/containerlab)
- [ContainerLab Lab Examples](https://containerlab.dev/lab-examples/lab-examples/)
- [ContainerLab Examples (GitHub)](https://github.com/srl-labs/containerlab/tree/master/lab-examples)

### Vendor Resources
- [Arista cEOS](https://www.arista.com/en/support/software-download)
- [Nokia SR Linux](https://www.nokia.com/networks/solutions/sr-linux/)
- [Cisco DevNet](https://developer.cisco.com/)
- [Juniper vMX](https://www.juniper.net/us/en/dm/downloads/)

### Community Resources
- [ContainerLab Community](https://github.com/srl-labs/containerlab/discussions)
- [Network Automation Examples](https://github.com/srl-labs/containerlab/tree/master/lab-examples)
- [Blog Posts and Tutorials](https://containerlab.dev/blog/)

For more on network automation tools, see the [NetDevOps Tools Index](/tools/).
