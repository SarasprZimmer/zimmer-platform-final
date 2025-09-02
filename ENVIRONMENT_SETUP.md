# 🚀 Environment Setup Guide

## Overview

This guide explains how to set up environment variables for the Zimmer platform. We've simplified the configuration to use **only one `.env` file per directory** for clarity and consistency.

## 📁 Environment File Structure

Each service now has **exactly one environment file**:

```
zimmer-full-structure/
├── zimmer-backend/
│   └── .env                    # Backend configuration
├── zimmermanagement/zimmer-admin-dashboard/
│   └── .env                    # Admin dashboard configuration
└── zimmer_user_panel/
    └── .env                    # User panel configuration
```

## 🔧 Setup Instructions

### 1. Backend Environment (zimmer-backend/.env)

```bash
# Navigate to backend directory
cd zimmer-backend

# Copy the template and rename it
cp env.backend .env

# Edit the .env file with your configuration
```

**Required Variables:**
```env
# Database Configuration
DATABASE_URL=sqlite:///./zimmer_dashboard.db

# JWT Configuration (REQUIRED)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# OpenAI Key Encryption (REQUIRED)
OAI_ENCRYPTION_SECRET=your_32_byte_base64_urlsafe_encryption_key_here
```

### 2. Admin Dashboard Environment (zimmermanagement/zimmer-admin-dashboard/.env)

```bash
# Navigate to admin dashboard directory
cd zimmermanagement/zimmer-admin-dashboard

# Copy the template and rename it
cp env.admin .env

# Edit the .env file with your configuration
```

**Required Variables:**
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Development Settings
NODE_ENV=development
```

### 3. User Panel Environment (zimmer_user_panel/.env)

```bash
# Navigate to user panel directory
cd zimmer_user_panel

# Copy the template and rename it
cp env.user .env

# Edit the .env file with your configuration
```

**Required Variables:**
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 🔑 Generating Secure Keys

### JWT Secret Key
```bash
# Generate a secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### OpenAI Encryption Key
```bash
# Generate a secure encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 🌍 Environment-Specific Configuration

### Development
- Use `localhost` URLs for all services
- Set `DEBUG=true` in backend
- Set `NODE_ENV=development` in frontend

### Production
- Use production domain URLs
- Set `DEBUG=false` in backend
- Set `NODE_ENV=production` in frontend
- Use HTTPS URLs for all services

## ✅ Verification Steps

After setting up the environment files:

1. **Backend**: Start and check logs for configuration errors
2. **Admin Dashboard**: Check browser console for API URL loading
3. **User Panel**: Verify API calls are working

## 🚫 What We Removed

We've cleaned up the confusing environment file structure by removing:
- ❌ `env.example` files
- ❌ `env.production` files
- ❌ `.env.local` files
- ❌ `.env.template` files

Now each service has **only one `.env` file** for simplicity.

## 🔍 Troubleshooting

### Common Issues

1. **"Environment variable not found"**
   - Make sure you've renamed the template file to `.env`
   - Check that the file is in the correct directory

2. **"API URL not loading"**
   - Verify `NEXT_PUBLIC_API_URL` is set correctly
   - Restart the frontend service after changes

3. **"CORS errors"**
   - Check that `ALLOWED_ORIGINS` includes your frontend URLs
   - Restart the backend after changes

### Debug Mode

To enable debug logging, add this to your backend `.env`:
```env
DEBUG=true
LOG_LEVEL=debug
```

## 📚 Related Documentation

- [Quick Start Guide](../README.md)
- [Backend Setup](../zimmer-backend/README.md)
- [Admin Dashboard Setup](../zimmermanagement/zimmer-admin-dashboard/README.md)
- [User Panel Setup](../zimmer_user_panel/README.md) 