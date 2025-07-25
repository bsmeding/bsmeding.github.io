---
authors: [bsmeding]
date: 2025-04-10
title: Nautobot Docker Images with Pre-Installed Apps
summary: Discover ready-to-use Nautobot Docker images with all major apps pre-installed. Learn how to deploy Nautobot with Docker Compose and activate the plugins you need—no manual builds or pip installs required.
tags: ["nautobot", "docker", "network automation", "cmdb", "ssot", "plugins", "apps"]
toc: true
layout: single
comments: true
---

# Nautobot Docker Images with Pre-Installed Apps

Managing and extending Nautobot with plugins and apps can be challenging, especially for users who are not familiar with Docker, Docker builds, or Python package management. To make things easier, I maintain a set of Docker images based on the official Nautobot images, but with almost all major Nautobot apps pre-installed and ready to use.
<!-- more -->

## 🚀 What Are These Images?
- **Based on the official Nautobot images** (latest two major versions: 1.x and 2.x)
- **All major Nautobot apps pre-installed** ([see full list of apps](https://docs.nautobot.com/projects/core/en/stable/apps/))
- **No need to build or install plugins manually**
- **Just activate the plugins you want** in your `nautobot_config.py`
- **Available on Docker Hub:** [bsmeding/nautobot](https://hub.docker.com/repository/docker/bsmeding/nautobot)

## 🧩 Included Nautobot Apps
The images include (but are not limited to):
- Nautobot ChatOps
- Nautobot Data Validation Engine
- Nautobot Device Lifecycle Management
- Nautobot Device Onboarding
- Nautobot Firewall Models
- Nautobot Golden Configuration
- Nautobot Plugin Nornir
- Nautobot Single Source of Truth (SSoT)

For the full and up-to-date list, see the [Nautobot Apps documentation](https://docs.nautobot.com/projects/core/en/stable/apps/).

## 🛠️ How to Use
1. **Pull the image from Docker Hub:**
   ```bash
   docker pull bsmeding/nautobot:2.x-latest  # or 1.x-latest for Nautobot 1.x
   ```
2. **Use the provided Docker Compose file:**
```yaml

services:
  nautobot:
    container_name: nautobot
    image: &shared_image bsmeding/nautobot:stable-py3.11
    depends_on:
      - postgres
      - redis
    ports:
      - "8080:8080"  # Exposes Nautobot on localhost:8080
    environment:
      - NAUTOBOT_DEBUG=True
      - NAUTOBOT_DJANGO_EXTENSIONS_ENABLED=False
      - NAUTOBOT_DJANGO_TOOLBAR_ENABLED=False
      - NAUTOBOT_HIDE_RESTRICTED_UI=True
      - NAUTOBOT_LOG_LEVEL=WARNING
      - NAUTOBOT_METRICS_ENABLED=False
      - NAUTOBOT_NAPALM_TIMEOUT=5
      - NAUTOBOT_MAX_PAGE_SIZE=0
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_ALLOWED_HOSTS=*
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379
      - NAUTOBOT_SUPERUSER_NAME=admin
      - NAUTOBOT_SUPERUSER_PASSWORD=admin
      - NAUTOBOT_SUPERUSER_API_TOKEN=1234567890abcde0987654321
      - NAUTOBOT_CREATE_SUPERUSER=true
      - NAUTOBOT_INSTALLATION_METRICS_ENABLED=false
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_SECURE_HSTS_SECONDS=3600
      - NAUTOBOT_SECURE_SSL_REDIRECT=True
      - NAUTOBOT_SESSION_COOKIE_SECURE=True
      - NAUTOBOT_CSRF_COOKIE_SECURE=True
    volumes:
      - nautobot_config:/opt/nautobot/
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
    command: ["nautobot-server", "runserver", "0.0.0.0:8080"]

  postgres:
    image: postgres:13-alpine
    container_name: postgres
    command:
      - "-c"
      - "max_connections=1000"
    healthcheck:
      test: "pg_isready --username=$$POSTGRES_USER --dbname=$$POSTGRES_DB"
      interval: "10s"
      timeout: "5s"
      retries: 10    
    environment:
      POSTGRES_USER: nautobot
      POSTGRES_PASSWORD: nautobotpassword
      POSTGRES_DB: nautobot
    volumes:
      - "postgres_data:/var/lib/postgresql/data"
    restart: unless-stopped

  redis:
    image: redis:6
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery-beat:
    container_name: nautobot_celery_beat
    image: *shared_image
    command: nautobot-server celery beat
    depends_on:
      nautobot:
        condition: "service_healthy"
    volumes:
      - nautobot_config:/opt/nautobot/
    environment:
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py

  celery-worker-1:
    image: *shared_image
    container_name: nautobot_celery_worker_1
    command: nautobot-server celery worker --concurrency=4
    depends_on:
      nautobot:
        condition: "service_healthy"
    healthcheck:
      interval: "30s"
      timeout: "10s"
      start_period: "30s"
      retries: 3
      test:
        [
          "CMD",
          "bash",
          "-c",
          "nautobot-server celery inspect ping --destination celery@$$HOSTNAME"  ## $$ because of docker-compose
        ]
    volumes:
      - nautobot_config:/opt/nautobot/
    environment:
      - NAUTOBOT_DB_HOST=postgres
      - NAUTOBOT_DB_PORT=5432
      - NAUTOBOT_DB_NAME=nautobot
      - NAUTOBOT_DB_USER=nautobot
      - NAUTOBOT_DB_PASSWORD=nautobotpassword
      - NAUTOBOT_REDIS_HOST=redis
      - NAUTOBOT_REDIS_PORT=6379      
      - NAUTOBOT_CELERY_BROKER_URL=redis://redis:6379/0
      - NAUTOBOT_CONFIG=/opt/nautobot/nautobot_config.py


volumes:
  nautobot_config: {}
  postgres_data: {}
  redis_data: {}
```
   - Source: [docker-compose.yml Gist](https://gist.github.com/bsmeding/d60cf4f23519c75ca2339148d6efd7fe)
   - This Compose file sets up Nautobot, Postgres, Redis, and volumes for persistent data.
3. **Configure your plugins/apps:**
   - Edit `nautobot_config.py` to activate the plugins you want. All are pre-installed, just enable them in the config.
   - Example:
     ```python
     PLUGINS = [
         "nautobot_chatops",
         "nautobot_golden_config",
         # ...add or remove as needed
     ]
     ```
4. **Start Nautobot:**
   ```bash
   docker compose up -d
   ```

## 🔍 Requirements Files
- For Nautobot 1.x: see `requirements_1.x.txt` in the [GitHub repo](https://github.com/bsmeding/nautobot-docker)
- For Nautobot 2.x: see `requirements2.x.txt` in the [GitHub repo](https://github.com/bsmeding/nautobot-docker)

## 📝 Why Use These Images?
- **Save time:** No need to build or install plugins manually.
- **Consistency:** All users get the same set of apps and versions.
- **Easy upgrades:** Just pull the latest image for new Nautobot or app versions.
- **Great for labs, demos, and production** where you want a quick start.

## 🔗 Resources
- [Nautobot Apps Documentation](https://docs.nautobot.com/projects/core/en/stable/apps/)
- [Docker Compose Example](https://gist.github.com/bsmeding/d60cf4f23519c75ca2339148d6efd7fe)
- [Docker Hub: bsmeding/nautobot](https://hub.docker.com/repository/docker/bsmeding/nautobot)
- [GitHub: bsmeding/nautobot-docker](https://github.com/bsmeding/nautobot-docker)

---

If you have questions or want to suggest more apps to include, feel free to open an issue or contact me via the links above! 