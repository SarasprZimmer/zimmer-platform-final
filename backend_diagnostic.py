#!/usr/bin/env python3
"""
Backend Diagnostic Script
Identifies and fixes backend performance issues
"""

import os
import sys
import time
import sqlite3
import requests
from pathlib import Path

def check_database_connectivity():
    """Check database connectivity and performance"""
    print("🔍 Checking database connectivity...")
    
    db_path = "instance/database.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        # Check database file size
        db_size = os.path.getsize(db_path)
        print(f"📊 Database size: {db_size / (1024*1024):.2f} MB")
        
        # Test database connection
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        # Test basic query
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        query_time = time.time() - start_time
        
        print(f"✅ Database connection successful")
        print(f"📊 Users count: {result[0]}")
        print(f"⏱️  Query time: {query_time:.3f}s")
        
        # Check for long-running queries
        if query_time > 1.0:
            print("⚠️  Database queries are slow")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def check_backend_processes():
    """Check backend process status"""
    print("\n🔍 Checking backend processes...")
    
    try:
        import psutil
        
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            if 'python' in proc.info['name'].lower():
                python_processes.append(proc.info)
        
        print(f"📊 Found {len(python_processes)} Python processes:")
        for proc in python_processes:
            memory_mb = proc['memory_info'].rss / (1024 * 1024)
            print(f"  PID {proc['pid']}: {proc['name']} - CPU: {proc['cpu_percent']:.1f}%, Memory: {memory_mb:.1f}MB")
        
        return python_processes
        
    except ImportError:
        print("⚠️  psutil not available, cannot check process details")
        return []

def check_backend_endpoints():
    """Check backend endpoint responsiveness"""
    print("\n🔍 Checking backend endpoints...")
    
    endpoints = [
        "/test-cors",
        "/api/auth/csrf", 
        "/api/me",
        "/api/notifications"
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", timeout=10)
            response_time = time.time() - start_time
            
            results[endpoint] = {
                "status": response.status_code,
                "time": response_time,
                "success": True
            }
            
            status_icon = "✅" if response.status_code in [200, 401] else "❌"
            print(f"  {status_icon} {endpoint}: {response.status_code} ({response_time:.2f}s)")
            
        except requests.exceptions.Timeout:
            results[endpoint] = {
                "status": "TIMEOUT",
                "time": 10.0,
                "success": False
            }
            print(f"  ❌ {endpoint}: TIMEOUT (>10s)")
            
        except Exception as e:
            results[endpoint] = {
                "status": "ERROR",
                "time": 0,
                "success": False
            }
            print(f"  ❌ {endpoint}: ERROR - {str(e)}")
    
    return results

def check_database_queries():
    """Check for problematic database queries"""
    print("\n🔍 Checking database query performance...")
    
    db_path = "instance/database.db"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        # Check table sizes
        tables = ['users', 'sessions', 'notifications', 'token_usage', 'payments']
        
        for table in tables:
            try:
                start_time = time.time()
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                query_time = time.time() - start_time
                
                status = "✅" if query_time < 0.1 else "⚠️" if query_time < 1.0 else "❌"
                print(f"  {status} {table}: {count} records ({query_time:.3f}s)")
                
            except Exception as e:
                print(f"  ❌ {table}: ERROR - {str(e)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database query check failed: {str(e)}")

def check_session_issues():
    """Check for session-related issues"""
    print("\n🔍 Checking session management...")
    
    db_path = "instance/database.db"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        # Check session count
        cursor.execute("SELECT COUNT(*) FROM sessions")
        session_count = cursor.fetchone()[0]
        print(f"📊 Total sessions: {session_count}")
        
        # Check for expired sessions
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE expires_at < datetime('now')")
        expired_count = cursor.fetchone()[0]
        print(f"📊 Expired sessions: {expired_count}")
        
        # Check for old sessions
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE created_at < datetime('now', '-7 days')")
        old_count = cursor.fetchone()[0]
        print(f"📊 Sessions older than 7 days: {old_count}")
        
        if session_count > 1000:
            print("⚠️  High session count may cause performance issues")
        
        if expired_count > 100:
            print("⚠️  Many expired sessions should be cleaned up")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Session check failed: {str(e)}")

def cleanup_expired_sessions():
    """Clean up expired sessions"""
    print("\n🧹 Cleaning up expired sessions...")
    
    db_path = "instance/database.db"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        # Count expired sessions before cleanup
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE expires_at < datetime('now')")
        expired_before = cursor.fetchone()[0]
        
        # Delete expired sessions
        cursor.execute("DELETE FROM sessions WHERE expires_at < datetime('now')")
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Cleaned up {deleted_count} expired sessions")
        
    except Exception as e:
        print(f"❌ Session cleanup failed: {str(e)}")

def optimize_database():
    """Optimize database performance"""
    print("\n⚡ Optimizing database...")
    
    db_path = "instance/database.db"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        # Run VACUUM to optimize database
        print("  Running VACUUM...")
        cursor.execute("VACUUM")
        
        # Analyze tables for better query planning
        print("  Analyzing tables...")
        cursor.execute("ANALYZE")
        
        conn.close()
        print("✅ Database optimization complete")
        
    except Exception as e:
        print(f"❌ Database optimization failed: {str(e)}")

def main():
    """Main diagnostic function"""
    print("🔧 Backend Diagnostic Tool")
    print("=" * 50)
    
    # Check database connectivity
    db_ok = check_database_connectivity()
    
    # Check backend processes
    processes = check_backend_processes()
    
    # Check backend endpoints
    endpoint_results = check_backend_endpoints()
    
    # Check database queries
    check_database_queries()
    
    # Check session issues
    check_session_issues()
    
    # Cleanup expired sessions
    cleanup_expired_sessions()
    
    # Optimize database
    optimize_database()
    
    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    working_endpoints = sum(1 for r in endpoint_results.values() if r["success"])
    total_endpoints = len(endpoint_results)
    
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"Backend Processes: {len(processes)}")
    print(f"Working Endpoints: {working_endpoints}/{total_endpoints}")
    
    if working_endpoints < total_endpoints:
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. Restart the backend server")
        print("2. Check for memory leaks")
        print("3. Monitor database performance")
        print("4. Review session management")
    
    print("\n✅ Diagnostic complete")

if __name__ == "__main__":
    main()
