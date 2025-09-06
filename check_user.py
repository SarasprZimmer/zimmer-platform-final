#!/usr/bin/env python3
"""
Simple script to check if saraspr1899@gmail.com exists in the database
"""

import sqlite3
import sys
import os

def check_user():
    # Try to find the database file
    db_paths = [
        "zimmer-backend/zimmer_dashboard.db",  # This is the correct one!
        "dev.db",
        "zimmer-backend/dev.db",
        "zimmer_dashboard.db",
        "zimmer-backend/database.db"
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ Database file not found")
        return
    
    print(f"📁 Found database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables in database: {[table[0] for table in tables]}")
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Users table not found")
            return
        
        # Check the structure of the users table
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print("📋 Users table structure:")
        for col in columns:
            print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Get all users (adjust column names based on actual structure)
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        print(f"📊 Total users in database: {len(users)}")
        if users:
            print("\n👥 All users:")
            print("-" * 100)
            for i, user in enumerate(users):
                print(f"User {i+1}: {user}")
        
        # Check specifically for saraspr1899@gmail.com
        cursor.execute("SELECT * FROM users WHERE email = ?", ("saraspr1899@gmail.com",))
        target_user = cursor.fetchone()
        
        if target_user:
            print(f"\n✅ Found target user: saraspr1899@gmail.com")
            print(f"   Data: {target_user}")
        else:
            print(f"\n❌ Target user saraspr1899@gmail.com not found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

if __name__ == "__main__":
    check_user()
