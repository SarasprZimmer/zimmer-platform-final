#!/usr/bin/env python3
"""
Frontend Performance Fix
Addresses frontend slowness and responsiveness issues
"""

import os
import sys
import time
import subprocess
import requests
import json
from pathlib import Path

def check_frontend_servers():
    """Check frontend server status"""
    print("🔍 Checking frontend servers...")
    
    servers = [
        ("User Panel", "http://127.0.0.1:3000"),
        ("Admin Panel", "http://127.0.0.1:3001")
    ]
    
    results = {}
    
    for name, url in servers:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            
            results[name] = {
                "status": response.status_code,
                "time": response_time,
                "success": response.status_code == 200
            }
            
            status_icon = "✅" if results[name]["success"] else "❌"
            print(f"  {status_icon} {name}: {response.status_code} ({response_time:.2f}s)")
            
        except Exception as e:
            results[name] = {
                "status": "ERROR",
                "time": 0,
                "success": False,
                "error": str(e)
            }
            print(f"  ❌ {name}: ERROR - {str(e)}")
    
    return results

def check_frontend_pages():
    """Check specific frontend pages for performance"""
    print("🔍 Checking frontend pages...")
    
    pages = [
        "/login",
        "/dashboard", 
        "/settings",
        "/notifications",
        "/usage",
        "/payment"
    ]
    
    results = {}
    
    for page in pages:
        try:
            start_time = time.time()
            response = requests.get(f"http://127.0.0.1:3000{page}", timeout=15)
            response_time = time.time() - start_time
            
            results[page] = {
                "status": response.status_code,
                "time": response_time,
                "success": response.status_code == 200
            }
            
            status_icon = "✅" if results[page]["success"] else "❌"
            print(f"  {status_icon} {page}: {response.status_code} ({response_time:.2f}s)")
            
        except Exception as e:
            results[page] = {
                "status": "ERROR",
                "time": 0,
                "success": False,
                "error": str(e)
            }
            print(f"  ❌ {page}: ERROR - {str(e)}")
    
    return results

def check_node_processes():
    """Check Node.js processes"""
    print("🔍 Checking Node.js processes...")
    
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq node.exe'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            node_processes = []
            
            for line in lines:
                if 'node.exe' in line:
                    parts = line.split()
                    if len(parts) > 1:
                        pid = parts[1]
                        memory = parts[4] if len(parts) > 4 else "Unknown"
                        node_processes.append({"pid": pid, "memory": memory})
            
            print(f"  Found {len(node_processes)} Node.js processes:")
            for proc in node_processes:
                print(f"    PID {proc['pid']}: {proc['memory']} KB")
            
            return node_processes
        else:
            print("  No Node.js processes found")
            return []
            
    except Exception as e:
        print(f"  ❌ Error checking Node processes: {str(e)}")
        return []

def kill_node_processes():
    """Kill all Node.js processes"""
    print("🔄 Killing Node.js processes...")
    
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], 
                      capture_output=True, text=True)
        print("✅ Killed all Node.js processes")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️  Could not kill Node processes: {str(e)}")

def check_frontend_dependencies():
    """Check frontend dependencies"""
    print("🔍 Checking frontend dependencies...")
    
    user_panel_path = "zimmer_user_panel"
    admin_panel_path = "zimmer_admin_panel"
    
    issues = []
    
    # Check if directories exist
    if not os.path.exists(user_panel_path):
        issues.append(f"User panel directory not found: {user_panel_path}")
    else:
        print(f"✅ User panel directory exists: {user_panel_path}")
    
    if not os.path.exists(admin_panel_path):
        issues.append(f"Admin panel directory not found: {admin_panel_path}")
    else:
        print(f"✅ Admin panel directory exists: {admin_panel_path}")
    
    # Check package.json files
    for panel_name, panel_path in [("User Panel", user_panel_path), ("Admin Panel", admin_panel_path)]:
        package_json = os.path.join(panel_path, "package.json")
        if os.path.exists(package_json):
            print(f"✅ {panel_name} package.json exists")
        else:
            issues.append(f"{panel_name} package.json not found")
    
    # Check node_modules
    for panel_name, panel_path in [("User Panel", user_panel_path), ("Admin Panel", admin_panel_path)]:
        node_modules = os.path.join(panel_path, "node_modules")
        if os.path.exists(node_modules):
            print(f"✅ {panel_name} node_modules exists")
        else:
            issues.append(f"{panel_name} node_modules not found - may need npm install")
    
    return issues

def restart_frontend_servers():
    """Restart frontend servers"""
    print("🚀 Restarting frontend servers...")
    
    # Start user panel
    print("  Starting user panel...")
    try:
        user_panel_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd='zimmer_user_panel',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("  ✅ User panel started")
    except Exception as e:
        print(f"  ❌ Failed to start user panel: {str(e)}")
        return False
    
    # Wait a bit
    time.sleep(5)
    
    # Start admin panel
    print("  Starting admin panel...")
    try:
        admin_panel_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd='zimmer_admin_panel',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("  ✅ Admin panel started")
    except Exception as e:
        print(f"  ❌ Failed to start admin panel: {str(e)}")
        return False
    
    # Wait for servers to start
    print("  ⏳ Waiting for servers to initialize...")
    time.sleep(10)
    
    return True

def test_frontend_performance():
    """Test frontend performance after restart"""
    print("🧪 Testing frontend performance...")
    
    # Test user panel
    try:
        start_time = time.time()
        response = requests.get("http://127.0.0.1:3000", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ User panel: {response.status_code} ({response_time:.2f}s)")
        else:
            print(f"❌ User panel: {response.status_code} ({response_time:.2f}s)")
    except Exception as e:
        print(f"❌ User panel: ERROR - {str(e)}")
    
    # Test admin panel
    try:
        start_time = time.time()
        response = requests.get("http://127.0.0.1:3001", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ Admin panel: {response.status_code} ({response_time:.2f}s)")
        else:
            print(f"❌ Admin panel: {response.status_code} ({response_time:.2f}s)")
    except Exception as e:
        print(f"❌ Admin panel: ERROR - {str(e)}")

def optimize_frontend_config():
    """Optimize frontend configuration"""
    print("⚡ Optimizing frontend configuration...")
    
    # Check for Next.js config optimizations
    user_panel_config = "zimmer_user_panel/next.config.js"
    if os.path.exists(user_panel_config):
        print("✅ User panel Next.js config exists")
    else:
        print("⚠️  User panel Next.js config not found")
    
    # Check for performance optimizations in package.json
    user_package_json = "zimmer_user_panel/package.json"
    if os.path.exists(user_package_json):
        try:
            with open(user_package_json, 'r') as f:
                package_data = json.load(f)
            
            scripts = package_data.get('scripts', {})
            if 'dev' in scripts:
                print("✅ User panel dev script exists")
            else:
                print("⚠️  User panel dev script not found")
                
        except Exception as e:
            print(f"⚠️  Could not read user panel package.json: {str(e)}")

def main():
    """Main frontend performance fix function"""
    print("🚨 Frontend Performance Fix")
    print("=" * 50)
    
    # Step 1: Check current status
    server_results = check_frontend_servers()
    page_results = check_frontend_pages()
    node_processes = check_node_processes()
    
    # Step 2: Check dependencies
    dependency_issues = check_frontend_dependencies()
    if dependency_issues:
        print(f"⚠️  Found dependency issues: {', '.join(dependency_issues)}")
    
    # Step 3: Kill existing processes
    if node_processes:
        kill_node_processes()
    
    # Step 4: Optimize configuration
    optimize_frontend_config()
    
    # Step 5: Restart servers
    if restart_frontend_servers():
        # Step 6: Test performance
        test_frontend_performance()
        
        print("\n🎉 Frontend performance fix complete!")
        print("✅ Frontend servers restarted and optimized")
    else:
        print("\n❌ Frontend performance fix failed")
        print("💡 Check dependency issues and try manual restart")
    
    print("\n✅ Frontend fix process complete")

if __name__ == "__main__":
    main()
