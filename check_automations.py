#!/usr/bin/env python3
"""
Check automations in the database
"""

import sys
import os
import sqlite3

def check_automations():
    """Check automations in the database"""
    print("🤖 Checking automations in database...")
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all automations
        cursor.execute("SELECT id, name, description, status, is_listed, health_status FROM automations")
        automations = cursor.fetchall()
        
        print(f"✅ Found {len(automations)} automations:")
        for auto in automations:
            print(f"   - ID: {auto[0]}, Name: {auto[1]}, Status: {auto[3]}, Listed: {auto[4]}, Health: {auto[5]}")
        
        conn.close()
        
        if len(automations) == 0:
            print("\n⚠️ No automations found! Creating a test automation...")
            create_test_automation()
        
    except Exception as e:
        print(f"❌ Error checking automations: {e}")

def create_test_automation():
    """Create a test automation"""
    try:
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'zimmer-backend', 'dev.db'))
        cursor = conn.cursor()
        
        # Create test automation
        cursor.execute("""
            INSERT INTO automations (name, description, pricing_type, price_per_token, status, is_listed, health_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Test Automation",
            "A test automation for testing the 5-token system",
            "per_token",
            0.01,  # 1 cent per token
            True,  # status
            True,  # is_listed
            "healthy",  # health_status
            "2025-01-10T00:00:00Z"  # created_at
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Test automation created!")
        
    except Exception as e:
        print(f"❌ Error creating test automation: {e}")

if __name__ == "__main__":
    check_automations()
