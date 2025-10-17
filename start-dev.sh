#!/bin/bash

# Start development environment
# This runs without Nginx for local development

set -e

echo "🚀 Starting Chores Development Environment..."

# Check if environment file exists
if [ -f ".env" ]; then
    echo "📁 Loading environment from .env"
    source .env
elif [ -f "dev.env" ]; then
    echo "📁 Loading environment from dev.env"
    source dev.env
else
    echo "⚠️  No environment file found, using defaults"
fi

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose down

# Build and start development services (with dev profile)
echo "🔨 Building and starting development services..."
docker-compose --profile dev up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 20

# Simple health checks
echo "🔍 Performing health checks..."

# Check if API is responding
API_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
if [ "$API_HEALTH" = "200" ]; then
    echo "✅ API service is healthy"
else
    echo "⚠️  API service health check failed (HTTP $API_HEALTH)"
fi

# Check if UI is responding
UI_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000 2>/dev/null || echo "000")
if [ "$UI_HEALTH" = "200" ]; then
    echo "✅ UI service is healthy"
else
    echo "⚠️  UI service health check failed (HTTP $UI_HEALTH)"
fi

echo ""
echo "✅ Development environment ready!"
echo "🌐 Frontend: http://localhost:9000"
echo "🔗 Backend API: http://localhost:8000"
echo "🗄️  Database: localhost:5432"

echo ""
echo "📋 Service status:"
docker-compose --profile dev ps

echo ""
echo "🔧 Useful commands:"
echo "  View logs: docker-compose --profile dev logs -f"
echo "  Stop all: docker-compose --profile dev down"
echo "  Restart: docker-compose --profile dev restart"
echo "  Shell into API: docker-compose exec api bash"
echo "  Shell into UI: docker-compose exec ui sh"