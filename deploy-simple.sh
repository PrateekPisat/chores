#!/bin/bash

# Quick deployment script for single-server setup (HTTP only)
# Use this for development/testing or when SSL is handled by a load balancer

set -e

echo "🚀 Deploying Chores Application (Single Server - HTTP)..."

# Check if environment file exists
ENV_FILE="dev.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  Warning: $ENV_FILE not found, using .env if available"
    if [ -f ".env" ]; then
        ENV_FILE=".env"
    else
        echo "❌ No environment file found. Please create .env.prod or .env"
        exit 1
    fi
fi

# Load environment variables
source "$ENV_FILE"

# Pull latest changes (optional - comment out for local development)
# echo "📥 Pulling latest changes..."
# git pull origin main

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose --profile production down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose --profile production up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Simple health checks
echo "🔍 Performing health checks..."

# Check if containers are running
RUNNING_CONTAINERS=$(docker-compose --profile production ps --services --filter "status=running" | wc -l)
TOTAL_SERVICES=7  # postgres, task_service, users_service, house_service, api, ui-prod, nginx

if [ "$RUNNING_CONTAINERS" -eq "$TOTAL_SERVICES" ]; then
    echo "✅ All $TOTAL_SERVICES services are running"
else
    echo "⚠️  Only $RUNNING_CONTAINERS out of $TOTAL_SERVICES services are running"
fi

# Test application availability
sleep 10
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Application is responding correctly"
else
    echo "⚠️  Application health check failed (HTTP $HTTP_STATUS)"
fi

echo ""
echo "✅ Deployment complete!"
echo "🌐 Application: http://localhost"
echo "🔗 API: http://localhost/api"
echo "📊 Health: http://localhost/health"

echo ""
echo "📋 Service status:"
docker-compose --profile production ps

echo ""
echo "🔧 Useful commands:"
echo "  View logs: docker-compose --profile production logs -f"
echo "  Stop all: docker-compose --profile production down"
echo "  Restart: docker-compose --profile production restart"