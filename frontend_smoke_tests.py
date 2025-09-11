#!/usr/bin/env python3
"""
Frontend-Specific Smoke Tests
Testing user panel and admin panel functionality, UI responsiveness, and integration
"""

import requests
import time
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class FrontendSmokeTester:
    """Comprehensive frontend smoke testing"""
    
    def __init__(self):
        self.user_panel_url = "http://localhost:3000"
        self.admin_panel_url = "http://localhost:4000"
        self.backend_url = "http://localhost:8000"
        self.results = {}
        self.test_user_token = None
        self.admin_token = None
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_user_panel_pages(self) -> Dict[str, Any]:
        """Test user panel page loading and content"""
        self.log("👤 Testing User Panel Pages...")
        results = {}
        
        pages = [
            ("/", "Home Page"),
            ("/login", "Login Page"),
            ("/signup", "Signup Page"),
            ("/dashboard", "Dashboard Page"),
            ("/automations", "Automations Page"),
            ("/automations/marketplace", "Marketplace Page"),
            ("/settings", "Settings Page"),
            ("/support", "Support Page")
        ]
        
        for page_path, page_name in pages:
            try:
                response = requests.get(f"{self.user_panel_url}{page_path}", timeout=10)
                
                # Check if page loads successfully
                page_loaded = response.status_code == 200
                
                # Check if it's a valid HTML page
                is_html = "text/html" in response.headers.get("content-type", "")
                
                # Check for basic HTML structure
                has_html_structure = False
                if page_loaded and is_html:
                    try:
                        has_html_structure = '<html' in response.text.lower() and '<body' in response.text.lower()
                    except:
                        has_html_structure = False
                
                # Check for React/Next.js indicators
                is_react_app = False
                if page_loaded and is_html:
                    is_react_app = any(indicator in response.text.lower() for indicator in [
                        'react', 'next', '__next', 'react-dom', 'next.js'
                    ])
                
                results[page_name.lower().replace(" ", "_")] = {
                    "status": "pass" if page_loaded and is_html and has_html_structure else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "is_html": is_html,
                    "has_html_structure": has_html_structure,
                    "is_react_app": is_react_app,
                    "content_length": len(response.text)
                }
                
            except Exception as e:
                results[page_name.lower().replace(" ", "_")] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_admin_panel_pages(self) -> Dict[str, Any]:
        """Test admin panel page loading and content"""
        self.log("👑 Testing Admin Panel Pages...")
        results = {}
        
        pages = [
            ("/", "Admin Home Page"),
            ("/login", "Admin Login Page"),
            ("/users", "Users Management"),
            ("/analytics", "Analytics Page"),
            ("/settings", "Admin Settings"),
            ("/automations", "Automations Management"),
            ("/payments", "Payments Management"),
            ("/notifications", "Notifications Management")
        ]
        
        for page_path, page_name in pages:
            try:
                response = requests.get(f"{self.admin_panel_url}{page_path}", timeout=10)
                
                # Check if page loads successfully
                page_loaded = response.status_code == 200
                
                # Check if it's a valid HTML page
                is_html = "text/html" in response.headers.get("content-type", "")
                
                # Check for basic HTML structure
                has_html_structure = False
                if page_loaded and is_html:
                    try:
                        has_html_structure = '<html' in response.text.lower() and '<body' in response.text.lower()
                    except:
                        has_html_structure = False
                
                # Check for admin-specific content
                has_admin_content = False
                if page_loaded and is_html:
                    has_admin_content = any(keyword in response.text.lower() for keyword in [
                        'admin', 'dashboard', 'management', 'users', 'analytics'
                    ])
                
                results[page_name.lower().replace(" ", "_")] = {
                    "status": "pass" if page_loaded and is_html and has_html_structure else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "is_html": is_html,
                    "has_html_structure": has_html_structure,
                    "has_admin_content": has_admin_content,
                    "content_length": len(response.text)
                }
                
            except Exception as e:
                results[page_name.lower().replace(" ", "_")] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_static_assets(self) -> Dict[str, Any]:
        """Test static assets loading (CSS, JS, images)"""
        self.log("🎨 Testing Static Assets...")
        results = {}
        
        # Test user panel assets
        user_assets = [
            ("/_next/static/css/", "User Panel CSS"),
            ("/_next/static/js/", "User Panel JS"),
            ("/favicon.ico", "Favicon"),
            ("/manifest.json", "Web App Manifest")
        ]
        
        for asset_path, asset_name in user_assets:
            try:
                response = requests.get(f"{self.user_panel_url}{asset_path}", timeout=10)
                results[f"user_{asset_name.lower().replace(' ', '_')}"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(response.content)
                }
            except Exception as e:
                results[f"user_{asset_name.lower().replace(' ', '_')}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Test admin panel assets
        admin_assets = [
            ("/_next/static/css/", "Admin Panel CSS"),
            ("/_next/static/js/", "Admin Panel JS"),
            ("/favicon.ico", "Admin Favicon"),
            ("/manifest.json", "Admin Web App Manifest")
        ]
        
        for asset_path, asset_name in admin_assets:
            try:
                response = requests.get(f"{self.admin_panel_url}{asset_path}", timeout=10)
                results[f"admin_{asset_name.lower().replace(' ', '_')}"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(response.content)
                }
            except Exception as e:
                results[f"admin_{asset_name.lower().replace(' ', '_')}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_api_integration(self) -> Dict[str, Any]:
        """Test frontend-backend API integration"""
        self.log("🔗 Testing API Integration...")
        results = {}
        
        # Test public API endpoints that frontend might call
        public_endpoints = [
            ("/api/optimized/automations/marketplace", "Optimized Marketplace API"),
            ("/health", "Health Check API")
        ]
        
        for endpoint, api_name in public_endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                results[f"api_{api_name.lower().replace(' ', '_')}"] = {
                    "status": "pass" if response.status_code == 200 else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "is_json": "application/json" in response.headers.get("content-type", ""),
                    "has_cors_headers": "access-control-allow-origin" in response.headers
                }
            except Exception as e:
                results[f"api_{api_name.lower().replace(' ', '_')}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_responsive_design(self) -> Dict[str, Any]:
        """Test responsive design and mobile compatibility"""
        self.log("📱 Testing Responsive Design...")
        results = {}
        
        # Test with different user agents
        user_agents = [
            ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)", "Mobile Safari"),
            ("Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0", "Mobile Firefox"),
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Desktop Chrome"),
            ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36", "Desktop Safari")
        ]
        
        for user_agent, browser_name in user_agents:
            try:
                headers = {"User-Agent": user_agent}
                response = requests.get(self.user_panel_url, headers=headers, timeout=10)
                
                # Check if page loads on different devices
                page_loaded = response.status_code == 200
                
                # Check for responsive design indicators
                has_viewport_meta = False
                has_responsive_css = False
                
                if page_loaded:
                    has_viewport_meta = 'name="viewport"' in response.text
                    
                    # Look for responsive CSS classes or media queries
                    has_responsive_css = any(keyword in response.text.lower() for keyword in [
                        'responsive', 'mobile', 'tablet', 'desktop', 'sm:', 'md:', 'lg:', 'xl:'
                    ])
                
                results[f"responsive_{browser_name.lower().replace(' ', '_')}"] = {
                    "status": "pass" if page_loaded and has_viewport_meta else "fail",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "has_viewport_meta": has_viewport_meta,
                    "has_responsive_css": has_responsive_css
                }
                
            except Exception as e:
                results[f"responsive_{browser_name.lower().replace(' ', '_')}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_performance_metrics(self) -> Dict[str, Any]:
        """Test frontend performance metrics"""
        self.log("⚡ Testing Performance Metrics...")
        results = {}
        
        # Test page load times
        pages_to_test = [
            (self.user_panel_url, "User Panel Home"),
            (f"{self.user_panel_url}/dashboard", "User Dashboard"),
            (self.admin_panel_url, "Admin Panel Home"),
            (f"{self.admin_panel_url}/dashboard", "Admin Dashboard")
        ]
        
        for url, page_name in pages_to_test:
            try:
                # Test multiple requests to get average load time
                load_times = []
                
                for i in range(5):
                    start_time = time.time()
                    response = requests.get(url, timeout=10)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        load_times.append(end_time - start_time)
                
                if load_times:
                    avg_load_time = sum(load_times) / len(load_times)
                    max_load_time = max(load_times)
                    min_load_time = min(load_times)
                    
                    results[page_name.lower().replace(" ", "_")] = {
                        "status": "pass" if avg_load_time < 3.0 else "fail",  # 3 second threshold
                        "avg_load_time": round(avg_load_time, 2),
                        "max_load_time": round(max_load_time, 2),
                        "min_load_time": round(min_load_time, 2),
                        "requests_tested": len(load_times)
                    }
                else:
                    results[page_name.lower().replace(" ", "_")] = {
                        "status": "fail",
                        "error": "No successful requests"
                    }
                    
            except Exception as e:
                results[page_name.lower().replace(" ", "_")] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def test_security_headers(self) -> Dict[str, Any]:
        """Test security headers and configurations"""
        self.log("🔒 Testing Security Headers...")
        results = {}
        
        # Test security headers on both panels
        panels = [
            (self.user_panel_url, "User Panel"),
            (self.admin_panel_url, "Admin Panel")
        ]
        
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "Referrer-Policy"
        ]
        
        for url, panel_name in panels:
            try:
                response = requests.get(url, timeout=10)
                
                panel_results = {}
                for header in security_headers:
                    panel_results[header.lower().replace("-", "_")] = {
                        "present": header in response.headers,
                        "value": response.headers.get(header, "")
                    }
                
                # Overall security score
                present_headers = sum(1 for h in security_headers if h in response.headers)
                security_score = (present_headers / len(security_headers)) * 100
                
                results[panel_name.lower().replace(" ", "_")] = {
                    "status": "pass" if security_score >= 50 else "fail",
                    "security_score": security_score,
                    "present_headers": present_headers,
                    "total_headers": len(security_headers),
                    "headers": panel_results
                }
                
            except Exception as e:
                results[panel_name.lower().replace(" ", "_")] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def run_all_tests(self):
        """Run all frontend smoke tests"""
        self.log("🚀 Starting Frontend Smoke Tests", "INFO")
        self.log("=" * 50, "INFO")
        
        # Run all test categories
        self.results["user_panel_pages"] = self.test_user_panel_pages()
        self.results["admin_panel_pages"] = self.test_admin_panel_pages()
        self.results["static_assets"] = self.test_static_assets()
        self.results["api_integration"] = self.test_api_integration()
        self.results["responsive_design"] = self.test_responsive_design()
        self.results["performance_metrics"] = self.test_performance_metrics()
        self.results["security_headers"] = self.test_security_headers()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        self.log("\n" + "=" * 50, "INFO")
        self.log("📊 FRONTEND SMOKE TEST SUMMARY", "INFO")
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
        
        self.log(f"🎯 Frontend Status: {'PASS' if success_rate >= 70 else 'FAIL'}", "INFO")
        self.log(f"📈 Success Rate: {success_rate:.1f}%", "INFO")
        self.log(f"✅ Passed: {passed_tests}", "INFO")
        self.log(f"❌ Failed: {failed_tests}", "INFO")
        self.log(f"⚠️  Errors: {error_tests}", "INFO")
        self.log(f"📊 Total Tests: {total_tests}", "INFO")
        
        # Save results
        with open('frontend_smoke_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        self.log(f"\n📄 Detailed results saved to frontend_smoke_test_results.json", "INFO")

def main():
    """Main function"""
    print("🧪 Frontend Smoke Tests")
    print("=" * 30)
    
    tester = FrontendSmokeTester()
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
    
    if success_rate >= 70:
        print("\n🎉 Frontend smoke tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some frontend smoke tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
