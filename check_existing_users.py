#!/usr/bin/env python3
"""
Check existing users in the system
"""

import requests
import json
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'zimmer-backend'))

# Configuration
BASE_URL = "http://localhost:8000"

def check_existing_users():
    """Check what users exist in the system"""
    print("👥 Checking existing users...")
    
    # Try to get users (this might require admin access)
    try:
        response = requests.get(f"{BASE_URL}/api/admin/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"   - {user.get('email', 'N/A')} (ID: {user.get('id', 'N/A')})")
        else:
            print(f"❌ Failed to get users: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error getting users: {e}")
    
    # Try some common test emails
    test_emails = [
        "test@example.com",
        "saraspr1899@gmail.com",
        "admin@zimmer.com",
        "user@example.com"
    ]
    
    print("\n🔍 Testing common email addresses...")
    for email in test_emails:
        try:
            # Try to login with each email
            login_data = {
                "email": email,
                "password": "testpassword123"
            }
            response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
            if response.status_code == 200:
                print(f"✅ {email} - Login successful!")
                return email
            else:
                print(f"❌ {email} - Login failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {email} - Error: {e}")
    
    return None

if __name__ == "__main__":
    working_email = check_existing_users()
    if working_email:
        print(f"\n🎯 Use this email for testing: {working_email}")
    else:
        print("\n❌ No working email found")
