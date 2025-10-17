#!/bin/bash

# Deploy Full Stack Chores Application on Single Server
# This script deploys both frontend and backend on one server

set -e

echo "🚀 Deploying Full Stack Chores Application..."

# Check if prod.env exists
if [ ! -f "prod.env" ]; then
    echo "❌ Error: prod.env file not found!"
    echo "Please create prod.env with all required environment variables."
    echo "You can use .env as a template."
    exit 1
fi

# Load environment variables
source prod.env

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose --profile production down

# Remove old images (optional - comment out if you want faster deployments)
echo "🧹 Cleaning up old images..."
docker system prune -f

# Build and start all services
echo "🔨 Building and starting services..."
docker-compose --profile production build --no-cache
docker-compose --profile production up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 60

# Check service health
echo "🔍 Checking service health..."

# Check if postgres is ready
until docker-compose --profile production exec -T postgres pg_isready -U postgres; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 5
done

# Check if API is responding
API_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
if [ "$API_HEALTH" = "200" ]; then
    echo "✅ API service is healthy"
else
    echo "⚠️  API service health check failed (HTTP $API_HEALTH)"
fi

# Check if Nginx is responding
NGINX_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health || echo "000")
if [ "$NGINX_HEALTH" = "200" ]; then
    echo "✅ Nginx service is healthy"
else
    echo "⚠️  Nginx service health check failed (HTTP $NGINX_HEALTH)"
fi

# Run database migrations (uncomment if you have them)
# echo "🔄 Running database migrations..."
# docker-compose --profile production exec api python -m alembic upgrade head

echo ""
echo "✅ Full stack deployment complete!"
echo "🌐 Application available at: http://$(hostname -I | awk '{print $1}')"
echo "🔗 API available at: http://$(hostname -I | awk '{print $1}')/api"
echo "📊 Health check: http://$(hostname -I | awk '{print $1}')/health"
echo ""
echo "Note: Application is configured for HTTP only."
echo "For HTTPS, consider using a reverse proxy like Cloudflare or configure SSL certificates."

echo ""
echo "📋 Running services:"
docker-compose --profile production ps

echo ""
echo "📝 To view logs: docker-compose --profile production logs -f"
echo "📝 To stop services: docker-compose --profile production down"