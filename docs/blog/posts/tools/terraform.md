---
title: Terraform Introduction & Getting Started
authors: [bsmeding]
date: 2024-10-06
summary: A practical introduction to Terraform, its IaC capabilities, and how to provision resources.
tags:
  - terraform
  - infrastructure as code
  - automation
  - devops
---

# Terraform: Introduction & Getting Started

![Terraform Logo](https://web-unified-docs-hashicorp.vercel.app/api/assets/terraform/latest/img/docs/intro-terraform-workflow.png){: style="max-width: 300px; display: block; margin: 0 auto;"}

**Terraform** is an open-source infrastructure as code (IaC) tool by HashiCorp for provisioning and managing cloud and on-premises resources declaratively.
<!-- more -->

## Why Use Terraform?
- Manage infrastructure as code across multiple providers
- Declarative, version-controlled infrastructure
- Large ecosystem of providers and modules

## How Terraform Works
- Uses HCL (HashiCorp Configuration Language) for configuration files
- Providers enable support for different platforms (AWS, Azure, etc.)
- State files track resource status

## Quick Start Example
1. **Install Terraform:**
   ```bash
   curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
   sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
   sudo apt update && sudo apt install terraform
   terraform version
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
   terraform init
   terraform apply
   ```

## Learn More
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Getting Started Guide](https://developer.hashicorp.com/terraform/tutorials) 