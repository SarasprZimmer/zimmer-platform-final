#!/usr/bin/env python3
"""
Backend-Specific Smoke Tests
Deep testing of backend API functionality, database operations, and error handling
"""

import requests
import time
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class BackendSmokeTester:
    """Comprehensive backend smoke testing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}
        self.test_user_token = None
        self.admin_token = None
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_database_operations(self) -> Dict[str, Any]:
        """Test database operations and data integrity"""
        self.log("🗄️ Testing Database Operations...")
        results = {}
        
        try:
            # Test user creation and retrieval
            test_email = f"dbtest_{int(time.time())}@zimmer.ai"
            user_data = {
                "name": "DB Test User",
                "email": test_email,
                "password": "dbtest123",
                "phone_number": "+1234567890"
            }
            
            # Create user
            response = requests.post(f"{self.base_url}/api/auth/register", json=user_data, timeout=10)
            results["user_creation"] = {
                "status": "pass" if response.status_code == 200 else "fail",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            if response.status_code == 200:
                # Login to get token
                login_response = requests.post(f"{self.base_url}/api/auth/login", 
                                             json={"email": test_email, "password": "dbtest123"}, 
                                             timeout=10)
                
                if login_response.status_code == 200:
                    self.test_user_token = login_response.json().get("access_token")
                    
                    # Test user profile retrieval
                    headers = {"Authorization": f"Bearer {self.test_user_token}"}
                    profile_response = requests.get(f"{self.base_url}/api/me", headers=headers, timeout=10)
                    
                    results["user_profile_retrieval"] = {
                        "status": "pass" if profile_response.status_code == 200 else "fail",
                        "status_code": profile_response.status_code,
                        "response_time": profile_response.elapsed.total_seconds()
                    }
                    
                    # Test user settings
                    settings_response = requests.get(f"{self.base_url}/api/user/settings", headers=headers, timeout=10)
                    results["user_settings"] = {
                        "status": "pass" if settings_response.status_code == 200 else "fail",
                        "status_code": settings_response.status_code,
                        "response_time": settings_response.elapsed.total_seconds()
                    }
        
        except Exception as e:
            results["error"] = str(e)
            self.log(f"❌ Database operations test failed: {e}", "ERROR")
        
        return results
    
    def test_api_error_handling(self) -> Dict[str, Any]:
        """Test API error handling and edge cases"""
        self.log("⚠️ Testing API Error Handling...")
        results = {}
        
        # Test invalid endpoints
        invalid_endpoints = [
            "/api/nonexistent",
            "/api/invalid/endpoint",
            "/api/users/invalid/123"
        ]
        
        for endpoint in invalid_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                results[f"invalid_endpoint_{endpoint.replace('/', '_')}"] = {
                    "status": "pass" if response.status_code == 404 else "fail",
                    "status_code": response.status_code,
                    "expected": 404
                }
            except Exception as e:
                results[f"invalid_endpoint_{endpoint.replace('/', '_')}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Test malformed JSON
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   data="invalid json", 
                                   headers={"Content-Type": "application/json"}, 
                                   timeout=10)
            results["malformed_json"] = {
                "status": "pass" if response.status_code == 422 else "fail",
                "status_code": response.status_code,
                "expected": 422
            }
        except Exception as e:
            results["malformed_json"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test missing required fields
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"email": "test@example.com"},  # Missing password
                                   timeout=10)
            results["missing_required_fields"] = {
                "status": "pass" if response.status_code == 422 else "fail",
                "status_code": response.status_code,
                "expected": 422
            }
        except Exception as e:
            results["missing_required_fields"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test invalid authentication
        try:
            response = requests.get(f"{self.base_url}/api/me", 
                                  headers={"Authorization": "Bearer invalid_token"}, 
                                  timeout=10)
            results["invalid_auth"] = {
                "status": "pass" if response.status_code == 401 else "fail",
                "status_code": response.status_code,
                "expected": 401
            }
        except Exception as e:
            results["invalid_auth"] = {
                "status": "error",
                "error": str(e)
            }
        
        return results
    
    def test_rate_limiting(self) -> Dict[str, Any]:
        """Test rate limiting and performance under load"""
        self.log("🚦 Testing Rate Limiting...")
        results = {}
        
        # Test rapid requests to same endpoint
        try:
            start_time = time.time()
            responses = []
            
            for i in range(20):  # 20 rapid requests
                response = requests.get(f"{self.base_url}/health", timeout=5)
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay between requests
            
            end_time = time.time()
            
            success_count = sum(1 for status in responses if status == 200)
            results["rapid_requests"] = {
                "status": "pass" if success_count >= 18 else "fail",  # Allow some failures
                "success_count": success_count,
                "total_requests": len(responses),
                "success_rate": (success_count / len(responses)) * 100,
                "total_time": end_time - start_time
            }
            
        except Exception as e:
            results["rapid_requests"] = {
                "status": "error",
                "error": str(e)
            }
        
        return results
    
    def test_data_validation(self) -> Dict[str, Any]:
        """Test data validation and sanitization"""
        self.log("🔍 Testing Data Validation...")
        results = {}
        
        # Test email validation
        invalid_emails = [
            "invalid-email",
            "@invalid.com",
            "test@",
            "test..test@example.com",
            "test@.com"
        ]
        
        for email in invalid_emails:
            try:
                response = requests.post(f"{self.base_url}/api/auth/register", 
                                       json={
                                           "name": "Test User",
                                           "email": email,
                                           "password": "test123"
                                       }, 
                                       timeout=10)
                results[f"email_validation_{email.replace('@', '_').replace('.', '_')}"] = {
                    "status": "pass" if response.status_code == 422 else "fail",
                    "status_code": response.status_code,
                    "expected": 422
                }
            except Exception as e:
                results[f"email_validation_{email.replace('@', '_').replace('.', '_')}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Test password validation
        weak_passwords = [
            "123",
            "password",
            "12345678",
            "abcdefgh"
        ]
        
        for password in weak_passwords:
            try:
                response = requests.post(f"{self.base_url}/api/auth/register", 
                                       json={
                                           "name": "Test User",
                                           "email": f"test_{int(time.time())}@example.com",
                                           "password": password
                                       }, 
                                       timeout=10)
                results[f"password_validation_{password}"] = {
                    "status": "pass" if response.status_code == 422 else "fail",
                    "status_code": response.status_code,
                    "expected": 422
                }
            except Exception as e:
                results[f"password_validation_{password}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_concurrent_operations(self) -> Dict[str, Any]:
        """Test concurrent operations and thread safety"""
        self.log("🔄 Testing Concurrent Operations...")
        results = {}
        
        import threading
        import queue
        
        def make_request(q, endpoint, headers=None):
            try:
                if headers:
                    response = requests.get(f"{self.base_url}{endpoint}", headers=headers, timeout=10)
                else:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                q.put(("success", response.status_code, response.elapsed.total_seconds()))
            except Exception as e:
                q.put(("error", str(e), 0))
        
        # Test concurrent health checks
        try:
            q = queue.Queue()
            threads = []
            
            for i in range(10):
                thread = threading.Thread(target=make_request, args=(q, "/health"))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            success_count = 0
            error_count = 0
            total_time = 0
            
            while not q.empty():
                result_type, data, response_time = q.get()
                if result_type == "success" and data == 200:
                    success_count += 1
                    total_time += response_time
                else:
                    error_count += 1
            
            results["concurrent_health_checks"] = {
                "status": "pass" if success_count >= 8 else "fail",
                "success_count": success_count,
                "error_count": error_count,
                "avg_response_time": total_time / max(success_count, 1)
            }
            
        except Exception as e:
            results["concurrent_health_checks"] = {
                "status": "error",
                "error": str(e)
            }
        
        return results
    
    def test_memory_leaks(self) -> Dict[str, Any]:
        """Test for memory leaks and resource management"""
        self.log("🧠 Testing Memory Management...")
        results = {}
        
        try:
            # Make many requests and monitor response times
            response_times = []
            
            for i in range(50):
                start_time = time.time()
                response = requests.get(f"{self.base_url}/health", timeout=10)
                end_time = time.time()
                
                response_times.append(end_time - start_time)
                time.sleep(0.1)
            
            # Check if response times are consistent (no significant degradation)
            early_times = response_times[:10]
            late_times = response_times[-10:]
            
            early_avg = sum(early_times) / len(early_times)
            late_avg = sum(late_times) / len(late_times)
            
            degradation = ((late_avg - early_avg) / early_avg) * 100 if early_avg > 0 else 0
            
            results["memory_management"] = {
                "status": "pass" if degradation < 50 else "fail",  # Allow up to 50% degradation
                "early_avg_response_time": early_avg,
                "late_avg_response_time": late_avg,
                "degradation_percent": degradation
            }
            
        except Exception as e:
            results["memory_management"] = {
                "status": "error",
                "error": str(e)
            }
        
        return results
    
    def run_all_tests(self):
        """Run all backend smoke tests"""
        self.log("🚀 Starting Backend Smoke Tests", "INFO")
        self.log("=" * 50, "INFO")
        
        # Run all test categories
        self.results["database_operations"] = self.test_database_operations()
        self.results["error_handling"] = self.test_api_error_handling()
        self.results["rate_limiting"] = self.test_rate_limiting()
        self.results["data_validation"] = self.test_data_validation()
        self.results["concurrent_operations"] = self.test_concurrent_operations()
        self.results["memory_management"] = self.test_memory_leaks()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        self.log("\n" + "=" * 50, "INFO")
        self.log("📊 BACKEND SMOKE TEST SUMMARY", "INFO")
        self.log("=" * 50, "INFO")
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        for category, tests in self.results.items():
            if isinstance(tests, dict):
                for test_name, result in tests.items():
                    if isinstance(result, dict) and "status" in result:
                        total_tests += 1
                        if result["status"] == "pass":
                            passed_tests += 1
                        elif result["status"] == "fail":
                            failed_tests += 1
                        else:
                            error_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.log(f"🎯 Backend Status: {'PASS' if success_rate >= 80 else 'FAIL'}", "INFO")
        self.log(f"📈 Success Rate: {success_rate:.1f}%", "INFO")
        self.log(f"✅ Passed: {passed_tests}", "INFO")
        self.log(f"❌ Failed: {failed_tests}", "INFO")
        self.log(f"⚠️  Errors: {error_tests}", "INFO")
        self.log(f"📊 Total Tests: {total_tests}", "INFO")
        
        # Save results
        with open('backend_smoke_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        self.log(f"\n📄 Detailed results saved to backend_smoke_test_results.json", "INFO")

def main():
    """Main function"""
    print("🧪 Backend Smoke Tests")
    print("=" * 30)
    
    tester = BackendSmokeTester()
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
        print("\n🎉 Backend smoke tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some backend smoke tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
