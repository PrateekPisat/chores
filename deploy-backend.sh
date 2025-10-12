#!/bin/bash

# Deploy Backend Services
# Run this on your backend server

set -e

echo "🚀 Deploying Chores Backend Services..."

# Load environment variables
source .env.backend.prod

# Pull latest changes
git pull origin main

# Build and start services
docker-compose -f docker-compose.backend.yml down
docker-compose -f docker-compose.backend.yml build --no-cache
docker-compose -f docker-compose.backend.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Run database migrations (if you have them)
# docker-compose -f docker-compose.backend.yml exec api python -m alembic upgrade head

echo "✅ Backend deployment complete!"
echo "🔗 API available at: http://$(hostname -I | awk '{print $1}'):8000"

# Show running services
docker-compose -f docker-compose.backend.yml ps