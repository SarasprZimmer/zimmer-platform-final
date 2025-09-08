#!/usr/bin/env python3
"""
Comprehensive Missing Items Test 2025
Tests for missing components, endpoints, and features after recent improvements
"""

import os
import sys
import time
import requests
import json
from pathlib import Path
from datetime import datetime

def test_backend_endpoints():
    """Test backend API endpoints"""
    print("🔍 Testing Backend Endpoints...")
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        # Auth endpoints
        ("/api/auth/login", "POST"),
        ("/api/auth/logout", "POST"),
        ("/api/auth/refresh", "POST"),
        ("/api/auth/csrf", "GET"),
        ("/api/auth/2fa/status", "GET"),
        ("/api/auth/request-email-verify", "POST"),
        
        # User endpoints
        ("/api/me", "GET"),
        ("/api/user/profile", "PUT"),
        ("/api/user/password", "POST"),
        ("/api/user/usage", "GET"),
        ("/api/user/usage/distribution", "GET"),
        ("/api/user/automations/active", "GET"),
        ("/api/user/payments", "GET"),
        ("/api/user/payments/summary", "GET"),
        
        # Optimized endpoints
        ("/api/optimized/me", "GET"),
        ("/api/optimized/user/dashboard", "GET"),
        ("/api/optimized/automations/marketplace", "GET"),
        ("/api/optimized/admin/dashboard", "GET"),
        ("/api/optimized/cache/stats", "GET"),
        
        # Admin endpoints
        ("/api/admin/users", "GET"),
        ("/api/admin/automations", "GET"),
        ("/api/admin/payments", "GET"),
        ("/api/admin/notifications", "GET"),
        ("/api/admin/tickets", "GET"),
        
        # Notifications
        ("/api/notifications", "GET"),
        ("/api/notifications/unread-count", "GET"),
        ("/api/notifications/mark-read", "POST"),
        ("/api/notifications/mark-all-read", "POST"),
        ("/api/notifications/stream", "GET"),
        
        # Support/Tickets
        ("/api/support/tickets", "GET"),
        ("/api/support/tickets", "POST"),
        
        # Automations
        ("/api/automations", "GET"),
        ("/api/automations/marketplace", "GET"),
        
        # Payments
        ("/api/payments/create", "POST"),
        ("/api/payments/verify", "POST"),
    ]
    
    results = {"working": [], "missing": [], "errors": []}
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code in [200, 401, 422]:  # 401/422 are expected for unauthenticated requests
                results["working"].append(endpoint)
                print(f"  ✅ {endpoint}: {response.status_code}")
            else:
                results["missing"].append(endpoint)
                print(f"  ❌ {endpoint}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            results["errors"].append(endpoint)
            print(f"  🔴 {endpoint}: Connection Error")
        except Exception as e:
            results["errors"].append(endpoint)
            print(f"  🔴 {endpoint}: {str(e)}")
    
    return results

def test_frontend_pages():
    """Test frontend pages"""
    print("\n🔍 Testing Frontend Pages...")
    
    base_url = "http://127.0.0.1:3000"
    pages = [
        "/",
        "/login",
        "/signup",
        "/dashboard",
        "/settings",
        "/notifications",
        "/usage",
        "/payment",
        "/payment/receipt",
        "/automations",
        "/automations/marketplace",
        "/support",
        "/forgot-password",
        "/reset-password",
        "/verify-email",
    ]
    
    results = {"working": [], "missing": [], "errors": []}
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}", timeout=10)
            
            if response.status_code == 200:
                results["working"].append(page)
                print(f"  ✅ {page}: {response.status_code}")
            else:
                results["missing"].append(page)
                print(f"  ❌ {page}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            results["errors"].append(page)
            print(f"  🔴 {page}: Connection Error")
        except Exception as e:
            results["errors"].append(page)
            print(f"  🔴 {page}: {str(e)}")
    
    return results

def test_admin_panel_pages():
    """Test admin panel pages"""
    print("\n🔍 Testing Admin Panel Pages...")
    
    base_url = "http://127.0.0.1:3001"
    pages = [
        "/",
        "/login",
        "/users",
        "/automations",
        "/payments",
        "/notifications",
        "/tickets",
        "/usage",
        "/knowledge",
        "/discounts",
        "/api-keys",
        "/backups",
        "/kb-monitoring",
        "/kb-templates",
        "/fallbacks",
        "/user-automations",
        "/tokens/adjustments",
    ]
    
    results = {"working": [], "missing": [], "errors": []}
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}", timeout=10)
            
            if response.status_code == 200:
                results["working"].append(page)
                print(f"  ✅ {page}: {response.status_code}")
            else:
                results["missing"].append(page)
                print(f"  ❌ {page}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            results["errors"].append(page)
            print(f"  🔴 {page}: Connection Error")
        except Exception as e:
            results["errors"].append(page)
            print(f"  🔴 {page}: {str(e)}")
    
    return results

def check_file_structure():
    """Check file structure and components"""
    print("\n🔍 Checking File Structure...")
    
    required_files = {
        "Backend": [
            "zimmer-backend/main.py",
            "zimmer-backend/database.py",
            "zimmer-backend/models/",
            "zimmer-backend/routers/",
            "zimmer-backend/schemas/",
            "zimmer-backend/services/",
            "zimmer-backend/utils/",
        ],
        "User Panel": [
            "zimmer_user_panel/pages/",
            "zimmer_user_panel/components/",
            "zimmer_user_panel/lib/",
            "zimmer_user_panel/contexts/",
            "zimmer_user_panel/hooks/",
        ],
        "Admin Panel": [
            "zimmermanagement/zimmer-admin-dashboard/pages/",
            "zimmermanagement/zimmer-admin-dashboard/components/",
            "zimmermanagement/zimmer-admin-dashboard/lib/",
            "zimmermanagement/zimmer-admin-dashboard/contexts/",
        ]
    }
    
    results = {"existing": [], "missing": []}
    
    for category, files in required_files.items():
        print(f"\n  📁 {category}:")
        for file_path in files:
            if os.path.exists(file_path):
                results["existing"].append(file_path)
                print(f"    ✅ {file_path}")
            else:
                results["missing"].append(file_path)
                print(f"    ❌ {file_path}")
    
    return results

def check_recent_improvements():
    """Check for recently added features"""
    print("\n🔍 Checking Recent Improvements...")
    
    recent_features = {
        "Usage Analytics": [
            "zimmer-backend/schemas/usage.py",
            "zimmer-backend/services/usage.py",
            "zimmer-backend/routers/user_usage.py",
            "zimmer_user_panel/pages/usage/index.tsx",
        ],
        "Billing System": [
            "zimmer-backend/schemas/billing_user.py",
            "zimmer-backend/services/billing_user.py",
            "zimmer-backend/routers/user_billing.py",
            "zimmer_user_panel/pages/payment/receipt.tsx",
        ],
        "Settings System": [
            "zimmer_user_panel/components/settings/ProfileForm.tsx",
            "zimmer_user_panel/components/settings/ChangePasswordForm.tsx",
            "zimmer_user_panel/components/settings/SecurityStatus.tsx",
        ],
        "Notifications System": [
            "zimmer_user_panel/lib/notifications.ts",
            "zimmer_user_panel/components/notifications/NotificationsBell.tsx",
            "zimmer_user_panel/pages/notifications/index.tsx",
            "zimmer_user_panel/pages/notifications/sse-check.tsx",
        ],
        "UI Components": [
            "zimmer_user_panel/components/ui/Kit.tsx",
        ]
    }
    
    results = {"implemented": [], "missing": []}
    
    for feature, files in recent_features.items():
        print(f"\n  🚀 {feature}:")
        feature_complete = True
        for file_path in files:
            if os.path.exists(file_path):
                results["implemented"].append(file_path)
                print(f"    ✅ {file_path}")
            else:
                results["missing"].append(file_path)
                feature_complete = False
                print(f"    ❌ {file_path}")
        
        if feature_complete:
            print(f"    🎉 {feature} - FULLY IMPLEMENTED")
        else:
            print(f"    ⚠️  {feature} - PARTIALLY IMPLEMENTED")
    
    return results

def check_database_tables():
    """Check database tables"""
    print("\n🔍 Checking Database Tables...")
    
    try:
        import sqlite3
        db_path = "zimmer_dashboard.db"
        
        if not os.path.exists(db_path):
            print("  ❌ Database file not found")
            return {"tables": [], "error": "Database file not found"}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"  📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"    ✅ {table}")
        
        conn.close()
        return {"tables": tables, "error": None}
        
    except Exception as e:
        print(f"  🔴 Database error: {str(e)}")
        return {"tables": [], "error": str(e)}

def generate_report(backend_results, frontend_results, admin_results, file_results, improvement_results, db_results):
    """Generate comprehensive report"""
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE MISSING ITEMS REPORT 2025")
    print("="*60)
    
    # Backend Status
    print(f"\n🔧 BACKEND STATUS:")
    print(f"  ✅ Working Endpoints: {len(backend_results['working'])}")
    print(f"  ❌ Missing Endpoints: {len(backend_results['missing'])}")
    print(f"  🔴 Error Endpoints: {len(backend_results['errors'])}")
    
    if backend_results['missing']:
        print(f"\n  Missing Backend Endpoints:")
        for endpoint in backend_results['missing']:
            print(f"    - {endpoint}")
    
    # Frontend Status
    print(f"\n🎨 USER PANEL STATUS:")
    print(f"  ✅ Working Pages: {len(frontend_results['working'])}")
    print(f"  ❌ Missing Pages: {len(frontend_results['missing'])}")
    print(f"  🔴 Error Pages: {len(frontend_results['errors'])}")
    
    if frontend_results['missing']:
        print(f"\n  Missing User Panel Pages:")
        for page in frontend_results['missing']:
            print(f"    - {page}")
    
    # Admin Panel Status
    print(f"\n👑 ADMIN PANEL STATUS:")
    print(f"  ✅ Working Pages: {len(admin_results['working'])}")
    print(f"  ❌ Missing Pages: {len(admin_results['missing'])}")
    print(f"  🔴 Error Pages: {len(admin_results['errors'])}")
    
    if admin_results['missing']:
        print(f"\n  Missing Admin Panel Pages:")
        for page in admin_results['missing']:
            print(f"    - {page}")
    
    # File Structure Status
    print(f"\n📁 FILE STRUCTURE STATUS:")
    print(f"  ✅ Existing Files: {len(file_results['existing'])}")
    print(f"  ❌ Missing Files: {len(file_results['missing'])}")
    
    # Recent Improvements Status
    print(f"\n🚀 RECENT IMPROVEMENTS STATUS:")
    print(f"  ✅ Implemented Files: {len(improvement_results['implemented'])}")
    print(f"  ❌ Missing Files: {len(improvement_results['missing'])}")
    
    # Database Status
    print(f"\n🗄️  DATABASE STATUS:")
    if db_results['error']:
        print(f"  🔴 Error: {db_results['error']}")
    else:
        print(f"  ✅ Tables: {len(db_results['tables'])}")
        print(f"  📊 Tables: {', '.join(db_results['tables'])}")
    
    # Overall Completion
    total_endpoints = len(backend_results['working']) + len(backend_results['missing']) + len(backend_results['errors'])
    total_pages = len(frontend_results['working']) + len(frontend_results['missing']) + len(frontend_results['errors'])
    total_admin_pages = len(admin_results['working']) + len(admin_results['missing']) + len(admin_results['errors'])
    
    backend_completion = (len(backend_results['working']) / total_endpoints * 100) if total_endpoints > 0 else 0
    frontend_completion = (len(frontend_results['working']) / total_pages * 100) if total_pages > 0 else 0
    admin_completion = (len(admin_results['working']) / total_admin_pages * 100) if total_admin_pages > 0 else 0
    
    print(f"\n📈 OVERALL COMPLETION:")
    print(f"  🔧 Backend: {backend_completion:.1f}%")
    print(f"  🎨 User Panel: {frontend_completion:.1f}%")
    print(f"  👑 Admin Panel: {admin_completion:.1f}%")
    
    overall_completion = (backend_completion + frontend_completion + admin_completion) / 3
    print(f"  🎯 Overall: {overall_completion:.1f}%")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if backend_results['errors']:
        print("  - Start backend server to fix connection errors")
    if frontend_results['errors']:
        print("  - Start user panel server to fix connection errors")
    if admin_results['errors']:
        print("  - Start admin panel server to fix connection errors")
    if improvement_results['missing']:
        print("  - Complete missing recent improvements")
    if file_results['missing']:
        print("  - Create missing file structure")
    
    print(f"\n✅ Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main test function"""
    print("🚨 Comprehensive Missing Items Test 2025")
    print("="*50)
    
    # Test backend endpoints
    backend_results = test_backend_endpoints()
    
    # Test frontend pages
    frontend_results = test_frontend_pages()
    
    # Test admin panel pages
    admin_results = test_admin_panel_pages()
    
    # Check file structure
    file_results = check_file_structure()
    
    # Check recent improvements
    improvement_results = check_recent_improvements()
    
    # Check database
    db_results = check_database_tables()
    
    # Generate comprehensive report
    generate_report(backend_results, frontend_results, admin_results, file_results, improvement_results, db_results)
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    main()
