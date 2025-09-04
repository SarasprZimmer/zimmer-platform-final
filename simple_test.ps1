# Simple Test Runner for Zimmer System
# Tests essential components without complex formatting

$ErrorActionPreference = "Stop"

Write-Host "Zimmer System Simple Test" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green
Write-Host ""

# 1. Backend Health Check
Write-Host "Backend Health Check..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    Write-Host "PASS: Backend is running and healthy" -ForegroundColor Green
} catch {
    Write-Host "FAIL: Backend health check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure the backend server is running on port 8000" -ForegroundColor Yellow
    exit 1
}

# 2. Admin Dashboard Build Check
Write-Host "`nAdmin Dashboard Build Check..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "PASS: Admin dashboard builds successfully" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Admin dashboard build failed" -ForegroundColor Red
    }
    Pop-Location
} catch {
    Write-Host "ERROR: Admin dashboard build check error: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. User Panel Build Check
Write-Host "`nUser Panel Build Check..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "PASS: User panel builds successfully" -ForegroundColor Green
    } else {
        Write-Host "FAIL: User panel build failed" -ForegroundColor Red
    }
    Pop-Location
} catch {
    Write-Host "ERROR: User panel build check error: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Critical Files Check
Write-Host "`nCritical Files Check..." -ForegroundColor Cyan
$criticalFiles = @(
    "zimmer-backend/main.py",
    "zimmer-backend/models/discount.py",
    "zimmer-backend/routers/admin_discounts.py",
    "zimmermanagement/zimmer-admin-dashboard/components/DiscountForm.tsx",
    "zimmermanagement/zimmer-admin-dashboard/pages/discounts/index.tsx",
    "zimmer_user_panel/components/DiscountCodeField.tsx",
    "zimmer_user_panel/pages/automations/[id]/purchase.tsx"
)

$missingFiles = @()
foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "PASS: $file" -ForegroundColor Green
    } else {
        Write-Host "FAIL: $file - MISSING" -ForegroundColor Red
        $missingFiles += $file
    }
}

# 5. Authentication Test
Write-Host "`nAuthentication Test..." -ForegroundColor Cyan
try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email":"admin@zimmer.com","password":"admin123"}' -TimeoutSec 5
    if ($loginResponse.access_token) {
        Write-Host "PASS: Admin authentication working" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Admin authentication failed" -ForegroundColor Red
    }
} catch {
    Write-Host "FAIL: Authentication test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# 6. Discount System Test
Write-Host "`nDiscount System Test..." -ForegroundColor Cyan
try {
    $token = $loginResponse.access_token
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    $discountResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/discounts" -Method GET -Headers $headers -TimeoutSec 5
    Write-Host "PASS: Discount system API working" -ForegroundColor Green
} catch {
    Write-Host "FAIL: Discount system test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Summary
Write-Host "`nTest Summary" -ForegroundColor Yellow
Write-Host "============" -ForegroundColor Yellow

if ($missingFiles.Count -eq 0) {
    Write-Host "SUCCESS: All critical files present!" -ForegroundColor Green
} else {
    Write-Host "WARNING: $($missingFiles.Count) critical files missing" -ForegroundColor Yellow
}

Write-Host "`nSimple test completed at $(Get-Date)" -ForegroundColor Green
