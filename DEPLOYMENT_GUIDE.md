# 🚀 Zimmer AI Platform - Production Deployment Guide

## Prerequisites
- Ubuntu 22.04 LTS server with sudo access
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

## Step 1: Server Initial Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git nginx certbot python3-certbot-nginx

# Install Python 3.10+
sudo apt install -y python3.10 python3.10-venv python3-pip

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib
```

## Step 2: Database Setup

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE zimmer_db;
CREATE USER zimmer_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE zimmer_db TO zimmer_user;
\q
```

## Step 3: Application Deployment

```bash
# Create application directory
sudo mkdir -p /var/www/zimmer
sudo chown $USER:$USER /var/www/zimmer
cd /var/www/zimmer

# Clone your repository
git clone https://github.com/yourusername/zimmer-full-structure.git .

# Backend Setup
cd zimmer-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create production environment file
cp env.example .env
```

## Step 4: Environment Configuration

Edit `/var/www/zimmer/zimmer-backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://zimmer_user:your_secure_password@localhost/zimmer_db

# Security (Generate secure keys)
JWT_SECRET_KEY=your_generated_jwt_secret
OAI_ENCRYPTION_SECRET=your_generated_encryption_key

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DEBUG=false

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
```

## Step 5: Frontend Setup

```bash
# User Panel
cd /var/www/zimmer/zimmer_user_panel
npm install
npm run build

# Admin Dashboard  
cd /var/www/zimmer/zimmermanagement/zimmer-admin-dashboard
npm install
npm run build
```

## Step 6: Process Management

Create systemd service for backend:

```bash
sudo nano /etc/systemd/system/zimmer-backend.service
```

```ini
[Unit]
Description=Zimmer Backend API
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/zimmer/zimmer-backend
Environment=PATH=/var/www/zimmer/zimmer-backend/venv/bin
ExecStart=/var/www/zimmer/zimmer-backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable zimmer-backend
sudo systemctl start zimmer-backend
```

Install PM2 for frontend apps:

```bash
sudo npm install -g pm2

# Start frontend applications
cd /var/www/zimmer/zimmer_user_panel
pm2 start npm --name "zimmer-user" -- start

cd /var/www/zimmer/zimmermanagement/zimmer-admin-dashboard  
pm2 start npm --name "zimmer-admin" -- start

# Save PM2 configuration
pm2 save
pm2 startup
```

## Step 7: Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/zimmer
```

```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}

# User Panel
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Admin Dashboard
server {
    listen 80;
    server_name admin.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/zimmer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Step 8: SSL Setup

```bash
# Install SSL certificates
sudo certbot --nginx -d yourdomain.com -d admin.yourdomain.com -d api.yourdomain.com
```

## Step 9: Security Hardening

```bash
# UFW Firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

## Step 10: Monitoring & Backup

```bash
# Install monitoring tools
sudo apt install htop iotop netstat

# Setup automated backups
sudo crontab -e
```

Add to crontab:
```bash
# Daily database backup at 2 AM
0 2 * * * pg_dump zimmer_db > /var/backups/zimmer_$(date +\%Y\%m\%d).sql

# Weekly cleanup (keep 30 days)
0 3 * * 0 find /var/backups -name "zimmer_*.sql" -mtime +30 -delete
```

## Verification Checklist

- [ ] Backend API responds at http://api.yourdomain.com/health
- [ ] User panel loads at http://yourdomain.com
- [ ] Admin dashboard loads at http://admin.yourdomain.com
- [ ] SSL certificates installed and working
- [ ] Database connection working
- [ ] All services start automatically on reboot
- [ ] Firewall configured
- [ ] Backups scheduled

## Troubleshooting

### Check service status:
```bash
sudo systemctl status zimmer-backend
pm2 status
sudo systemctl status nginx
```

### View logs:
```bash
sudo journalctl -u zimmer-backend -f
pm2 logs
sudo tail -f /var/log/nginx/error.log
```

### Common issues:
1. **500 errors**: Check backend logs and environment variables
2. **Connection refused**: Verify services are running on correct ports
3. **CORS errors**: Update ALLOWED_ORIGINS in backend .env
4. **Database errors**: Check PostgreSQL connection and credentials
