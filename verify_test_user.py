#!/usr/bin/env python3
"""
Verify the test user and test password hashing
"""

import sys
import os
import sqlite3
import bcrypt

def verify_test_user():
    """Verify the test user and test password"""
    print("🔍 Verifying test user...")
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get the test user
        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()
        
        if not user:
            print("❌ Test user not found!")
            return False
        
        print(f"✅ Test user found:")
        print(f"   ID: {user[0]}")
        print(f"   Email: {user[1]}")
        print(f"   Password hash: {user[2][:50]}...")
        
        # Test password verification
        password = "testpassword123"
        stored_hash = user[2]
        
        print(f"\n🔐 Testing password verification...")
        print(f"   Password: {password}")
        print(f"   Stored hash: {stored_hash[:50]}...")
        
        # Test with bcrypt
        is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f"   Password valid: {is_valid}")
        
        if not is_valid:
            print("❌ Password verification failed!")
            print("   This might be why login is failing.")
            
            # Try to create a new hash
            print("\n🔄 Creating new password hash...")
            new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(f"   New hash: {new_hash[:50]}...")
            
            # Update the user with new hash
            cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (new_hash, "test@example.com"))
            conn.commit()
            print("✅ Updated user with new password hash!")
        
        conn.close()
        return is_valid
        
    except Exception as e:
        print(f"❌ Error verifying user: {e}")
        return False

if __name__ == "__main__":
    success = verify_test_user()
    sys.exit(0 if success else 1)
