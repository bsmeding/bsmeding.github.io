---
title: "ContainerLab"
tags: ["containerlab", "network automation", "lab environment", "docker", "networking", "testing"]
date: 2024-06-11
summary: ContainerLab is a powerful tool for creating and managing container-based network labs. Learn how to set up a complete lab environment with free vendor images for network automation testing.
---

# ContainerLab

<img src="https://camo.githubusercontent.com/223ecd49b5a869d166bd6b86752960600ccb5fb10b8b5bc278e51ba06550690e/68747470733a2f2f6769746c61622e636f6d2f72646f64696e2f706963732f2d2f77696b69732f75706c6f6164732f30316663646332313265653163376465373065663564326138643130393034342f696d6167652e706e67" alt="ContainerLab Logo" class="tool-image">

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

For detailed Docker installation instructions, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Supported platforms:**
- Ubuntu 20.04+ / Debian
- CentOS 8+ / RHEL 8+
- Other Linux distributions with Docker support

### Step 2: Install ContainerLab

For detailed ContainerLab installation instructions, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Installation methods:**
- Official install script (recommended)
- Manual installation from GitHub releases
- Docker-based installation
- Package manager installation

### Step 3: Install Additional Tools (Optional)

For detailed instructions on installing additional tools, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Optional tools:**
- Docker Compose (for advanced deployments)
- Network utilities (bridge-utils, iproute2, net-tools, tcpdump)
- Monitoring tools (Grafana, Prometheus)
- Web UI components

### Step 4: Docker Compose Installation (Alternative Method)

For those who prefer using Docker Compose for ContainerLab deployment, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html) for complete setup instructions.

**Docker Compose features:**
- Complete ContainerLab environment in containers
- Optional Web UI for lab management
- Monitoring with Grafana and Prometheus
- Persistent storage and configuration management

### Step 5: Ansible Role Deployment (Coming Soon)

**Note**: An Ansible role for automated ContainerLab deployment will be created and made available. This role will include:

- Automated Docker installation
- ContainerLab installation and configuration
- Pre-configured lab topologies
- Integration with existing automation workflows
- Support for multiple deployment scenarios

The Ansible role will be published to the [bsmeding.containerlab](https://github.com/bsmeding/ansible-role-containerlab) repository and will be available through Ansible Galaxy.

## Getting Started with Free Vendor Images

For a step-by-step tutorial on setting up ContainerLab and downloading vendor images, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

### Available Free Images

#### 1. **Arista cEOS (Cloud Edition)**
- **License**: Free for lab use
- **Download**: Available from Arista website
- **Features**: Full EOS functionality, REST API, eAPI

#### 2. **Nokia SR Linux**
- **License**: Free for lab use
- **Download**: Available from GitHub Container Registry
- **Features**: Full SR Linux functionality, gNMI, gRPC

#### 3. **Cisco XE (Subscription Required)**
- **License**: Requires Cisco subscription
- **Download**: Available through Cisco DevNet
- **Features**: Full IOS XE functionality, RESTCONF, NETCONF

#### 4. **Juniper Images (Various Licenses)**
- **Available**: cRPD, vQFX, vSRX, vJunos-router, vJunos-switch, vJunosEvolved, cJunosEvolved
- **Download**: Available through Juniper support portal
- **Features**: Full Junos functionality, NETCONF, REST API

### Downloading Free Images

For detailed instructions on downloading and importing vendor images, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Available free images:**
- Arista cEOS (requires registration)
- Nokia SR Linux (available from GitHub Container Registry)
- Other vendor images with various licensing requirements

## Traffic Generation with Ostinato

For comprehensive network testing and validation, you can use **Ostinato** - a powerful traffic generator that integrates seamlessly with ContainerLab. Ostinato allows you to generate realistic network traffic to test your configurations, validate QoS policies, and measure network performance.

### What is Ostinato?

Ostinato is a commercial network packet generator and analyzer that supports:
- **Multiple protocols**: TCP, UDP, ICMP, ARP, BGP, OSPF, and more
- **Custom packet crafting**: Full control over packet headers and payloads
- **Traffic patterns**: Burst, continuous, and custom traffic patterns
- **Statistics**: Real-time packet statistics and analysis
- **Container support**: Runs natively in Docker containers
- **Multiple platforms**: Windows, macOS, Linux, Raspberry Pi, Docker containers

**Pricing Tiers:**
- **Starter**: $49+/user (single platform)
- **Pro Bundle**: $169+/user/yr (multiple platforms, email support)
- **Business Bundle**: $289+/user/yr (all platforms, priority support)

### Installing Ostinato in ContainerLab

#### Method 1: Using Official Ostinato Docker Image

For detailed Ostinato installation instructions, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Note**: Ostinato requires a valid license to use. Visit [https://ostinato.org/pricing/](https://ostinato.org/pricing/) for licensing options.

#### Method 2: Alternative Open-Source Traffic Generators

Since Ostinato is now commercial, consider these open-source alternatives:

**Available alternatives:**
- **Scapy** (Python-based packet manipulation)
- **Iperf3** (Bandwidth testing and measurement)
- **Pktgen** (High-performance packet generation)
- **Custom Python scripts** for specific traffic patterns

### Integrating Ostinato with ContainerLab

#### Basic Traffic Generation Topology

For detailed traffic generation topology examples, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Traffic generator options:**
- **Ostinato** (commercial, requires license)
- **Scapy** (open-source Python-based)
- **Iperf3** (bandwidth testing)
- **Custom scripts** for specific protocols

#### Advanced Traffic Generation Configuration

For advanced traffic generation scenarios and configurations, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Advanced features:**
- Multiple traffic generator types in single topology
- Custom traffic profiles and scripts
- Automated traffic testing workflows
- Integration with network automation tools

### Creating Traffic Profiles

For detailed traffic profile examples and configurations, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Traffic profile types:**
- **BGP traffic profiles** (Ostinato format)
- **Custom Python scripts** (Scapy-based)
- **Iperf3 configurations** (bandwidth testing)
- **Protocol-specific templates** (HTTP, TCP, UDP, etc.)

### Using Traffic Generator Interfaces

#### Accessing Traffic Generator Interfaces

For detailed instructions on using traffic generator interfaces, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Available interfaces:**
- **Ostinato GUI** (commercial, requires license)
- **Scapy interactive mode** (open-source)
- **Iperf3 command-line interface** (open-source)
- **Custom web interfaces** (for advanced setups)

### Command-Line Traffic Generation

For detailed command-line traffic generation examples, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Command-line tools:**
- **ostinato-drone** (commercial, requires license)
- **Scapy Python scripts** (open-source)
- **Iperf3 commands** (open-source)
- **Custom automation scripts** (bash, Python, etc.)

### Monitoring and Analysis

For detailed monitoring and analysis examples, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Monitoring capabilities:**
- **Real-time statistics** from traffic generators
- **Packet capture and analysis** with tcpdump
- **Network performance metrics** collection
- **Traffic pattern analysis** and reporting

### Integration with Network Automation

For detailed network automation integration examples, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Automation integration:**
- **Ansible playbooks** for traffic testing
- **Python scripts** for automated testing
- **CI/CD pipeline integration** for continuous testing
- **Custom automation workflows** for specific use cases

### Best Practices

#### 1. **Traffic Planning**
- Define clear test objectives
- Use realistic traffic patterns
- Consider network capacity limits
- Plan for different traffic types

#### 2. **Resource Management**
- Monitor system resources during traffic generation
- Use appropriate packet rates
- Clean up completed test sessions
- Limit concurrent traffic streams

#### 3. **Configuration Management**
- Store traffic profiles in version control
- Document traffic patterns and purposes
- Use consistent naming conventions
- Create reusable traffic templates

#### 4. **Monitoring and Validation**
- Monitor network device statistics
- Validate QoS policies
- Check for packet loss and latency
- Analyze traffic patterns

### Troubleshooting

For detailed troubleshooting guides and solutions, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Common troubleshooting areas:**
- **Service status verification** and diagnostics
- **Network connectivity issues** resolution
- **Performance optimization** techniques
- **Resource management** and system limits

For more information about Ostinato, visit [https://ostinato.org/](https://ostinato.org/).


### Creating Your First Lab

For a complete example of building a reusable network automation lab with ContainerLab, see [Building a Reusable Network Automation Lab with ContainerLab](/blog/posts/2025/2025-08-10-building-reusable-network-automation-lab-with-containerlab.html).

For detailed step-by-step instructions on creating your first lab, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Basic lab components:**
- **Network devices** (Arista cEOS, Nokia SR Linux, etc.)
- **Linux hosts** for testing and automation
- **Network links** connecting devices
- **Management network** for device access

## Advanced Lab Examples

For detailed advanced lab examples and configurations, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Advanced lab types:**
- **Multi-vendor labs** with different network operating systems
- **Automation-ready labs** with management servers
- **Complex topologies** with core/distribution/access layers
- **Custom configurations** and startup scripts

### Ansible Integration

For detailed Ansible integration examples and playbooks, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Ansible integration features:**
- **Inventory management** for network devices and hosts
- **Network automation playbooks** for device configuration
- **Multi-vendor support** with different network operating systems
- **Configuration management** and validation workflows

## Working with Different Vendor Images

For detailed instructions on working with different vendor images, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Supported vendor images:**
- **Cisco images** (subscription required)
- **Juniper images** (various licensing requirements)
- **Arista images** (free for lab use)
- **Nokia images** (free for lab use)
- **Other vendor images** with specific licensing terms

## Lab Management Commands

For detailed lab management commands and examples, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Basic commands:**
- `containerlab deploy` - Deploy lab topologies
- `containerlab destroy` - Remove lab deployments
- `containerlab list` - List running labs
- `containerlab inspect` - Inspect lab details
- `containerlab exec` - Execute commands on nodes

**Advanced commands:**
- `containerlab graph` - Generate topology graphs
- `containerlab save/load` - Save and restore lab states
- `containerlab logs` - View lab logs
- `containerlab export` - Export lab configurations

## Integration with Automation Tools

For detailed automation tool integration examples, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Supported automation tools:**
- **Nornir** - Python-based network automation framework
- **Terraform** - Infrastructure as Code integration
- **Ansible** - Configuration management and automation
- **Custom Python scripts** - Direct API integration

### Ansible Role Integration (Coming Soon)

A dedicated Ansible role for ContainerLab deployment will be available, providing:

**Role features:**
- **Automated installation** of ContainerLab and dependencies
- **Lab management** with deployment and destruction workflows
- **Image management** for vendor network operating systems
- **Configuration templates** for common lab topologies
- **Monitoring integration** with Grafana and Prometheus

The role will be available at: `bsmeding.containerlab`

## Troubleshooting

For detailed troubleshooting guides and solutions, see the [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html).

**Common troubleshooting areas:**
- **Docker permission issues** and user group configuration
- **Image import problems** and corruption resolution
- **Network connectivity issues** between containers
- **Performance optimization** and resource management

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

### Tutorials and Guides
- [ContainerLab Getting Started Guide](/tutorials/containerlab_getting_started.html) - Step-by-step tutorial
- [Building a Reusable Network Automation Lab](/blog/posts/2025/2025-08-10-building-reusable-network-automation-lab-with-containerlab.html) - Complete lab example

### Vendor Resources
- [Arista cEOS](https://www.arista.com/en/support/software-download)
- [Nokia SR Linux](https://www.nokia.com/networks/solutions/sr-linux/)
- [Cisco DevNet](https://developer.cisco.com/)
- [Juniper Container Images](https://www.juniper.net/documentation/us/en/software/junos/junos-vm/junos-vm-docker/)

### Community Resources
- [ContainerLab Community](https://github.com/srl-labs/containerlab/discussions)
- [Network Automation Examples](https://github.com/srl-labs/containerlab/tree/master/lab-examples)
- [Blog Posts and Tutorials](https://containerlab.dev/blog/)

For more on network automation tools, see the [NetDevOps Tools Index](/tools/).
