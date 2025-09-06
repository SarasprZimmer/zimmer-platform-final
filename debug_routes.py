#!/usr/bin/env python3
"""
Debug what routes are actually registered in the server
"""

import requests
import json

def debug_routes():
    try:
        # Get the OpenAPI spec
        response = requests.get('http://127.0.0.1:8000/openapi.json')
        if response.status_code == 200:
            openapi_spec = response.json()
            paths = openapi_spec.get('paths', {})
            
            print("All routes containing 'openai' or 'keys':")
            print("=" * 50)
            
            matching_routes = []
            for path in paths.keys():
                if 'openai' in path.lower() or 'keys' in path.lower():
                    matching_routes.append(path)
            
            if matching_routes:
                for route in matching_routes:
                    methods = list(paths[route].keys())
                    print(f"  {route} -> {methods}")
            else:
                print("No routes containing 'openai' or 'keys' found")
                
            print(f"\nTotal routes: {len(paths)}")
            
            # Check for any routes that might conflict
            print("\nAdmin routes that might conflict:")
            admin_routes = [path for path in paths.keys() if '/api/admin/' in path]
            for route in admin_routes:
                if 'test' in route or 'key' in route.lower():
                    methods = list(paths[route].keys())
                    print(f"  {route} -> {methods}")
                    
        else:
            print(f"Could not access OpenAPI spec: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_routes()
