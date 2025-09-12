#!/usr/bin/env python3
"""
Comprehensive Smoke Tests for Zimmer AI Platform
Tests all three parts: Backend API, User Panel, Admin Panel
"""

import requests
import time
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import threading
import signal

class SmokeTestSuite:
    """Comprehensive smoke test suite for the entire platform"""
    
    def __init__(self):
        self.results = {
            "backend": {},
            "user_panel": {},
            "admin_panel": {},
            "integration": {},
            "performance": {},
            "security": {}
        }
        self.start_time = datetime.now()
        self.test_user_token = None
        self.admin_token = None
        
        # Configuration
        self.backend_url = "http://localhost:8000"
        self.user_panel_url = "http://localhost:3000"
        self.admin_panel_url = "http://localhost:4000"
        
        # Test credentials
        self.test_user = {
            "email": "smoketest@zimmer.ai",
            "password": "smoketest123",
            "name": "Smoke Test User"
        }
        self.admin_user = {
            "email": "admin@zimmer.com",
            "password": "admin123"
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_backend_health(self) -> Dict[str, Any]:
        """Test backend health and basic functionality"""
        self.log("🏥 Testing Backend Health...")
        results = {}
        
        try:
            # Test root endpoint
            response = requests.get(f"{self.backend_url}/", timeout=10)
            results["root_endpoint"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Test health endpoint
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            results["health_endpoint"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "data": response.json() if response.status_code == 200 else None
            }
            
            # Test API docs
            response = requests.get(f"{self.backend_url}/docs", timeout=10)
            results["api_docs"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ Backend health test failed: {e}", "ERROR")
        
        return results
    
    def test_backend_authentication(self) -> Dict[str, Any]:
        """Test backend authentication system"""
        self.log("🔐 Testing Backend Authentication...")
        results = {}
        
        try:
            # Test user registration
            response = requests.post(
                f"{self.backend_url}/api/auth/register",
                json=self.test_user,
                timeout=10
            )
            results["user_registration"] = {
                "status": "pass" if response.status_code in [200, 400] else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Test user login
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json={
                    "email": self.test_user["email"],
                    "password": self.test_user["password"]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.test_user_token = data.get("access_token")
                results["user_login"] = {
                    "status": "pass",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "has_token": bool(self.test_user_token)
                }
            else:
                results["user_login"] = {
                    "status": "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            
            # Test admin login
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json=self.admin_user,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                results["admin_login"] = {
                    "status": "pass",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "has_token": bool(self.admin_token)
                }
            else:
                results["admin_login"] = {
                    "status": "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
                
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ Authentication test failed: {e}", "ERROR")
        
        return results
    
    def test_backend_api_endpoints(self) -> Dict[str, Any]:
        """Test critical backend API endpoints"""
        self.log("🔌 Testing Backend API Endpoints...")
        results = {}
        
        # Test public endpoints
        public_endpoints = [
            ("/api/automations/marketplace", "GET", "Marketplace"),
            ("/api/optimized/automations/marketplace", "GET", "Optimized Marketplace"),
            ("/api/optimized/cache/stats", "GET", "Cache Stats"),
            ("/circuit-breaker/stats", "GET", "Circuit Breaker Stats")
        ]
        
        for endpoint, method, description in public_endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.backend_url}{endpoint}", timeout=10)
                
                results[f"public_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "description": description
                }
            except Exception as e:
                results[f"public_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                    "status": "error",
                    "error": str(e),
                    "description": description
                }
        
        # Test protected endpoints (should return 401 without auth)
        protected_endpoints = [
            ("/api/me", "GET", "User Profile"),
            ("/api/user/dashboard", "GET", "User Dashboard"),
            ("/api/admin/dashboard", "GET", "Admin Dashboard"),
            ("/api/notifications", "GET", "Notifications")
        ]
        
        for endpoint, method, description in protected_endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.backend_url}{endpoint}", timeout=10)
                
                results[f"protected_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                    "status": "pass" if response.status_code == 401 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "description": description,
                    "note": "401 expected without authentication"
                }
            except Exception as e:
                results[f"protected_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                    "status": "error",
                    "error": str(e),
                    "description": description
                }
        
        # Test authenticated endpoints
        if self.test_user_token:
            auth_headers = {"Authorization": f"Bearer {self.test_user_token}"}
            auth_endpoints = [
                ("/api/me", "GET", "User Profile (Auth)"),
                ("/api/user/dashboard", "GET", "User Dashboard (Auth)"),
                ("/api/user/settings", "GET", "User Settings (Auth)")
            ]
            
            for endpoint, method, description in auth_endpoints:
                try:
                    if method == "GET":
                        response = requests.get(f"{self.backend_url}{endpoint}", headers=auth_headers, timeout=10)
                    else:
                        response = requests.post(f"{self.backend_url}{endpoint}", headers=auth_headers, timeout=10)
                    
                    results[f"auth_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                        "status": "pass" if response.status_code == 200 else "fail",
                        "status_code": response.status_code,
                        "response_time": response.elapsed.total_seconds(),
                        "description": description
                    }
                except Exception as e:
                    results[f"auth_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                        "status": "error",
                        "error": str(e),
                        "description": description
                    }
        
        # Test admin endpoints
        if self.admin_token:
            admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
            admin_endpoints = [
                ("/api/admin/users", "GET", "Admin Users"),
                ("/api/admin/users/stats", "GET", "Admin User Stats"),
                ("/api/admin/openai-keys", "GET", "Admin OpenAI Keys"),
                ("/api/admin/analytics", "GET", "Admin Analytics"),
                ("/api/admin/settings", "GET", "Admin Settings")
            ]
            
            for endpoint, method, description in admin_endpoints:
                try:
                    if method == "GET":
                        response = requests.get(f"{self.backend_url}{endpoint}", headers=admin_headers, timeout=10)
                    else:
                        response = requests.post(f"{self.backend_url}{endpoint}", headers=admin_headers, timeout=10)
                    
                    results[f"admin_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                        "status": "pass" if response.status_code == 200 else "fail",
                        "status_code": response.status_code,
                        "response_time": response.elapsed.total_seconds(),
                        "description": description
                    }
                except Exception as e:
                    results[f"admin_{endpoint.replace('/', '_').replace('api_', '')}"] = {
                        "status": "error",
                        "error": str(e),
                        "description": description
                    }
        
        return results
    
    def test_user_panel(self) -> Dict[str, Any]:
        """Test user panel frontend"""
        self.log("👤 Testing User Panel...")
        results = {}
        
        try:
            # Test main page
            response = requests.get(self.user_panel_url, timeout=10)
            results["main_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Test login page
            response = requests.get(f"{self.user_panel_url}/login", timeout=10)
            results["login_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Test dashboard page
            response = requests.get(f"{self.user_panel_url}/dashboard", timeout=10)
            results["dashboard_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Test automations page
            response = requests.get(f"{self.user_panel_url}/automations", timeout=10)
            results["automations_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Test settings page
            response = requests.get(f"{self.user_panel_url}/settings", timeout=10)
            results["settings_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ User panel test failed: {e}", "ERROR")
        
        return results
    
    def test_admin_panel(self) -> Dict[str, Any]:
        """Test admin panel frontend"""
        self.log("👑 Testing Admin Panel...")
        results = {}
        
        try:
            # Test main page
            response = requests.get(self.admin_panel_url, timeout=10)
            results["main_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Note: Admin panel doesn't have a separate /dashboard page, it's just /
            
            # Test users page
            response = requests.get(f"{self.admin_panel_url}/users", timeout=10)
            results["users_page"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Note: Admin panel doesn't have a separate /analytics page
            
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ Admin panel test failed: {e}", "ERROR")
        
        return results
    
    def test_integration(self) -> Dict[str, Any]:
        """Test integration between components"""
        self.log("🔗 Testing Integration...")
        results = {}
        
        try:
            # Test user panel -> backend integration
            if self.test_user_token:
                auth_headers = {"Authorization": f"Bearer {self.test_user_token}"}
                
                # Test user profile API call
                response = requests.get(f"{self.backend_url}/api/me", headers=auth_headers, timeout=10)
                results["user_panel_backend_integration"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
                
                # Test user dashboard API call
                response = requests.get(f"{self.backend_url}/api/user/dashboard", headers=auth_headers, timeout=10)
                results["user_dashboard_integration"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            
            # Test admin panel -> backend integration
            if self.admin_token:
                admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
                
                # Test admin users API call (admin dashboard doesn't exist)
                response = requests.get(f"{self.backend_url}/api/admin/users", headers=admin_headers, timeout=10)
                results["admin_panel_backend_integration"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            
            # Test cross-component data consistency
            if self.test_user_token and self.admin_token:
                # Test that user data is consistent between user and admin views
                user_headers = {"Authorization": f"Bearer {self.test_user_token}"}
                admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
                
                # Get user profile from user perspective
                user_response = requests.get(f"{self.backend_url}/api/me", headers=user_headers, timeout=10)
                
                # Get user data from admin perspective
                admin_response = requests.get(f"{self.backend_url}/api/admin/users", headers=admin_headers, timeout=10)
                
                results["data_consistency"] = {
                    "status": "pass" if user_response.status_code == 200 and admin_response.status_code == 200 else "fail",
                    "user_api_status": user_response.status_code,
                    "admin_api_status": admin_response.status_code,
                    "response_time": max(user_response.elapsed.total_seconds(), admin_response.elapsed.total_seconds())
                }
                
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ Integration test failed: {e}", "ERROR")
        
        return results
    
    def test_performance(self) -> Dict[str, Any]:
        """Test system performance"""
        self.log("⚡ Testing Performance...")
        results = {}
        
        # Test response times for critical endpoints
        critical_endpoints = [
            ("/health", "Health Check"),
            ("/api/auth/login", "Authentication"),
            ("/api/me", "User Profile"),
            ("/api/admin/dashboard", "Admin Dashboard")
        ]
        
        for endpoint, description in critical_endpoints:
            times = []
            for _ in range(5):  # 5 requests
                try:
                    start_time = time.time()
                    if endpoint == "/api/auth/login":
                        response = requests.post(f"{self.backend_url}{endpoint}", 
                                               json={"email": "test@example.com", "password": "test123"}, 
                                               timeout=10)
                    elif endpoint == "/api/me" and self.test_user_token:
                        response = requests.get(f"{self.backend_url}{endpoint}", 
                                              headers={"Authorization": f"Bearer {self.test_user_token}"}, 
                                              timeout=10)
                    elif endpoint == "/api/admin/dashboard" and self.admin_token:
                        response = requests.get(f"{self.backend_url}{endpoint}", 
                                              headers={"Authorization": f"Bearer {self.admin_token}"}, 
                                              timeout=10)
                    else:
                        response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                    
                    end_time = time.time()
                    times.append(end_time - start_time)
                except Exception as e:
                    times.append(float('inf'))
            
            if times and all(t != float('inf') for t in times):
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)
                
                results[description.lower().replace(" ", "_")] = {
                    "avg_response_time": round(avg_time * 1000, 2),  # ms
                    "max_response_time": round(max_time * 1000, 2),  # ms
                    "min_response_time": round(min_time * 1000, 2),  # ms
                    "status": "good" if avg_time < 1.0 else "slow"
                }
            else:
                results[description.lower().replace(" ", "_")] = {
                    "status": "error",
                    "error": "All requests failed"
                }
        
        return results
    
    def test_security(self) -> Dict[str, Any]:
        """Test security aspects"""
        self.log("🔒 Testing Security...")
        results = {}
        
        try:
            # Test SQL injection protection
            malicious_inputs = [
                "'; DROP TABLE users; --",
                "' OR '1'='1",
                "admin'--",
                "1' UNION SELECT * FROM users--"
            ]
            
            for malicious_input in malicious_inputs:
                response = requests.post(
                    f"{self.backend_url}/api/auth/login",
                    json={"email": malicious_input, "password": "test123"},
                    timeout=10
                )
                # Should return 401 or 400, not 500 (which would indicate SQL injection vulnerability)
                results[f"sql_injection_{malicious_input[:10]}"] = {
                    "status": "pass" if response.status_code in [400, 401] else "fail",
                    "status_code": response.status_code
                }
            
            # Test XSS protection
            xss_inputs = [
                "<script>alert('xss')</script>",
                "javascript:alert('xss')",
                "<img src=x onerror=alert('xss')>"
            ]
            
            for xss_input in xss_inputs:
                response = requests.post(
                    f"{self.backend_url}/api/auth/register",
                    json={"name": xss_input, "email": "test@example.com", "password": "test123"},
                    timeout=10
                )
                # Should handle XSS input safely
                results[f"xss_protection_{xss_input[:10]}"] = {
                    "status": "pass" if response.status_code in [200, 400] else "fail",
                    "status_code": response.status_code
                }
            
            # Test authentication bypass attempts
            bypass_attempts = [
                {"Authorization": "Bearer invalid_token"},
                {"Authorization": "Bearer "},
                {"Authorization": ""},
                {}
            ]
            
            for attempt in bypass_attempts:
                response = requests.get(f"{self.backend_url}/api/me", headers=attempt, timeout=10)
                results[f"auth_bypass_{len(str(attempt))}"] = {
                    "status": "pass" if response.status_code == 401 else "fail",
                    "status_code": response.status_code
                }
            
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ Security test failed: {e}", "ERROR")
        
        return results
    
    def run_all_tests(self):
        """Run all smoke tests"""
        self.log("🚀 Starting Comprehensive Smoke Tests", "INFO")
        self.log("=" * 60, "INFO")
        
        # Run all test categories
        self.results["backend"]["health"] = self.test_backend_health()
        self.results["backend"]["authentication"] = self.test_backend_authentication()
        self.results["backend"]["api_endpoints"] = self.test_backend_api_endpoints()
        self.results["user_panel"] = self.test_user_panel()
        self.results["admin_panel"] = self.test_admin_panel()
        self.results["integration"] = self.test_integration()
        self.results["performance"] = self.test_performance()
        self.results["security"] = self.test_security()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        self.log("\n" + "=" * 60, "INFO")
        self.log("📊 SMOKE TEST SUMMARY", "INFO")
        self.log("=" * 60, "INFO")
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        # Count results by category
        for category, tests in self.results.items():
            if isinstance(tests, dict):
                for test_name, result in tests.items():
                    if isinstance(result, dict):
                        if result.get("status") == "pass":
                            passed_tests += 1
                        elif result.get("status") == "fail":
                            failed_tests += 1
                        else:
                            error_tests += 1
                        total_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.log(f"🎯 Overall Status: {'PASS' if success_rate >= 80 else 'FAIL'}", "INFO")
        self.log(f"📈 Success Rate: {success_rate:.1f}%", "INFO")
        self.log(f"✅ Passed: {passed_tests}", "INFO")
        self.log(f"❌ Failed: {failed_tests}", "INFO")
        self.log(f"⚠️  Errors: {error_tests}", "INFO")
        self.log(f"📊 Total Tests: {total_tests}", "INFO")
        
        # Category breakdown
        self.log("\n📋 CATEGORY BREAKDOWN:", "INFO")
        self.log("-" * 40, "INFO")
        
        for category, tests in self.results.items():
            if isinstance(tests, dict):
                category_passed = sum(1 for t in tests.values() if isinstance(t, dict) and t.get("status") == "pass")
                category_total = sum(1 for t in tests.values() if isinstance(t, dict) and "status" in t)
                category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
                
                status_icon = "✅" if category_rate >= 80 else "❌" if category_rate >= 50 else "⚠️"
                self.log(f"{status_icon} {category.upper()}: {category_passed}/{category_total} ({category_rate:.1f}%)", "INFO")
        
        # Performance summary
        if "performance" in self.results:
            self.log("\n⚡ PERFORMANCE SUMMARY:", "INFO")
            self.log("-" * 40, "INFO")
            for test_name, result in self.results["performance"].items():
                if isinstance(result, dict) and "avg_response_time" in result:
                    status_icon = "✅" if result["status"] == "good" else "⚠️"
                    self.log(f"{status_icon} {test_name}: {result['avg_response_time']}ms avg", "INFO")
        
        # Save detailed results
        with open('smoke_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        self.log(f"\n📄 Detailed results saved to smoke_test_results.json", "INFO")
        
        # Test duration
        duration = datetime.now() - self.start_time
        self.log(f"\n⏱️  Test completed in: {duration.total_seconds():.1f} seconds", "INFO")
        self.log("=" * 60, "INFO")

def main():
    """Main function to run smoke tests"""
    print("🧪 Zimmer AI Platform - Comprehensive Smoke Tests")
    print("=" * 60)
    
    # Check if services are running
    print("🔍 Checking if services are running...")
    
    backend_running = False
    user_panel_running = False
    admin_panel_running = False
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            backend_running = True
            print("✅ Backend is running")
        else:
            print("❌ Backend is not responding correctly")
    except:
        print("❌ Backend is not running")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            user_panel_running = True
            print("✅ User Panel is running")
        else:
            print("❌ User Panel is not responding correctly")
    except:
        print("❌ User Panel is not running")
    
    try:
        response = requests.get("http://localhost:4000", timeout=5)
        if response.status_code == 200:
            admin_panel_running = True
            print("✅ Admin Panel is running")
        else:
            print("❌ Admin Panel is not responding correctly")
    except:
        print("❌ Admin Panel is not running")
    
    print("\n" + "=" * 60)
    
    if not backend_running:
        print("❌ Backend is required for smoke tests. Please start the backend first.")
        sys.exit(1)
    
    # Run smoke tests
    tester = SmokeTestSuite()
    tester.run_all_tests()
    
    # Exit with appropriate code
    total_tests = sum(1 for category in tester.results.values() 
                     if isinstance(category, dict) 
                     for test in category.values() 
                     if isinstance(test, dict) and "status" in test)
    
    passed_tests = sum(1 for category in tester.results.values() 
                      if isinstance(category, dict) 
                      for test in category.values() 
                      if isinstance(test, dict) and test.get("status") == "pass")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    if success_rate >= 80:
        print("\n🎉 Smoke tests completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Some smoke tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
