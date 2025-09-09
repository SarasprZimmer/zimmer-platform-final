#!/usr/bin/env python3
"""
Detailed System Analysis - Identify what's working vs what's missing
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

class DetailedSystemAnalyzer:
    """Detailed analysis of system components"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Critical endpoints that should be working
        self.critical_endpoints = {
            "Authentication": [
                ("/api/auth/login", "POST"),
                ("/api/auth/logout", "POST"), 
                ("/api/auth/refresh", "POST"),
                ("/api/auth/csrf", "GET"),
                ("/api/auth/register", "POST"),
            ],
            "User Management": [
                ("/api/me", "GET"),
                ("/api/user/dashboard", "GET"),
                ("/api/user/profile", "GET"),
                ("/api/user/settings", "GET"),
                ("/api/user/password", "POST"),
            ],
            "Admin Functions": [
                ("/api/admin/dashboard", "GET"),
                ("/api/admin/users", "GET"),
                ("/api/admin/automations", "GET"),
                ("/api/admin/payments", "GET"),
            ],
            "Automation System": [
                ("/api/automations", "GET"),
                ("/api/automations/marketplace", "GET"),
                ("/api/automations/my-automations", "GET"),
            ],
            "Payment System": [
                ("/api/payments", "GET"),
                ("/api/payments/create", "POST"),
                ("/api/payments/history", "GET"),
            ],
            "Support System": [
                ("/api/support/tickets", "GET"),
                ("/api/support/tickets/create", "POST"),
                ("/api/support/knowledge-base", "GET"),
            ],
            "System Monitoring": [
                ("/health", "GET"),
                ("/api/system/stats", "GET"),
                ("/circuit-breaker/stats", "GET"),
            ]
        }
    
    def test_endpoint_detailed(self, endpoint: str, method: str = "GET") -> Dict[str, Any]:
        """Test endpoint with detailed analysis"""
        try:
            if method == "GET":
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
            elif method == "POST":
                response = self.session.post(f"{self.base_url}{endpoint}", json={}, timeout=10)
            elif method == "PUT":
                response = self.session.put(f"{self.base_url}{endpoint}", json={}, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(f"{self.base_url}{endpoint}", timeout=10)
            
            # Analyze response
            status = "working"
            if response.status_code == 404:
                status = "missing"
            elif response.status_code == 405:
                status = "method_not_allowed"
            elif response.status_code == 401:
                status = "requires_auth"
            elif response.status_code >= 500:
                status = "server_error"
            elif response.status_code >= 400:
                status = "client_error"
            
            return {
                "status": status,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "method": method,
                "endpoint": endpoint,
                "content_type": response.headers.get("content-type", ""),
                "response_size": len(response.content)
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "connection_error",
                "error": "Connection refused",
                "method": method,
                "endpoint": endpoint
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "method": method,
                "endpoint": endpoint
            }
    
    def analyze_system(self) -> Dict[str, Any]:
        """Run detailed system analysis"""
        print("🔍 Running Detailed System Analysis...")
        print("=" * 60)
        
        results = {
            "working": [],
            "missing": [],
            "requires_auth": [],
            "method_not_allowed": [],
            "server_errors": [],
            "client_errors": [],
            "connection_errors": []
        }
        
        for category, endpoints in self.critical_endpoints.items():
            print(f"\n📋 Testing {category}:")
            
            for endpoint, method in endpoints:
                result = self.test_endpoint_detailed(endpoint, method)
                
                # Categorize results
                if result["status"] == "working":
                    results["working"].append((endpoint, method, result))
                    print(f"  ✅ {method} {endpoint} - {result['status_code']}")
                elif result["status"] == "missing":
                    results["missing"].append((endpoint, method, result))
                    print(f"  ❌ {method} {endpoint} - MISSING (404)")
                elif result["status"] == "requires_auth":
                    results["requires_auth"].append((endpoint, method, result))
                    print(f"  🔒 {method} {endpoint} - Requires Auth (401)")
                elif result["status"] == "method_not_allowed":
                    results["method_not_allowed"].append((endpoint, method, result))
                    print(f"  ⚠️  {method} {endpoint} - Method Not Allowed (405)")
                elif result["status"] == "server_error":
                    results["server_errors"].append((endpoint, method, result))
                    print(f"  💥 {method} {endpoint} - Server Error ({result.get('status_code', 'N/A')})")
                elif result["status"] == "connection_error":
                    results["connection_errors"].append((endpoint, method, result))
                    print(f"  🔌 {method} {endpoint} - Connection Error")
                else:
                    results["client_errors"].append((endpoint, method, result))
                    print(f"  ⚠️  {method} {endpoint} - {result['status']}")
        
        return results
    
    def generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Missing endpoints
        if results["missing"]:
            recommendations.append(f"🚨 CRITICAL: {len(results['missing'])} endpoints are completely missing")
            for endpoint, method, _ in results["missing"][:5]:
                recommendations.append(f"   • Implement {method} {endpoint}")
        
        # Method not allowed (might need different HTTP method)
        if results["method_not_allowed"]:
            recommendations.append(f"⚠️  {len(results['method_not_allowed'])} endpoints have method issues")
            for endpoint, method, _ in results["method_not_allowed"][:3]:
                recommendations.append(f"   • Check HTTP method for {endpoint} (tried {method})")
        
        # Server errors
        if results["server_errors"]:
            recommendations.append(f"💥 {len(results['server_errors'])} endpoints have server errors")
            for endpoint, method, _ in results["server_errors"][:3]:
                recommendations.append(f"   • Fix server error in {method} {endpoint}")
        
        # Connection errors
        if results["connection_errors"]:
            recommendations.append(f"🔌 {len(results['connection_errors'])} endpoints have connection issues")
        
        # Positive feedback
        working_count = len(results["working"])
        auth_count = len(results["requires_auth"])
        total_tested = sum(len(category) for category in results.values())
        
        recommendations.append(f"✅ {working_count} endpoints are working correctly")
        recommendations.append(f"🔒 {auth_count} endpoints properly require authentication")
        recommendations.append(f"📊 Overall system health: {round((working_count + auth_count) / total_tested * 100, 1)}%")
        
        return recommendations
    
    def print_summary(self, results: Dict[str, Any], recommendations: List[str]):
        """Print analysis summary"""
        print("\n" + "=" * 60)
        print("📊 DETAILED SYSTEM ANALYSIS SUMMARY")
        print("=" * 60)
        
        # Counts
        working_count = len(results["working"])
        missing_count = len(results["missing"])
        auth_count = len(results["requires_auth"])
        method_issues = len(results["method_not_allowed"])
        server_errors = len(results["server_errors"])
        total_tested = sum(len(category) for category in results.values())
        
        print(f"\n🎯 SYSTEM STATUS:")
        print(f"   ✅ Working Endpoints: {working_count}")
        print(f"   🔒 Protected Endpoints: {auth_count}")
        print(f"   ❌ Missing Endpoints: {missing_count}")
        print(f"   ⚠️  Method Issues: {method_issues}")
        print(f"   💥 Server Errors: {server_errors}")
        print(f"   📊 Total Tested: {total_tested}")
        
        # Health percentage
        healthy_endpoints = working_count + auth_count
        health_percentage = round((healthy_endpoints / total_tested) * 100, 1) if total_tested > 0 else 0
        print(f"   🏥 System Health: {health_percentage}%")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "=" * 60)
        print(f"⏱️  Analysis completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 60)

def main():
    """Main function"""
    analyzer = DetailedSystemAnalyzer()
    results = analyzer.analyze_system()
    recommendations = analyzer.generate_recommendations(results)
    analyzer.print_summary(results, recommendations)
    
    # Save detailed results
    with open("detailed_system_analysis.json", "w") as f:
        json.dump({
            "results": results,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }, f, indent=2, default=str)
    
    print(f"\n💾 Detailed analysis saved to: detailed_system_analysis.json")

if __name__ == "__main__":
    main()
