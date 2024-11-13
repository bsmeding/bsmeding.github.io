---
authors: [bsmeding]
toc: true
date: 2023-09-25
layout: single
comments: true
title: Network Automation Development Setup
tags: ["ansible", "nnetdevops","devnetops","student","course","git", "gitea", "nginx","awx","lldap", "docker"]
---

I create a (repo)[https://github.com/bsmeding/network_automation_dev_setup] to start with Network Automation, you can use this setup to check en build an environment with CMDB (Nautobot) Ansible AWX (version 17.1 as this is the latest docker version, old but working for automated tasks)=, LDAP server, Git server, Reverse proxy, Nautobot and Ansible AWX all built in Docker containers.

# network_automation_dev_setup
My host setup for network automation tests, docker, Nautobot, Ansible, AWX etc

* Install Docker
* Install LLDAP server
* Install Nautobot CMDB
* Install AWX
* Install Gitea
* Install Nginx

DO NOT USE IN PRODUCTION ENVIRONMENTS!!! ONLY FOR DEV/TEST

# Setup

Ensure that target machine is Up-to-date and restarted

* install dependencies: For Debian/Ubuntu `sudo apt install python3-pip git` / For CentOS/RHEL: `sudo yum install python3-pip git`

* Clone this repository: `git clone https://github.com/bsmeding/network_automation_dev_setup`
* `cd network_automation_dev_setup`


As NON-ROOT USER:
* install python dependencies: `pip3 install -r requirements.txt`

* install Ansible roles: `ansible-galaxy install -r ./roles/requirements.yml`
* install Ansible collections: `ansible-galaxy install -r ./collections/requirements.yml`
* change `inventory` file, set correct IP addresses
* change `group_vars/all` file and add login username
* Install Nautobot: `ansible-playbook install_nautobot.yml -i ./inventory -kK`


# Update
To update roles: `ansible-galaxy install -r ./roles/requirements.yml --force`
To update collections: `ansible-galaxy install -r ./collections/requirements.yml --force`
To update images / version from container, please check Variables (next section) either change value name or re-run to pull latest image

# Variables
Variables that can be used, either in the playbook or create host_vars or group_var files:
The roles are shipped with default value's, all defaults can be overwritten in the playbook or in a file in `group_vars` or `host_vars`

See role variables for: 
* (Docker)[https://github.com/bsmeding/ansible_role_docker/blob/main/defaults/main.yml]
  * and (geerlingguy.docker role)[https://github.com/geerlingguy/ansible-role-docker/blob/master/defaults/main.yml]
* (Nautobot)[https://github.com/bsmeding/ansible_role_nautobot_docker/blob/1.1.0/defaults/main.yml]
* (Ansible AWX)[https://github.com/bsmeding/ansible_role_awx_docker/blob/1.1.0/defaults/main.yml]
* (LDAP)[https://github.com/bsmeding/ansible_role_lldap_docker]
* (Nginx Reverse Proxy)[https://github.com/bsmeding/ansible_role_nginx_docker/blob/main/defaults/main.yml]


# Install Full
To install all tools on one server, use the `install_full.yml` playbook. Please note the variables in the playbook as well as the hostname users `srv1` this hostname must match the inventory file.

All the settings for this full install are placed in the role (./roles/full_install_config/defaults/main.yml)[roles/full_install_config/defaults/main.yml]

Full install will do:
* Install Docker
* Install LLDAP server
* Install Nautobot CMDB
* Install AWX
* Install Gitea
* Install Nginx
* Configure to use LLDAP as Authentication source for Nautobot, AWX. (Gitea must be set manualy)
* Configure Nginx to serve all the containers on port 80 and/or 443 based on URL

## URLS
Change URLS according you're setup and/or DNS settings. Or keep these settings and add to you're local Hosts file:
`<serverip>  git.lab.local cmdb.lab.local awx.lab.local ldap.lab.local`

## LDAP
Login: admin / devnetops
http://<serverip>:8080
http://ldap.lab.local (if not changed in playbook)

Default LDAP users:
* user01 / password01
* user02 / password02

## Nautobot
Login: admin / devnetops
  or: LDAP
http://<serverip>:8081
http://cmdb.lab.local (if not changed in playbook)

## Gitea
For Gitea, the first user created by the online registration form will be the admin user.
url: http://<serverip>:8082
http://git.lab.local (if not changed in playbook)
To add LDAP to Gitea, see example config in the (guide)[https://github.com/nitnelave/lldap/blob/main/example_configs/gitea.md]
  ldapserver is: `ldap` (the name of the LDAP container, as they are on the same docker network they can find each other)

## AWX
http://<serverip>:8083
http://awx.lab.local (if not changed in playbook)
Login: admin / devnetops
  or: LDAP 