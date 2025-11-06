---
title: Docker Images
tags:
  - docker
  - ansible
  - cicd
  - automation
  - infrastructure
---

# Docker Images

I maintain several Docker images, mostly to run Ansible CI/CD pipelines and network/infrastructure applications with enhancements for my daily work.

---

## Docker CI/CD Images

These images are designed for testing Ansible playbooks, roles, and more. They are based on various Linux distributions with Ansible and other packages pre-installed, mainly for **Network Automation** (NetDevOps). For each distro, there is a versionless image that always contains the latest release (e.g., `ansible_cicd_debian` is the same as `ansible_cicd_debian12`).

**Currently installed Python packages for network and CMDB testing:**
- ansible (version varies by distribution)
- cryptography
- yamllint
- pynautobot
- pynetbox
- jmespath
- netaddr
- pywinrm
- **Network automation:** netmiko, ncclient, scrapli, napalm, paramiko, textfsm, ntc-templates, pyats
- **CI/CD testing:** ansible-lint, molecule, molecule-plugins, pytest, pytest-ansible
- **Cloud/API automation:** requests, boto3, openstacksdk, kubernetes
- **Utilities:** jinja2, passlib

| Container | CI Status   | Downloads |
| --------- | ----------- | --------- |
| [ansible_cicd_debian11](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian11/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian11) |
| [ansible_cicd_debian12](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian12/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian12) |
| [ansible_cicd_debian13](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian13/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian13) |
| [ansible_cicd_debian](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian) |
| [ansible_cicd_rockylinux8](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_rockylinux8/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_rockylinux8) |
| [ansible_cicd_rockylinux9](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_rockylinux9/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_rockylinux9) |
| [ansible_cicd_rockylinux](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_rockylinux/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_rockylinux) |
| [ansible_cicd_ubuntu2004](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu2004/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu2004) |
| [ansible_cicd_ubuntu2204](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu2204/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu2204) |
| [ansible_cicd_ubuntu2404](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu2404/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu2404) |
| [ansible_cicd_ubuntu](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu) |
| [ansible_cicd_alpine3.20](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_alpine3.20/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_alpine3.20) |
| [ansible_cicd_alpine3.21](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_alpine3.21/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_alpine3.21) |
| [ansible_cicd_alpine3](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_alpine3/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_alpine3) |

---

## Docker Applications

These images are for running specific applications with enhancements for network automation and infrastructure labs.

| Container | Description | CI Status | Downloads |
| --------- | ----------- | --------- | --------- |
| [nautobot](https://hub.docker.com/repository/docker/bsmeding/nautobot/general) | Nautobot including plugins and apps | ![Build](https://github.com/bsmeding/docker_container_nautobot/actions/workflows/build.yml/badge.svg) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/nautobot) |


