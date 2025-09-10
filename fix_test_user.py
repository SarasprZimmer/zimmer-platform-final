#!/usr/bin/env python3
"""
Fix the test user configuration
"""

import sys
import os
import sqlite3

def fix_test_user():
    """Fix the test user configuration"""
    print("🔧 Fixing test user configuration...")
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update the test user to ensure it's properly configured
        cursor.execute("""
            UPDATE users 
            SET is_active = 1, 
                role = 'user',
                email_verified_at = datetime('now')
            WHERE email = 'test@example.com'
        """)
        
        conn.commit()
        
        # Verify the user
        cursor.execute("SELECT id, email, is_active, role, email_verified_at FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()
        
        if user:
            print("✅ Test user updated:")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Is Active: {user[2]}")
            print(f"   Role: {user[3]}")
            print(f"   Email Verified: {user[4]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error fixing user: {e}")
        return False

if __name__ == "__main__":
    success = fix_test_user()
    sys.exit(0 if success else 1)
