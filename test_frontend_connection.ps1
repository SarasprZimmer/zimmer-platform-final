Write-Host "Frontend Connection Test"
Write-Host "========================"

$backendUrl = "http://127.0.0.1:8000"
$adminUrl = "http://127.0.0.1:3001"

Write-Host "`nStep 1: Test Backend from PowerShell"
Write-Host "--------------------------------------"
try {
    $response = Invoke-WebRequest -Uri "$backendUrl/docs" -Method GET -TimeoutSec 10
    Write-Host "✅ Backend accessible from PowerShell: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not accessible from PowerShell: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 2: Test Backend Login API from PowerShell"
Write-Host "------------------------------------------------"
$loginData = @{
    email = "admin@zimmer.com"
    password = "admin123"
}

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/auth/login" -Method POST -Body ($loginData | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 10
    Write-Host "✅ Login API accessible from PowerShell" -ForegroundColor Green
    Write-Host "   User ID: $($response.user.id)" -ForegroundColor Green
} catch {
    Write-Host "❌ Login API failed from PowerShell: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 3: Test Admin Dashboard"
Write-Host "-----------------------------"
try {
    $response = Invoke-WebRequest -Uri "$adminUrl" -Method GET -TimeoutSec 10
    Write-Host "✅ Admin dashboard accessible: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Admin dashboard not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 4: Test Network Configuration"
Write-Host "-----------------------------------"
Write-Host "Backend URL: $backendUrl" -ForegroundColor Yellow
Write-Host "Admin URL: $adminUrl" -ForegroundColor Yellow
Write-Host "Frontend will try to connect to: $backendUrl" -ForegroundColor Yellow

Write-Host "`nTest completed!"
