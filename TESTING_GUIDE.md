# Zimmer System Testing Guide

This guide covers all the testing scripts and procedures for the Zimmer system, including the new discount system, 2FA, email verification, and purchase functionality.

## 🚀 Quick Start

### Run All Tests
```powershell
.\run_all_tests.ps1
```

### Quick Health Check
```powershell
.\quick_test.ps1
```

## 📋 Test Scripts Overview

### 1. Master Test Runner (`run_all_tests.ps1`)
**Purpose**: Comprehensive test suite that runs all other tests
**Coverage**: 
- Backend smoke tests
- Admin dashboard tests
- API endpoints tests
- Frontend components tests
- E2E tests
- Component-specific tests

**Usage**:
```powershell
.\run_all_tests.ps1
```

### 2. Quick Test (`quick_test.ps1`)
**Purpose**: Rapid health check for essential components
**Coverage**:
- Backend health
- Build status
- Critical files
- Authentication
- Discount system

**Usage**:
```powershell
.\quick_test.ps1
```

### 3. Backend Smoke Test (`ops/smoke/smoke_backend.ps1`)
**Purpose**: Backend infrastructure and core functionality
**Coverage**:
- Python environment
- Dependencies installation
- Database migrations
- Migration drift check
- Constraint validation
- Core pytest tests including:
  - Health checks
  - Authentication flow
  - User profile/password
  - Payments (sandbox)
  - Notifications
  - Admin notifications
  - Migration guards
  - **NEW**: Discount system tests
  - **NEW**: 2FA tests
  - **NEW**: Email verification tests

**Usage**:
```powershell
.\ops\smoke\smoke_backend.ps1
```

### 4. Admin Dashboard Smoke Test (`ops/smoke/smoke_admin_dashboard.ps1`)
**Purpose**: Admin dashboard build and file structure
**Coverage**:
- Node.js environment
- Dependencies installation
- Build process
- Critical files including:
  - Core components
  - **NEW**: Discount pages and components
  - Configuration files
- Environment configuration

**Usage**:
```powershell
.\ops\smoke\smoke_admin_dashboard.ps1
```

### 5. API Endpoints Test (`ops/smoke/api_endpoints_comprehensive_test.ps1`)
**Purpose**: Comprehensive API endpoint testing
**Coverage**:
- Health and system endpoints
- Authentication endpoints
- Admin endpoints
- **NEW**: Discount system endpoints
- Payment endpoints
- User panel endpoints
- **NEW**: 2FA and security endpoints

**Usage**:
```powershell
.\ops\smoke\api_endpoints_comprehensive_test.ps1
```

### 6. Frontend Components Test (`ops/smoke/frontend_components_test.ps1`)
**Purpose**: Frontend components and pages validation
**Coverage**:
- Admin dashboard components
- User panel components
- **NEW**: Discount system components
- **NEW**: 2FA components
- **NEW**: Purchase system components
- Configuration files
- Build tests

**Usage**:
```powershell
.\ops\smoke\frontend_components_test.ps1
```

### 7. Comprehensive E2E Test (`comprehensive_e2e_test.ps1`)
**Purpose**: End-to-end system integration testing
**Coverage**:
- Backend health and API
- Admin dashboard build and config
- User panel build and config
- Database schema
- Payment gateway configuration
- **NEW**: Discount system files
- **NEW**: 2FA system files
- **NEW**: Email verification files
- **NEW**: Purchase system files

**Usage**:
```powershell
.\comprehensive_e2e_test.ps1
```

## 🎯 Test Coverage by Component

### Backend Components
- ✅ **Authentication System**: Login, signup, refresh, logout
- ✅ **Admin Endpoints**: Users, automations, payments, tickets, usage, backups, notifications, fallbacks, knowledge, API keys, token adjustments
- ✅ **Discount System**: CRUD operations, validation, redemptions
- ✅ **2FA System**: Initiate, activate, disable, recovery codes
- ✅ **Email Verification**: Token generation and validation
- ✅ **Payment Gateway**: Zarinpal integration, init, callback
- ✅ **Database**: Schema validation, migrations, constraints

### Frontend Components

#### Admin Dashboard
- ✅ **Core Components**: Layout, Sidebar, Topbar, ProtectedRoute, ErrorBoundary, Toast, LoadingSkeletons, ResponsiveTable, MobileBottomNav
- ✅ **NEW**: DiscountForm component
- ✅ **Pages**: All existing pages plus new discount pages (list, create, edit, redemptions)
- ✅ **Authentication**: Login, protected routes
- ✅ **API Integration**: All admin endpoints

#### User Panel
- ✅ **Core Components**: DashboardLayout, Sidebar, Topbar, ProtectedRoute, ClientAuthProvider, Toast, PurchaseModal, PaymentLoading, HeaderAuth
- ✅ **NEW**: TwoFADialog component
- ✅ **NEW**: DiscountCodeField component
- ✅ **NEW**: PriceSummary component
- ✅ **Pages**: All existing pages plus new security settings and purchase pages
- ✅ **Authentication**: Login, signup, 2FA, email verification
- ✅ **NEW**: Purchase flow with discount support

## 🔧 Prerequisites

### Backend Requirements
- Python 3.8+
- pip packages from `requirements.txt`
- Database (SQLite for testing)
- Backend server running on port 8000

### Frontend Requirements
- Node.js 16+
- npm packages installed
- Environment files configured

### Test Environment
- PowerShell 5.1+ (Windows)
- Internet connection for package downloads
- Sufficient disk space for builds

## 📊 Test Results Interpretation

### Status Codes
- **PASS** ✅: Test completed successfully
- **FAIL** ❌: Test failed, needs attention
- **WARNING** ⚠️: Test passed with warnings
- **ERROR** 💥: Test encountered an error

### Success Criteria
- **Excellent**: All tests PASS, no failures or errors
- **Good**: No critical failures, some warnings acceptable
- **Needs Attention**: Critical failures detected, system may not be fully operational

## 🚨 Troubleshooting

### Common Issues

#### Backend Not Running
```
❌ Backend health check failed
💡 Make sure the backend server is running on port 8000
```
**Solution**: Start the backend server:
```powershell
cd zimmer-backend
uvicorn main:app --reload
```

#### Build Failures
```
❌ Admin dashboard build failed
```
**Solution**: Check for TypeScript errors, missing dependencies, or configuration issues.

#### Missing Files
```
❌ Some component files missing
```
**Solution**: Ensure all new components have been created and are in the correct locations.

#### Authentication Failures
```
❌ Authentication test failed
```
**Solution**: Check database seeding, ensure test users exist, verify JWT configuration.

## 📈 Continuous Integration

### Automated Testing
These scripts can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Zimmer Tests
  run: |
    .\run_all_tests.ps1
```

### Scheduled Testing
Set up regular test runs to ensure system health:
```powershell
# Daily health check
.\quick_test.ps1

# Weekly comprehensive test
.\run_all_tests.ps1
```

## 🔄 Test Maintenance

### Adding New Tests
1. Create test file in appropriate directory
2. Add to relevant test runner
3. Update this documentation
4. Test the new test script

### Updating Existing Tests
1. Modify test script
2. Test the changes
3. Update documentation if needed
4. Verify integration with master test runner

## 📞 Support

For issues with testing:
1. Check the troubleshooting section above
2. Review test output for specific error messages
3. Ensure all prerequisites are met
4. Verify system components are properly installed and configured

---

**Last Updated**: September 2025
**Version**: 2.0 (includes discount system, 2FA, email verification, and purchase functionality)
