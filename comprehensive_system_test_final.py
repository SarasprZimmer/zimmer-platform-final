#!/usr/bin/env python3
"""
Comprehensive System Test - Final Check
Tests all implemented features and identifies missing components
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
USER_PANEL_URL = "http://localhost:3000"
ADMIN_PANEL_URL = "http://localhost:3001"

# Test credentials
TEST_USER = {
    "email": "test@zimmer.ai",
    "password": "testpass123",
    "name": "Test User"
}

ADMIN_USER = {
    "email": "admin@zimmer.com", 
    "password": "admin123"
}

class SystemTester:
    def __init__(self):
        self.results = {}
        self.user_token = None
        self.admin_token = None
        self.test_user_id = None
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
        
    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code == 200:
                self.log("✅ Backend is running", "SUCCESS")
                return True
            else:
                self.log(f"❌ Backend returned status {response.status_code}", "ERROR")
                return False
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Backend not accessible: {e}", "ERROR")
            return False
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        try:
            # First try to register a new user
            test_email = f"test_{int(time.time())}@zimmer.ai"
            data = {
                "name": "Test User",
                "email": test_email,
                "password": "testpass123",
                "phone_number": "+1234567890"
            }
            response = requests.post(f"{BASE_URL}/api/auth/register", json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.test_user_id = result.get('user_id')
                self.log("✅ User registration working", "SUCCESS")
                return True
            elif response.status_code == 400 and "already exists" in response.text:
                self.log("✅ User registration working (user exists)", "SUCCESS")
                return True
            else:
                self.log(f"❌ User registration failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ User registration error: {e}", "ERROR")
            return False
    
    def test_user_login(self):
        """Test user login and get token"""
        try:
            data = {
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
            response = requests.post(f"{BASE_URL}/api/auth/login", json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.user_token = result.get('access_token')
                self.log("✅ User login working", "SUCCESS")
                return True
            else:
                self.log(f"❌ User login failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ User login error: {e}", "ERROR")
            return False
    
    def test_admin_login(self):
        """Test admin login"""
        try:
            data = {
                "email": ADMIN_USER["email"],
                "password": ADMIN_USER["password"]
            }
            response = requests.post(f"{BASE_URL}/api/auth/login", json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.admin_token = result.get('access_token')
                self.log("✅ Admin login working", "SUCCESS")
                return True
            else:
                self.log(f"❌ Admin login failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Admin login error: {e}", "ERROR")
            return False
    
    def test_user_endpoints(self):
        """Test user-specific endpoints"""
        if not self.user_token:
            self.log("❌ No user token available", "ERROR")
            return False
            
        headers = {"Authorization": f"Bearer {self.user_token}"}
        endpoints = [
            ("/api/me", "GET", "User profile"),
            ("/api/user/settings", "GET", "User settings"),
            ("/api/user/dashboard", "GET", "User dashboard"),
            ("/api/user/automations/active", "GET", "Active automations"),
            ("/api/user/usage/distribution", "GET", "Usage distribution"),
            ("/api/user/payments", "GET", "User payments")
        ]
        
        results = {}
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.log(f"✅ {description} working", "SUCCESS")
                    results[endpoint] = "working"
                else:
                    self.log(f"❌ {description} failed: {response.status_code}", "ERROR")
                    results[endpoint] = f"failed_{response.status_code}"
            except Exception as e:
                self.log(f"❌ {description} error: {e}", "ERROR")
                results[endpoint] = f"error_{str(e)}"
        
        return results
    
    def test_admin_endpoints(self):
        """Test admin-specific endpoints"""
        if not self.admin_token:
            self.log("❌ No admin token available", "ERROR")
            return False
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoints = [
            ("/api/admin/users", "GET", "List users"),
            ("/api/admin/users/stats", "GET", "User statistics"),
            ("/api/admin/openai-keys", "GET", "OpenAI keys management"),
            ("/api/admin/analytics", "GET", "Analytics dashboard"),
            ("/api/admin/settings", "GET", "Admin settings")
        ]
        
        results = {}
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.log(f"✅ {description} working", "SUCCESS")
                    results[endpoint] = "working"
                else:
                    self.log(f"❌ {description} failed: {response.status_code}", "ERROR")
                    results[endpoint] = f"failed_{response.status_code}"
            except Exception as e:
                self.log(f"❌ {description} error: {e}", "ERROR")
                results[endpoint] = f"error_{str(e)}"
        
        return results
    
    def test_frontend_accessibility(self):
        """Test if frontend panels are accessible"""
        panels = [
            (USER_PANEL_URL, "User Panel"),
            (ADMIN_PANEL_URL, "Admin Panel")
        ]
        
        results = {}
        for url, name in panels:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.log(f"✅ {name} accessible", "SUCCESS")
                    results[name] = "accessible"
                else:
                    self.log(f"❌ {name} not accessible: {response.status_code}", "ERROR")
                    results[name] = f"not_accessible_{response.status_code}"
            except Exception as e:
                self.log(f"❌ {name} error: {e}", "ERROR")
                results[name] = f"error_{str(e)}"
        
        return results
    
    def test_critical_missing_features(self):
        """Test for critical missing features"""
        missing_features = []
        
        # Test if we can create a new automation
        if self.user_token:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            try:
                response = requests.post(f"{BASE_URL}/api/user/automations", 
                                      json={"name": "Test Automation", "type": "test"}, 
                                      headers=headers, timeout=10)
                if response.status_code not in [200, 201]:
                    missing_features.append("User automation creation")
            except:
                missing_features.append("User automation creation")
        
        # Test if we can manage OpenAI keys
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            try:
                response = requests.post(f"{BASE_URL}/api/admin/openai-keys", 
                                       json={"name": "Test Key", "key": "test-key"}, 
                                       headers=headers, timeout=10)
                if response.status_code not in [200, 201]:
                    missing_features.append("OpenAI key management")
            except:
                missing_features.append("OpenAI key management")
        
        return missing_features
    
    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        self.log("🚀 Starting Comprehensive System Test", "INFO")
        self.log("=" * 50, "INFO")
        
        # Test backend health
        backend_healthy = self.test_backend_health()
        if not backend_healthy:
            self.log("❌ Backend not running - cannot continue tests", "ERROR")
            return
        
        # Test authentication
        self.log("\n🔐 Testing Authentication", "INFO")
        self.test_user_registration()
        user_login = self.test_user_login()
        admin_login = self.test_admin_login()
        
        # Test user endpoints
        if user_login:
            self.log("\n👤 Testing User Endpoints", "INFO")
            user_results = self.test_user_endpoints()
            self.results['user_endpoints'] = user_results
        
        # Test admin endpoints
        if admin_login:
            self.log("\n👑 Testing Admin Endpoints", "INFO")
            admin_results = self.test_admin_endpoints()
            self.results['admin_endpoints'] = admin_results
        
        # Test frontend accessibility
        self.log("\n🌐 Testing Frontend Accessibility", "INFO")
        frontend_results = self.test_frontend_accessibility()
        self.results['frontend'] = frontend_results
        
        # Test missing features
        self.log("\n🔍 Testing Critical Missing Features", "INFO")
        missing_features = self.test_critical_missing_features()
        self.results['missing_features'] = missing_features
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        self.log("\n" + "=" * 50, "INFO")
        self.log("📊 TEST SUMMARY", "INFO")
        self.log("=" * 50, "INFO")
        
        # Count working vs failed endpoints
        if 'user_endpoints' in self.results:
            user_working = sum(1 for v in self.results['user_endpoints'].values() if v == 'working')
            user_total = len(self.results['user_endpoints'])
            self.log(f"👤 User Endpoints: {user_working}/{user_total} working", "INFO")
        
        if 'admin_endpoints' in self.results:
            admin_working = sum(1 for v in self.results['admin_endpoints'].values() if v == 'working')
            admin_total = len(self.results['admin_endpoints'])
            self.log(f"👑 Admin Endpoints: {admin_working}/{admin_total} working", "INFO")
        
        if 'frontend' in self.results:
            frontend_working = sum(1 for v in self.results['frontend'].values() if v == 'accessible')
            frontend_total = len(self.results['frontend'])
            self.log(f"🌐 Frontend Panels: {frontend_working}/{frontend_total} accessible", "INFO")
        
        if 'missing_features' in self.results and self.results['missing_features']:
            self.log(f"\n❌ Missing Critical Features:", "ERROR")
            for feature in self.results['missing_features']:
                self.log(f"   - {feature}", "ERROR")
        else:
            self.log("\n✅ No critical missing features detected", "SUCCESS")
        
        # Save results to file
        with open('system_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        self.log(f"\n📄 Detailed results saved to system_test_results.json", "INFO")

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_comprehensive_test()
