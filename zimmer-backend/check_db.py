#!/usr/bin/env python3
import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('zimmer_dashboard.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("Database Tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_database() 