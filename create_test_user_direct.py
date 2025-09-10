#!/usr/bin/env python3
"""
Create a test user directly in the database
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
    """Create a test user directly in the database"""
    print("👤 Creating test user directly in database...")
    
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
        
        # Create new user
        password_hash = hash_password("testpassword123")
        now = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, name, phone_number, role, is_active, email_verified, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "test@example.com",
            password_hash,
            "Test User",
            "1234567890",
            "user",
            True,
            True,
            now,
            now
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
