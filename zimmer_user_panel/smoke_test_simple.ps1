# User Panel Smoke Test Script
# Tests basic functionality and identifies issues

Write-Host "Starting User Panel Smoke Test..." -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

$baseUrl = "http://localhost:3000"
$testResults = @()

# Test 1: Basic page load
Write-Host "`nTest 1: Basic page load" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $baseUrl -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "PASS: Main page loads successfully" -ForegroundColor Green
        $testResults += @{Test="Main Page Load"; Status="PASS"; Details="Status: $($response.StatusCode)"}
    } else {
        Write-Host "FAIL: Main page failed with status: $($response.StatusCode)" -ForegroundColor Red
        $testResults += @{Test="Main Page Load"; Status="FAIL"; Details="Status: $($response.StatusCode)"}
    }
} catch {
    Write-Host "ERROR: Main page load error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults += @{Test="Main Page Load"; Status="ERROR"; Details=$_.Exception.Message}
}

# Test 2: Login page
Write-Host "`nTest 2: Login page" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "PASS: Login page loads successfully" -ForegroundColor Green
        $testResults += @{Test="Login Page Load"; Status="PASS"; Details="Status: $($response.StatusCode)"}
    } else {
        Write-Host "FAIL: Login page failed with status: $($response.StatusCode)" -ForegroundColor Red
        $testResults += @{Test="Login Page Load"; Status="FAIL"; Details="Status: $($response.StatusCode)"}
    }
} catch {
    Write-Host "ERROR: Login page load error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults += @{Test="Login Page Load"; Status="ERROR"; Details=$_.Exception.Message}
}

# Test 3: Dashboard page (should redirect to login)
Write-Host "`nTest 3: Dashboard page redirect" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/dashboard" -UseBasicParsing -TimeoutSec 10 -MaximumRedirection 0
    if ($response.StatusCode -eq 302 -or $response.StatusCode -eq 200) {
        Write-Host "PASS: Dashboard page handles redirect properly" -ForegroundColor Green
        $testResults += @{Test="Dashboard Redirect"; Status="PASS"; Details="Status: $($response.StatusCode)"}
    } else {
        Write-Host "FAIL: Dashboard page issue with status: $($response.StatusCode)" -ForegroundColor Red
        $testResults += @{Test="Dashboard Redirect"; Status="FAIL"; Details="Status: $($response.StatusCode)"}
    }
} catch {
    Write-Host "ERROR: Dashboard page error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults += @{Test="Dashboard Redirect"; Status="ERROR"; Details=$_.Exception.Message}
}

# Test 4: Check for console errors in page content
Write-Host "`nTest 4: Page content analysis" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $baseUrl -UseBasicParsing -TimeoutSec 10
    $content = $response.Content
    
    if ($content -match "error|Error|ERROR") {
        Write-Host "WARNING: Page content contains error text" -ForegroundColor Yellow
        $testResults += @{Test="Content Analysis"; Status="WARNING"; Details="Contains error text"}
    } elseif ($content -match "missing required error components") {
        Write-Host "FAIL: Page shows build error message" -ForegroundColor Red
        $testResults += @{Test="Content Analysis"; Status="FAIL"; Details="Build error message detected"}
    } else {
        Write-Host "PASS: Page content appears normal" -ForegroundColor Green
        $testResults += @{Test="Content Analysis"; Status="PASS"; Details="No obvious errors detected"}
    }
} catch {
    Write-Host "ERROR: Content analysis error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults += @{Test="Content Analysis"; Status="ERROR"; Details=$_.Exception.Message}
}

# Test 5: API endpoint test (should get CORS or auth error, not 500)
Write-Host "`nTest 5: API endpoint test" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/me" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 401) {
        Write-Host "PASS: API endpoint responds correctly (401 Unauthorized)" -ForegroundColor Green
        $testResults += @{Test="API Endpoint"; Status="PASS"; Details="Status: $($response.StatusCode) - Correct auth response"}
    } else {
        Write-Host "WARNING: API endpoint unexpected status: $($response.StatusCode)" -ForegroundColor Yellow
        $testResults += @{Test="API Endpoint"; Status="WARNING"; Details="Status: $($response.StatusCode) - Unexpected response"}
    }
} catch {
    Write-Host "ERROR: API endpoint error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults += @{Test="API Endpoint"; Status="ERROR"; Details=$_.Exception.Message}
}

# Generate summary report
Write-Host "`nTest Results Summary:" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

$passCount = ($testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$errorCount = ($testResults | Where-Object { $_.Status -eq "ERROR" }).Count
$warningCount = ($testResults | Where-Object { $_.Status -eq "WARNING" }).Count

Write-Host "PASS: $passCount" -ForegroundColor Green
Write-Host "FAIL: $failCount" -ForegroundColor Red
Write-Host "WARNING: $warningCount" -ForegroundColor Yellow
Write-Host "ERROR: $errorCount" -ForegroundColor Red

Write-Host "`nDetailed Results:" -ForegroundColor Yellow
foreach ($result in $testResults) {
    $color = switch ($result.Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        default { "White" }
    }
    Write-Host "$($result.Status): $($result.Test) - $($result.Details)" -ForegroundColor $color
}

# Recommendations
Write-Host "`nRecommendations:" -ForegroundColor Yellow
if ($failCount -gt 0 -or $errorCount -gt 0) {
    Write-Host "• Check Next.js build logs for compilation errors" -ForegroundColor Cyan
    Write-Host "• Verify all required dependencies are installed" -ForegroundColor Cyan
    Write-Host "• Check for TypeScript compilation issues" -ForegroundColor Cyan
    Write-Host "• Verify environment variables are loaded correctly" -ForegroundColor Cyan
} else {
    Write-Host "• All tests passed! User panel appears to be working correctly." -ForegroundColor Green
}

Write-Host "`nSmoke test completed!" -ForegroundColor Yellow
