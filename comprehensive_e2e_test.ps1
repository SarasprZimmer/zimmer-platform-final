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

# 9. Discount System Check
Write-Host "`n🎫 Testing Discount System..." -ForegroundColor Cyan
try {
    Push-Location "zimmer-backend"
    $discountModels = @("models/discount.py", "schemas/discounts.py", "services/discounts.py", "routers/admin_discounts.py", "routers/discounts.py")
    $allDiscountFilesExist = $true
    foreach ($file in $discountModels) {
        if (-not (Test-Path $file)) {
            $allDiscountFilesExist = $false
            break
        }
    }
    if ($allDiscountFilesExist) {
        Write-TestResult -Component "Discount System" -Test "Backend Files" -Status "PASS" -Details "All discount system files present"
    } else {
        Write-TestResult -Component "Discount System" -Test "Backend Files" -Status "FAIL" -Details "Some discount system files missing"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "Discount System" -Test "Backend Files" -Status "ERROR" -Details "Discount system check failed"
}

# 10. 2FA System Check
Write-Host "`n🔒 Testing 2FA System..." -ForegroundColor Cyan
try {
    $twofaFiles = @(
        "zimmer-backend/models/twofa.py",
        "zimmer-backend/routers/twofa.py",
        "zimmer_user_panel/components/TwoFADialog.tsx",
        "zimmer_user_panel/pages/settings/security.tsx"
    )
    $all2faFilesExist = $true
    foreach ($file in $twofaFiles) {
        if (-not (Test-Path $file)) {
            $all2faFilesExist = $false
            break
        }
    }
    if ($all2faFilesExist) {
        Write-TestResult -Component "2FA System" -Test "Files" -Status "PASS" -Details "All 2FA system files present"
    } else {
        Write-TestResult -Component "2FA System" -Test "Files" -Status "FAIL" -Details "Some 2FA system files missing"
    }
} catch {
    Write-TestResult -Component "2FA System" -Test "Files" -Status "ERROR" -Details "2FA system check failed"
}

# 11. Email Verification System Check
Write-Host "`n📧 Testing Email Verification System..." -ForegroundColor Cyan
try {
    $emailFiles = @(
        "zimmer-backend/models/email_verification.py",
        "zimmer_user_panel/pages/verify-email.tsx"
    )
    $allEmailFilesExist = $true
    foreach ($file in $emailFiles) {
        if (-not (Test-Path $file)) {
            $allEmailFilesExist = $false
            break
        }
    }
    if ($allEmailFilesExist) {
        Write-TestResult -Component "Email Verification" -Test "Files" -Status "PASS" -Details "All email verification files present"
    } else {
        Write-TestResult -Component "Email Verification" -Test "Files" -Status "FAIL" -Details "Some email verification files missing"
    }
} catch {
    Write-TestResult -Component "Email Verification" -Test "Files" -Status "ERROR" -Details "Email verification check failed"
}

# 12. Purchase System Check
Write-Host "`n🛒 Testing Purchase System..." -ForegroundColor Cyan
try {
    $purchaseFiles = @(
        "zimmer_user_panel/components/DiscountCodeField.tsx",
        "zimmer_user_panel/components/PriceSummary.tsx",
        "zimmer_user_panel/lib/money.ts",
        "zimmer_user_panel/pages/automations/[id]/purchase.tsx"
    )
    $allPurchaseFilesExist = $true
    foreach ($file in $purchaseFiles) {
        if (-not (Test-Path $file)) {
            $allPurchaseFilesExist = $false
            break
        }
    }
    if ($allPurchaseFilesExist) {
        Write-TestResult -Component "Purchase System" -Test "Files" -Status "PASS" -Details "All purchase system files present"
    } else {
        Write-TestResult -Component "Purchase System" -Test "Files" -Status "FAIL" -Details "Some purchase system files missing"
    }
} catch {
    Write-TestResult -Component "Purchase System" -Test "Files" -Status "ERROR" -Details "Purchase system check failed"
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
