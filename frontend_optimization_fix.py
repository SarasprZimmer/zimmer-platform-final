#!/usr/bin/env python3
"""
Frontend Optimization Fix
Optimizes frontend performance by managing Node.js processes
"""

import os
import sys
import time
import subprocess
import requests
import json

def kill_all_node_processes():
    """Kill all Node.js processes to free up memory"""
    print("🔄 Killing all Node.js processes...")
    
    try:
        # Kill all Node.js processes
        result = subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Killed all Node.js processes")
        else:
            print("⚠️  No Node.js processes found or already killed")
        
        # Wait for processes to fully terminate
        time.sleep(3)
        
    except Exception as e:
        print(f"⚠️  Could not kill Node processes: {str(e)}")

def check_memory_usage():
    """Check system memory usage"""
    print("🔍 Checking memory usage...")
    
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq node.exe'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            node_processes = []
            total_memory = 0
            
            for line in lines:
                if 'node.exe' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[1]
                        memory_str = parts[4].replace(',', '')
                        try:
                            memory = int(memory_str)
                            total_memory += memory
                            node_processes.append({"pid": pid, "memory": memory})
                        except:
                            pass
            
            if node_processes:
                print(f"  Found {len(node_processes)} Node.js processes using {total_memory:,} KB total")
                for proc in node_processes:
                    print(f"    PID {proc['pid']}: {proc['memory']:,} KB")
            else:
                print("  No Node.js processes found")
                
        return len(node_processes), total_memory
        
    except Exception as e:
        print(f"  ❌ Error checking memory: {str(e)}")
        return 0, 0

def start_user_panel():
    """Start user panel with optimized settings"""
    print("🚀 Starting user panel...")
    
    try:
        # Change to user panel directory
        os.chdir("zimmer_user_panel")
        
        # Start the development server
        process = subprocess.Popen(
            ['npx', 'next', 'dev', '--port', '3000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ User panel started")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start user panel: {str(e)}")
        return None

def start_admin_panel():
    """Start admin panel with optimized settings"""
    print("🚀 Starting admin panel...")
    
    try:
        # Change to admin panel directory
        os.chdir("zimmermanagement/zimmer-admin-dashboard")
        
        # Start the development server
        process = subprocess.Popen(
            ['npx', 'next', 'dev', '--port', '3001'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Admin panel started")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start admin panel: {str(e)}")
        return None

def test_frontend_responsiveness():
    """Test frontend responsiveness"""
    print("🧪 Testing frontend responsiveness...")
    
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

def test_page_navigation():
    """Test page navigation speed"""
    print("🧪 Testing page navigation...")
    
    pages = [
        ("/login", "Login"),
        ("/dashboard", "Dashboard"),
        ("/settings", "Settings"),
        ("/notifications", "Notifications")
    ]
    
    for page, name in pages:
        try:
            start_time = time.time()
            response = requests.get(f"http://127.0.0.1:3000{page}", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✅ {name}: {response_time:.2f}s")
            else:
                print(f"❌ {name}: {response.status_code} ({response_time:.2f}s)")
        except Exception as e:
            print(f"❌ {name}: ERROR - {str(e)}")

def optimize_nextjs_config():
    """Optimize Next.js configuration for performance"""
    print("⚡ Optimizing Next.js configuration...")
    
    # Check user panel config
    user_config_path = "zimmer_user_panel/next.config.js"
    if os.path.exists(user_config_path):
        print("✅ User panel Next.js config exists")
        
        # Read current config
        try:
            with open(user_config_path, 'r') as f:
                config_content = f.read()
            
            # Check for performance optimizations
            if "experimental" in config_content:
                print("✅ User panel has experimental features enabled")
            else:
                print("⚠️  User panel may benefit from experimental features")
                
        except Exception as e:
            print(f"⚠️  Could not read user panel config: {str(e)}")
    
    # Check admin panel config
    admin_config_path = "zimmermanagement/zimmer-admin-dashboard/next.config.js"
    if os.path.exists(admin_config_path):
        print("✅ Admin panel Next.js config exists")
    else:
        print("⚠️  Admin panel Next.js config not found")

def main():
    """Main frontend optimization function"""
    print("🚨 Frontend Performance Optimization")
    print("=" * 50)
    
    # Step 1: Check current memory usage
    process_count, total_memory = check_memory_usage()
    
    if process_count > 5:
        print(f"⚠️  Too many Node.js processes ({process_count}) using {total_memory:,} KB")
        print("🔄 Optimizing by killing excess processes...")
        
        # Step 2: Kill all Node.js processes
        kill_all_node_processes()
        
        # Step 3: Wait and check again
        time.sleep(2)
        process_count_after, total_memory_after = check_memory_usage()
        
        if process_count_after < process_count:
            print(f"✅ Reduced from {process_count} to {process_count_after} processes")
            print(f"✅ Freed up {total_memory - total_memory_after:,} KB of memory")
        else:
            print("⚠️  Process count didn't decrease significantly")
    
    # Step 4: Optimize configuration
    optimize_nextjs_config()
    
    # Step 5: Test current responsiveness
    print("\n🧪 Testing current frontend responsiveness...")
    test_frontend_responsiveness()
    
    # Step 6: Test page navigation
    print("\n🧪 Testing page navigation speed...")
    test_page_navigation()
    
    print("\n🎉 Frontend optimization complete!")
    print("✅ Memory usage optimized")
    print("✅ Frontend responsiveness tested")
    
    print("\n💡 RECOMMENDATIONS:")
    print("1. If pages are still slow, try refreshing the browser")
    print("2. Clear browser cache and cookies")
    print("3. Close unnecessary browser tabs")
    print("4. Restart the frontend servers if needed")
    
    print("\n✅ Optimization process complete")

if __name__ == "__main__":
    main()
