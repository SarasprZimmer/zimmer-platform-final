Write-Host "Testing Admin Dashboard Login"
Write-Host "============================="

# Test the admin dashboard login
$backendUrl = "http://localhost:8000"
$adminUrl = "http://localhost:3001"

Write-Host "`nStep 1: Test Backend Connectivity"
Write-Host "-------------------------------------"
try {
    $response = Invoke-WebRequest -Uri "$backendUrl/docs" -Method GET -ErrorAction Stop
    Write-Host "✅ Backend is accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend is not accessible: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 2: Test Admin Dashboard"
Write-Host "-------------------------------"
try {
    $response = Invoke-WebRequest -Uri "$adminUrl" -Method GET -ErrorAction Stop
    Write-Host "✅ Admin dashboard is accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Admin dashboard is not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 3: Test Login with Manager Credentials"
Write-Host "----------------------------------------------"
$loginData = @{
    email = "admin@zimmer.com"
    password = "admin123"
}

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/auth/login" -Method POST -Body ($loginData | ConvertTo-Json) -ContentType "application/json" -ErrorAction Stop
    Write-Host "✅ Login successful!" -ForegroundColor Green
    Write-Host "   Access Token: $($response.access_token)" -ForegroundColor Green
    Write-Host "   User ID: $($response.user_id)" -ForegroundColor Green
    Write-Host "   Email: $($response.email)" -ForegroundColor Green
    Write-Host "   Name: $($response.name)" -ForegroundColor Green
    Write-Host "   Role: $($response.role)" -ForegroundColor Green
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "   Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        Write-Host "   Response: $($_.Exception.Response.Content)" -ForegroundColor Red
    }
}

Write-Host "`nStep 4: Test Frontend Login Form"
Write-Host "----------------------------------"
Write-Host "Now try logging in through the admin dashboard at: $adminUrl" -ForegroundColor Yellow
Write-Host "Use these credentials:" -ForegroundColor Yellow
Write-Host "   Email: admin@zimmer.com" -ForegroundColor Yellow
Write-Host "   Password: admin123" -ForegroundColor Yellow

Write-Host "`nLogin test completed!"
