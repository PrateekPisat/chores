# Chores Application

## Database Configuration

This application supports different database configurations for development and production environments.

### Development Environment

In development mode, PostgreSQL runs as a Docker container:

```bash
# Start development environment with local PostgreSQL
./start-dev.sh
```

This will:
- Start a PostgreSQL container accessible at `localhost:5432`
- Use default credentials: `postgres/postgres`
- Create a database named `chores`

### Production Environment

In production mode, PostgreSQL is **not included** in the Docker Compose setup. You need to configure an external database.

#### Required Environment Variables

Update your `prod.env` file with your external database configuration:

```bash
# External Database Configuration
DATABASE_HOST="your-external-db-host"        # e.g., "db.example.com"
DATABASE_USERNAME="your-db-username"
DATABASE_PASSWORD="your-db-password"
DATABASE_DATABASE="chores"
DATABASE_PORT=5432
```

#### Supported External Database Options

- **Managed PostgreSQL Services:**
  - AWS RDS PostgreSQL
  - Google Cloud SQL for PostgreSQL
  - Azure Database for PostgreSQL
  - DigitalOcean Managed Databases
  
- **Self-hosted PostgreSQL:**
  - Separate PostgreSQL server
  - PostgreSQL running on the same server (outside Docker)

#### Database Migration

Before running in production, ensure your external database has the required schema:

```bash
# Run migrations against your external database
docker-compose --profile production exec api python -m alembic upgrade head
```

### Commands

```bash
# Development (with local PostgreSQL)
./start-dev.sh

# Production (with external database)
./deploy-full-stack.sh
```

## Security Notes

- Always use strong passwords for production databases
- Enable SSL/TLS connections to your external database
- Consider using connection pooling for better performance
- Regularly backup your production database