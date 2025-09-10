#!/usr/bin/env python3
"""
Check the database schema
"""

import sys
import os
import sqlite3

def check_database_schema():
    """Check the database schema"""
    print("🔍 Checking database schema...")
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    print(f"Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 Users table schema:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - Default: {col[4]}")
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📋 All tables ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking schema: {e}")

if __name__ == "__main__":
    check_database_schema()
