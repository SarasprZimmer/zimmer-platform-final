#!/usr/bin/env python3
"""
Create user automation directly in database to test 5-token system
"""

import sys
import os
import sqlite3
from datetime import datetime

def create_user_automation_direct():
    """Create user automation directly in database"""
    print("🤖 Creating user automation directly in database...")
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()
        
        if not user:
            print("❌ Test user not found!")
            return False
        
        user_id = user[0]
        print(f"✅ Found user ID: {user_id}")
        
        # Get automation ID
        cursor.execute("SELECT id FROM automations WHERE name = ?", ("Test Automation",))
        automation = cursor.fetchone()
        
        if not automation:
            print("❌ Test automation not found!")
            return False
        
        automation_id = automation[0]
        print(f"✅ Found automation ID: {automation_id}")
        
        # Check if user already has this automation
        cursor.execute("SELECT id FROM user_automations WHERE user_id = ? AND automation_id = ?", 
                      (user_id, automation_id))
        existing = cursor.fetchone()
        
        if existing:
            print("✅ User already has this automation!")
            return True
        
        # Create user automation with 5 tokens by default
        now = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO user_automations 
            (user_id, automation_id, telegram_bot_token, tokens_remaining, demo_tokens, 
             is_demo_active, demo_expired, status, provisioned_at, integration_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            automation_id,
            None,  # telegram_bot_token
            5,     # tokens_remaining - 5 tokens by default
            5,     # demo_tokens
            True,  # is_demo_active
            False, # demo_expired
            "active",  # status
            now,   # provisioned_at
            "pending", # integration_status
            now    # created_at
        ))
        
        conn.commit()
        
        # Verify the creation
        cursor.execute("SELECT id, tokens_remaining, demo_tokens FROM user_automations WHERE user_id = ? AND automation_id = ?", 
                      (user_id, automation_id))
        created = cursor.fetchone()
        
        if created:
            print("✅ User automation created successfully!")
            print(f"   User Automation ID: {created[0]}")
            print(f"   Tokens Remaining: {created[1]}")
            print(f"   Demo Tokens: {created[2]}")
            
            if created[1] == 5:
                print("✅ SUCCESS: User got 5 tokens by default!")
                return True
            else:
                print(f"❌ FAILED: Expected 5 tokens, got {created[1]}")
                return False
        else:
            print("❌ Failed to create user automation!")
            return False
        
    except Exception as e:
        print(f"❌ Error creating user automation: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    success = create_user_automation_direct()
    sys.exit(0 if success else 1)
