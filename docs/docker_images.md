# Docker images

I maintain a couple of Docker images, mostly to run Ansible CiCd pipelines and network/infra structure application with enhancements for my daily work


---

## Docker CiCd images

You can use this images to test Ansible playbooks, roles etc, the images are based on different Linux OS's with Ansible installed and some other packages mainly for `Network Automaiion` (`NetDevOps`). For all distro's there is a verionless images that contains the latest distro release, so `ansible_cicd_debian` is same as `ansbile_cicd_debian12`.

currently installed Python packages for network and CMDB testing:
* ansible
* cryptography
* yamllint
* pynautobot
* pynetbox
* jmespath
* netaddr
* pywinrm



| Container | CI Status   | downloads | more info | 
| --------- | ----------- | --------- | --------- |
| [ansible_cicd_debian11](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian11/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian11)
| [ansible_cicd_debian12](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian12/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml)  | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian12)
| [ansible_cicd_debian](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_debian/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml)  | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_debian)
| [ansible_cicd_rockylinux8](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_rockylinux8/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml)  | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_rockylinux8)
| [ansible_cicd_rockylinux9](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_rockylinux9/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_rockylinux9)
| [ansible_cicd_rockylinux](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_rockylinux/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_rockylinux)
| [ansible_cicd_ubuntu2004](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu2004/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu2004)
| [ansible_cicd_ubuntu2204](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu2204/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu2204)
| [ansible_cicd_ubuntu2404](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu2404/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu2404)
| [ansible_cicd_ubuntu](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_ubuntu/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_ubuntu)
| [ansible_cicd_alpine3.20](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_alpine3.20/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_alpine3.20)
| [ansible_cicd_alpine3.21](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_alpine3.21/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_alpine3.21)
| [ansible_cicd_alpine3](https://hub.docker.com/repository/docker/bsmeding/ansible_cicd_alpine3/general) | [![Build and Push Ansible Images](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml/badge.svg)](https://github.com/bsmeding/docker_containers_ansible_cicd/actions/workflows/docker.yml) | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/ansible_cicd_alpine3)



## Docker applications



| Container | description | CI Status | downloads | more info | 
| --------- | ----------- | --------- | --------- | --------- |
| [nautobot](https://hub.docker.com/repository/docker/bsmeding/nautobot/general) | Nautobot including plugins and apps | ![Build](https://github.com/bsmeding/docker_container_nautobot/actions/workflows/build.yml/badge.svg)  | ![Docker Pulls](https://img.shields.io/docker/pulls/bsmeding/nautobot) | LINK |


