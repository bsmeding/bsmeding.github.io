# Installing Nautobot in Docker Containers

**⚠️ IMPORTANT: This tutorial is for DEVELOPMENT purposes only. This setup is NOT suitable for production use.**

This tutorial will guide you through setting up Nautobot using Docker containers for development purposes using the [Nautobot Development Environment](https://github.com/bsmeding/nautobot_development_environment) repository.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later
- **Git**: For cloning the repository
- **Make**: For running convenience commands (optional but recommended)

## Step 1: Clone the Repository

First, clone the Nautobot development environment repository:

```bash
git clone https://github.com/bsmeding/nautobot_development_environment.git
cd nautobot_development_environment
```

## Step 2: Configure Environment Variables

Copy the example environment file and configure it for your setup:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferred settings. Key variables to configure:

```bash
# Database settings
POSTGRES_DB=nautobot
POSTGRES_USER=nautobot
POSTGRES_PASSWORD=your_secure_password

# Redis settings
REDIS_PASSWORD=your_redis_password

# Nautobot settings
NAUTOBOT_SECRET_KEY=your_secret_key_here
NAUTOBOT_ALLOWED_HOSTS=localhost,127.0.0.1
NAUTOBOT_SUPERUSER_NAME=admin
NAUTOBOT_SUPERUSER_EMAIL=admin@example.com
NAUTOBOT_SUPERUSER_PASSWORD=your_admin_password
```

## Step 3: Build and Start the Containers

Use Docker Compose to build and start all services:

```bash
docker-compose up -d --build
```

This command will:
- Build the Nautobot application container
- Start PostgreSQL database
- Start Redis for caching
- Start the Nautobot web application

## Step 4: Verify Installation

Check that all containers are running:

```bash
docker-compose ps
```

You should see all services (nautobot, postgres, redis) in the "Up" state.

## Step 5: Initialize the Database

Run database migrations and create the superuser:

```bash
docker-compose exec nautobot nautobot-server migrate
docker-compose exec nautobot nautobot-server createsuperuser
```

## Step 6: Access Nautobot

Once all services are running, you can access Nautobot at:

- **Web Interface**: http://localhost:8080
- **API**: http://localhost:8080/api/

Log in using the superuser credentials you created in Step 5.

## Development Workflow

### Making Code Changes

The repository is configured with volume mounts, so any changes you make to the Nautobot source code will be reflected immediately:

1. Make your changes to the code
2. The changes will be automatically detected
3. Restart the Nautobot container if needed: `docker-compose restart nautobot`

### Running Commands

Execute Nautobot management commands:

```bash
# Run shell
docker-compose exec nautobot nautobot-server shell

# Run tests
docker-compose exec nautobot nautobot-server test

# Collect static files
docker-compose exec nautobot nautobot-server collectstatic --no-input
```

### Viewing Logs

Monitor application logs:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f nautobot
```

## Useful Commands

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes (Clean Slate)
```bash
docker-compose down -v
```

### Rebuild After Dependencies Change
```bash
docker-compose up -d --build
```

### Access Database
```bash
docker-compose exec postgres psql -U nautobot -d nautobot
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**: If port 8080 is already in use, change the port mapping in `docker-compose.yml`

2. **Database Connection Issues**: Ensure PostgreSQL container is fully started before Nautobot tries to connect

3. **Permission Issues**: Make sure Docker has proper permissions to access the project directory

### Reset Everything

To completely reset your development environment:

```bash
docker-compose down -v
docker system prune -f
docker-compose up -d --build
```

## Next Steps

Now that you have Nautobot running in Docker, you can:

- Explore the web interface
- Create your first devices and sites
- Install and configure plugins
- Develop custom applications
- Contribute to the Nautobot project

For more information about Nautobot development, visit the [official documentation](https://nautobot.readthedocs.io/).
