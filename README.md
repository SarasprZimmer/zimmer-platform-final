# Zimmer Full Structure Platform

A comprehensive AI automation management platform with admin dashboard, user panel, and backend API.

## 🚀 System Overview

The Zimmer platform consists of three main components:

- **Backend API** (FastAPI) - Core business logic and data management
- **Admin Dashboard** (Next.js) - Administrative interface for system management
- **User Panel** (Next.js) - User-facing interface for automation management

## 📊 Current Status

**Status**: ✅ FULLY OPERATIONAL  
**Last Updated**: January 3, 2025  
**Version**: Latest with authentication consistency fixes

### System Health
- ✅ Backend: Running on `http://127.0.0.1:8000`
- ✅ Admin Dashboard: Running on `http://localhost:3001`
- ✅ User Panel: Available for deployment
- ✅ Database: SQLite with proper schema
- ✅ Authentication: Fully functional
- ✅ All Endpoints: 18/18 admin endpoints working

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd zimmer-backend
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Admin Dashboard Setup
```bash
cd zimmermanagement/zimmer-admin-dashboard
npm install
npm run dev
```

### User Panel Setup
```bash
cd zimmer_user_panel
npm install
npm run dev
```

## 🔧 Recent Fixes (January 3, 2025)

### Authentication Consistency
- Standardized all authentication calls to use `authClient.getAccessToken()`
- Fixed token inconsistency across 8 frontend files
- Added proper import statements for auth client

### API Response Handling
- Fixed `automations.map is not a function` errors
- Added proper handling for nested API response structures
- Implemented safety checks for array operations

### Usage Page Fixes
- Updated to use correct `/api/admin/usage/stats` endpoint
- Fixed endpoint mismatch that was causing 404 errors
- Improved error handling and user experience

## 📁 Project Structure

```
zimmer-full-structure/
├── zimmer-backend/           # FastAPI backend
├── zimmermanagement/
│   └── zimmer-admin-dashboard/  # Admin dashboard
├── zimmer_user_panel/        # User panel
├── ops/                      # Operations scripts
├── scripts/                  # Utility scripts
└── docs/                     # Documentation
```

## 🔐 Authentication

The system uses JWT-based authentication with:
- Admin users for dashboard access
- Regular users for panel access
- Token-based API authentication
- Secure password reset functionality

## 📊 Key Features

### Admin Dashboard
- User management
- Automation monitoring
- KB (Knowledge Base) management
- Token usage tracking
- Payment management
- System notifications
- Backup management

### User Panel
- Automation creation and management
- Payment processing
- Dashboard analytics
- Settings management

### Backend API
- RESTful API endpoints
- Database management
- Authentication services
- Payment gateway integration (Zarinpal)
- File upload handling

## 🧪 Testing

### Smoke Tests
```bash
# Backend tests
cd ops/smoke
.\smoke_backend.ps1

# Admin dashboard tests
.\admin_endpoint_connectivity_test.ps1
```

### Build Tests
```bash
# Admin dashboard build
cd zimmermanagement/zimmer-admin-dashboard
npm run build
```

## 📚 Documentation

- [System Status Report](SYSTEM_STATUS_REPORT.md) - Current system status
- [Changelog](CHANGELOG.md) - Detailed change history
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment
- [Developer Quick Reference](DEVELOPER_QUICK_REFERENCE.md) - Development setup

## 🚨 Troubleshooting

### Common Issues
1. **Backend won't start**: Check if port 8000 is available
2. **Frontend build errors**: Run `npm install` and check for missing dependencies
3. **Authentication issues**: Verify backend is running and accessible
4. **Database errors**: Check SQLite file permissions and schema

### Getting Help
- Check the [System Status Report](SYSTEM_STATUS_REPORT.md) for current issues
- Review the [Changelog](CHANGELOG.md) for recent fixes
- Run smoke tests to verify system health

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

**Last Updated**: January 3, 2025  
**Maintainer**: Zimmer Development Team
