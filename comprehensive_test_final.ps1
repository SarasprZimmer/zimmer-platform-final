# Comprehensive Zimmer System Test - Final Version
# Tests all major components and provides detailed results

Write-Host "=== ZIMMER SYSTEM COMPREHENSIVE TEST ===" -ForegroundColor Green
Write-Host "Testing all components and endpoints..." -ForegroundColor White
Write-Host ""

$startTime = Get-Date
$totalTests = 0
$passedTests = 0
$failedTests = 0

function Test-Endpoint {
    param($Name, $Uri, $Method = "GET", $Headers = @{}, $Body = $null)
    
    $totalTests++
    Write-Host "Testing $Name..." -ForegroundColor Cyan
    
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Uri -Method $Method -Headers $Headers -Body $Body -TimeoutSec 10
        } else {
            $response = Invoke-RestMethod -Uri $Uri -Method $Method -Headers $Headers -TimeoutSec 10
        }
        Write-Host "  ✅ PASS: $Name" -ForegroundColor Green
        $passedTests++
        return $response
    } catch {
        Write-Host "  ❌ FAIL: $Name - $($_.Exception.Message)" -ForegroundColor Red
        $failedTests++
        return $null
    }
}

# 1. Backend Health Check
Write-Host "1. BACKEND HEALTH CHECK" -ForegroundColor Yellow
Test-Endpoint "Backend Health" "http://localhost:8000/health"

# 2. Authentication Test
Write-Host "`n2. AUTHENTICATION SYSTEM" -ForegroundColor Yellow
$loginResponse = Test-Endpoint "Admin Login" "http://localhost:8000/api/auth/login" "POST" @{"Content-Type"="application/json"} '{"email":"admin@zimmer.com","password":"admin123"}'

if ($loginResponse) {
    $token = $loginResponse.access_token
    $authHeaders = @{"Authorization" = "Bearer $token"; "Content-Type" = "application/json"}
    
    # 3. Admin API Tests
    Write-Host "`n3. ADMIN API ENDPOINTS" -ForegroundColor Yellow
    Test-Endpoint "Admin Dashboard" "http://localhost:8000/api/admin/dashboard" "GET" $authHeaders
    Test-Endpoint "Admin Users" "http://localhost:8000/api/admin/users" "GET" $authHeaders
    Test-Endpoint "Admin Automations" "http://localhost:8000/api/admin/automations" "GET" $authHeaders
    Test-Endpoint "Admin Discounts" "http://localhost:8000/api/admin/discounts" "GET" $authHeaders
    
    # 4. Public API Tests
    Write-Host "`n4. PUBLIC API ENDPOINTS" -ForegroundColor Yellow
    Test-Endpoint "Public Automations" "http://localhost:8000/api/automations" "GET"
    Test-Endpoint "Public Discount Validation" "http://localhost:8000/api/discounts/validate" "POST" @{"Content-Type"="application/json"} '{"code":"TEST20","automation_id":1,"amount":10000}'
}

# 5. Frontend Build Tests
Write-Host "`n5. FRONTEND BUILD TESTS" -ForegroundColor Yellow

# Admin Dashboard Build
Write-Host "Testing Admin Dashboard Build..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    $buildResult = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ PASS: Admin Dashboard builds successfully" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "  ❌ FAIL: Admin Dashboard build failed" -ForegroundColor Red
        $failedTests++
    }
    Pop-Location
} catch {
    Write-Host "  ❌ FAIL: Admin Dashboard build error - $($_.Exception.Message)" -ForegroundColor Red
    $failedTests++
}
$totalTests++

# User Panel Build
Write-Host "Testing User Panel Build..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $buildResult = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ PASS: User Panel builds successfully" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "  ❌ FAIL: User Panel build failed" -ForegroundColor Red
        $failedTests++
    }
    Pop-Location
} catch {
    Write-Host "  ❌ FAIL: User Panel build error - $($_.Exception.Message)" -ForegroundColor Red
    $failedTests++
}
$totalTests++

# 6. Critical Files Check
Write-Host "`n6. CRITICAL FILES CHECK" -ForegroundColor Yellow
$criticalFiles = @(
    "zimmer-backend/main.py",
    "zimmer-backend/models/discount.py",
    "zimmer-backend/routers/admin_discounts.py",
    "zimmer-backend/routers/discounts.py",
    "zimmermanagement/zimmer-admin-dashboard/components/DiscountForm.tsx",
    "zimmermanagement/zimmer-admin-dashboard/pages/discounts/index.tsx",
    "zimmer_user_panel/components/DiscountCodeField.tsx",
    "zimmer_user_panel/pages/automations/[id]/purchase.tsx"
)

$missingFiles = 0
foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "  ❌ $file - MISSING" -ForegroundColor Red
        $failedTests++
        $missingFiles++
    }
    $totalTests++
}

# 7. Final Results
Write-Host "`n=== FINAL TEST RESULTS ===" -ForegroundColor Green
Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: $passedTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor Red
Write-Host "Success Rate: $([math]::Round(($passedTests / $totalTests) * 100, 1))%" -ForegroundColor Cyan

$endTime = Get-Date
$duration = $endTime - $startTime
Write-Host "`nTest Duration: $($duration.TotalSeconds.ToString('F1')) seconds" -ForegroundColor Gray

# Overall Status
Write-Host "`n🎯 OVERALL SYSTEM STATUS:" -ForegroundColor Cyan
if ($failedTests -eq 0) {
    Write-Host "🎉 EXCELLENT! All tests passed. System is fully operational!" -ForegroundColor Green
} elseif ($failedTests -lt 3) {
    Write-Host "✅ GOOD! Most tests passed. Minor issues to address." -ForegroundColor Yellow
} else {
    Write-Host "⚠️ ATTENTION NEEDED! Multiple failures detected." -ForegroundColor Red
}

Write-Host "`nComprehensive test completed at $(Get-Date)" -ForegroundColor Green
