# Ansible Role: AWX Docker (`bsmeding.awx_docker`)

This Ansible role deploys AWX (the open-source version of Ansible Tower) in Docker containers. It is designed for easy, automated AWX deployments for labs, demos, or production.

- **GitHub:** [bsmeding/ansible_role_awx_docker](https://github.com/bsmeding/ansible_role_awx_docker)
- **Ansible Galaxy:** [bsmeding.awx_docker](https://galaxy.ansible.com/bsmeding/awx_docker)

---

## Features
- Deploys AWX, Postgres, and Redis in Docker
- Easily set admin credentials and ports
- Mounts volumes for persistent data
- Supports custom organizations, teams, and LDAP
- Integrates with other roles (e.g., Docker, Nginx, Nautobot)

---

## Requirements
- Linux system with Docker installed (use `bsmeding.docker` role)
- Python and Ansible installed

---

## Common Role Variables
Below are some of the most useful variables. For the full list and advanced options, see the [role README](https://github.com/bsmeding/ansible_role_awx_docker#role-variables).

```yaml
# Admin credentials
awx__admin_user: admin
awx__admin_password: password

# Web ports
awx__port_web_http: 9080
awx__port_web_https: 9443

# Postgres credentials
awx__postgres_username: awxpguser
awx__postgres_password: awxpgpass
awx__postgres_db: awx

# Host root directory
awx__host_root: /opt/awx

# Volumes to mount
awx__project_data_dir: "{{ awx__host_root }}/projects"
awx__docker_compose_dir: "{{ awx__host_root }}/docker_compose"

# AWX version
awx__version: 17.1.0
```

---

## Example Playbook
```yaml
- hosts: all
  become: true
  roles:
    - role: bsmeding.docker  # Ensure Docker is installed
    - role: bsmeding.awx_docker
      vars:
        awx__admin_user: admin
        awx__admin_password: password
```

---

## Usage Tips
- Use with the `bsmeding.docker` role to ensure Docker is present.
- For advanced options, see the [role README](https://github.com/bsmeding/ansible_role_awx_docker#role-variables).

---

## More Information
- [GitHub Repository](https://github.com/bsmeding/ansible_role_awx_docker)
- [Ansible Galaxy Documentation](https://galaxy.ansible.com/bsmeding/awx_docker)

---

*MIT License. Created and maintained by Bart Smeding.*
