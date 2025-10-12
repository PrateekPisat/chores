# Multi-stage build for Quasar app
FROM node:lts-alpine AS base

# Install Quasar CLI globally
RUN npm install -g @quasar/cli

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production --silent

# Development stage
FROM base AS development

# Install all dependencies (including dev dependencies)
RUN npm ci --silent

# Copy source code
COPY . .

# Expose port for dev server
EXPOSE 9000

# Start development server
CMD ["quasar", "dev", "--host", "0.0.0.0", "--port", "9000"]

# Build stage
FROM base AS build

# Install all dependencies for building
RUN npm ci --silent

# Copy source code
COPY . .

# Build the app
RUN quasar build

# Production stage
FROM nginx:alpine AS production

# Copy built app from build stage
COPY --from=build /app/dist/spa /usr/share/nginx/html

# Copy custom nginx config if needed (optional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
