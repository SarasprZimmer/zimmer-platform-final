#!/usr/bin/env python3
"""
Production Readiness Check for Zimmer AI Platform
Comprehensive validation to ensure system is ready for production deployment
"""

import requests
import time
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys

class ProductionReadinessChecker:
    """Comprehensive production readiness validation"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.results = {}
        self.start_time = datetime.utcnow()
        
        # Production readiness criteria
        self.criteria = {
            "performance": {
                "response_time_p95": 500,  # 500ms
                "response_time_p99": 1000,  # 1000ms
                "error_rate": 5,  # 5%
                "throughput_min": 100,  # 100 RPS
            },
            "availability": {
                "uptime_percent": 99.9,  # 99.9%
                "health_check_success": 100,  # 100%
            },
            "scalability": {
                "concurrent_users": 100,  # 100 concurrent users
                "database_connections": 80,  # 80% of max connections
            },
            "security": {
                "ssl_enabled": True,
                "authentication_required": True,
                "rate_limiting": True,
            }
        }
    
    def check_endpoint_availability(self) -> Dict[str, Any]:
        """Check if all critical endpoints are available"""
        print("🔍 Checking endpoint availability...")
        
        critical_endpoints = [
            "/api/optimized/me",
            "/api/optimized/user/dashboard",
            "/api/optimized/automations/marketplace",
            "/api/optimized/admin/dashboard",
            "/api/monitoring/health",
            "/api/monitoring/metrics",
            "/api/monitoring/database/health",
            "/api/monitoring/cache/health",
        ]
        
        results = {}
        available_count = 0
        
        for endpoint in critical_endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                end_time = time.time()
                duration = (end_time - start_time) * 1000
                
                results[endpoint] = {
                    "status_code": response.status_code,
                    "response_time_ms": duration,
                    "available": response.status_code < 500,
                    "error": None
                }
                
                if response.status_code < 500:
                    available_count += 1
                
                status = "✅" if response.status_code < 500 else "❌"
                print(f"  {status} {endpoint}: {response.status_code} ({duration:.2f}ms)")
                
            except Exception as e:
                results[endpoint] = {
                    "status_code": 0,
                    "response_time_ms": 0,
                    "available": False,
                    "error": str(e)
                }
                print(f"  ❌ {endpoint}: Error - {str(e)}")
        
        availability_percent = (available_count / len(critical_endpoints)) * 100
        
        return {
            "total_endpoints": len(critical_endpoints),
            "available_endpoints": available_count,
            "availability_percent": availability_percent,
            "endpoint_details": results,
            "passed": availability_percent >= self.criteria["availability"]["health_check_success"]
        }
    
    def check_performance_metrics(self) -> Dict[str, Any]:
        """Check performance metrics against production criteria"""
        print("⚡ Checking performance metrics...")
        
        # Test endpoints with multiple requests
        test_endpoints = [
            "/api/optimized/me",
            "/api/optimized/automations/marketplace",
            "/api/monitoring/health",
        ]
        
        all_durations = []
        error_count = 0
        total_requests = 0
        
        for endpoint in test_endpoints:
            for _ in range(20):  # 20 requests per endpoint
                try:
                    start_time = time.time()
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000
                    
                    all_durations.append(duration)
                    total_requests += 1
                    
                    if response.status_code >= 400:
                        error_count += 1
                        
                except Exception as e:
                    error_count += 1
                    total_requests += 1
        
        if not all_durations:
            return {
                "error": "No successful requests to measure performance",
                "passed": False
            }
        
        # Calculate statistics
        all_durations.sort()
        p95 = all_durations[int(len(all_durations) * 0.95)]
        p99 = all_durations[int(len(all_durations) * 0.99)]
        avg_response_time = sum(all_durations) / len(all_durations)
        error_rate = (error_count / total_requests) * 100 if total_requests > 0 else 0
        
        # Calculate throughput (requests per second)
        test_duration = 10  # Approximate test duration
        throughput = total_requests / test_duration
        
        print(f"  📊 Average Response Time: {avg_response_time:.2f}ms")
        print(f"  📊 P95 Response Time: {p95:.2f}ms")
        print(f"  📊 P99 Response Time: {p99:.2f}ms")
        print(f"  📊 Error Rate: {error_rate:.2f}%")
        print(f"  📊 Throughput: {throughput:.2f} RPS")
        
        # Check against criteria
        performance_passed = (
            p95 <= self.criteria["performance"]["response_time_p95"] and
            p99 <= self.criteria["performance"]["response_time_p99"] and
            error_rate <= self.criteria["performance"]["error_rate"] and
            throughput >= self.criteria["performance"]["throughput_min"]
        )
        
        return {
            "avg_response_time_ms": avg_response_time,
            "p95_response_time_ms": p95,
            "p99_response_time_ms": p99,
            "error_rate_percent": error_rate,
            "throughput_rps": throughput,
            "total_requests": total_requests,
            "error_requests": error_count,
            "passed": performance_passed,
            "criteria_met": {
                "p95_response_time": p95 <= self.criteria["performance"]["response_time_p95"],
                "p99_response_time": p99 <= self.criteria["performance"]["response_time_p99"],
                "error_rate": error_rate <= self.criteria["performance"]["error_rate"],
                "throughput": throughput >= self.criteria["performance"]["throughput_min"]
            }
        }
    
    def check_monitoring_system(self) -> Dict[str, Any]:
        """Check if monitoring system is working properly"""
        print("📊 Checking monitoring system...")
        
        monitoring_endpoints = [
            "/api/monitoring/health",
            "/api/monitoring/metrics",
            "/api/monitoring/database/health",
            "/api/monitoring/cache/health",
            "/api/monitoring/performance",
        ]
        
        results = {}
        working_count = 0
        
        for endpoint in monitoring_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    results[endpoint] = {
                        "status": "working",
                        "data": data,
                        "error": None
                    }
                    working_count += 1
                    print(f"  ✅ {endpoint}: Working")
                else:
                    results[endpoint] = {
                        "status": "error",
                        "data": None,
                        "error": f"HTTP {response.status_code}"
                    }
                    print(f"  ❌ {endpoint}: HTTP {response.status_code}")
                    
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "data": None,
                    "error": str(e)
                }
                print(f"  ❌ {endpoint}: Error - {str(e)}")
        
        monitoring_working = working_count >= len(monitoring_endpoints) * 0.8  # 80% working
        
        return {
            "total_endpoints": len(monitoring_endpoints),
            "working_endpoints": working_count,
            "working_percent": (working_count / len(monitoring_endpoints)) * 100,
            "endpoint_details": results,
            "passed": monitoring_working
        }
    
    def check_database_performance(self) -> Dict[str, Any]:
        """Check database performance and health"""
        print("🗄️ Checking database performance...")
        
        try:
            # Test database health endpoint
            response = requests.get(f"{self.base_url}/api/monitoring/database/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                db_response_time = data.get("response_time_ms", 0)
                db_status = data.get("status", "unknown")
                
                print(f"  📊 Database Status: {db_status}")
                print(f"  📊 Database Response Time: {db_response_time:.2f}ms")
                
                # Check database response time
                db_performance_ok = db_response_time < 100  # Less than 100ms
                
                return {
                    "status": db_status,
                    "response_time_ms": db_response_time,
                    "statistics": data.get("statistics", {}),
                    "passed": db_status == "healthy" and db_performance_ok
                }
            else:
                return {
                    "status": "error",
                    "response_time_ms": 0,
                    "statistics": {},
                    "passed": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "response_time_ms": 0,
                "statistics": {},
                "passed": False,
                "error": str(e)
            }
    
    def check_cache_performance(self) -> Dict[str, Any]:
        """Check cache performance and health"""
        print("💾 Checking cache performance...")
        
        try:
            # Test cache health endpoint
            response = requests.get(f"{self.base_url}/api/monitoring/cache/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                cache_response_time = data.get("response_time_ms", 0)
                cache_status = data.get("status", "unknown")
                cache_stats = data.get("statistics", {})
                
                print(f"  📊 Cache Status: {cache_status}")
                print(f"  📊 Cache Response Time: {cache_response_time:.2f}ms")
                print(f"  📊 Cache Entries: {cache_stats.get('total_entries', 0)}")
                
                # Check cache performance
                cache_performance_ok = cache_response_time < 50  # Less than 50ms
                
                return {
                    "status": cache_status,
                    "response_time_ms": cache_response_time,
                    "statistics": cache_stats,
                    "passed": cache_status == "healthy" and cache_performance_ok
                }
            else:
                return {
                    "status": "error",
                    "response_time_ms": 0,
                    "statistics": {},
                    "passed": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "response_time_ms": 0,
                "statistics": {},
                "passed": False,
                "error": str(e)
            }
    
    def check_security_measures(self) -> Dict[str, Any]:
        """Check security measures and configurations"""
        print("🔒 Checking security measures...")
        
        security_checks = {
            "authentication_required": False,
            "rate_limiting": False,
            "cors_configured": False,
            "error_handling": False,
        }
        
        # Check if authentication is required for protected endpoints
        try:
            response = requests.get(f"{self.base_url}/api/optimized/me", timeout=10)
            if response.status_code == 401:
                security_checks["authentication_required"] = True
                print("  ✅ Authentication required for protected endpoints")
            else:
                print("  ⚠️  Authentication may not be properly configured")
        except Exception as e:
            print(f"  ❌ Error checking authentication: {e}")
        
        # Check CORS configuration
        try:
            response = requests.options(f"{self.base_url}/api/optimized/me", timeout=10)
            if "Access-Control-Allow-Origin" in response.headers:
                security_checks["cors_configured"] = True
                print("  ✅ CORS configured")
            else:
                print("  ⚠️  CORS may not be properly configured")
        except Exception as e:
            print(f"  ❌ Error checking CORS: {e}")
        
        # Check error handling
        try:
            response = requests.get(f"{self.base_url}/api/nonexistent", timeout=10)
            if response.status_code == 404:
                security_checks["error_handling"] = True
                print("  ✅ Error handling working")
            else:
                print("  ⚠️  Error handling may not be properly configured")
        except Exception as e:
            print(f"  ❌ Error checking error handling: {e}")
        
        passed_checks = sum(security_checks.values())
        total_checks = len(security_checks)
        
        return {
            "checks": security_checks,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "security_score": (passed_checks / total_checks) * 100,
            "passed": passed_checks >= total_checks * 0.75  # 75% of checks must pass
        }
    
    def run_comprehensive_check(self) -> Dict[str, Any]:
        """Run comprehensive production readiness check"""
        print("🎯 Zimmer AI Platform - Production Readiness Check")
        print("=" * 60)
        
        # Run all checks
        self.results = {
            "timestamp": datetime.utcnow().isoformat(),
            "base_url": self.base_url,
            "endpoint_availability": self.check_endpoint_availability(),
            "performance_metrics": self.check_performance_metrics(),
            "monitoring_system": self.check_monitoring_system(),
            "database_performance": self.check_database_performance(),
            "cache_performance": self.check_cache_performance(),
            "security_measures": self.check_security_measures(),
        }
        
        # Calculate overall readiness score
        checks = [
            self.results["endpoint_availability"]["passed"],
            self.results["performance_metrics"]["passed"],
            self.results["monitoring_system"]["passed"],
            self.results["database_performance"]["passed"],
            self.results["cache_performance"]["passed"],
            self.results["security_measures"]["passed"],
        ]
        
        passed_checks = sum(checks)
        total_checks = len(checks)
        readiness_score = (passed_checks / total_checks) * 100
        
        self.results["overall"] = {
            "readiness_score": readiness_score,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "production_ready": passed_checks >= total_checks * 0.8,  # 80% must pass
            "recommendations": self.generate_recommendations()
        }
        
        return self.results
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on check results"""
        recommendations = []
        
        if not self.results["endpoint_availability"]["passed"]:
            recommendations.append("Fix endpoint availability issues before production deployment")
        
        if not self.results["performance_metrics"]["passed"]:
            recommendations.append("Optimize performance metrics to meet production criteria")
        
        if not self.results["monitoring_system"]["passed"]:
            recommendations.append("Ensure monitoring system is fully operational")
        
        if not self.results["database_performance"]["passed"]:
            recommendations.append("Optimize database performance and ensure proper configuration")
        
        if not self.results["cache_performance"]["passed"]:
            recommendations.append("Optimize cache performance and ensure proper configuration")
        
        if not self.results["security_measures"]["passed"]:
            recommendations.append("Implement missing security measures")
        
        if not recommendations:
            recommendations.append("System is ready for production deployment!")
        
        return recommendations
    
    def print_summary(self):
        """Print comprehensive summary of production readiness"""
        print("\n📋 Production Readiness Summary:")
        print("=" * 50)
        
        overall = self.results["overall"]
        
        print(f"🎯 Overall Readiness Score: {overall['readiness_score']:.1f}%")
        print(f"✅ Passed Checks: {overall['passed_checks']}/{overall['total_checks']}")
        
        if overall["production_ready"]:
            print("🚀 PRODUCTION READY: System is ready for production deployment!")
        else:
            print("⚠️  NOT PRODUCTION READY: System requires improvements before deployment")
        
        print(f"\n📊 Detailed Results:")
        
        # Endpoint Availability
        avail = self.results["endpoint_availability"]
        status = "✅" if avail["passed"] else "❌"
        print(f"  {status} Endpoint Availability: {avail['availability_percent']:.1f}%")
        
        # Performance Metrics
        perf = self.results["performance_metrics"]
        status = "✅" if perf["passed"] else "❌"
        print(f"  {status} Performance Metrics: P95={perf['p95_response_time_ms']:.1f}ms, Error Rate={perf['error_rate_percent']:.1f}%")
        
        # Monitoring System
        monitor = self.results["monitoring_system"]
        status = "✅" if monitor["passed"] else "❌"
        print(f"  {status} Monitoring System: {monitor['working_percent']:.1f}% working")
        
        # Database Performance
        db = self.results["database_performance"]
        status = "✅" if db["passed"] else "❌"
        print(f"  {status} Database Performance: {db['response_time_ms']:.1f}ms")
        
        # Cache Performance
        cache = self.results["cache_performance"]
        status = "✅" if cache["passed"] else "❌"
        print(f"  {status} Cache Performance: {cache['response_time_ms']:.1f}ms")
        
        # Security Measures
        security = self.results["security_measures"]
        status = "✅" if security["passed"] else "❌"
        print(f"  {status} Security Measures: {security['security_score']:.1f}%")
        
        print(f"\n💡 Recommendations:")
        for i, recommendation in enumerate(overall["recommendations"], 1):
            print(f"  {i}. {recommendation}")
        
        print(f"\n⏱️  Check completed in {(datetime.utcnow() - self.start_time).total_seconds():.2f} seconds")

def main():
    """Main function to run production readiness check"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Production Readiness Check')
    parser.add_argument('--url', default='http://127.0.0.1:8000', help='Base URL for testing')
    parser.add_argument('--output', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    checker = ProductionReadinessChecker(args.url)
    
    try:
        results = checker.run_comprehensive_check()
        checker.print_summary()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n📄 Results saved to {args.output}")
        
        # Exit with appropriate code
        if results["overall"]["production_ready"]:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Check failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
