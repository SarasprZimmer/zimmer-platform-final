#!/bin/bash

# 🚀 Zimmer AI Platform Deployment Script
# This script automates the deployment of the Zimmer AI Platform

set -e  # Exit on any error

echo "🚀 Starting Zimmer AI Platform Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/SarasprZimmer/zimmer-platform-final.git"
DEPLOY_DIR="/home/zimmer"
DOMAIN_NAME="zimmerai.com"
ADMIN_DOMAIN="admin.zimmerai.com"
DB_NAME="zimmer_platform"
DB_USER="zimmer_user"

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

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please do not run this script as root. Run as a regular user with sudo privileges."
    exit 1
fi

# Check if sudo is available
if ! command -v sudo &> /dev/null; then
    print_error "sudo is required but not installed. Please install sudo first."
    exit 1
fi

print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

print_status "Installing required system packages..."
sudo apt install -y python3.9 python3.9-pip python3.9-venv python3.9-dev
sudo apt install -y nodejs npm nginx postgresql postgresql-contrib
sudo apt install -y git curl wget unzip build-essential
sudo apt install -y certbot python3-certbot-nginx
sudo apt install -y ufw

print_status "Installing PM2 globally..."
sudo npm install -g pm2

print_status "Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD 'secure_password_123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"

print_status "Creating deployment directory..."
sudo mkdir -p $DEPLOY_DIR
sudo chown $USER:$USER $DEPLOY_DIR
cd $DEPLOY_DIR

print_status "Cloning repository..."
git clone $REPO_URL .
cd zimmer-platform-final

print_status "Setting up backend..."
cd zimmer-backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

print_status "Creating environment file..."
cat > .env << EOF
DATABASE_URL=postgresql://$DB_USER:secure_password_123@localhost:5432/$DB_NAME
JWT_SECRET_KEY=your_super_secret_jwt_key_$(date +%s)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
API_BASE_URL=https://$DOMAIN_NAME
FRONTEND_URL=https://$DOMAIN_NAME
ADMIN_URL=https://$ADMIN_DOMAIN
ZARRINPAL_MERCHANT_ID=your_zarinpal_merchant_id
ZARRINPAL_BASE_URL=https://api.zarinpal.com/pg/rest/WebGate
PAYMENTS_MODE=sandbox
OPENAI_API_KEY=your_openai_api_key_here
EOF

print_status "Running database migrations..."
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"

print_status "Setting up user panel..."
cd ../zimmer_user_panel
npm install
npm run build

print_status "Setting up admin dashboard..."
cd ../zimmermanagement/zimmer-admin-dashboard
npm install
npm run build

print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/zimmer-platform > /dev/null << 'EOF'
# Upstream definitions
upstream zimmer_backend {
    server 127.0.0.1:8000;
}

upstream zimmer_user_panel {
    server 127.0.0.1:3000;
}

upstream zimmer_admin_dashboard {
    server 127.0.0.1:3001;
}

# Main server block
server {
    listen 80;
    server_name zimmerai.com www.zimmerai.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name zimmerai.com www.zimmerai.com;

    # SSL Configuration (will be updated by certbot)
    ssl_certificate /etc/letsencrypt/live/zimmerai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/zimmerai.com/privkey.pem;

    # User Panel (Main Site)
    location / {
        proxy_pass http://zimmer_user_panel;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://zimmer_backend;
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

# Admin Dashboard
server {
    listen 443 ssl http2;
    server_name admin.zimmerai.com;

    # SSL Configuration (will be updated by certbot)
    ssl_certificate /etc/letsencrypt/live/zimmerai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/zimmerai.com/privkey.pem;

    location / {
        proxy_pass http://zimmer_admin_dashboard;
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
EOF

sudo ln -sf /etc/nginx/sites-available/zimmer-platform /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 8000/tcp
sudo ufw deny 3000/tcp
sudo ufw deny 3001/tcp

print_status "Starting applications with PM2..."
cd $DEPLOY_DIR/zimmer-platform-final

# Start backend
cd zimmer-backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name zimmer-backend

# Start user panel
cd ../zimmer_user_panel
pm2 start "npm start" --name zimmer-user-panel

# Start admin dashboard
cd ../zimmermanagement/zimmer-admin-dashboard
pm2 start "npm start" --name zimmer-admin-dashboard

# Save PM2 configuration
pm2 save
pm2 startup

print_status "Setting up SSL certificates..."
print_warning "You need to update the domain names in the Nginx configuration first!"
print_warning "Replace 'zimmerai.com' and 'admin.zimmerai.com' with your actual domains."
print_warning "Then run: sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d admin.yourdomain.com"

print_success "Deployment completed successfully!"
print_status "Next steps:"
echo "1. Update domain names in Nginx configuration"
echo "2. Obtain SSL certificates with certbot"
echo "3. Update environment variables with your actual API keys"
echo "4. Test all applications"
echo "5. Set up monitoring and backups"

print_status "Application URLs:"
echo "- User Panel: http://$DOMAIN_NAME (will redirect to HTTPS after SSL setup)"
echo "- Admin Dashboard: http://$ADMIN_DOMAIN (will redirect to HTTPS after SSL setup)"
echo "- API Backend: http://$DOMAIN_NAME/api/"

print_status "PM2 Status:"
pm2 status

print_success "🎉 Zimmer AI Platform deployment completed!"
