# Ansible Role: GitLab CE Docker (`bsmeding.gitlab_ce_docker`)

This Ansible role deploys GitLab Community Edition in a Docker container. It is designed for easy, automated GitLab deployments for labs, demos, or production.

- **GitHub:** [bsmeding/ansible_role_gitlab_ce_docker](https://github.com/bsmeding/ansible_role_gitlab_ce_docker)
- **Ansible Galaxy:** [bsmeding.gitlab_ce_docker](https://galaxy.ansible.com/bsmeding/gitlab_ce_docker)

---

## Features
- Deploys GitLab CE in Docker
- Supports custom hostname, ports, and SSL
- LDAP integration and registry support
- Mounts volumes for persistent data
- Integrates with other roles (e.g., Docker, Nginx, SWAG)

---

## Requirements
- Linux system with Docker installed (use `bsmeding.docker` role)
- Python and Ansible installed

---

## Common Role Variables
Below are some of the most useful variables. For the full list and advanced options, see the [role README](https://github.com/bsmeding/ansible_role_gitlab_ce_docker#role-variables).

```yaml
# Name of the container
gitlab__name: gitlab

# Docker image to use
gitlab__image: 'gitlab/gitlab-ce:latest'

# Hostname and ports
gitlab__hostname: git.example.com
gitlab__port_web_http: 9081
gitlab__port_web_https: 9444
gitlab__port_ssh: 2222

# LDAP integration
gitlab__ldap_server_host_ip: ''
gitlab__ldap_auth_bind_dn: ''
gitlab__ldap_auth_bind_pass: ''

# Volumes to mount
gitlab__directory_volumes:
  - "{{ gitlab__home }}/config:/etc/gitlab"
  - "{{ gitlab__home }}/logs:/var/log/gitlab"
  - "{{ gitlab__home }}/data:/var/opt/gitlab"
```

---

## Example Playbook
```yaml
- hosts: all
  become: true
  roles:
    - role: bsmeding.docker  # Ensure Docker is installed
    - role: bsmeding.gitlab_ce_docker
      vars:
        gitlab__hostname: git.example.com
        gitlab__port_web_http: 9081
        gitlab__port_web_https: 9444
        gitlab__port_ssh: 2222
```

---

## Usage Tips
- Use with the `bsmeding.docker` role to ensure Docker is present.
- For advanced options, see the [role README](https://github.com/bsmeding/ansible_role_gitlab_ce_docker#role-variables).

---

## More Information
- [GitHub Repository](https://github.com/bsmeding/ansible_role_gitlab_ce_docker)
- [Ansible Galaxy Documentation](https://galaxy.ansible.com/bsmeding/gitlab_ce_docker)

---

*MIT License. Created and maintained by Bart Smeding.*
