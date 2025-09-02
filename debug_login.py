#!/usr/bin/env python3
"""
Simple script to debug login issues
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_backend():
    """Test backend connectivity and login flow"""
    print("🔍 Testing Zimmer Backend Login Flow...")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False
    
    # Test 2: Seed Data
    print("\n2️⃣ Seeding Test Data...")
    try:
        response = requests.post(f"{BASE_URL}/dev/seed", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Seed failed: {e}")
        
    # Test 3: Login Attempt
    print("\n3️⃣ Testing Login...")
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            return True
        else:
            print(f"   ❌ Login failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Login request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if success:
        print("\n✅ Backend is working correctly!")
    else:
        print("\n❌ Backend has issues that need to be resolved.")
