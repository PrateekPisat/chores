#!/bin/bash

# SSL Certificate Setup Script for Chores App
# This script helps you obtain SSL certificates using Let's Encrypt

set -e

echo "🔐 SSL Certificate Setup for Chores App"
echo "========================================"

# Check if email is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide your email address"
    echo "Usage: ./setup-ssl.sh your-email@example.com"
    exit 1
fi

EMAIL=$1
DOMAINS="chores.prateekpisat.com,www.chores.prateekpisat.com,api.chores.prateekpisat.com"

echo "📧 Email: $EMAIL"
echo "🌐 Domains: $DOMAINS"
echo ""

# Step 1: Start services without SSL first
echo "🚀 Step 1: Starting services in HTTP mode..."
docker compose --profile production down 2>/dev/null || true

# Create a temporary nginx config for HTTP-only mode during certificate generation
cp nginx/conf.d/default.conf nginx/conf.d/default.conf.ssl-backup

# Create HTTP-only config for initial certificate generation
cat > nginx/conf.d/default.conf << 'EOF'
# Upstream for backend API (local container network)
upstream backend_api {
    server api:8000;
}

# Main HTTP server (for certificate generation)
server {
    listen 80;
    server_name chores.prateekpisat.com www.chores.prateekpisat.com;

    # Let's Encrypt challenge location
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Temporary location for other requests during setup
    location / {
        proxy_pass http://ui-prod:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# API HTTP server (for certificate generation)
server {
    listen 80;
    server_name api.chores.prateekpisat.com;

    # Let's Encrypt challenge location
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Temporary location for other requests during setup
    location / {
        proxy_pass http://backend_api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Start services
docker compose --profile production up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Step 2: Obtain certificates
echo ""
echo "🔑 Step 2: Obtaining SSL certificates..."

# Get certificates for main domain and API domain
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d chores.prateekpisat.com

docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d api.chores.prateekpisat.com

# Step 3: Restore SSL configuration
echo ""
echo "🔄 Step 3: Enabling SSL configuration..."

# Restore the SSL-enabled nginx config
mv nginx/conf.d/default.conf.ssl-backup nginx/conf.d/default.conf

# Restart nginx with SSL configuration
docker compose restart nginx

echo ""
echo "✅ SSL setup complete!"
echo ""
echo "🎉 Your applications are now available at:"
echo "   🌐 Main site: https://chores.prateekpisat.com"
echo "   🔗 API: https://api.chores.prateekpisat.com"
echo ""
echo "📋 Certificate locations:"
echo "   📁 Main domain: /etc/letsencrypt/live/chores.prateekpisat.com/"
echo "   📁 API domain: /etc/letsencrypt/live/api.chores.prateekpisat.com/"
echo ""
echo "🔄 Certificates will auto-renew every 12 hours via the certbot container"
echo ""
echo "💡 To check certificate status:"
echo "   docker compose run --rm certbot certificates"