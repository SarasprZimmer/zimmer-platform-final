#!/usr/bin/env python3
"""
Frontend Performance Optimization Script for Zimmer AI Platform
Optimizes frontend loading, rendering, and API calls
"""

import os
import json
from pathlib import Path

def optimize_nextjs_config():
    """Optimize Next.js configuration for better performance"""
    print("🔧 Optimizing Next.js configuration...")
    
    # Check if Next.js config exists
    nextjs_configs = [
        "zimmer_user_panel/next.config.js",
        "zimmermanagement/zimmer-admin-dashboard/next.config.js"
    ]
    
    for config_path in nextjs_configs:
        if os.path.exists(config_path):
            print(f"  📝 Found Next.js config: {config_path}")
            
            # Read existing config
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Add performance optimizations if not present
            optimizations = """
// Performance optimizations
const nextConfig = {
  // Enable compression
  compress: true,
  
  // Optimize images
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
  },
  
  // Enable experimental features for performance
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['@heroicons/react'],
  },
  
  // Webpack optimizations
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      // Enable tree shaking
      config.optimization.usedExports = true;
      config.optimization.sideEffects = false;
      
      // Optimize chunks
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
        },
      };
    }
    return config;
  },
  
  // Headers for caching
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=300, s-maxage=300',
          },
        ],
      },
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};
"""
            
            # Write optimized config
            with open(f"{config_path}.optimized", 'w') as f:
                f.write(optimizations)
            
            print(f"  ✅ Created optimized config: {config_path}.optimized")
        else:
            print(f"  ⚠️  Next.js config not found: {config_path}")

def optimize_api_calls():
    """Create optimized API call patterns"""
    print("🔧 Creating optimized API call patterns...")
    
    api_optimizations = """
// Optimized API Call Patterns for Zimmer AI Platform

// 1. Batch API calls
export const batchApiCalls = async (calls) => {
  const promises = calls.map(call => 
    fetch(call.url, call.options).then(response => ({
      ...call,
      response: response.ok ? response.json() : null,
      error: response.ok ? null : response.statusText
    }))
  );
  
  return Promise.all(promises);
};

// 2. Cached API calls with TTL
const apiCache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export const cachedApiCall = async (url, options = {}, ttl = CACHE_TTL) => {
  const cacheKey = `${url}:${JSON.stringify(options)}`;
  const cached = apiCache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.data;
  }
  
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    apiCache.set(cacheKey, {
      data,
      timestamp: Date.now()
    });
    
    return data;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// 3. Optimized user data fetching
export const fetchUserData = async () => {
  return cachedApiCall('/api/optimized/me');
};

// 4. Optimized dashboard data fetching
export const fetchDashboardData = async () => {
  return cachedApiCall('/api/optimized/user/dashboard');
};

// 5. Optimized marketplace data fetching
export const fetchMarketplaceData = async () => {
  return cachedApiCall('/api/optimized/automations/marketplace');
};

// 6. Debounced search
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// 7. Optimized form submission
export const submitForm = async (url, data, options = {}) => {
  const defaultOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  };
  
  const response = await fetch(url, { ...defaultOptions, ...options });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
};
"""
    
    with open("api_optimizations.js", "w") as f:
        f.write(api_optimizations)
    
    print("  ✅ Created optimized API call patterns!")

def optimize_react_components():
    """Create React component optimization patterns"""
    print("🔧 Creating React component optimization patterns...")
    
    react_optimizations = """
// React Component Optimization Patterns for Zimmer AI Platform

import React, { memo, useMemo, useCallback, lazy, Suspense } from 'react';

// 1. Memoized components for expensive renders
export const MemoizedUserCard = memo(({ user, onUpdate }) => {
  const handleUpdate = useCallback((data) => {
    onUpdate(user.id, data);
  }, [user.id, onUpdate]);
  
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={handleUpdate}>Update</button>
    </div>
  );
});

// 2. Lazy loading for heavy components
export const LazyDashboard = lazy(() => import('./Dashboard'));
export const LazyAdminPanel = lazy(() => import('./AdminPanel'));

// 3. Optimized data processing
export const useOptimizedData = (rawData, dependencies) => {
  return useMemo(() => {
    if (!rawData) return null;
    
    // Expensive data processing
    return rawData.map(item => ({
      ...item,
      processed: expensiveCalculation(item)
    }));
  }, dependencies);
};

// 4. Virtual scrolling for large lists
export const VirtualizedList = ({ items, itemHeight, containerHeight }) => {
  const [scrollTop, setScrollTop] = useState(0);
  
  const visibleItems = useMemo(() => {
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight) + 1,
      items.length
    );
    
    return items.slice(startIndex, endIndex).map((item, index) => ({
      ...item,
      index: startIndex + index
    }));
  }, [items, scrollTop, itemHeight, containerHeight]);
  
  return (
    <div 
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: 'relative' }}>
        {visibleItems.map(item => (
          <div
            key={item.id}
            style={{
              position: 'absolute',
              top: item.index * itemHeight,
              height: itemHeight,
              width: '100%'
            }}
          >
            {/* Render item content */}
          </div>
        ))}
      </div>
    </div>
  );
};

// 5. Optimized form handling
export const useOptimizedForm = (initialData) => {
  const [data, setData] = useState(initialData);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const updateField = useCallback((field, value) => {
    setData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  }, [errors]);
  
  const validateForm = useCallback(() => {
    const newErrors = {};
    // Validation logic
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, []);
  
  const submitForm = useCallback(async (onSubmit) => {
    if (!validateForm()) return;
    
    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } catch (error) {
      setErrors({ submit: error.message });
    } finally {
      setIsSubmitting(false);
    }
  }, [data, validateForm]);
  
  return {
    data,
    errors,
    isSubmitting,
    updateField,
    submitForm
  };
};

// 6. Performance monitoring hook
export const usePerformanceMonitor = (componentName) => {
  useEffect(() => {
    const startTime = performance.now();
    
    return () => {
      const endTime = performance.now();
      const renderTime = endTime - startTime;
      
      if (renderTime > 16) { // More than one frame (16ms)
        console.warn(`${componentName} render took ${renderTime.toFixed(2)}ms`);
      }
    };
  });
};
"""
    
    with open("react_optimizations.js", "w") as f:
        f.write(react_optimizations)
    
    print("  ✅ Created React component optimization patterns!")

def create_performance_monitoring():
    """Create performance monitoring setup"""
    print("🔧 Creating performance monitoring setup...")
    
    monitoring_setup = """
// Performance Monitoring for Zimmer AI Platform

// 1. Web Vitals monitoring
export const reportWebVitals = (metric) => {
  console.log(metric);
  
  // Send to analytics service
  if (metric.label === 'web-vital') {
    // Example: send to Google Analytics
    // gtag('event', metric.name, {
    //   value: Math.round(metric.value),
    //   event_category: 'Web Vitals',
    //   event_label: metric.id,
    //   non_interaction: true,
    // });
  }
};

// 2. API performance monitoring
export const monitorApiCall = async (url, options = {}) => {
  const startTime = performance.now();
  
  try {
    const response = await fetch(url, options);
    const endTime = performance.now();
    
    const duration = endTime - startTime;
    
    // Log slow API calls
    if (duration > 1000) { // More than 1 second
      console.warn(`Slow API call: ${url} took ${duration.toFixed(2)}ms`);
    }
    
    return response;
  } catch (error) {
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    console.error(`API call failed: ${url} after ${duration.toFixed(2)}ms`, error);
    throw error;
  }
};

// 3. Component render monitoring
export const withPerformanceMonitoring = (WrappedComponent, componentName) => {
  return React.memo((props) => {
    const renderStart = useRef(performance.now());
    
    useEffect(() => {
      const renderEnd = performance.now();
      const renderTime = renderEnd - renderStart.current;
      
      if (renderTime > 16) { // More than one frame
        console.warn(`${componentName} render took ${renderTime.toFixed(2)}ms`);
      }
    });
    
    return <WrappedComponent {...props} />;
  });
};

// 4. Bundle size monitoring
export const logBundleSize = () => {
  if (typeof window !== 'undefined' && window.performance) {
    const navigation = window.performance.getEntriesByType('navigation')[0];
    const loadTime = navigation.loadEventEnd - navigation.loadEventStart;
    
    console.log(`Page load time: ${loadTime.toFixed(2)}ms`);
  }
};
"""
    
    with open("performance_monitoring.js", "w") as f:
        f.write(monitoring_setup)
    
    print("  ✅ Created performance monitoring setup!")

def create_optimized_test_script():
    """Create optimized test script using new endpoints"""
    print("🔧 Creating optimized test script...")
    
    optimized_test = """
#!/usr/bin/env python3
\"\"\"
Optimized Test Script for Zimmer AI Platform
Uses optimized endpoints for better performance testing
\"\"\"

import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

class OptimizedTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def test_optimized_endpoints(self):
        \"\"\"Test optimized endpoints with performance measurement\"\"\"
        print("🚀 Testing Optimized Endpoints...")
        
        endpoints = [
            ("/api/optimized/me", "GET"),
            ("/api/optimized/user/dashboard", "GET"),
            ("/api/optimized/automations/marketplace", "GET"),
            ("/api/optimized/admin/dashboard", "GET"),
            ("/api/optimized/cache/stats", "GET"),
        ]
        
        results = []
        
        for endpoint, method in endpoints:
            start_time = time.time()
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", timeout=10)
                
                end_time = time.time()
                duration = (end_time - start_time) * 1000  # Convert to milliseconds
                
                status = "✅" if response.status_code == 200 else "❌"
                print(f"  {status} {endpoint}: {response.status_code} ({duration:.2f}ms)")
                
                results.append({
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'duration_ms': duration,
                    'success': response.status_code == 200
                })
                
            except Exception as e:
                end_time = time.time()
                duration = (end_time - start_time) * 1000
                print(f"  ❌ {endpoint}: Error - {str(e)} ({duration:.2f}ms)")
                
                results.append({
                    'endpoint': endpoint,
                    'status_code': 0,
                    'duration_ms': duration,
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def test_concurrent_requests(self, endpoint, num_requests=10):
        \"\"\"Test concurrent requests to measure performance under load\"\"\"
        print(f"🔄 Testing {num_requests} concurrent requests to {endpoint}...")
        
        def make_request():
            start_time = time.time()
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                end_time = time.time()
                return {
                    'status_code': response.status_code,
                    'duration_ms': (end_time - start_time) * 1000,
                    'success': response.status_code == 200
                }
            except Exception as e:
                end_time = time.time()
                return {
                    'status_code': 0,
                    'duration_ms': (end_time - start_time) * 1000,
                    'success': False,
                    'error': str(e)
                }
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        # Calculate statistics
        successful_requests = [r for r in results if r['success']]
        avg_duration = sum(r['duration_ms'] for r in successful_requests) / len(successful_requests) if successful_requests else 0
        max_duration = max(r['duration_ms'] for r in results)
        min_duration = min(r['duration_ms'] for r in results)
        
        print(f"  📊 Results: {len(successful_requests)}/{num_requests} successful")
        print(f"  ⏱️  Average: {avg_duration:.2f}ms, Min: {min_duration:.2f}ms, Max: {max_duration:.2f}ms")
        
        return results
    
    def run_performance_test(self):
        \"\"\"Run comprehensive performance test\"\"\"
        print("🎯 Running Comprehensive Performance Test")
        print("=" * 50)
        
        # Test optimized endpoints
        endpoint_results = self.test_optimized_endpoints()
        print()
        
        # Test concurrent requests
        concurrent_results = self.test_concurrent_requests("/api/optimized/me", 20)
        print()
        
        # Test cache performance
        print("💾 Testing Cache Performance...")
        cache_results = []
        for i in range(5):
            start_time = time.time()
            try:
                response = self.session.get(f"{self.base_url}/api/optimized/me", timeout=10)
                end_time = time.time()
                duration = (end_time - start_time) * 1000
                cache_results.append(duration)
                print(f"  Request {i+1}: {duration:.2f}ms")
            except Exception as e:
                print(f"  Request {i+1}: Error - {str(e)}")
        
        if cache_results:
            avg_cache_duration = sum(cache_results) / len(cache_results)
            print(f"  📊 Average cached request: {avg_cache_duration:.2f}ms")
        
        # Summary
        print("\\n📋 Performance Test Summary:")
        successful_endpoints = len([r for r in endpoint_results if r['success']])
        print(f"  ✅ Successful endpoints: {successful_endpoints}/{len(endpoint_results)}")
        
        if cache_results:
            print(f"  ⚡ Average response time: {avg_cache_duration:.2f}ms")
        
        return {
            'endpoint_results': endpoint_results,
            'concurrent_results': concurrent_results,
            'cache_results': cache_results
        }

if __name__ == "__main__":
    tester = OptimizedTester()
    tester.run_performance_test()
"""
    
    with open("optimized_test_script.py", "w") as f:
        f.write(optimized_test)
    
    print("  ✅ Created optimized test script!")

def main():
    """Main optimization function"""
    print("🚀 Starting Frontend Performance Optimization")
    print("=" * 60)
    
    try:
        # Step 1: Optimize Next.js configuration
        optimize_nextjs_config()
        print()
        
        # Step 2: Create optimized API call patterns
        optimize_api_calls()
        print()
        
        # Step 3: Create React component optimizations
        optimize_react_components()
        print()
        
        # Step 4: Create performance monitoring
        create_performance_monitoring()
        print()
        
        # Step 5: Create optimized test script
        create_optimized_test_script()
        print()
        
        print("🎉 Frontend performance optimization completed!")
        print("\\n📋 Next Steps:")
        print("1. Apply Next.js configuration optimizations")
        print("2. Implement API call optimizations in components")
        print("3. Add performance monitoring to critical components")
        print("4. Run the optimized test script to measure improvements")
        
    except Exception as e:
        print(f"❌ Frontend optimization failed: {e}")

if __name__ == "__main__":
    main()
"""
