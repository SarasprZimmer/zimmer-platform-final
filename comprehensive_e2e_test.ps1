# Comprehensive End-to-End Test for Zimmer System
# Tests Backend, Admin Dashboard, and User Panel together

Write-Host "🚀 Zimmer System Comprehensive E2E Test" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# Test Results
$testResults = @()

function Add-TestResult {
    param(
        [string]$Component,
        [string]$Test,
        [string]$Status,
        [string]$Details
    )
    $testResults += [PSCustomObject]@{
        Component = $Component
        Test = $Test
        Status = $Status
        Details = $Details
        Timestamp = Get-Date
    }
}

function Write-TestResult {
    param(
        [string]$Component,
        [string]$Test,
        [string]$Status,
        [string]$Details
    )
    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }
    
    Write-Host "[$Component] $Test - " -NoNewline
    Write-Host $Status -ForegroundColor $color
    if ($Details) {
        Write-Host "  Details: $Details" -ForegroundColor Gray
    }
    
    Add-TestResult -Component $Component -Test $Test -Status $Status -Details $Details
}

# 1. Backend Health Check
Write-Host "🔧 Testing Backend..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 10
    Write-TestResult -Component "Backend" -Test "Health Check" -Status "PASS" -Details "Backend is running and accessible"
} catch {
    Write-TestResult -Component "Backend" -Test "Health Check" -Status "FAIL" -Details "Backend not accessible: $($_.Exception.Message)"
}

# 2. Backend API Test
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/health" -Method Get -TimeoutSec 10
    Write-TestResult -Component "Backend" -Test "API Health" -Status "PASS" -Details "API health endpoint responding"
} catch {
    Write-TestResult -Component "Backend" -Test "API Health" -Status "FAIL" -Details "API health endpoint failed: $($_.Exception.Message)"
}

# 3. Admin Dashboard Build Test
Write-Host "`n🎯 Testing Admin Dashboard..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "Admin Dashboard" -Test "Build" -Status "PASS" -Details "Build successful"
    } else {
        Write-TestResult -Component "Admin Dashboard" -Test "Build" -Status "FAIL" -Details "Build failed"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "Admin Dashboard" -Test "Build" -Status "ERROR" -Details "Build test error: $($_.Exception.Message)"
}

# 4. Admin Dashboard Environment Check
try {
    $envFile = "zimmermanagement/zimmer-admin-dashboard/.env.local"
    if (Test-Path $envFile) {
        $envContent = Get-Content $envFile
        $apiUrl = $envContent | Where-Object { $_ -match "NEXT_PUBLIC_API_URL" }
        if ($apiUrl -match "127.0.0.1:8000") {
            Write-TestResult -Component "Admin Dashboard" -Test "Environment Config" -Status "PASS" -Details "API URL correctly configured"
        } else {
            Write-TestResult -Component "Admin Dashboard" -Test "Environment Config" -Status "WARNING" -Details "API URL may be incorrect"
        }
    } else {
        Write-TestResult -Component "Admin Dashboard" -Test "Environment Config" -Status "FAIL" -Details "No .env.local file found"
    }
} catch {
    Write-TestResult -Component "Admin Dashboard" -Test "Environment Config" -Status "ERROR" -Details "Environment check failed"
}

# 5. User Panel Build Test
Write-Host "`n👥 Testing User Panel..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "User Panel" -Test "Build" -Status "PASS" -Details "Build successful"
    } else {
        Write-TestResult -Component "User Panel" -Test "Build" -Status "FAIL" -Details "Build failed"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "User Panel" -Test "Build" -Status "ERROR" -Details "Build test error: $($_.Exception.Message)"
}

# 6. User Panel Environment Check
try {
    $envFiles = @("zimmer_user_panel/env.corrected", "zimmer_user_panel/env.user")
    $envFound = $false
    foreach ($envFile in $envFiles) {
        if (Test-Path $envFile) {
            $envFound = $true
            break
        }
    }
    if ($envFound) {
        Write-TestResult -Component "User Panel" -Test "Environment Config" -Status "PASS" -Details "Environment file found"
    } else {
        Write-TestResult -Component "User Panel" -Test "Environment Config" -Status "WARNING" -Details "No environment files found"
    }
} catch {
    Write-TestResult -Component "User Panel" -Test "Environment Config" -Status "ERROR" -Details "Environment check failed"
}

# 7. Database Schema Check
Write-Host "`n🗄️ Testing Database..." -ForegroundColor Cyan
try {
    Push-Location "zimmer-backend"
    $pythonOutput = python -c "from database import get_db; from models.automation import Automation; print('Database models import successfully')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "Database" -Test "Schema Models" -Status "PASS" -Details "Database models import successfully"
    } else {
        Write-TestResult -Component "Database" -Test "Schema Models" -Status "FAIL" -Details "Database models import failed"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "Database" -Test "Schema Models" -Status "ERROR" -Details "Database test error: $($_.Exception.Message)"
}

# 8. Payment Gateway Check
try {
    Push-Location "zimmer-backend"
    $envPayments = "env.payments"
    if (Test-Path $envPayments) {
        $envContent = Get-Content $envPayments
        $zarinpalUrl = $envContent | Where-Object { $_ -match "ZARRINPAL_BASE" }
        if ($zarinpalUrl -match "zarinpal.com") {
            Write-TestResult -Component "Payment Gateway" -Test "Zarinpal Config" -Status "PASS" -Details "Zarinpal configuration found"
        } else {
            Write-TestResult -Component "Payment Gateway" -Test "Zarinpal Config" -Status "WARNING" -Details "Zarinpal configuration incomplete"
        }
    } else {
        Write-TestResult -Component "Payment Gateway" -Test "Zarinpal Config" -Status "FAIL" -Details "No payment environment file found"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "Payment Gateway" -Test "Zarinpal Config" -Status "ERROR" -Details "Payment gateway check failed"
}

# Generate Summary Report
Write-Host "`n📊 E2E Test Results Summary" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

$passCount = ($testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$warningCount = ($testResults | Where-Object { $_.Status -eq "WARNING" }).Count
$errorCount = ($testResults | Where-Object { $_.Status -eq "ERROR" }).Count

Write-Host "✅ PASS: $passCount" -ForegroundColor Green
Write-Host "❌ FAIL: $failCount" -ForegroundColor Red
Write-Host "⚠️ WARNING: $warningCount" -ForegroundColor Yellow
Write-Host "💥 ERROR: $errorCount" -ForegroundColor Red

Write-Host "`n📋 Detailed Results:" -ForegroundColor Yellow
foreach ($result in $testResults) {
    $color = switch ($result.Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }
    Write-Host "[$($result.Component)] $($result.Test): $($result.Status)" -ForegroundColor $color
}

# Overall System Status
Write-Host "`n🎯 Overall System Status:" -ForegroundColor Cyan
if ($failCount -eq 0 -and $errorCount -eq 0) {
    Write-Host "🎉 EXCELLENT! All critical tests passed. System is fully operational!" -ForegroundColor Green
} elseif ($failCount -eq 0) {
    Write-Host "✅ GOOD! No critical failures, but some errors to investigate." -ForegroundColor Yellow
} else {
    Write-Host "⚠️ ATTENTION NEEDED! Critical failures detected. System may not be fully operational." -ForegroundColor Red
}

Write-Host "`n🚀 E2E Test completed at $(Get-Date)" -ForegroundColor Green
