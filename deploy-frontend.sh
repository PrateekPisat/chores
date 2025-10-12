#!/bin/bash

# Deploy Frontend Services
# Run this on your frontend server

set -e

echo "🚀 Deploying Chores Frontend..."

# Load environment variables
source .env.frontend.prod

# Pull latest changes
git pull origin main

# Update nginx configuration with your backend server IP
read -p "Enter your backend server IP: " BACKEND_IP
sed -i "s/YOUR_BACKEND_SERVER_IP/$BACKEND_IP/g" nginx/conf.d/default.conf

# Build and start services
docker-compose -f docker-compose.frontend.yml down
docker-compose -f docker-compose.frontend.yml build --no-cache
docker-compose -f docker-compose.frontend.yml up -d

echo "✅ Frontend deployment complete!"
echo "🌐 Website available at: https://your-domain.com"

# Show running services
docker-compose -f docker-compose.frontend.yml ps