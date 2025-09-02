Write-Host "Simple Login Test"
Write-Host "=================="

$backendUrl = "http://localhost:8000"
$adminUrl = "http://localhost:3001"

Write-Host "`nStep 1: Test Backend Login API"
Write-Host "--------------------------------"
$loginData = @{
    email = "admin@zimmer.com"
    password = "admin123"
}

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/auth/login" -Method POST -Body ($loginData | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 10
    Write-Host "✅ Login API successful!" -ForegroundColor Green
    Write-Host "   Access Token: $($response.access_token)" -ForegroundColor Green
    Write-Host "   User ID: $($response.user.id)" -ForegroundColor Green
    Write-Host "   User Name: $($response.user.name)" -ForegroundColor Green
    Write-Host "   User Email: $($response.user.email)" -ForegroundColor Green
    Write-Host "   Is Admin: $($response.user.is_admin)" -ForegroundColor Green
} catch {
    Write-Host "❌ Login API failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "   Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}

Write-Host "`nStep 2: Test Admin Dashboard Access"
Write-Host "-----------------------------------"
try {
    $response = Invoke-WebRequest -Uri "$adminUrl" -Method GET -TimeoutSec 10
    Write-Host "✅ Admin dashboard accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Admin dashboard not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nTest completed!"
