# 🚀 Zimmer Platform Deployment Guide

This guide covers deploying the Zimmer AI Platform to various environments.

## 📋 Prerequisites

- **Server**: Linux/Windows server with Docker support
- **Domain**: Registered domain name (optional but recommended)
- **SSL Certificate**: Let's Encrypt or commercial certificate
- **Database**: PostgreSQL (recommended) or SQLite (development)

## 🐳 Docker Deployment (Recommended)

### 1. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: zimmer_db
      POSTGRES_USER: zimmer_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  # Backend API
  backend:
    build: ./zimmer-backend
    environment:
      - DATABASE_URL=postgresql://zimmer_user:${DB_PASSWORD}@postgres:5432/zimmer_db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - EMAIL_HOST=${EMAIL_HOST}
      - EMAIL_PORT=${EMAIL_PORT}
      - EMAIL_USERNAME=${EMAIL_USERNAME}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    depends_on:
      - postgres
    restart: unless-stopped
    ports:
      - "8000:8000"

  # Admin Dashboard
  admin-dashboard:
    build: ./zimmermanagement/zimmer-admin-dashboard
    environment:
      - NEXT_PUBLIC_API_BASE_URL=${API_BASE_URL}
    restart: unless-stopped
    ports:
      - "3000:3000"

  # User Panel
  user-panel:
    build: ./zimmer_user_panel
    environment:
      - NEXT_PUBLIC_API_URL=${API_BASE_URL}
    restart: unless-stopped
    ports:
      - "3001:3001"

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - admin-dashboard
      - user-panel
    restart: unless-stopped

volumes:
  postgres_data:
```

### 2. Environment Variables

Create `.env` file:

```env
# Database
DB_PASSWORD=your-secure-db-password

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-64-chars-long

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# API URLs
API_BASE_URL=https://yourdomain.com/api

# Automation Service Tokens
AUTOMATION_1_SERVICE_TOKEN=your-service-token
AUTOMATION_2_SERVICE_TOKEN=your-service-token
```

### 3. Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream admin-dashboard {
        server admin-dashboard:3000;
    }

    upstream user-panel {
        server user-panel:3001;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security Headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";

        # API Routes
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Admin Dashboard
        location /admin/ {
            proxy_pass http://admin-dashboard/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # User Panel
        location / {
            proxy_pass http://user-panel/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 4. Deploy

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## ☁️ Cloud Deployment

### AWS Deployment

#### 1. EC2 Setup

```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Clone repository
git clone https://github.com/yourusername/zimmer-ai-platform.git
cd zimmer-ai-platform

# Setup SSL with Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem
```

#### 2. RDS Database (Optional)

```bash
# Create RDS PostgreSQL instance
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@your-rds-endpoint:5432/zimmer_db
```

#### 3. Deploy

```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d

# Setup SSL renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Google Cloud Platform

#### 1. Compute Engine

```bash
# Create VM instance
gcloud compute instances create zimmer-platform \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud

# Install Docker
gcloud compute ssh zimmer-platform --zone=us-central1-a
sudo apt update && sudo apt install docker.io docker-compose
```

#### 2. Cloud SQL (Optional)

```bash
# Create Cloud SQL instance
gcloud sql instances create zimmer-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create zimmer_db --instance=zimmer-db
```

### DigitalOcean

#### 1. Droplet Setup

```bash
# Create droplet with Docker image
# SSH into droplet
ssh root@your-droplet-ip

# Clone and deploy
git clone https://github.com/yourusername/zimmer-ai-platform.git
cd zimmer-ai-platform
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Manual Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip nodejs npm postgresql nginx

# Install Python dependencies
cd zimmer-backend
pip3 install -r requirements.txt

# Install Node.js dependencies
cd ../zimmermanagement/zimmer-admin-dashboard
npm install

cd ../../zimmer_user_panel
npm install
```

### 2. Database Setup

```bash
# PostgreSQL
sudo -u postgres createdb zimmer_db
sudo -u postgres createuser zimmer_user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE zimmer_db TO zimmer_user;"
```

### 3. Service Configuration

Create systemd services:

```bash
# Backend service
sudo nano /etc/systemd/system/zimmer-backend.service

[Unit]
Description=Zimmer Backend API
After=network.target

[Service]
Type=simple
User=zimmer
WorkingDirectory=/opt/zimmer/zimmer-backend
Environment=PATH=/opt/zimmer/venv/bin
ExecStart=/opt/zimmer/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/zimmer

server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin/ {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://localhost:3001/;
        proxy_set_header Host $host;
    }
}

sudo ln -s /etc/nginx/sites-available/zimmer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔐 SSL Configuration

### Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Commercial SSL

```bash
# Upload certificate files
sudo cp cert.pem /etc/nginx/ssl/
sudo cp key.pem /etc/nginx/ssl/

# Update nginx configuration
sudo nano /etc/nginx/sites-available/zimmer
# Add SSL configuration
```

## 📊 Monitoring & Logging

### 1. Application Logs

```bash
# Docker logs
docker-compose -f docker-compose.prod.yml logs -f

# System logs
sudo journalctl -u zimmer-backend -f
sudo journalctl -u nginx -f
```

### 2. Database Monitoring

```bash
# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log

# Database size
psql -d zimmer_db -c "SELECT pg_size_pretty(pg_database_size('zimmer_db'));"
```

### 3. Performance Monitoring

```bash
# System resources
htop
df -h
free -h

# Network connections
netstat -tulpn
```

## 🔄 Backup Strategy

### 1. Database Backup

```bash
# Create backup script
sudo nano /opt/zimmer/backup.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/zimmer/backups"
DB_NAME="zimmer_db"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump $DB_NAME > $BACKUP_DIR/zimmer_db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/zimmer_db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

# Make executable
chmod +x /opt/zimmer/backup.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /opt/zimmer/backup.sh
```

### 2. Application Backup

```bash
# Backup application files
tar -czf /opt/zimmer/backups/app_$(date +%Y%m%d).tar.gz \
  /opt/zimmer/zimmer-backend \
  /opt/zimmer/zimmermanagement \
  /opt/zimmer/zimmer_user_panel
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection**
```bash
# Check database status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U zimmer_user -d zimmer_db
```

2. **Port Conflicts**
```bash
# Check port usage
sudo netstat -tulpn | grep :8000
sudo lsof -i :3000
```

3. **SSL Issues**
```bash
# Test SSL configuration
openssl s_client -connect yourdomain.com:443

# Check certificate expiry
openssl x509 -in /etc/nginx/ssl/cert.pem -text -noout
```

4. **Memory Issues**
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head

# Increase swap if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Test database connectivity
4. Check firewall settings
5. Review nginx configuration

---

**Happy Deploying! 🚀**
