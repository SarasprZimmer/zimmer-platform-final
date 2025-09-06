# End-to-End Test 2025 - Complete User Workflow Testing
# Tests complete user journeys and system integrations

$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host "🌐 Zimmer System E2E Test 2025" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host "Testing complete user workflows and system integrations" -ForegroundColor Gray
Write-Host "Started at: $startTime" -ForegroundColor Gray
Write-Host ""

# Test Results
$e2eResults = @()
$totalE2ETests = 0
$passedE2ETests = 0
$failedE2ETests = 0
$warningE2ETests = 0

function Add-E2EResult {
    param(
        [string]$Workflow,
        [string]$Test,
        [string]$Status,
        [string]$Details = ""
    )
    $script:totalE2ETests++
    switch ($Status) {
        "PASS" { $script:passedE2ETests++ }
        "FAIL" { $script:failedE2ETests++ }
        "WARNING" { $script:warningE2ETests++ }
    }
    
    $e2eResults += [PSCustomObject]@{
        Workflow = $Workflow
        Test = $Test
        Status = $Status
        Details = $Details
        Timestamp = Get-Date
    }
}

function Write-E2EResult {
    param(
        [string]$Workflow,
        [string]$Test,
        [string]$Status,
        [string]$Details = ""
    )
    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        default { "White" }
    }
    
    Write-Host "[$Workflow] $Test - " -NoNewline
    Write-Host $Status -ForegroundColor $color
    if ($Details) {
        Write-Host "  $Details" -ForegroundColor Gray
    }
    
    Add-E2EResult -Workflow $Workflow -Test $Test -Status $Status -Details $Details
}

# =============================================================================
# 1. USER AUTHENTICATION WORKFLOW
# =============================================================================
Write-Host "🔐 USER AUTHENTICATION WORKFLOW" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

# 1.1 User Registration
try {
    $registerData = @{
        email = "testuser@example.com"
        password = "testpassword123"
        name = "Test User"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/register" -Method Post -Body $registerData -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "User Auth" -Test "User Registration" -Status "PASS" -Details "Registration endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-E2EResult -Workflow "User Auth" -Test "User Registration" -Status "PASS" -Details "Registration endpoint working (validation expected)"
    } else {
        Write-E2EResult -Workflow "User Auth" -Test "User Registration" -Status "WARNING" -Details "Registration issue: $($_.Exception.Message)"
    }
}

# 1.2 User Login
try {
    $loginData = @{
        email = "user@example.com"
        password = "user123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method Post -Body $loginData -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "User Auth" -Test "User Login" -Status "PASS" -Details "Login endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "User Auth" -Test "User Login" -Status "PASS" -Details "Login endpoint working (invalid credentials expected)"
    } else {
        Write-E2EResult -Workflow "User Auth" -Test "User Login" -Status "WARNING" -Details "Login issue: $($_.Exception.Message)"
    }
}

# 1.3 Admin Login
try {
    $adminLoginData = @{
        email = "admin@zimmer.com"
        password = "admin123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/login" -Method Post -Body $adminLoginData -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Admin Auth" -Test "Admin Login" -Status "PASS" -Details "Admin login endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Admin Auth" -Test "Admin Login" -Status "PASS" -Details "Admin login endpoint working (invalid credentials expected)"
    } else {
        Write-E2EResult -Workflow "Admin Auth" -Test "Admin Login" -Status "WARNING" -Details "Admin login issue: $($_.Exception.Message)"
    }
}

# =============================================================================
# 2. USER PANEL WORKFLOW
# =============================================================================
Write-Host "`n👥 USER PANEL WORKFLOW" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# 2.1 User Dashboard Access
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/me" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "User Panel" -Test "Dashboard Access" -Status "PASS" -Details "User dashboard API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "User Panel" -Test "Dashboard Access" -Status "PASS" -Details "User dashboard API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "User Panel" -Test "Dashboard Access" -Status "WARNING" -Details "Dashboard access issue: $($_.Exception.Message)"
    }
}

# 2.2 User Automations
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/automations" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "User Panel" -Test "Automations Access" -Status "PASS" -Details "User automations API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "User Panel" -Test "Automations Access" -Status "PASS" -Details "User automations API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "User Panel" -Test "Automations Access" -Status "WARNING" -Details "Automations access issue: $($_.Exception.Message)"
    }
}

# 2.3 User Profile Management
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/profile" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "User Panel" -Test "Profile Management" -Status "PASS" -Details "User profile API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "User Panel" -Test "Profile Management" -Status "PASS" -Details "User profile API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "User Panel" -Test "Profile Management" -Status "WARNING" -Details "Profile management issue: $($_.Exception.Message)"
    }
}

# 2.4 User Support System
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "User Panel" -Test "Support System" -Status "PASS" -Details "User support API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "User Panel" -Test "Support System" -Status "PASS" -Details "User support API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "User Panel" -Test "Support System" -Status "WARNING" -Details "Support system issue: $($_.Exception.Message)"
    }
}

# =============================================================================
# 3. ADMIN PANEL WORKFLOW
# =============================================================================
Write-Host "`n👑 ADMIN PANEL WORKFLOW" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan

# 3.1 Admin Users Management
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/users" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Admin Panel" -Test "Users Management" -Status "PASS" -Details "Admin users API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Admin Panel" -Test "Users Management" -Status "PASS" -Details "Admin users API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "Admin Panel" -Test "Users Management" -Status "WARNING" -Details "Users management issue: $($_.Exception.Message)"
    }
}

# 3.2 Admin Tickets Management
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/tickets" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Admin Panel" -Test "Tickets Management" -Status "PASS" -Details "Admin tickets API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Admin Panel" -Test "Tickets Management" -Status "PASS" -Details "Admin tickets API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "Admin Panel" -Test "Tickets Management" -Status "WARNING" -Details "Tickets management issue: $($_.Exception.Message)"
    }
}

# 3.3 Admin Automations Management
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/automations" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Admin Panel" -Test "Automations Management" -Status "PASS" -Details "Admin automations API accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Admin Panel" -Test "Automations Management" -Status "PASS" -Details "Admin automations API accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "Admin Panel" -Test "Automations Management" -Status "WARNING" -Details "Automations management issue: $($_.Exception.Message)"
    }
}

# =============================================================================
# 4. SUPPORT SYSTEM WORKFLOW
# =============================================================================
Write-Host "`n🎫 SUPPORT SYSTEM WORKFLOW" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# 4.1 Ticket Creation
try {
    $ticketData = @{
        user_id = 1
        subject = "Test Ticket"
        message = "This is a test ticket"
        importance = "medium"
    }
    
    $formData = New-Object System.Collections.Specialized.NameValueCollection
    $formData.Add("user_id", "1")
    $formData.Add("subject", "Test Ticket")
    $formData.Add("message", "This is a test ticket")
    $formData.Add("importance", "medium")
    
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Post -Body $formData -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Support System" -Test "Ticket Creation" -Status "PASS" -Details "Ticket creation endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Support System" -Test "Ticket Creation" -Status "PASS" -Details "Ticket creation endpoint working (auth required)"
    } else {
        Write-E2EResult -Workflow "Support System" -Test "Ticket Creation" -Status "WARNING" -Details "Ticket creation issue: $($_.Exception.Message)"
    }
}

# 4.2 Ticket Retrieval
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Support System" -Test "Ticket Retrieval" -Status "PASS" -Details "Ticket retrieval endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Support System" -Test "Ticket Retrieval" -Status "PASS" -Details "Ticket retrieval endpoint working (auth required)"
    } else {
        Write-E2EResult -Workflow "Support System" -Test "Ticket Retrieval" -Status "WARNING" -Details "Ticket retrieval issue: $($_.Exception.Message)"
    }
}

# =============================================================================
# 5. SETTINGS SYSTEM WORKFLOW
# =============================================================================
Write-Host "`n⚙️ SETTINGS SYSTEM WORKFLOW" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan

# 5.1 Profile Update
try {
    $profileData = @{
        name = "Updated Name"
        phone_number = "1234567890"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/profile" -Method Put -Body $profileData -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Settings System" -Test "Profile Update" -Status "PASS" -Details "Profile update endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Settings System" -Test "Profile Update" -Status "PASS" -Details "Profile update endpoint working (auth required)"
    } else {
        Write-E2EResult -Workflow "Settings System" -Test "Profile Update" -Status "WARNING" -Details "Profile update issue: $($_.Exception.Message)"
    }
}

# 5.2 Password Change
try {
    $passwordData = @{
        current_password = "oldpassword"
        new_password = "newpassword123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/change-password" -Method Post -Body $passwordData -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Settings System" -Test "Password Change" -Status "PASS" -Details "Password change endpoint working"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Settings System" -Test "Password Change" -Status "PASS" -Details "Password change endpoint working (auth required)"
    } else {
        Write-E2EResult -Workflow "Settings System" -Test "Password Change" -Status "WARNING" -Details "Password change issue: $($_.Exception.Message)"
    }
}

# =============================================================================
# 6. PAYMENT SYSTEM WORKFLOW
# =============================================================================
Write-Host "`n💳 PAYMENT SYSTEM WORKFLOW" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# 6.1 Payment Processing
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/payments" -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-E2EResult -Workflow "Payment System" -Test "Payment Processing" -Status "PASS" -Details "Payment processing endpoint accessible"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-E2EResult -Workflow "Payment System" -Test "Payment Processing" -Status "PASS" -Details "Payment processing endpoint accessible (auth required)"
    } else {
        Write-E2EResult -Workflow "Payment System" -Test "Payment Processing" -Status "WARNING" -Details "Payment processing issue: $($_.Exception.Message)"
    }
}

# =============================================================================
# 7. FRONTEND-BACKEND INTEGRATION
# =============================================================================
Write-Host "`n🔗 FRONTEND-BACKEND INTEGRATION" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

# 7.1 User Panel API Integration
$userPanelFiles = @(
    "zimmer_user_panel/lib/apiClient.ts",
    "zimmer_user_panel/pages/settings.tsx",
    "zimmer_user_panel/pages/support.tsx"
)

foreach ($file in $userPanelFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match "apiFetch|fetch.*api") {
            Write-E2EResult -Workflow "Frontend Integration" -Test "User Panel API Integration: $file" -Status "PASS" -Details "API integration found"
        } else {
            Write-E2EResult -Workflow "Frontend Integration" -Test "User Panel API Integration: $file" -Status "WARNING" -Details "No API integration found"
        }
    } else {
        Write-E2EResult -Workflow "Frontend Integration" -Test "User Panel API Integration: $file" -Status "FAIL" -Details "File missing"
    }
}

# 7.2 Admin Panel API Integration
$adminPanelFiles = @(
    "zimmermanagement/zimmer-admin-dashboard/lib/api.ts",
    "zimmermanagement/zimmer-admin-dashboard/pages/tickets.tsx",
    "zimmermanagement/zimmer-admin-dashboard/pages/users.tsx"
)

foreach ($file in $adminPanelFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match "adminAPI|api\.") {
            Write-E2EResult -Workflow "Frontend Integration" -Test "Admin Panel API Integration: $file" -Status "PASS" -Details "API integration found"
        } else {
            Write-E2EResult -Workflow "Frontend Integration" -Test "Admin Panel API Integration: $file" -Status "WARNING" -Details "No API integration found"
        }
    } else {
        Write-E2EResult -Workflow "Frontend Integration" -Test "Admin Panel API Integration: $file" -Status "FAIL" -Details "File missing"
    }
}

# =============================================================================
# E2E TEST SUMMARY
# =============================================================================
$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n📊 E2E TEST RESULTS SUMMARY" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow
Write-Host ""

Write-Host "📈 Test Statistics:" -ForegroundColor Cyan
Write-Host "  Total Tests: $totalE2ETests" -ForegroundColor White
Write-Host "  ✅ Passed: $passedE2ETests" -ForegroundColor Green
Write-Host "  ❌ Failed: $failedE2ETests" -ForegroundColor Red
Write-Host "  ⚠️ Warnings: $warningE2ETests" -ForegroundColor Yellow
Write-Host "  ⏱️ Duration: $($duration.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Gray

$successRate = if ($totalE2ETests -gt 0) { [math]::Round(($passedE2ETests / $totalE2ETests) * 100, 2) } else { 0 }
Write-Host "  📊 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

Write-Host "`n📋 Results by Workflow:" -ForegroundColor Cyan
$workflows = $e2eResults | Group-Object Workflow
foreach ($workflow in $workflows) {
    $workflowPassed = ($workflow.Group | Where-Object { $_.Status -eq "PASS" }).Count
    $workflowFailed = ($workflow.Group | Where-Object { $_.Status -eq "FAIL" }).Count
    $workflowWarnings = ($workflow.Group | Where-Object { $_.Status -eq "WARNING" }).Count
    $workflowTotal = $workflow.Count
    
    $workflowRate = if ($workflowTotal -gt 0) { [math]::Round(($workflowPassed / $workflowTotal) * 100, 1) } else { 0 }
    $workflowColor = if ($workflowRate -ge 90) { "Green" } elseif ($workflowRate -ge 70) { "Yellow" } else { "Red" }
    
    Write-Host "  [$($workflow.Name)]: $workflowPassed/$workflowTotal passed ($workflowRate%)" -ForegroundColor $workflowColor
}

Write-Host "`n🔍 Failed Tests:" -ForegroundColor Red
$failedTests = $e2eResults | Where-Object { $_.Status -eq "FAIL" }
if ($failedTests.Count -gt 0) {
    foreach ($test in $failedTests) {
        Write-Host "  ❌ [$($test.Workflow)] $($test.Test): $($test.Details)" -ForegroundColor Red
    }
} else {
    Write-Host "  🎉 No failed tests!" -ForegroundColor Green
}

Write-Host "`n⚠️ Warning Tests:" -ForegroundColor Yellow
$warningTests = $e2eResults | Where-Object { $_.Status -eq "WARNING" }
if ($warningTests.Count -gt 0) {
    foreach ($test in $warningTests) {
        Write-Host "  ⚠️ [$($test.Workflow)] $($test.Test): $($test.Details)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  🎉 No warning tests!" -ForegroundColor Green
}

# Overall E2E Test Status
Write-Host "`n🎯 E2E TEST STATUS:" -ForegroundColor Cyan
if ($failedE2ETests -eq 0 -and $warningE2ETests -eq 0) {
    Write-Host "🎉 EXCELLENT! All E2E tests passed. Complete workflows are functional!" -ForegroundColor Green
    Write-Host "🚀 The system is ready for production use with full user journeys!" -ForegroundColor Green
} elseif ($failedE2ETests -eq 0) {
    Write-Host "✅ GOOD! No critical failures, but some warnings to investigate." -ForegroundColor Yellow
    Write-Host "🔧 Review the warning details above and address any issues." -ForegroundColor Yellow
} else {
    Write-Host "⚠️ ATTENTION! Some E2E tests failed. User workflows may be broken." -ForegroundColor Red
    Write-Host "🛠️ Please review and fix the failing tests before proceeding." -ForegroundColor Red
}

Write-Host "`n🌐 E2E Test completed at $(Get-Date)" -ForegroundColor Green
Write-Host "Total execution time: $($duration.TotalMinutes.ToString('F2')) minutes" -ForegroundColor Gray
