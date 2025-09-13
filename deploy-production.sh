#!/bin/bash

# Zimmer Platform Production Deployment Script
# This script deploys the Zimmer platform using Docker Compose

set -e

echo "🚀 Starting Zimmer Platform Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Create production environment file if it doesn't exist
if [ ! -f "env.production" ]; then
    print_warning "Production environment file not found. Creating from template..."
    cp env.production env.production.backup 2>/dev/null || true
    print_warning "Please edit env.production with your production values before continuing."
    print_warning "Required variables:"
    echo "  - JWT_SECRET_KEY"
    echo "  - GOOGLE_CLIENT_ID"
    echo "  - GOOGLE_CLIENT_SECRET"
    echo "  - ZARRINPAL_MERCHANT_ID"
    echo "  - OPENAI_API_KEY"
    echo "  - SMTP credentials"
    exit 1
fi

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Clean up old images and containers
print_status "Cleaning up old Docker resources..."
docker system prune -f || true

# Build and start services
print_status "Building and starting services..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check service health
print_status "Checking service health..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend is healthy"
else
    print_error "Backend health check failed"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

# Check user panel
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "User panel is accessible"
else
    print_warning "User panel health check failed"
fi

# Check admin dashboard
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    print_success "Admin dashboard is accessible"
else
    print_warning "Admin dashboard health check failed"
fi

# Show running containers
print_status "Running containers:"
docker-compose -f docker-compose.prod.yml ps

print_success "Deployment completed!"
print_status "Services are available at:"
echo "  - Backend API: http://localhost:8000"
echo "  - User Panel: http://localhost:3000"
echo "  - Admin Dashboard: http://localhost:3001"
echo ""
print_status "To view logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
print_status "To stop services:"
echo "  docker-compose -f docker-compose.prod.yml down"
