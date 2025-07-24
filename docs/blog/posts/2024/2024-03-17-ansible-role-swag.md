---
authors: [bsmeding]
toc: true
draft: true
date: 2024-03-17
layout: single
comments: true
title: Ansible Role - SWAG
tags: ["ansible", "swag", "docker", "linuxserver"]
---

# Ansible Role: SWAG (Secure Web Application Gateway)

We've released a new Ansible Role to deploy the SWAG (Secure Web Application Gateway) reverse-proxy server created by [linuxserver.io](https://www.linuxserver.io/). This role installs the SWAG Docker image on Linux systems running Docker.

Repository: [linuxserver/docker-swag](https://github.com/linuxserver/docker-swag)

---

## What is SWAG?

SWAG (Secure Web Application Gateway, formerly known as letsencrypt) sets up an Nginx webserver and reverse proxy with PHP support and a built-in certbot client for automated SSL certificate generation and renewal (Let's Encrypt and ZeroSSL). It also includes fail2ban for intrusion prevention.

---

## Certbot Plugins

SWAG includes many Certbot plugins out of the box. If you need a plugin that's not included, use the Universal Package Install Docker Mod:

```yaml
environment:
  DOCKER_MODS: linuxserver/mods:universal-package-install
  INSTALL_PIP_PACKAGES: certbot-dns-<plugin>
```

Set the required credentials in `/config/dns-conf/<plugin>.ini`. Test with `STAGING=true` first.

---

## Security and Password Protection

- SWAG detects changes to URLs and subdomains, revokes existing certs, and generates new ones on start.
- To password-protect your sites, use htpasswd:
  ```bash
  docker exec -it swag htpasswd -c /config/nginx/.htpasswd <username>
  ```
- For additional users, omit the `-c` flag.
- LDAP authentication is also supported (see the provided `ldap.conf` and use the `linuxserver/ldap-auth` image).

---

## Site Config and Reverse Proxy

- Default site config: `/config/nginx/site-confs/default.conf`
- Add or modify conf files in this directory. Deleting the default will recreate it on container start.
- Preset reverse proxy configs for popular apps are available in `/config/nginx/proxy_confs`.
- To hide your site from search engines, add this to your site config:
  ```nginx
  add_header X-Robots-Tag "noindex, nofollow, nosnippet, noarchive";
  ```
- To redirect HTTP to HTTPS, expose port 80.

---

## Using Certs in Other Containers

- Mount the SWAG config folder in other containers to use certs:
  ```bash
  -v /path-to-swag-config:/swag-ssl
  # Use certs from /swag-ssl/keys/letsencrypt/
  ```
- Or, mount only the `/etc` subfolder for more security:
  ```bash
  -v /path-to-swag-config/etc:/swag-ssl
  # Use certs from /swag-ssl/letsencrypt/live/<your.domain.url>/
  ```

---

## Using fail2ban

- SWAG includes fail2ban with 5 default jails.
- To check status:
  ```bash
  docker exec -it swag fail2ban-client status
  docker exec -it swag fail2ban-client status <jail name>
  ```
- To unban an IP:
  ```bash
  docker exec -it swag fail2ban-client set <jail name> unbanip <IP>
  ```
- See [fail2ban commands](https://www.fail2ban.org/wiki/index.php/Commands) for more.

---

## Updating Configs

- Config updates are noted in the changelog but not automatically applied.
- If you have modified a config file, review changes and apply manually, or delete and restart the container to regenerate.
- Proxy sample updates are not listed in the changelog. See [reverse-proxy-confs commits](https://github.com/linuxserver/reverse-proxy-confs/commits/master).

---

## Example Playbook

This example installs Docker and the SWAG reverse proxy container with most defaults. Set `swag__url` to your own domain and subdomains as needed.

> **Note:** This playbook uses another role, `bsmeding.docker`, to install Docker. Install it with `ansible-galaxy role install bsmeding.docker` or install Docker manually and comment out the first task.

```yaml
---
- name: Install DMZ
  hosts: [dmz]
  gather_facts: true
  become: yes
  vars:
    swag__port_web: 80
    swag__port_ssh: 443
    swag__url: 'example.com'
    swag__subdomains: 'www'
    swag__validation: 'http'
  tasks:
    - name: Check if docker is installed
      ansible.builtin.include_role:
        name: bsmeding.docker

    - name: Check if SWAG is installed
      ansible.builtin.include_role:
        name: bsmeding.docker_swag
```

---

## Subdomain Reverse Proxy Example

To use the reverse proxy, templates are available so you don't have to create Nginx config files yourself. For example, to point `https://dash.example.com` to `http://192.168.111.241:9090`:

```yaml
swag__proxy_confs_subdomain:
  - server_name: dash.example.com
    listen: 443
    default_upstream_proto: http
    default_upstream_url: 192.168.1.10
    default_upstream_port: 9090
```

---

## Variables

A selection of variables you can use (see the role for full list):

| Variable                            | Default Value                                       | Description                                                                                           |
|-------------------------------------|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `swag__name`                        | `swag`                                              | The name of the container.                                                                            |
| `swag__image`                       | `lscr.io/linuxserver/swag`                          | The Docker image to use for SWAG.                                                                     |
| `swag__port_web`                    | `80`                                                | Port for web traffic.                                                                                 |
| `swag__port_ssh`                    | `443`                                               | Port for SSH/SSL traffic.                                                                             |
| `swag__skip_setup`                  | `false`                                             | Set to `true` to disable the setup stage of the SWAG image.                                           |
| `swag__url`                         | `'example.com'`                                     | The base URL for the SWAG setup.                                                                      |
| `swag__subdomains`                  | `'www'`                                             | Subdomains for the SWAG setup.                                                                        |
| `swag__validation`                  | `'http'`                                            | Method of validation (`http` or `dns`).                                                               |
| `swag__certprovider`                | `''` (optional)                                     | Certificate provider (e.g., `zerossl`).                                                               |
| `swag__dnsplugin`                   | `''` (optional)                                     | DNS plugin (e.g., `cloudflare`).                                                                      |
| `swag__cloudflare_global_email`     | `''` (optional)                                     | Cloudflare global email (if using Cloudflare DNS plugin).                                             |
| `swag__cloudflare_global_api`       | `''` (optional)                                     | Cloudflare global API key (if using Cloudflare DNS plugin).                                           |
| `swag__cloudflare_api_token`        | `''` (optional)                                     | Cloudflare API token (if using Cloudflare DNS plugin).                                                |
| `swag__email`                       | `'mail@example.com'`                                | Email for certificate provider notifications.                                                          |
| `swag__only_subdomains`             | `'false'`                                           | Use only subdomains for the SSL certificate.                                                          |
| `swag__extra_domain`                | `''`                                                | Additional domains for the SSL certificate.                                                           |
| `swag__staging`                     | `'true'`                                            | Use staging environment (recommended for testing with Let's Encrypt).                                 |
| `swag__docker_mods`                 | `'linuxserver/mods:swag-cloudflare-real-ip'`        | Docker mods to use with SWAG.                                                                         |
| `swag__remove_existing_container`   | `no`                                                | Remove any existing container before creating a new one.                                              |
| `swag__remove_existing_home_dir`    | `no`                                                | Removes the home directory (for testing purposes only!).                                              |
| `swag__pull_image`                  | `yes`                                               | Pull the Docker image if not already pulled.                                                          |
| `swag__network_mode`                | `'default'`                                         | Network mode for Docker container.                                                                    |
| `swag__network_cidr`                | `'172.16.81.0/26'`                                  | CIDR for network configuration.                                                                       |
| `swag__network`                     | `'proxy'`                                           | Network to connect the container to.                                                                  |
| `swag__container_networks`          | `[{'name': 'bridge'}, {'name': swag__network}]`     | List of networks for the container to join.                                                           |
| `swag__purge_networks`              | `no`                                                | Remove all networks upon container removal.                                                           |
| `swag__log_driver`                  | `'json-file'`                                       | Log driver for Docker.                                                                                |
| `swag__log_options`                 | `{}`                                                | Additional options for the log driver.                                                                |
| `swag__home`                        | `"/opt/{{ swag__name }}"`                           | Home directory for SWAG files.                                                                        |
| `swag__use_local_directories_instead_of_volumes` | `true`                  | Use mapped folders instead of volumes (volumes not set up).                                           |
| `swag__directories`                 | List of directories with paths and permissions      | Directories to create with specific permissions.                                                      |
| `swag__ports`                       | `["{{ swag__port_web }}:80", "{{ swag__port_ssh }}:443"]` | Ports to expose for SWAG container.                                                      |
| `swag__directory_volumes`           | `["{{ swag__home }}/config:/config"]`               | Directory volumes for the container.                                                                  |
| `swag__file_volumes`                | `["/var/run/docker.sock:/var/run/docker.sock:ro"]`  | File volumes for the container.                                                                       |
| `swag__default_env`                 | Various defaults (see below)                        | Default environment variables for the SWAG container.                                                 |
| `swag__env`                         | `{}`                                                | Additional environment variables.                                                                     |
| `swag__proxy_confs_subdomain`       | List of subdomain configuration proxies             | Subdomain proxy configurations for different applications.                                            |

### Default Environment Variables (`swag__default_env`)

- `TZ`: Time zone for the container (default: `Europe/Paris`).
- `PUID`: User ID for Docker (default: `1040`).
- `PGID`: Group ID for Docker (default: `1001`).
- `URL`: Base URL for SWAG.
- `SUBDOMAINS`: Subdomains to use (default: `www`).
- `VALIDATION`: Validation method (default: `http`).
- `CERTPROVIDER`: Certificate provider (optional).
- `DNSPLUGIN`: DNS plugin (optional).
- `EMAIL`: Email for certificate notifications.
- `ONLY_SUBDOMAINS`: Use only subdomains (default: `false`).
- `EXTRA_DOMAINS`: Extra domains for SSL (optional).
- `STAGING`: Use staging environment for testing (default: `false`).
- `DOCKER_MODS`: Docker mods (optional).
- `CF_ZONE_ID`, `CF_ACCOUNT_ID`, `CF_API_TOKEN`: Cloudflare credentials if using Cloudflare DNS validation.

---

## Proxy Configuration Examples

In `swag__proxy_confs_subdomain`, you can configure additional subdomain proxies as follows:

```yaml
swag__proxy_confs_subdomain:
  - server_name: dash.example.com
    listen: 443
    enable_ldap: false
    enable_authelia: true
    default_upstream_proto: http
    default_upstream_url: dashboard
    default_upstream_port: 9090
  - server_name: app1.example.com
    listen: 443
    enable_ldap: false
    enable_authelia: false
    default_upstream_proto: http
    default_upstream_url: 192.168.1.10
    default_upstream_port: 8080
```
