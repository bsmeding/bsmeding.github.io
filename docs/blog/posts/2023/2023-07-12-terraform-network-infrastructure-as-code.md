---
title: "Terraform for Network Infrastructure as Code: A Complete Guide"
authors: [bsmeding]
date: 2023-07-12
summary: Learn how to use Terraform to manage network infrastructure as code, from basic concepts to advanced networking scenarios.
tags:
  - terraform
  - infrastructure as code
  - netdevops
  - automation
  - networking
  - cloud
---

# Terraform for Network Infrastructure as Code: A Complete Guide

**Terraform** has revolutionized how organizations manage network infrastructure by treating it as code. This comprehensive guide explores how to use Terraform for network automation, from basic concepts to advanced networking scenarios.

<!-- more -->

## What is Infrastructure as Code (IaC)?

Infrastructure as Code is the practice of managing and provisioning computing infrastructure through machine-readable definition files rather than physical hardware configuration or interactive configuration tools. Terraform is one of the most popular IaC tools, offering:

- **Declarative Configuration**: Define desired state rather than procedural steps
- **Version Control**: Track infrastructure changes in Git
- **Automation**: Eliminate manual configuration processes
- **Consistency**: Ensure identical environments across deployments
- **Scalability**: Manage complex infrastructure efficiently

## Getting Started with Terraform

### Installation

```bash
# Download and install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update && sudo apt install terraform

# Verify installation
terraform version
```

### Basic Project Structure

```bash
network-terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── providers.tf
└── modules/
    ├── vpc/
    ├── subnets/
    └── security/
```

## Core Concepts

### Providers

Providers are plugins that Terraform uses to interact with cloud providers, SaaS providers, and other APIs.

```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
}
```

### Variables

Define input variables for your configuration:

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Resources

Resources are the infrastructure objects that Terraform manages:

```hcl
# main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name        = "${var.environment}-public-${count.index + 1}"
    Environment = var.environment
  }
}
```

## Network Infrastructure Examples

### VPC and Subnet Configuration

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.name}-public-${count.index + 1}"
  })
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${var.name}-private-${count.index + 1}"
  })
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = merge(var.tags, {
    Name = "${var.name}-igw"
  })
}

resource "aws_nat_gateway" "this" {
  count         = length(var.public_subnets)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(var.tags, {
    Name = "${var.name}-nat-${count.index + 1}"
  })
}

resource "aws_eip" "nat" {
  count = length(var.public_subnets)
  vpc   = true

  tags = merge(var.tags, {
    Name = "${var.name}-eip-${count.index + 1}"
  })
}
```

### Security Groups and Network ACLs

```hcl
# modules/security/main.tf
resource "aws_security_group" "web" {
  name_prefix = "${var.name}-web-"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-web-sg"
  })
}

resource "aws_security_group" "database" {
  name_prefix = "${var.name}-db-"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-db-sg"
  })
}
```

### Load Balancer Configuration

```hcl
# modules/alb/main.tf
resource "aws_lb" "this" {
  name               = "${var.name}-alb"
  internal           = var.internal
  load_balancer_type = "application"
  security_groups    = var.security_groups
  subnets            = var.subnets

  enable_deletion_protection = var.enable_deletion_protection

  tags = merge(var.tags, {
    Name = "${var.name}-alb"
  })
}

resource "aws_lb_target_group" "this" {
  count    = length(var.target_groups)
  name     = "${var.name}-tg-${count.index}"
  port     = var.target_groups[count.index].port
  protocol = var.target_groups[count.index].protocol
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = var.target_groups[count.index].health_check_path
    port                = "traffic-port"
    protocol            = var.target_groups[count.index].protocol
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = merge(var.tags, {
    Name = "${var.name}-tg-${count.index}"
  })
}

resource "aws_lb_listener" "this" {
  count             = length(var.listeners)
  load_balancer_arn = aws_lb.this.arn
  port              = var.listeners[count.index].port
  protocol          = var.listeners[count.index].protocol

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this[var.listeners[count.index].target_group_index].arn
  }
}
```

## Advanced Networking Scenarios

### Multi-Region Deployment

```hcl
# multi-region/main.tf
module "vpc_us_west" {
  source = "../modules/vpc"

  providers = {
    aws = aws.us-west-2
  }

  name = "us-west-2"
  vpc_cidr = "10.1.0.0/16"
  public_subnets = ["10.1.1.0/24", "10.1.2.0/24"]
  private_subnets = ["10.1.10.0/24", "10.1.11.0/24"]
  availability_zones = ["us-west-2a", "us-west-2b"]
}

module "vpc_us_east" {
  source = "../modules/vpc"

  providers = {
    aws = aws.us-east-1
  }

  name = "us-east-1"
  vpc_cidr = "10.2.0.0/16"
  public_subnets = ["10.2.1.0/24", "10.2.2.0/24"]
  private_subnets = ["10.2.10.0/24", "10.2.11.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b"]
}

# VPC Peering
resource "aws_vpc_peering_connection" "us_west_to_us_east" {
  provider = aws.us-west-2
  vpc_id   = module.vpc_us_west.vpc_id
  peer_vpc_id = module.vpc_us_east.vpc_id
  peer_region = "us-east-1"

  tags = {
    Name = "us-west-2-to-us-east-1"
  }
}
```

### Transit Gateway Configuration

```hcl
# modules/transit-gateway/main.tf
resource "aws_ec2_transit_gateway" "this" {
  description = "${var.name} Transit Gateway"

  default_route_table_association = "enable"
  default_route_table_propagation = "enable"

  tags = merge(var.tags, {
    Name = "${var.name}-tgw"
  })
}

resource "aws_ec2_transit_gateway_vpc_attachment" "this" {
  count = length(var.vpc_attachments)

  subnet_ids         = var.vpc_attachments[count.index].subnet_ids
  transit_gateway_id = aws_ec2_transit_gateway.this.id
  vpc_id             = var.vpc_attachments[count.index].vpc_id

  tags = merge(var.tags, {
    Name = "${var.name}-tgw-attachment-${count.index}"
  })
}

resource "aws_ec2_transit_gateway_route_table" "this" {
  count = length(var.route_tables)

  transit_gateway_id = aws_ec2_transit_gateway.this.id

  tags = merge(var.tags, {
    Name = "${var.name}-tgw-rt-${count.index}"
  })
}
```

## Best Practices

### 1. Use Modules for Reusability

```hcl
# modules/network/main.tf
module "vpc" {
  source = "../vpc"

  name = var.name
  vpc_cidr = var.vpc_cidr
  public_subnets = var.public_subnets
  private_subnets = var.private_subnets
  availability_zones = var.availability_zones
}

module "security" {
  source = "../security"

  name = var.name
  vpc_id = module.vpc.vpc_id
  allowed_ssh_cidr = var.allowed_ssh_cidr
}
```

### 2. Implement State Management

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-west-2"
    
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### 3. Use Data Sources for Dynamic Configuration

```hcl
# data.tf
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "latest_amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

### 4. Implement Proper Tagging

```hcl
# locals.tf
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}
```

## CI/CD Integration

### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - apply

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform

validate:
  stage: validate
  script:
    - cd $TF_ROOT
    - terraform init
    - terraform validate
    - terraform fmt -check

plan:
  stage: plan
  script:
    - cd $TF_ROOT
    - terraform init
    - terraform plan -out=plan.tfplan
  artifacts:
    paths:
      - $TF_ROOT/plan.tfplan
    expire_in: 1 week

apply:
  stage: apply
  script:
    - cd $TF_ROOT
    - terraform init
    - terraform apply plan.tfplan
  when: manual
  only:
    - main
```

### GitHub Actions Workflow

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v1
      
    - name: Terraform Init
      run: terraform init
      
    - name: Terraform Validate
      run: terraform validate
      
    - name: Terraform Plan
      run: terraform plan
      if: github.event_name == 'pull_request'
```

## Monitoring and Validation

### Output Configuration

```hcl
# outputs.tf
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "load_balancer_dns" {
  description = "The DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}
```

### Validation Rules

```hcl
# validation.tf
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "subnet_cidrs" {
  description = "List of subnet CIDR blocks"
  type        = list(string)
  
  validation {
    condition = alltrue([
      for cidr in var.subnet_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "All subnet CIDR blocks must be valid."
  }
}
```

## Troubleshooting Common Issues

### 1. State Management Issues

```bash
# Refresh state
terraform refresh

# Import existing resources
terraform import aws_vpc.main vpc-12345678

# Move resources
terraform state mv aws_subnet.old aws_subnet.new
```

### 2. Dependency Issues

```hcl
# Use depends_on for explicit dependencies
resource "aws_instance" "web" {
  ami           = data.aws_ami.latest.id
  instance_type = "t3.micro"
  
  depends_on = [aws_security_group.web]
}
```

### 3. Variable Validation

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  
  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Instance type must be t3.micro, t3.small, or t3.medium."
  }
}
```

## Conclusion

Terraform provides a powerful and flexible platform for managing network infrastructure as code. By following the practices outlined in this guide, you can build robust, scalable, and maintainable network infrastructure.

Key takeaways:
- Use modules for reusability and maintainability
- Implement proper state management
- Follow naming conventions and tagging strategies
- Integrate with CI/CD pipelines
- Implement validation and testing
- Document your infrastructure code

## Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [Network Infrastructure Examples](https://github.com/hashicorp/terraform-aws-vpc)

---

*This guide provides a comprehensive overview of using Terraform for network infrastructure as code. For more advanced topics, check out our other articles on specific Terraform modules and best practices.* 