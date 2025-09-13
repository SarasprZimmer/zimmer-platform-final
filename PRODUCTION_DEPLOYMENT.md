# 🚀 Zimmer Platform Production Deployment Guide

This guide covers deploying the Zimmer platform to production using Docker Compose.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Domain names configured:
  - `api.zimmerai.com` → Your server IP
  - `panel.zimmerai.com` → Your server IP  
  - `dashboard.zimmerai.com` → Your server IP
- SSL certificates (recommended for production)

## 🔧 Environment Configuration

### 1. Create Production Environment File

Copy the template and configure your production values:

```bash
cp env.production .env.production
```

Edit `.env.production` with your production values:

```bash
# Database Configuration
POSTGRES_USER=zimmer
POSTGRES_PASSWORD=your-secure-database-password
POSTGRES_DB=zimmer
DATABASE_URL=postgresql+psycopg2://zimmer:your-secure-database-password@postgres:5432/zimmer

# API URLs
NEXT_PUBLIC_API_URL=https://api.zimmerai.com
NEXT_PUBLIC_API_BASE_URL=https://api.zimmerai.com

# JWT Configuration (REQUIRED - Generate a strong secret key)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Google OAuth (Production)
GOOGLE_CLIENT_ID=your-production-google-client-id
GOOGLE_CLIENT_SECRET=your-production-google-client-secret

# Payment Configuration
ZARRINPAL_MERCHANT_ID=your-production-merchant-id
PAYMENTS_MODE=live

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Email Configuration
SMTP_HOST=your-smtp-host
SMTP_USER=your-smtp-user
SMTP_PASSWORD=your-smtp-password
```

### 2. Backend Environment File

The backend uses `zimmer-backend/env.production` for additional configuration.

## 🚀 Deployment

### Quick Deployment

```bash
# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check service health
curl http://localhost:8000/health
```

### Step-by-Step Deployment

1. **Stop existing services:**
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

2. **Clean up old resources:**
   ```bash
   docker system prune -f
   ```

3. **Build and start services:**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

4. **Wait for services to be ready:**
   ```bash
   sleep 30
   ```

5. **Verify deployment:**
   ```bash
   # Check backend
   curl http://localhost:8000/health
   
   # Check user panel
   curl http://localhost:3000
   
   # Check admin dashboard
   curl http://localhost:3001
   ```

## 🔍 Service Health Checks

### Backend API
- **URL:** `http://localhost:8000/health`
- **Expected Response:** `{"status":"healthy","timestamp":...}`

### User Panel
- **URL:** `http://localhost:3000`
- **Expected Response:** HTML page

### Admin Dashboard
- **URL:** `http://localhost:3001`
- **Expected Response:** HTML page

## 📊 Monitoring

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f user_panel
docker-compose -f docker-compose.prod.yml logs -f admin_dashboard
```

### Check Container Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Resource Usage
```bash
docker stats
```

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :3001
   ```

2. **Database connection issues:**
   ```bash
   # Check database logs
   docker-compose -f docker-compose.prod.yml logs postgres
   ```

3. **Frontend not connecting to backend:**
   - Verify environment variables are set correctly
   - Check CORS configuration in backend
   - Ensure API URLs are accessible

### Reset Everything
```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Remove all containers and images
docker system prune -a --volumes

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🔒 Security Considerations

1. **Change default passwords** in environment files
2. **Use strong JWT secrets** (32+ characters)
3. **Enable HTTPS** with proper SSL certificates
4. **Configure firewall** to only allow necessary ports
5. **Regular security updates** for base images

## 📈 Performance Optimization

1. **Database optimization:**
   - Configure PostgreSQL for production
   - Set up database indexes
   - Monitor query performance

2. **Application optimization:**
   - Adjust UVICORN_WORKERS based on CPU cores
   - Configure Redis for caching (if needed)
   - Monitor memory usage

3. **Nginx optimization:**
   - Enable gzip compression
   - Configure rate limiting
   - Set up proper caching headers

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify environment variables are set correctly
3. Ensure all required services are running
4. Check network connectivity between services

---

**Note:** This deployment uses the production Docker Compose configuration with proper environment variable handling and security settings.
