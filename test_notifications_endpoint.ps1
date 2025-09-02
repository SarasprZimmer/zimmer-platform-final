Write-Host "Testing Notifications Endpoint"
Write-Host "=============================="

# Test the notifications endpoint directly
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

Write-Host "`nStep 3: Test Notifications Endpoint (Unauthenticated)"
Write-Host "--------------------------------------------------------"
try {
    $response = Invoke-WebRequest -Uri "$backendUrl/api/admin/notifications/broadcast" -Method POST -Body '{"type":"test","title":"Test","body":"Test notification"}' -ContentType "application/json" -ErrorAction Stop
    Write-Host "❌ Endpoint should require authentication but didn't" -ForegroundColor Yellow
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ Endpoint correctly requires authentication" -ForegroundColor Green
    } else {
        Write-Host "❌ Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nStep 4: Test Authentication"
Write-Host "-------------------------------"
$loginData = @{
    email = "admin@zimmer.com"
    password = "admin123"
}

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/auth/login" -Method POST -Body ($loginData | ConvertTo-Json) -ContentType "application/json" -ErrorAction Stop
    $accessToken = $response.access_token
    Write-Host "✅ Authentication successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Authentication failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 5: Test Notifications Endpoint (Authenticated)"
Write-Host "-------------------------------------------------------"
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

$notificationData = @{
    type = "system"
    title = "Test Notification"
    body = "This is a test notification from the test script"
}

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/admin/notifications/broadcast" -Method POST -Headers $headers -Body ($notificationData | ConvertTo-Json) -ContentType "application/json" -ErrorAction Stop
    Write-Host "✅ Notifications endpoint working! Created: $($response.created) notifications" -ForegroundColor Green
} catch {
    Write-Host "❌ Notifications endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nNotifications endpoint test completed!"
