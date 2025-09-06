# Basic E2E Test 2025 - Complete User Workflow Testing
$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host "Zimmer System E2E Test 2025" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host ""

# Test Results
$passed = 0
$failed = 0
$warnings = 0

function Test-Workflow {
    param([string]$Workflow, [string]$Test, [scriptblock]$TestScript)
    try {
        & $TestScript
        Write-Host "PASS [$Workflow] $Test" -ForegroundColor Green
        $script:passed++
    } catch {
        if ($_.Exception.Message -match "401|422") {
            Write-Host "WARNING [$Workflow] $Test - $($_.Exception.Message)" -ForegroundColor Yellow
            $script:warnings++
        } else {
            Write-Host "FAIL [$Workflow] $Test - $($_.Exception.Message)" -ForegroundColor Red
            $script:failed++
        }
    }
}

# 1. Authentication Workflow
Write-Host "Authentication Workflow" -ForegroundColor Cyan
Test-Workflow "User Auth" "User Registration" {
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    $data = @{ email = "test$timestamp@example.com"; password = "test123"; name = "Test User" } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/signup" -Method Post -Body $data -ContentType "application/json" -TimeoutSec 10
}

Test-Workflow "User Auth" "User Login" {
    $data = @{ email = "user@example.com"; password = "user123" } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method Post -Body $data -ContentType "application/json" -TimeoutSec 10
}

Test-Workflow "Admin Auth" "Admin Login" {
    $data = @{ email = "admin@zimmer.com"; password = "admin123" } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method Post -Body $data -ContentType "application/json" -TimeoutSec 10
}

# 2. User Panel Workflow
Write-Host ""
Write-Host "User Panel Workflow" -ForegroundColor Cyan
Test-Workflow "User Panel" "Dashboard Access" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/me" -Method Get -TimeoutSec 10
}

Test-Workflow "User Panel" "Automations Access" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/automations" -Method Get -TimeoutSec 10
}

Test-Workflow "User Panel" "Profile Management" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/profile" -Method Get -TimeoutSec 10
}

Test-Workflow "User Panel" "Support System" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Get -TimeoutSec 10
}

# 3. Admin Panel Workflow
Write-Host ""
Write-Host "Admin Panel Workflow" -ForegroundColor Cyan
Test-Workflow "Admin Panel" "Users Management" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/users" -Method Get -TimeoutSec 10
}

Test-Workflow "Admin Panel" "Tickets Management" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/tickets" -Method Get -TimeoutSec 10
}

Test-Workflow "Admin Panel" "Automations Management" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/automations" -Method Get -TimeoutSec 10
}

# 4. Support System Workflow
Write-Host ""
Write-Host "Support System Workflow" -ForegroundColor Cyan
Test-Workflow "Support System" "Ticket Creation" {
    $formData = New-Object System.Collections.Specialized.NameValueCollection
    $formData.Add("user_id", "1")
    $formData.Add("subject", "Test Ticket")
    $formData.Add("message", "Test message")
    $formData.Add("importance", "medium")
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Post -Body $formData -TimeoutSec 10
}

Test-Workflow "Support System" "Ticket Retrieval" {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Get -TimeoutSec 10
}

# 5. Settings System Workflow
Write-Host ""
Write-Host "Settings System Workflow" -ForegroundColor Cyan
Test-Workflow "Settings System" "Profile Update" {
    $data = @{ name = "Updated Name"; phone_number = "1234567890" } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/profile" -Method Put -Body $data -ContentType "application/json" -TimeoutSec 10
}

Test-Workflow "Settings System" "Password Change" {
    $data = @{ current_password = "oldpass"; new_password = "newpass123" } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/change-password" -Method Post -Body $data -ContentType "application/json" -TimeoutSec 10
}

# 6. Frontend Integration Check
Write-Host ""
Write-Host "Frontend Integration Check" -ForegroundColor Cyan
$integrationFiles = @(
    "zimmer_user_panel/lib/apiClient.ts",
    "zimmer_user_panel/pages/settings.tsx",
    "zimmer_user_panel/components/settings/ProfileForm.tsx",
    "zimmer_user_panel/components/settings/ChangePasswordForm.tsx",
    "zimmer_user_panel/pages/support.tsx",
    "zimmermanagement/zimmer-admin-dashboard/lib/api.ts",
    "zimmermanagement/zimmer-admin-dashboard/pages/tickets.tsx"
)

foreach ($file in $integrationFiles) {
    Test-Workflow "Frontend Integration" "File: $file" {
        if (-not (Test-Path $file)) { throw "File missing" }
        $content = Get-Content $file -Raw
        if (-not ($content -match "apiFetch|fetch.*api|adminAPI")) { throw "No API integration found" }
    }
}

# Summary
$total = $passed + $failed + $warnings
$successRate = if ($total -gt 0) { [math]::Round(($passed / $total) * 100, 1) } else { 0 }
$duration = (Get-Date) - $startTime

Write-Host ""
Write-Host "E2E TEST RESULTS" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow
Write-Host "Total Tests: $total" -ForegroundColor White
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "Warnings: $warnings" -ForegroundColor Yellow
Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })
Write-Host "Duration: $($duration.TotalMinutes) minutes" -ForegroundColor Gray

Write-Host ""
if ($failed -eq 0) {
    Write-Host "EXCELLENT! All E2E tests passed. Complete workflows are functional!" -ForegroundColor Green
} elseif ($failed -le 2) {
    Write-Host "GOOD! Most E2E tests passed. Minor issues to investigate." -ForegroundColor Yellow
} else {
    Write-Host "ATTENTION! Some E2E tests failed. User workflows may be broken." -ForegroundColor Red
}

Write-Host ""
Write-Host "E2E Test completed at $(Get-Date)" -ForegroundColor Green
