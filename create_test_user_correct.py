#!/usr/bin/env python3
"""
Create a test user with correct database schema
"""

import sys
import os
import sqlite3
import hashlib
import secrets
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_test_user():
    """Create a test user with correct schema"""
    print("👤 Creating test user with correct schema...")
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    print(f"Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",))
        existing = cursor.fetchone()
        
        if existing:
            print("✅ Test user already exists!")
            conn.close()
            return True
        
        # Create new user with correct schema
        password_hash = hash_password("testpassword123")
        now = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO users (name, email, phone_number, password_hash, role, is_active, created_at, email_verified_at, twofa_enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Test User",
            "test@example.com",
            "1234567890",
            password_hash,
            "user",
            True,
            now,
            now,  # email_verified_at
            False  # twofa_enabled
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Test user created successfully!")
        print("   Email: test@example.com")
        print("   Password: testpassword123")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

if __name__ == "__main__":
    success = create_test_user()
    sys.exit(0 if success else 1)
