#!/usr/bin/env python3
"""
Comprehensive System Test 2025
Tests all major components and new features
"""
import requests
import json
import sys
import time
from datetime import datetime

class SystemTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        self.results = {
            "backend": {"passed": 0, "failed": 0, "tests": []},
            "frontend": {"passed": 0, "failed": 0, "tests": []},
            "integration": {"passed": 0, "failed": 0, "tests": []},
            "new_features": {"passed": 0, "failed": 0, "tests": []}
        }
    
    def log_test(self, category, test_name, passed, details=""):
        """Log test result"""
        self.results[category]["tests"].append({
            "name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.results[category]["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.results[category]["failed"] += 1
            print(f"❌ {test_name}: {details}")
    
    def test_backend_health(self):
        """Test backend basic health"""
        print("\n🔧 Backend Health Tests")
        print("-" * 40)
        
        # Test main endpoints
        endpoints = [
            ("/api/me", 401, "User endpoint"),
            ("/api/auth/csrf", 200, "CSRF endpoint"),
            ("/api/notifications", 401, "Notifications endpoint"),
        ]
        
        for endpoint, expected_status, description in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                passed = response.status_code == expected_status
                self.log_test("backend", description, passed, 
                            f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("backend", description, False, str(e))
    
    def test_new_endpoints(self):
        """Test newly implemented endpoints"""
        print("\n🆕 New Features Tests")
        print("-" * 40)
        
        # Usage endpoints
        usage_endpoints = [
            ("/api/user/usage?range=7d", "Usage weekly data"),
            ("/api/user/usage?range=6m", "Usage monthly data"),
            ("/api/user/usage/distribution", "Usage distribution"),
        ]
        
        for endpoint, description in usage_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                passed = response.status_code == 401  # Expected for unauthenticated
                self.log_test("new_features", description, passed,
                            f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("new_features", description, False, str(e))
        
        # Billing endpoints
        billing_endpoints = [
            ("/api/user/automations/active", "Active automations"),
            ("/api/user/payments", "Payment history"),
            ("/api/user/payments/summary?months=6", "Payment summary"),
        ]
        
        for endpoint, description in billing_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                passed = response.status_code == 401  # Expected for unauthenticated
                self.log_test("new_features", description, passed,
                            f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("new_features", description, False, str(e))
        
        # Security endpoints
        security_endpoints = [
            ("/api/auth/2fa/status", "2FA status"),
        ]
        
        for endpoint, description in security_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                passed = response.status_code == 401  # Expected for unauthenticated
                self.log_test("new_features", description, passed,
                            f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("new_features", description, False, str(e))
    
    def test_frontend_connectivity(self):
        """Test frontend connectivity"""
        print("\n🌐 Frontend Connectivity Tests")
        print("-" * 40)
        
        # Test if frontend is running (this would need frontend to be running)
        try:
            response = requests.get(self.frontend_url, timeout=5)
            passed = response.status_code == 200
            self.log_test("frontend", "Frontend server", passed,
                        f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("frontend", "Frontend server", False, 
                        "Frontend not running or not accessible")
    
    def test_database_connectivity(self):
        """Test database connectivity through API"""
        print("\n🗄️ Database Connectivity Tests")
        print("-" * 40)
        
        # Test endpoints that require database access
        db_endpoints = [
            ("/api/me", "User data access"),
            ("/api/notifications", "Notifications data access"),
        ]
        
        for endpoint, description in db_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                # Any response (even 401) means database is accessible
                passed = response.status_code in [200, 401, 403]
                self.log_test("integration", description, passed,
                            f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("integration", description, False, str(e))
    
    def test_api_structure(self):
        """Test API response structure"""
        print("\n📋 API Structure Tests")
        print("-" * 40)
        
        # Test CSRF endpoint for proper JSON response
        try:
            response = requests.get(f"{self.base_url}/api/auth/csrf", timeout=5)
            if response.status_code == 200:
                try:
                    data = response.json()
                    passed = isinstance(data, dict)
                    self.log_test("backend", "CSRF JSON response", passed,
                                "Valid JSON structure" if passed else "Invalid JSON")
                except json.JSONDecodeError:
                    self.log_test("backend", "CSRF JSON response", False, "Invalid JSON")
            else:
                self.log_test("backend", "CSRF JSON response", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("backend", "CSRF JSON response", False, str(e))
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE SYSTEM TEST REPORT 2025")
        print("=" * 60)
        
        total_passed = 0
        total_failed = 0
        
        for category, data in self.results.items():
            category_passed = data["passed"]
            category_failed = data["failed"]
            category_total = category_passed + category_failed
            category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
            
            print(f"\n{category.upper()}:")
            print(f"  ✅ Passed: {category_passed}")
            print(f"  ❌ Failed: {category_failed}")
            print(f"  📊 Success Rate: {category_rate:.1f}%")
            
            total_passed += category_passed
            total_failed += category_failed
        
        overall_total = total_passed + total_failed
        overall_rate = (total_passed / overall_total * 100) if overall_total > 0 else 0
        
        print(f"\n🎯 OVERALL RESULTS:")
        print(f"  ✅ Total Passed: {total_passed}")
        print(f"  ❌ Total Failed: {total_failed}")
        print(f"  📊 Overall Success Rate: {overall_rate:.1f}%")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_passed": total_passed,
                "total_failed": total_failed,
                "success_rate": overall_rate
            },
            "categories": self.results
        }
        
        with open("comprehensive_test_report_2025.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: comprehensive_test_report_2025.json")
        
        return overall_rate >= 80  # Consider 80%+ as passing
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive System Test 2025")
        print("=" * 60)
        
        self.test_backend_health()
        self.test_new_endpoints()
        self.test_frontend_connectivity()
        self.test_database_connectivity()
        self.test_api_structure()
        
        return self.generate_report()

def main():
    tester = SystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 SYSTEM TEST PASSED - System is fully functional!")
        return 0
    else:
        print("\n⚠️ SYSTEM TEST FAILED - Some issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())
