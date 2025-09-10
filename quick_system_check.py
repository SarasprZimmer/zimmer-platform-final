#!/usr/bin/env python3
"""
Quick System Check - Test what's working and what's missing
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
        
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {description}: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ {description}: Error - {e}")
        return False

def main():
    print("🔍 Quick System Check")
    print("=" * 40)
    
    # Test backend health
    print("\n1. Backend Health:")
    test_endpoint("/", "GET", description="Backend root")
    
    # Test authentication endpoints
    print("\n2. Authentication:")
    test_endpoint("/api/auth/login", "POST", 
                 {"email": "test@zimmer.ai", "password": "testpass123"}, 
                 "Login endpoint")
    test_endpoint("/api/auth/register", "POST", 
                 {"name": "Test", "email": "test2@zimmer.ai", "password": "test123", "phone_number": "+1234567890"}, 
                 "Register endpoint")
    
    # Test user endpoints (without auth for now)
    print("\n3. User Endpoints:")
    test_endpoint("/api/me", "GET", description="User profile")
    test_endpoint("/api/user/settings", "GET", description="User settings")
    test_endpoint("/api/user/dashboard", "GET", description="User dashboard")
    test_endpoint("/api/user/automations/active", "GET", description="Active automations")
    test_endpoint("/api/user/usage/distribution", "GET", description="Usage distribution")
    
    # Test admin endpoints
    print("\n4. Admin Endpoints:")
    test_endpoint("/api/admin/users", "GET", description="List users")
    test_endpoint("/api/admin/users/stats", "GET", description="User stats")
    test_endpoint("/api/admin/openai-keys", "GET", description="OpenAI keys")
    test_endpoint("/api/admin/analytics", "GET", description="Analytics")
    
    print("\n" + "=" * 40)
    print("Check complete!")

if __name__ == "__main__":
    main()
