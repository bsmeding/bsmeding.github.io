# Ansible Role: Nautobot Docker (`bsmeding.nautobot_docker`)

This Ansible role deploys Nautobot (Network Source of Truth) in a Docker container. It is designed for easy, automated Nautobot deployments for labs, demos, or production.

- **GitHub:** [bsmeding/ansible_role_nautobot_docker](https://github.com/bsmeding/ansible_role_nautobot_docker)
- **Ansible Galaxy:** [bsmeding.nautobot_docker](https://galaxy.ansible.com/bsmeding/nautobot_docker)

---

## Features
- Deploys Nautobot and dependencies (Postgres, Redis) in Docker
- Supports plugins, LDAP, and custom configuration
- Easily set admin credentials and API token
- Mounts volumes for persistent data
- Integrates with other roles (e.g., Docker, Nginx, AWX)

---

## Requirements
- Linux system with Docker installed (use `bsmeding.docker` role)
- Python and Ansible installed

---

## Common Role Variables
Below are some of the most useful variables. For the full list and advanced options, see the [role README](https://github.com/bsmeding/ansible_role_nautobot_docker#role-variables).

```yaml
# Name of the container
nautobot__name: nautobot

# Docker image to use
nautobot__image: nautobot:2.3

# HTTP/HTTPS ports
nautobot__port_http: 8080
nautobot__port_https: 8444

# Admin credentials
nautobot__superuser_name: admin
nautobot__superuser_password: admin
nautobot__superuser_api_token: "1234567890abcdefghijklmnopqrstuvwxyz"

# Enable/disable internal Postgres/Redis
nautobot__install_own_postgres_db: true

# Volumes to mount
nautobot__directory_volumes:
  - "{{ nautobot__home }}/logs:/var/log/nautobot"
  - "{{ nautobot__home }}/media:/opt/nautobot/media"
  - "{{ nautobot__home }}/jobs:/opt/nautobot/jobs"
  - "{{ nautobot__home }}/static:/opt/nautobot/static"

# Plugins
nautobot__plugins: []
```

---

## Example Playbook
```yaml
- hosts: all
  become: true
  roles:
    - role: bsmeding.docker  # Ensure Docker is installed
    - role: bsmeding.nautobot_docker
      vars:
        nautobot__superuser_name: admin
        nautobot__superuser_password: admin
        nautobot__superuser_api_token: "myapitoken"
```

---

## Usage Tips
- Use with the `bsmeding.docker` role to ensure Docker is present.
- Set `nautobot__install_own_postgres_db: false` to use an external Postgres DB.
- For advanced options, see the [role README](https://github.com/bsmeding/ansible_role_nautobot_docker#role-variables).

---

## More Information
- [GitHub Repository](https://github.com/bsmeding/ansible_role_nautobot_docker)
- [Ansible Galaxy Documentation](https://galaxy.ansible.com/bsmeding/nautobot_docker)

---

*MIT License. Created and maintained by Bart Smeding.*
