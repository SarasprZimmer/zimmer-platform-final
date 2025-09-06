#!/usr/bin/env python3
"""
Admin Panel Data Audit Script
Tests all admin panel API endpoints to ensure data is loading correctly
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin@zimmer.com"
ADMIN_PASSWORD = "admin123"  # Default admin password

class AdminPanelAuditor:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "endpoints_tested": 0,
            "endpoints_passed": 0,
            "endpoints_failed": 0,
            "issues": [],
            "recommendations": []
        }

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def authenticate(self):
        """Authenticate as admin user"""
        try:
            self.log("Authenticating as admin user...")
            response = self.session.post(f"{BASE_URL}/api/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                })
                self.log("Authentication successful")
                return True
            else:
                self.log(f"Authentication failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Authentication error: {str(e)}", "ERROR")
            return False

    def test_endpoint(self, method, endpoint, expected_fields=None, description=""):
        """Test a single API endpoint"""
        self.results["endpoints_tested"] += 1
        url = f"{BASE_URL}{endpoint}"
        
        try:
            self.log(f"Testing {method} {endpoint} - {description}")
            
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json={})
            else:
                self.log(f"Unsupported method: {method}", "ERROR")
                return False
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ {endpoint} - Status: {response.status_code}")
                
                # Check for expected fields
                if expected_fields:
                    missing_fields = []
                    for field in expected_fields:
                        if field not in data:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        self.results["issues"].append({
                            "endpoint": endpoint,
                            "issue": f"Missing expected fields: {missing_fields}",
                            "severity": "WARNING"
                        })
                        self.log(f"⚠️  {endpoint} - Missing fields: {missing_fields}", "WARNING")
                    else:
                        self.log(f"✅ {endpoint} - All expected fields present")
                
                self.results["endpoints_passed"] += 1
                return True
            else:
                self.log(f"❌ {endpoint} - Status: {response.status_code} - {response.text}", "ERROR")
                self.results["issues"].append({
                    "endpoint": endpoint,
                    "issue": f"HTTP {response.status_code}: {response.text}",
                    "severity": "ERROR"
                })
                self.results["endpoints_failed"] += 1
                return False
                
        except Exception as e:
            self.log(f"❌ {endpoint} - Exception: {str(e)}", "ERROR")
            self.results["issues"].append({
                "endpoint": endpoint,
                "issue": f"Exception: {str(e)}",
                "severity": "ERROR"
            })
            self.results["endpoints_failed"] += 1
            return False

    def run_audit(self):
        """Run comprehensive audit of all admin panel endpoints"""
        self.log("Starting Admin Panel Data Audit")
        
        # Authenticate first
        if not self.authenticate():
            self.log("Cannot proceed without authentication", "ERROR")
            return False
        
        # Test all admin endpoints
        endpoints_to_test = [
            # Core admin endpoints
            ("GET", "/api/admin/users", ["total_count", "users"], "Users list"),
            ("GET", "/api/admin/payments", ["total_count", "payments"], "Payments list"),
            ("GET", "/api/admin/tickets", ["total_count", "tickets"], "Tickets list"),
            ("GET", "/api/admin/automations", ["total_count", "automations"], "Automations list"),
            ("GET", "/api/admin/user-automations", None, "User automations list"),
            ("GET", "/api/admin/usage/stats", None, "Usage statistics"),
            
            # Knowledge base endpoints
            ("GET", "/api/admin/knowledge", None, "Knowledge base list"),
            ("GET", "/api/admin/kb-templates", None, "KB templates list"),
            ("GET", "/api/admin/kb-monitoring", None, "KB monitoring"),
            
            # System endpoints
            ("GET", "/api/admin/system/status", None, "System status"),
            ("GET", "/api/admin/backups", None, "Backups list"),
            
            # Discount endpoints
            ("GET", "/api/admin/discounts", None, "Discounts list"),
            
            # OpenAI keys - use the correct endpoint (no openai-keys prefix)
            ("GET", "/api/admin/list", None, "OpenAI keys list"),
            
            # Fallback logs
            ("GET", "/api/admin/fallbacks", None, "Fallback logs"),
            
            # Notifications
            ("GET", "/api/notifications", None, "Notifications"),
        ]
        
        # Test each endpoint
        for method, endpoint, expected_fields, description in endpoints_to_test:
            self.test_endpoint(method, endpoint, expected_fields, description)
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Print summary
        self.print_summary()
        
        return self.results["endpoints_failed"] == 0

    def generate_recommendations(self):
        """Generate recommendations based on audit results"""
        recommendations = []
        
        # Check for common issues
        error_endpoints = [issue["endpoint"] for issue in self.results["issues"] if issue["severity"] == "ERROR"]
        
        if error_endpoints:
            recommendations.append({
                "priority": "HIGH",
                "issue": f"{len(error_endpoints)} endpoints are failing",
                "action": "Fix failing endpoints: " + ", ".join(error_endpoints)
            })
        
        # Check for missing fields
        missing_field_issues = [issue for issue in self.results["issues"] if "Missing expected fields" in issue["issue"]]
        if missing_field_issues:
            recommendations.append({
                "priority": "MEDIUM",
                "issue": "Some endpoints missing expected fields",
                "action": "Update frontend to handle actual API response structure"
            })
        
        # Check success rate
        success_rate = (self.results["endpoints_passed"] / self.results["endpoints_tested"]) * 100 if self.results["endpoints_tested"] > 0 else 0
        if success_rate < 80:
            recommendations.append({
                "priority": "HIGH",
                "issue": f"Low success rate: {success_rate:.1f}%",
                "action": "Investigate and fix failing endpoints"
            })
        elif success_rate < 95:
            recommendations.append({
                "priority": "MEDIUM",
                "issue": f"Moderate success rate: {success_rate:.1f}%",
                "action": "Review and improve endpoint reliability"
            })
        
        self.results["recommendations"] = recommendations

    def print_summary(self):
        """Print audit summary"""
        print("\n" + "="*60)
        print("ADMIN PANEL DATA AUDIT SUMMARY")
        print("="*60)
        
        total = self.results["endpoints_tested"]
        passed = self.results["endpoints_passed"]
        failed = self.results["endpoints_failed"]
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"Endpoints Tested: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.results["issues"]:
            print(f"\nIssues Found: {len(self.results['issues'])}")
            for issue in self.results["issues"]:
                print(f"  - {issue['endpoint']}: {issue['issue']} ({issue['severity']})")
        
        if self.results["recommendations"]:
            print(f"\nRecommendations:")
            for rec in self.results["recommendations"]:
                print(f"  [{rec['priority']}] {rec['action']}")
        
        print("="*60)

def main():
    auditor = AdminPanelAuditor()
    success = auditor.run_audit()
    
    # Save results to file
    with open("admin_panel_audit_results.json", "w", encoding="utf-8") as f:
        json.dump(auditor.results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: admin_panel_audit_results.json")
    
    if success:
        print("✅ All endpoints are working correctly!")
        sys.exit(0)
    else:
        print("❌ Some endpoints have issues that need attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()
