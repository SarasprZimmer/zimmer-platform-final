# Smoke Test 2025 - Quick System Health Check
# Tests critical system components for basic functionality

$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host "💨 Zimmer System Smoke Test 2025" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "Quick health check for critical components" -ForegroundColor Gray
Write-Host "Started at: $startTime" -ForegroundColor Gray
Write-Host ""

# Test Results
$smokeResults = @()
$totalSmokeTests = 0
$passedSmokeTests = 0
$failedSmokeTests = 0

function Add-SmokeResult {
    param(
        [string]$Test,
        [string]$Status,
        [string]$Details = ""
    )
    $script:totalSmokeTests++
    if ($Status -eq "PASS") { $script:passedSmokeTests++ } else { $script:failedSmokeTests++ }
    
    $smokeResults += [PSCustomObject]@{
        Test = $Test
        Status = $Status
        Details = $Details
        Timestamp = Get-Date
    }
}

function Write-SmokeResult {
    param(
        [string]$Test,
        [string]$Status,
        [string]$Details = ""
    )
    $color = if ($Status -eq "PASS") { "Green" } else { "Red" }
    Write-Host "$Test - " -NoNewline
    Write-Host $Status -ForegroundColor $color
    if ($Details) {
        Write-Host "  $Details" -ForegroundColor Gray
    }
    Add-SmokeResult -Test $Test -Status $Status -Details $Details
}

# =============================================================================
# CRITICAL SYSTEM CHECKS
# =============================================================================

# 1. Backend Health Check
Write-Host "🔧 Backend Health Check..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 10
    Write-SmokeResult -Test "Backend Health" -Status "PASS" -Details "Backend accessible"
} catch {
    Write-SmokeResult -Test "Backend Health" -Status "FAIL" -Details "Backend not accessible: $($_.Exception.Message)"
}

# 2. Backend API Health
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/health" -Method Get -TimeoutSec 10
    Write-SmokeResult -Test "API Health" -Status "PASS" -Details "API health endpoint responding"
} catch {
    Write-SmokeResult -Test "API Health" -Status "FAIL" -Details "API health endpoint failed: $($_.Exception.Message)"
}

# 3. User Panel Build Check
Write-Host ""
Write-Host "👥 User Panel Build Check..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-SmokeResult -Test "User Panel Build" -Status "PASS" -Details "Build successful"
    } else {
        Write-SmokeResult -Test "User Panel Build" -Status "FAIL" -Details "Build failed"
    }
    Pop-Location
} catch {
    Write-SmokeResult -Test "User Panel Build" -Status "FAIL" -Details "Build error: $($_.Exception.Message)"
}

# 4. Admin Panel Build Check
Write-Host ""
Write-Host "👑 Admin Panel Build Check..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-SmokeResult -Test "Admin Panel Build" -Status "PASS" -Details "Build successful"
    } else {
        Write-SmokeResult -Test "Admin Panel Build" -Status "FAIL" -Details "Build failed"
    }
    Pop-Location
} catch {
    Write-SmokeResult -Test "Admin Panel Build" -Status "FAIL" -Details "Build error: $($_.Exception.Message)"
}

# 5. Database File Check
Write-Host ""
Write-Host "🗄️ Database Check..." -ForegroundColor Cyan
if (Test-Path "zimmer_dashboard.db") {
    Write-SmokeResult -Test "Database File" -Status "PASS" -Details "SQLite database exists"
} else {
    Write-SmokeResult -Test "Database File" -Status "FAIL" -Details "Database file missing"
}

# 6. Critical API Endpoints Check
Write-Host ""
Write-Host "🔍 Critical API Endpoints..." -ForegroundColor Cyan
$criticalEndpoints = @(
    @{ Path = "/api/auth/login"; Name = "User Login" },
    @{ Path = "/api/admin/login"; Name = "Admin Login" },
    @{ Path = "/api/users"; Name = "Users API" },
    @{ Path = "/api/tickets"; Name = "Tickets API" }
)

foreach ($endpoint in $criticalEndpoints) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000$($endpoint.Path)" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
        Write-SmokeResult -Test $endpoint.Name -Status "PASS" -Details "Endpoint accessible"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 401 -or $_.Exception.Response.StatusCode -eq 422) {
            Write-SmokeResult -Test $endpoint.Name -Status "PASS" -Details "Endpoint accessible (auth/validation required)"
        } else {
            Write-SmokeResult -Test $endpoint.Name -Status "FAIL" -Details "Endpoint failed: $($_.Exception.Message)"
        }
    }
}

# 7. Critical Files Check
Write-Host ""
Write-Host "📁 Critical Files Check..." -ForegroundColor Cyan
$criticalFiles = @(
    "zimmer_user_panel/lib/apiClient.ts",
    "zimmermanagement/zimmer-admin-dashboard/lib/api.ts",
    "zimmer_user_panel/pages/dashboard.tsx",
    "zimmermanagement/zimmer-admin-dashboard/pages/dashboard.tsx",
    "zimmer_user_panel/components/DashboardLayout.tsx",
    "zimmer_user_panel/pages/settings.tsx",
    "zimmer_user_panel/pages/support.tsx"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-SmokeResult -Test "File: $file" -Status "PASS" -Details "File exists"
    } else {
        Write-SmokeResult -Test "File: $file" -Status "FAIL" -Details "File missing"
    }
}

# 8. Environment Configuration Check
Write-Host ""
Write-Host "⚙️ Environment Configuration..." -ForegroundColor Cyan
$envFiles = @(
    "zimmer_user_panel/env.corrected",
    "zimmermanagement/zimmer-admin-dashboard/.env.local"
)

foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        Write-SmokeResult -Test "Env: $envFile" -Status "PASS" -Details "Environment file exists"
    } else {
        Write-SmokeResult -Test "Env: $envFile" -Status "FAIL" -Details "Environment file missing"
    }
}

# =============================================================================
# SMOKE TEST SUMMARY
# =============================================================================
$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host "📊 SMOKE TEST RESULTS" -ForegroundColor Yellow
Write-Host "=====================" -ForegroundColor Yellow
Write-Host ""

Write-Host "📈 Test Statistics:" -ForegroundColor Cyan
Write-Host "  Total Tests: $totalSmokeTests" -ForegroundColor White
Write-Host "  ✅ Passed: $passedSmokeTests" -ForegroundColor Green
Write-Host "  ❌ Failed: $failedSmokeTests" -ForegroundColor Red
Write-Host "  ⏱️ Duration: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor Gray

$successRate = if ($totalSmokeTests -gt 0) { [math]::Round(($passedSmokeTests / $totalSmokeTests) * 100, 2) } else { 0 }
Write-Host "  📊 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

Write-Host ""
Write-Host "🔍 Failed Tests:" -ForegroundColor Red
$failedTests = $smokeResults | Where-Object { $_.Status -eq "FAIL" }
if ($failedTests.Count -gt 0) {
    foreach ($test in $failedTests) {
        Write-Host "  ❌ $($test.Test): $($test.Details)" -ForegroundColor Red
    }
} else {
    Write-Host "  🎉 No failed tests!" -ForegroundColor Green
}

# Overall Smoke Test Status
Write-Host ""
Write-Host "🎯 SMOKE TEST STATUS:" -ForegroundColor Cyan
if ($failedSmokeTests -eq 0) {
    Write-Host "🎉 EXCELLENT! All smoke tests passed. System is healthy!" -ForegroundColor Green
    Write-Host "🚀 Ready for comprehensive testing and production use!" -ForegroundColor Green
} else {
    Write-Host "⚠️ ATTENTION! Some smoke tests failed. System may have issues." -ForegroundColor Red
    Write-Host "🛠️ Please fix the failed tests before proceeding." -ForegroundColor Red
}

Write-Host ""
Write-Host "💨 Smoke Test completed at $(Get-Date)" -ForegroundColor Green
Write-Host "Total execution time: $($duration.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Gray
