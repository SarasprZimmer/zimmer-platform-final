# Simple Smoke Test 2025 - Quick System Health Check
$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host "💨 Zimmer System Smoke Test 2025" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Test Results
$passed = 0
$failed = 0

function Test-Component {
    param([string]$Name, [scriptblock]$Test)
    try {
        & $Test
        Write-Host "✅ $Name - PASS" -ForegroundColor Green
        $script:passed++
    } catch {
        Write-Host "❌ $Name - FAIL: $($_.Exception.Message)" -ForegroundColor Red
        $script:failed++
    }
}

# 1. Backend Health Check
Test-Component "Backend Health" {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 10
}

# 2. API Health
Test-Component "API Health" {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/test-cors" -Method Get -TimeoutSec 10
}

# 3. User Panel Build
Test-Component "User Panel Build" {
    Push-Location "zimmer_user_panel"
    npm run build | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Build failed" }
    Pop-Location
}

# 4. Admin Panel Build
Test-Component "Admin Panel Build" {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    npm run build | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Build failed" }
    Pop-Location
}

# 5. Database File
Test-Component "Database File" {
    if (-not (Test-Path "zimmer_dashboard.db")) { throw "Database file missing" }
}

# 6. Critical Files
$criticalFiles = @(
    "zimmer_user_panel/lib/apiClient.ts",
    "zimmermanagement/zimmer-admin-dashboard/lib/api.ts",
    "zimmer_user_panel/pages/dashboard.tsx",
    "zimmer_user_panel/pages/settings.tsx",
    "zimmer_user_panel/pages/support.tsx"
)

foreach ($file in $criticalFiles) {
    Test-Component "File: $file" {
        if (-not (Test-Path $file)) { throw "File missing" }
    }
}

# 7. API Endpoints
Test-Component "API: /api/auth/login" {
    $data = @{ email = "test@example.com"; password = "test123" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method Post -Body $data -ContentType "application/json" -TimeoutSec 5 -ErrorAction SilentlyContinue
}

Test-Component "API: /api/users" {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
}

Test-Component "API: /api/tickets" {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
}

# Summary
$total = $passed + $failed
$successRate = if ($total -gt 0) { [math]::Round(($passed / $total) * 100, 1) } else { 0 }
$duration = (Get-Date) - $startTime

Write-Host ""
Write-Host "📊 SMOKE TEST RESULTS" -ForegroundColor Yellow
Write-Host "=====================" -ForegroundColor Yellow
Write-Host "Total Tests: $total" -ForegroundColor White
Write-Host "✅ Passed: $passed" -ForegroundColor Green
Write-Host "❌ Failed: $failed" -ForegroundColor Red
Write-Host "📊 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })
Write-Host "⏱️ Duration: $($duration.TotalSeconds) seconds" -ForegroundColor Gray

Write-Host ""
if ($failed -eq 0) {
    Write-Host "🎉 EXCELLENT! All smoke tests passed. System is healthy!" -ForegroundColor Green
} else {
    Write-Host "⚠️ ATTENTION! Some smoke tests failed. System may have issues." -ForegroundColor Red
}

Write-Host ""
Write-Host "💨 Smoke Test completed at $(Get-Date)" -ForegroundColor Green
