---
title: Install Docker Compose on Synology NAS
tags:
  - synology
  - docker-compose
  - tutorial
---

# Install Docker Compose on Synology NAS

This guide walks you through installing Docker Compose on your Synology NAS using SSH. Docker Compose is a tool for defining and running multi-container Docker applications.

---

## 📦 Prerequisites

Before you begin, make sure you have:

- A Synology NAS with Docker installed
- SSH access enabled on your Synology device ([see Synology documentation](https://kb.synology.com/en-global/DSM/tutorial/How_to_login_to_DSM_with_root_permission_via_SSH_Telnet))
- Administrator privileges

---

## 🛠 Installation Steps

1. **Login to your Synology NAS via SSH**
   - Use a terminal application (e.g., Terminal on macOS/Linux, PuTTY on Windows)
   - Connect using your NAS IP address and your admin credentials

2. **Switch to the root user:**

   ```sh
   sudo -i
   ```

3. **Download Docker Compose binary:**

   ```sh
   curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
     -o /usr/local/bin/docker-compose
   ```

4. **Make the binary executable:**

   ```sh
   chmod +x /usr/local/bin/docker-compose
   ```

5. **Verify the installation:**

   ```sh
   docker-compose version
   ```

You should see the installed Docker Compose version.

---

## 🚀 Next Steps
- Start using `docker-compose.yml` files to manage multi-container applications.
- Check the [Docker Compose documentation](https://docs.docker.com/compose/) for configuration options and examples.

---

## 📚 Resources
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Synology SSH Access Guide](https://kb.synology.com/en-global/DSM/tutorial/How_to_login_to_DSM_with_root_permission_via_SSH_Telnet)