# Ansible Role: Nginx Docker (`bsmeding.nginx_docker`)

This Ansible role deploys Nginx as a reverse proxy in a Docker container. It is designed for flexible, automated Nginx deployments and can be used as a standalone reverse proxy or as part of a larger automation stack.

- **GitHub:** [bsmeding/ansible_role_nginx_docker](https://github.com/bsmeding/ansible_role_nginx_docker)
- **Ansible Galaxy:** [bsmeding.nginx_docker](https://galaxy.ansible.com/bsmeding/nginx_docker)

---

## Features
- Deploys Nginx in a Docker container
- Supports custom Nginx configuration via templates
- Easily expose ports and mount volumes
- Works with Let's Encrypt, SSL, and custom certificates
- Integrates with other roles (e.g., Docker, SWAG, GitLab)

---

## Requirements
- Linux system with Docker installed (use `bsmeding.docker` role)
- Python and Ansible installed

---

## Common Role Variables
Below are some of the most useful variables. For the full list and advanced options, see the [role README](https://github.com/bsmeding/ansible_role_nginx_docker#role-variables).

```yaml
# Name of the container
nginx__name: nginx

# Docker image to use
nginx__image: linuxserver/nginx:latest

# Ports to expose
nginx__ports:
  - "80:80"
  - "443:443"

# Volumes to mount
nginx__directory_volumes:
  - "/etc/nginx/conf.d:/etc/nginx/conf.d"
  - "/etc/letsencrypt:/etc/letsencrypt"

# Custom environment variables
nginx__env: {}

# Custom Nginx config template
nginx__config_template: "nginx.conf.j2"
```

---

## Example Playbook
```yaml
- hosts: all
  become: true
  roles:
    - role: bsmeding.docker  # Ensure Docker is installed
    - role: bsmeding.nginx_docker
      vars:
        nginx__ports:
          - "80:80"
          - "443:443"
        nginx__directory_volumes:
          - "/etc/nginx/conf.d:/etc/nginx/conf.d"
          - "/etc/letsencrypt:/etc/letsencrypt"
```

---

## Usage Tips
- Use with the `bsmeding.docker` role to ensure Docker is present.
- Customize Nginx configuration by providing your own template or mounting config files.
- Expose only the ports you need for your environment.
- For advanced options, see the [role README](https://github.com/bsmeding/ansible_role_nginx_docker#role-variables).

---

## More Information
- [GitHub Repository](https://github.com/bsmeding/ansible_role_nginx_docker)
- [Ansible Galaxy Documentation](https://galaxy.ansible.com/bsmeding/nginx_docker)

---

*MIT License. Created and maintained by Bart Smeding.*
