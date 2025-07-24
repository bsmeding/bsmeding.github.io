# Ansible Role: Docker (`bsmeding.docker`)

This Ansible role installs Docker on Linux systems and is designed to work seamlessly with other Docker container roles. It is based on [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker) with enhancements for better integration and automation.

- **GitHub:** [bsmeding/ansible_role_docker](https://github.com/bsmeding/ansible_role_docker)
- **Ansible Galaxy:** [bsmeding.docker](https://galaxy.ansible.com/bsmeding/docker)

---

## Features
- Installs Docker CE (Community Edition) or EE (Enterprise Edition)
- Optionally installs Docker Compose (plugin or standalone)
- Adds users to the `docker` group
- Sets `docker_uid` and `docker_gid` for use in other roles
- Removes Podman on RedHat-based systems
- Supports Ubuntu, Debian, Rocky Linux, Pop!_OS, and Linux Mint
- Configurable proxy, repository, and daemon options

---

## Requirements
- Linux system (Ubuntu, Debian, Rocky Linux, etc.)
- Python and Ansible installed

---

## Role Variables (Common)
Below are some of the most useful variables. See the [role README](https://github.com/bsmeding/ansible_role_docker#role-variables) for the full list.

```yaml
# Docker edition ('ce' for Community Edition, 'ee' for Enterprise Edition)
docker_edition: 'ce'

# List of users to add to the docker group
docker_users: []

# Install Docker Compose plugin?
docker_install_compose_plugin: true

# Install Docker Compose standalone binary?
docker_install_compose: false

# Proxy settings (if needed)
http_proxy: ''
https_proxy: ''
no_proxy: ''

# Manage Docker service
docker_service_manage: true
docker_service_state: started
docker_service_enabled: true
```

---

## Example Playbook
```yaml
- hosts: all
  become: true
  roles:
    - role: bsmeding.docker
      vars:
        docker_users:
          - youruser
        docker_install_compose_plugin: true
```

---

## Usage Tips
- To use with other roles, simply include `bsmeding.docker` before your container roles.
- The role sets `docker_uid` and `docker_gid` facts for use in downstream roles.
- For advanced configuration, override variables in your playbook or inventory.

---

## More Information
- [GitHub Repository](https://github.com/bsmeding/ansible_role_docker)
- [Ansible Galaxy Documentation](https://galaxy.ansible.com/ui/standalone/roles/bsmeding/docker/documentation/)
- [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker) (upstream)

---

*MIT License. Originally created by Jeff Geerling, extended by Bart Smeding.*


