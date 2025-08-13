# 🚀 Zimmer Environment Setup Guide

This guide will help you set up the environment configuration files for all three applications in the Zimmer system.

## 📁 What are Environment Files?

Environment files (`.env`, `.env.local`) contain configuration variables that are specific to your environment. They allow you to:
- Configure API URLs
- Set secret keys for authentication
- Configure database connections
- Set development/production settings
- Keep sensitive information out of your code

## 🛠️ Quick Setup

### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
setup-env.bat
```

**For Linux/Mac:**
```bash
chmod +x setup-env.sh
./setup-env.sh
```

### Option 2: Manual Setup

If you prefer to create the files manually, follow these steps:

#### 1. Backend Environment (zimmer-backend/.env)
```bash
cp zimmer-backend/env.example zimmer-backend/.env
```

#### 2. User Panel Environment (zimmer_user_panel/.env.local)
```bash
cp zimmer_user_panel/env.example zimmer_user_panel/.env.local
```

#### 3. Admin Dashboard Environment (zimmermanagement/zimmer-admin-dashboard/.env.local)
```bash
cp zimmermanagement/zimmer-admin-dashboard/env.example zimmermanagement/zimmer-admin-dashboard/.env.local
```

## ⚙️ Configuration Variables

### 🔑 Critical Variables (Must Match Across Applications)

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `JWT_SECRET_KEY` | Secret key for JWT token signing | `your-super-secret-jwt-key-change-this-in-production` |
| `NEXT_PUBLIC_API_URL` | Backend API URL for frontends | `http://localhost:8000` |

### 🏗️ Backend Variables (zimmer-backend/.env)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./zimmer_dashboard.db` | ✅ |
| `JWT_SECRET_KEY` | JWT signing secret | - | ✅ |
| `HOST` | Server host | `0.0.0.0` | ❌ |
| `PORT` | Server port | `8000` | ❌ |
| `DEBUG` | Enable debug mode | `true` | ❌ |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://localhost:3001` | ❌ |

### 🎨 Frontend Variables (Both .env.local files)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` | ✅ |
| `NODE_ENV` | Environment mode | `development` | ❌ |

## 🔒 Security Best Practices

### 1. JWT Secret Key
- **Never** use the default value in production
- Use a strong, random string (at least 32 characters)
- Keep it secret and never commit it to version control
- Use the same value across all applications

### 2. Environment File Security
- `.env` and `.env.local` files are automatically ignored by git
- Never commit these files to version control
- Share configuration through example files (`.env.example`)

### 3. Production Deployment
- Use different values for development and production
- Consider using environment variables from your hosting platform
- Rotate secrets regularly

## 🚀 Starting the Applications

After setting up your environment files:

### 1. Start the Backend
```bash
cd zimmer-backend
python main.py
```
The API will be available at `http://localhost:8000`

### 2. Start the User Panel
```bash
cd zimmer_user_panel
npm run dev
```
The user panel will be available at `http://localhost:3000`

### 3. Start the Admin Dashboard
```bash
cd zimmermanagement/zimmer-admin-dashboard
npm run dev
```
The admin dashboard will be available at `http://localhost:3001`

## 🔍 Troubleshooting

### Common Issues

#### 1. "JWT_SECRET_KEY not found"
- Make sure you've created the `.env` file in the backend
- Ensure the variable name is exactly `JWT_SECRET_KEY`

#### 2. "API connection failed"
- Check that `NEXT_PUBLIC_API_URL` is correct in both frontend `.env.local` files
- Ensure the backend is running on the specified port
- Check CORS configuration in the backend

#### 3. "Authentication failed"
- Verify that `JWT_SECRET_KEY` is identical across all applications
- Check that the backend is properly configured

#### 4. "Environment variables not loading"
- Make sure you're using `.env.local` for Next.js applications
- Restart your development servers after changing environment files
- Check that variable names start with `NEXT_PUBLIC_` for client-side access

### Debug Mode

To enable debug logging, add this to your backend `.env`:
```
LOG_LEVEL=debug
DEBUG=true
```

## 📋 Environment File Templates

### Backend (.env)
```env
DATABASE_URL=sqlite:///./zimmer_dashboard.db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://zimmerai.com
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

## 🎯 Next Steps

1. ✅ Set up environment files
2. 🔧 Configure your specific values
3. 🚀 Start all applications
4. 🧪 Test the authentication flow
5. 📚 Review the API documentation at `http://localhost:8000/docs`

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all environment variables are set correctly
3. Ensure all applications are running on the correct ports
4. Check the browser console and backend logs for error messages 