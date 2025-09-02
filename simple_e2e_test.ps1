# Simple E2E Test for Zimmer System
Write-Host "Zimmer System E2E Test" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""

# Test 1: Backend Health
Write-Host "Testing Backend..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 10
    Write-Host "Backend Health: PASS" -ForegroundColor Green
} catch {
    Write-Host "Backend Health: FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Admin Dashboard Build
Write-Host "`nTesting Admin Dashboard Build..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    npm run build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Admin Dashboard Build: PASS" -ForegroundColor Green
    } else {
        Write-Host "Admin Dashboard Build: FAIL" -ForegroundColor Red
    }
    Pop-Location
} catch {
    Write-Host "Admin Dashboard Build: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: User Panel Build
Write-Host "`nTesting User Panel Build..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    npm run build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "User Panel Build: PASS" -ForegroundColor Green
    } else {
        Write-Host "User Panel Build: FAIL" -ForegroundColor Red
    }
    Pop-Location
} catch {
    Write-Host "User Panel Build: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Environment Files
Write-Host "`nTesting Environment Configuration..." -ForegroundColor Cyan

# Admin Dashboard env
$adminEnv = "zimmermanagement/zimmer-admin-dashboard/.env.local"
if (Test-Path $adminEnv) {
    Write-Host "Admin Dashboard Environment: PASS" -ForegroundColor Green
} else {
    Write-Host "Admin Dashboard Environment: FAIL - No .env.local file" -ForegroundColor Red
}

# User Panel env
$userEnv = "zimmer_user_panel/env.corrected"
if (Test-Path $userEnv) {
    Write-Host "User Panel Environment: PASS" -ForegroundColor Green
} else {
    Write-Host "User Panel Environment: FAIL - No env.corrected file" -ForegroundColor Red
}

# Payment env
$paymentEnv = "zimmer-backend/env.payments"
if (Test-Path $paymentEnv) {
    Write-Host "Payment Environment: PASS" -ForegroundColor Green
} else {
    Write-Host "Payment Environment: FAIL - No env.payments file" -ForegroundColor Red
}

# Test 5: Database Models
Write-Host "`nTesting Database Models..." -ForegroundColor Cyan
try {
    Push-Location "zimmer-backend"
    python -c "from models.automation import Automation; print('Database models: PASS')"
    Pop-Location
} catch {
    Write-Host "Database Models: FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nE2E Test completed!" -ForegroundColor Green
