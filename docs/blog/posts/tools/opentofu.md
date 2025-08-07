---
title: OpenTofu Introduction & Getting Started
authors: [bsmeding]
date: 2024-09-29
summary: A quick start guide to OpenTofu, an open-source IaC tool forked from Terraform.
tags:
  - opentofu
  - infrastructure as code
  - automation
  - devops
---

# OpenTofu: Introduction & Getting Started

![OpenTofu Logo](https://opentofu.org/images/logo.png?w=300&h=auto){: style="max-width: 300px; display: block; margin: 0 auto;"}

**OpenTofu** is an open-source infrastructure as code (IaC) tool, forked from Terraform, designed to provision and manage cloud and on-premises resources declaratively.
<!-- more -->

## Why Use OpenTofu?
- Open-source alternative to Terraform
- Manage infrastructure as code across multiple providers
- Declarative, version-controlled infrastructure

## How OpenTofu Works
- Uses HCL (HashiCorp Configuration Language) for configuration files
- Providers enable support for different platforms (AWS, Azure, etc.)
- State files track resource status

## Quick Start Example
1. **Install OpenTofu:**
   ```bash
   curl -sSfL https://get.opentofu.org/install.sh | sh
   tofu --version
   ```
2. **Write a simple configuration (`main.tf`):**
   ```hcl
   terraform {
     required_providers {
       random = {
         source = "hashicorp/random"
       }
     }
   }

   provider "random" {}

   resource "random_pet" "name" {}

   output "pet_name" {
     value = random_pet.name.id
   }
   ```
3. **Initialize and apply:**
   ```bash
   tofu init
   tofu apply
   ```

## Learn More
- [OpenTofu Documentation](https://opentofu.org/docs/)
- [Getting Started Guide](https://opentofu.org/docs/getting-started/) 