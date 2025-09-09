#!/usr/bin/env python3
"""
Comprehensive System Test for Zimmer AI Platform - Current Version
Tests the current system state after JWT authentication fixes and cleanup
"""

import requests
import time
import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys

class ComprehensiveSystemTester:
    """Comprehensive testing for current system state"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.results = {}
        self.start_time = datetime.utcnow()
        self.session = requests.Session()
        
        # Test endpoints based on current system
        self.endpoints = {
            "health": "/health",
            "auth_csrf": "/api/auth/csrf",
            "auth_login": "/api/auth/login",
            "auth_refresh": "/api/auth/refresh",
            "user_me": "/api/me",
            "user_dashboard": "/api/user/dashboard",
            "admin_dashboard": "/api/admin/dashboard",
            "marketplace": "/api/automations/marketplace",
            "optimized_marketplace": "/api/optimized/automations/marketplace",
            "optimized_me": "/api/optimized/me",
            "optimized_dashboard": "/api/optimized/user/dashboard",
            "cache_stats": "/api/optimized/cache/stats",
            "circuit_breaker_stats": "/circuit-breaker/stats",
            "notifications": "/api/notifications",
        }
        
        # Test users
        self.test_users = [
            {"email": "test@zimmer.ai", "password": "test123"},
            {"email": "admin@zimmer.ai", "password": "admin123"},
        ]
    
    def test_health_endpoint(self) -> Dict[str, Any]:
        """Test health endpoint"""
        print("🏥 Testing health endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            return {
                "status": "success" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def test_auth_endpoints(self) -> Dict[str, Any]:
        """Test authentication endpoints"""
        print("🔐 Testing authentication endpoints...")
        results = {}
        
        # Test CSRF endpoint
        try:
            response = self.session.get(f"{self.base_url}/api/auth/csrf", timeout=10)
            results["csrf"] = {
                "status": "success" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            results["csrf"] = {"status": "error", "error": str(e)}
        
        # Test login endpoint
        try:
            login_data = {"email": "test@example.com", "password": "test123"}
            response = self.session.post(f"{self.base_url}/api/auth/login", 
                                       json=login_data, timeout=10)
            results["login"] = {
                "status": "success" if response.status_code in [200, 401] else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "note": "401 expected for invalid credentials"
            }
        except Exception as e:
            results["login"] = {"status": "error", "error": str(e)}
        
        return results
    
    def test_public_endpoints(self) -> Dict[str, Any]:
        """Test public endpoints that don't require authentication"""
        print("🌐 Testing public endpoints...")
        results = {}
        
        public_endpoints = [
            "/api/automations/marketplace",
            "/api/optimized/automations/marketplace",
            "/api/optimized/cache/stats",
            "/circuit-breaker/stats"
        ]
        
        for endpoint in public_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                results[endpoint] = {
                    "status": "success" if response.status_code == 200 else "failed",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            except Exception as e:
                results[endpoint] = {"status": "error", "error": str(e)}
        
        return results
    
    def test_protected_endpoints(self) -> Dict[str, Any]:
        """Test protected endpoints (should return 401 without auth)"""
        print("🔒 Testing protected endpoints...")
        results = {}
        
        protected_endpoints = [
            "/api/me",
            "/api/user/dashboard",
            "/api/admin/dashboard",
            "/api/notifications"
        ]
        
        for endpoint in protected_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                results[endpoint] = {
                    "status": "success" if response.status_code == 401 else "failed",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "note": "401 expected without authentication"
                }
            except Exception as e:
                results[endpoint] = {"status": "error", "error": str(e)}
        
        return results
    
    def test_jwt_authentication_flow(self) -> Dict[str, Any]:
        """Test complete JWT authentication flow"""
        print("🎫 Testing JWT authentication flow...")
        results = {}
        
        # Test with a real user (if exists)
        test_user = {"email": "test@zimmer.ai", "password": "test123"}
        
        try:
            # Step 1: Login
            login_response = self.session.post(f"{self.base_url}/api/auth/login", 
                                             json=test_user, timeout=10)
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                access_token = login_data.get("access_token")
                
                if access_token:
                    # Step 2: Test protected endpoint with token
                    headers = {"Authorization": f"Bearer {access_token}"}
                    me_response = self.session.get(f"{self.base_url}/api/me", 
                                                  headers=headers, timeout=10)
                    
                    results["jwt_flow"] = {
                        "status": "success" if me_response.status_code == 200 else "failed",
                        "login_status": login_response.status_code,
                        "me_status": me_response.status_code,
                        "has_token": bool(access_token),
                        "response_time": me_response.elapsed.total_seconds()
                    }
                else:
                    results["jwt_flow"] = {
                        "status": "failed",
                        "error": "No access token in login response"
                    }
            else:
                results["jwt_flow"] = {
                    "status": "failed",
                    "error": f"Login failed with status {login_response.status_code}",
                    "response": login_response.text
                }
        except Exception as e:
            results["jwt_flow"] = {"status": "error", "error": str(e)}
        
        return results
    
    def test_performance(self) -> Dict[str, Any]:
        """Test system performance"""
        print("⚡ Testing system performance...")
        results = {}
        
        # Test response times for key endpoints
        test_endpoints = [
            "/health",
            "/api/auth/csrf",
            "/api/automations/marketplace"
        ]
        
        for endpoint in test_endpoints:
            times = []
            for _ in range(5):  # 5 requests
                try:
                    start_time = time.time()
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                    end_time = time.time()
                    times.append(end_time - start_time)
                except Exception as e:
                    times.append(float('inf'))
            
            if times and all(t != float('inf') for t in times):
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)
                
                results[endpoint] = {
                    "avg_response_time": round(avg_time * 1000, 2),  # ms
                    "max_response_time": round(max_time * 1000, 2),  # ms
                    "min_response_time": round(min_time * 1000, 2),  # ms
                    "status": "good" if avg_time < 1.0 else "slow"
                }
            else:
                results[endpoint] = {"status": "error", "error": "All requests failed"}
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        print("🚀 Starting comprehensive system test...")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run all test categories
        self.results = {
            "health": self.test_health_endpoint(),
            "auth": self.test_auth_endpoints(),
            "public": self.test_public_endpoints(),
            "protected": self.test_protected_endpoints(),
            "jwt_flow": self.test_jwt_authentication_flow(),
            "performance": self.test_performance()
        }
        
        # Calculate overall status
        self.results["summary"] = self.calculate_summary()
        
        return self.results
    
    def calculate_summary(self) -> Dict[str, Any]:
        """Calculate overall test summary"""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        for category, tests in self.results.items():
            if category == "summary":
                continue
                
            if isinstance(tests, dict):
                for test_name, result in tests.items():
                    total_tests += 1
                    if isinstance(result, dict) and result.get("status") == "success":
                        passed_tests += 1
                    elif isinstance(result, dict) and result.get("status") == "failed":
                        failed_tests += 1
                    else:
                        error_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "success_rate": round(success_rate, 2),
            "overall_status": "PASS" if success_rate >= 80 else "FAIL"
        }
    
    def print_results(self):
        """Print formatted test results"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE SYSTEM TEST RESULTS")
        print("=" * 60)
        
        # Print summary
        summary = self.results.get("summary", {})
        print(f"\n🎯 OVERALL STATUS: {summary.get('overall_status', 'UNKNOWN')}")
        print(f"📈 Success Rate: {summary.get('success_rate', 0)}%")
        print(f"✅ Passed: {summary.get('passed', 0)}")
        print(f"❌ Failed: {summary.get('failed', 0)}")
        print(f"⚠️  Errors: {summary.get('errors', 0)}")
        print(f"📊 Total Tests: {summary.get('total_tests', 0)}")
        
        # Print detailed results
        print("\n📋 DETAILED RESULTS:")
        print("-" * 40)
        
        for category, tests in self.results.items():
            if category == "summary":
                continue
                
            print(f"\n🔸 {category.upper()}:")
            if isinstance(tests, dict):
                for test_name, result in tests.items():
                    if isinstance(result, dict):
                        status = result.get("status", "unknown")
                        status_icon = "✅" if status == "success" else "❌" if status == "failed" else "⚠️"
                        print(f"  {status_icon} {test_name}: {status}")
                        
                        if "response_time" in result:
                            print(f"     Response Time: {result['response_time']:.3f}s")
                        if "status_code" in result:
                            print(f"     Status Code: {result['status_code']}")
                        if "error" in result:
                            print(f"     Error: {result['error']}")
                        if "note" in result:
                            print(f"     Note: {result['note']}")
                    else:
                        print(f"  ⚠️  {test_name}: {result}")
        
        print("\n" + "=" * 60)
        print(f"⏱️  Test completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 60)

def main():
    """Main function to run the comprehensive test"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive System Test for Zimmer AI Platform")
    parser.add_argument("--url", default="http://127.0.0.1:8000", 
                       help="Base URL for the API (default: http://127.0.0.1:8000)")
    parser.add_argument("--output", help="Output file for JSON results")
    
    args = parser.parse_args()
    
    # Run tests
    tester = ComprehensiveSystemTester(args.url)
    results = tester.run_all_tests()
    
    # Print results
    tester.print_results()
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with appropriate code
    summary = results.get("summary", {})
    if summary.get("overall_status") == "PASS":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
