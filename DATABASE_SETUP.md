# 🗄️ Database Setup Guide

This guide covers all your database hosting options for the Zimmer system.

## 🏠 **Self-Hosting Options**

### **1. SQLite (Current - Easiest)**
**Perfect for development and small projects**

**Pros:**
- ✅ No server setup required
- ✅ Zero configuration
- ✅ Database is just a file
- ✅ Perfect for development

**Cons:**
- ⚠️ Limited concurrent users
- ⚠️ Not ideal for high-traffic production

**Current Configuration:**
```env
DATABASE_URL=sqlite:///./zimmer_dashboard.db
```

### **2. PostgreSQL (Recommended for Production)**
**Best choice for self-hosted production**

**Pros:**
- ✅ Free and open-source
- ✅ Excellent performance
- ✅ Advanced features
- ✅ Great for concurrent users
- ✅ Easy to self-host

**Cons:**
- ⚠️ Requires server setup
- ⚠️ More complex than SQLite

## 🚀 **Self-Hosting Setup Methods**

### **Method 1: Docker Compose (Recommended)**

**Step 1: Install Docker**
- Download from [docker.com](https://docker.com)
- Install Docker Desktop

**Step 2: Update your backend .env file**
```env
DATABASE_URL=postgresql://zimmer_user:your_secure_password_here@localhost:5432/zimmer_dashboard
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENVIRONMENT=development
```

**Step 3: Start the database**
```bash
# Start only the database
docker-compose up postgres -d

# Or start everything (database + backend)
docker-compose up -d
```

**Step 4: Run database migrations**
```bash
cd zimmer-backend
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### **Method 2: Local PostgreSQL Installation**

**Windows:**
1. Download PostgreSQL from [postgresql.org](https://postgresql.org/download/windows/)
2. Install with default settings
3. Create database and user:
```sql
CREATE DATABASE zimmer_dashboard;
CREATE USER zimmer_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE zimmer_dashboard TO zimmer_user;
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser zimmer_user
sudo -u postgres createdb zimmer_dashboard
sudo -u postgres psql -c "ALTER USER zimmer_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE zimmer_dashboard TO zimmer_user;"
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
createdb zimmer_dashboard
createuser zimmer_user
psql -c "ALTER USER zimmer_user WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE zimmer_dashboard TO zimmer_user;"
```

### **Method 3: VPS (Virtual Private Server)**

**Popular VPS Providers:**
- **DigitalOcean** - $5-10/month
- **Linode** - $5-10/month  
- **Vultr** - $5-10/month
- **Hetzner** - €3-5/month

**Setup Steps:**
1. Rent a VPS
2. Install PostgreSQL on the VPS
3. Configure firewall and security
4. Connect your applications to the remote database

## 🔧 **Database Configuration**

### **Environment Variables**

| Variable | SQLite | PostgreSQL | Description |
|----------|--------|------------|-------------|
| `DATABASE_URL` | `sqlite:///./zimmer_dashboard.db` | `postgresql://user:pass@host:port/db` | Database connection string |
| `DB_HOST` | - | `localhost` | Database host |
| `DB_PORT` | - | `5432` | Database port |
| `DB_NAME` | - | `zimmer_dashboard` | Database name |
| `DB_USER` | - | `zimmer_user` | Database user |
| `DB_PASSWORD` | - | `your_password` | Database password |

### **Connection String Formats**

**SQLite:**
```
sqlite:///./zimmer_dashboard.db
```

**PostgreSQL:**
```
postgresql://username:password@host:port/database_name
```

**Example:**
```
postgresql://zimmer_user:mysecretpass@localhost:5432/zimmer_dashboard
```

## 🔒 **Security Best Practices**

### **1. Database Security**
- Use strong passwords
- Don't expose database port to internet
- Use SSL connections in production
- Regular backups
- Keep PostgreSQL updated

### **2. Environment Security**
- Never commit passwords to git
- Use environment variables
- Rotate passwords regularly
- Use different passwords for dev/prod

### **3. Network Security**
- Use firewall rules
- Limit database access to application servers
- Use VPN for remote access
- Monitor access logs

## 📊 **Performance Considerations**

### **SQLite vs PostgreSQL**

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Concurrent Users** | 1-10 | 1000+ |
| **Data Size** | Up to 100GB | Unlimited |
| **Complex Queries** | Limited | Excellent |
| **Backup** | File copy | pg_dump |
| **Replication** | No | Yes |
| **Setup Complexity** | None | Medium |

### **When to Use Each**

**Use SQLite when:**
- Development/testing
- Small projects (< 10 users)
- Simple data structure
- No concurrent writes needed

**Use PostgreSQL when:**
- Production applications
- Multiple concurrent users
- Complex queries needed
- Data integrity critical
- Future scalability important

## 🚀 **Migration from SQLite to PostgreSQL**

### **Step 1: Backup SQLite Data**
```bash
cp zimmer_dashboard.db zimmer_dashboard_backup.db
```

### **Step 2: Set up PostgreSQL**
Follow one of the setup methods above.

### **Step 3: Update Environment**
Change `DATABASE_URL` in your `.env` file.

### **Step 4: Run Migrations**
```bash
cd zimmer-backend
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### **Step 5: Test**
Verify all functionality works with the new database.

## 💰 **Cost Comparison**

### **Self-Hosting Costs**
- **VPS**: $5-20/month
- **Domain**: $10-15/year
- **SSL Certificate**: Free (Let's Encrypt)
- **Total**: ~$60-250/year

### **Cloud Database Costs**
- **Iranian Providers**: 500K-2M Toman/month
- **International**: $20-100/month
- **Total**: 6M-24M Toman/year or $240-1200/year

### **Self-Hosting Savings**
- **vs Iranian Providers**: 80-90% cheaper
- **vs International**: 60-80% cheaper

## 🎯 **Recommendation**

**For Development:**
- Stick with SQLite (current setup)

**For Production:**
- Use PostgreSQL with Docker Compose
- Self-host on a VPS
- Estimated cost: $60-120/year

**Migration Path:**
1. Start with SQLite (current)
2. Move to PostgreSQL when you have >10 users
3. Self-host to save costs

Would you like me to help you set up any specific database configuration? 