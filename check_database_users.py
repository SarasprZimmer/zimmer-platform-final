#!/usr/bin/env python3
"""
Check users in the database directly
"""

import sys
import os
import sqlite3

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'zimmer-backend'))

def check_database_users():
    """Check users directly in the database"""
    print("🔍 Checking users in database...")
    
    # Connect to the database
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    print(f"Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute("SELECT id, email, name, role FROM users")
        users = cursor.fetchall()
        
        print(f"✅ Found {len(users)} users in database:")
        for user in users:
            print(f"   - ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}")
        
        conn.close()
        
        # Try to create a test user if none exist
        if len(users) == 0:
            print("\n👤 No users found, creating a test user...")
            create_test_user()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

def create_test_user():
    """Create a test user directly in the database"""
    try:
        # Import the backend modules
        from zimmer_backend.database import SessionLocal
        from zimmer_backend.models.user import User
        from zimmer_backend.utils.security import hash_password
        
        db = SessionLocal()
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("✅ Test user already exists!")
            db.close()
            return
        
        # Create new user
        new_user = User(
            email="test@example.com",
            password_hash=hash_password("testpassword123"),
            name="Test User",
            phone_number="1234567890",
            role="user",
            is_active=True,
            email_verified=True
        )
        
        db.add(new_user)
        db.commit()
        db.close()
        
        print("✅ Test user created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")

if __name__ == "__main__":
    check_database_users()
