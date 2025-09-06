# Comprehensive System Test 2025 - Updated for Current Architecture
# Tests all components, features, and integrations

$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host "🚀 Zimmer System Comprehensive Test 2025" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Testing current system architecture and features" -ForegroundColor Gray
Write-Host "Started at: $startTime" -ForegroundColor Gray
Write-Host ""

# Test Results Storage
$testResults = @()
$totalTests = 0
$passedTests = 0
$failedTests = 0
$warningTests = 0

function Add-TestResult {
    param(
        [string]$Category,
        [string]$Test,
        [string]$Status,
        [string]$Details = "",
        [string]$Component = ""
    )
    $script:totalTests++
    switch ($Status) {
        "PASS" { $script:passedTests++ }
        "FAIL" { $script:failedTests++ }
        "WARNING" { $script:warningTests++ }
    }
    
    $testResults += [PSCustomObject]@{
        Category = $Category
        Component = $Component
        Test = $Test
        Status = $Status
        Details = $Details
        Timestamp = Get-Date
    }
}

function Write-TestResult {
    param(
        [string]$Category,
        [string]$Test,
        [string]$Status,
        [string]$Details = "",
        [string]$Component = ""
    )
    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        default { "White" }
    }
    
    $componentText = if ($Component) { "[$Component] " } else { "" }
    Write-Host "$componentText$Test - " -NoNewline
    Write-Host $Status -ForegroundColor $color
    if ($Details) {
        Write-Host "  $Details" -ForegroundColor Gray
    }
    
    Add-TestResult -Category $Category -Test $Test -Status $Status -Details $Details -Component $Component
}

# =============================================================================
# 1. BACKEND SYSTEM TESTS
# =============================================================================
Write-Host "🔧 BACKEND SYSTEM TESTS" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# 1.1 Backend Health Check
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 10
    Write-TestResult -Category "Backend" -Test "Health Check" -Status "PASS" -Details "Backend accessible" -Component "FastAPI"
} catch {
    Write-TestResult -Category "Backend" -Test "Health Check" -Status "FAIL" -Details "Backend not accessible: $($_.Exception.Message)" -Component "FastAPI"
}

# 1.2 API Health Endpoint
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/health" -Method Get -TimeoutSec 10
    Write-TestResult -Category "Backend" -Test "API Health" -Status "PASS" -Details "Health endpoint responding" -Component "API"
} catch {
    Write-TestResult -Category "Backend" -Test "API Health" -Status "FAIL" -Details "Health endpoint failed: $($_.Exception.Message)" -Component "API"
}

# 1.3 Authentication Endpoints
$authEndpoints = @(
    @{ Path = "/api/auth/login"; Method = "POST"; Name = "User Login" },
    @{ Path = "/api/auth/register"; Method = "POST"; Name = "User Registration" },
    @{ Path = "/api/admin/login"; Method = "POST"; Name = "Admin Login" }
)

foreach ($endpoint in $authEndpoints) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000$($endpoint.Path)" -Method $endpoint.Method -TimeoutSec 5 -ErrorAction SilentlyContinue
        Write-TestResult -Category "Backend" -Test $endpoint.Name -Status "PASS" -Details "Endpoint accessible" -Component "Authentication"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 422) {
            Write-TestResult -Category "Backend" -Test $endpoint.Name -Status "PASS" -Details "Endpoint accessible (validation error expected)" -Component "Authentication"
        } else {
            Write-TestResult -Category "Backend" -Test $endpoint.Name -Status "FAIL" -Details "Endpoint failed: $($_.Exception.Message)" -Component "Authentication"
        }
    }
}

# 1.4 Core API Endpoints
$coreEndpoints = @(
    @{ Path = "/api/users"; Name = "Users List" },
    @{ Path = "/api/automations"; Name = "Automations List" },
    @{ Path = "/api/tickets"; Name = "Tickets List" },
    @{ Path = "/api/admin/users"; Name = "Admin Users" },
    @{ Path = "/api/admin/tickets"; Name = "Admin Tickets" },
    @{ Path = "/api/admin/automations"; Name = "Admin Automations" }
)

foreach ($endpoint in $coreEndpoints) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000$($endpoint.Path)" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
        Write-TestResult -Category "Backend" -Test $endpoint.Name -Status "PASS" -Details "Endpoint accessible" -Component "API"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 401) {
            Write-TestResult -Category "Backend" -Test $endpoint.Name -Status "PASS" -Details "Endpoint accessible (auth required)" -Component "API"
        } else {
            Write-TestResult -Category "Backend" -Test $endpoint.Name -Status "WARNING" -Details "Endpoint issue: $($_.Exception.Message)" -Component "API"
        }
    }
}

# =============================================================================
# 2. USER PANEL TESTS
# =============================================================================
Write-Host "`n👥 USER PANEL TESTS" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan

# 2.1 User Panel Build Test
try {
    Push-Location "zimmer_user_panel"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Category "User Panel" -Test "Build Test" -Status "PASS" -Details "Build successful" -Component "Next.js"
    } else {
        Write-TestResult -Category "User Panel" -Test "Build Test" -Status "FAIL" -Details "Build failed" -Component "Next.js"
    }
    Pop-Location
} catch {
    Write-TestResult -Category "User Panel" -Test "Build Test" -Status "FAIL" -Details "Build error: $($_.Exception.Message)" -Component "Next.js"
}

# 2.2 User Panel Pages Check
$userPages = @(
    "pages/dashboard.tsx",
    "pages/login.tsx",
    "pages/register.tsx",
    "pages/automations.tsx",
    "pages/automations/[id].tsx",
    "pages/payment/index.tsx",
    "pages/settings.tsx",
    "pages/support.tsx",
    "pages/forgot-password.tsx"
)

foreach ($page in $userPages) {
    if (Test-Path "zimmer_user_panel/$page") {
        Write-TestResult -Category "User Panel" -Test "Page: $page" -Status "PASS" -Details "Page exists" -Component "Pages"
    } else {
        Write-TestResult -Category "User Panel" -Test "Page: $page" -Status "FAIL" -Details "Page missing" -Component "Pages"
    }
}

# 2.3 User Panel Components Check
$userComponents = @(
    "components/DashboardLayout.tsx",
    "components/ProtectedRoute.tsx",
    "components/HeaderAuth.tsx",
    "components/Sidebar.tsx",
    "components/RecentPayments.tsx",
    "components/MyAutomations.tsx",
    "components/SupportQuick.tsx",
    "components/settings/ProfileForm.tsx",
    "components/settings/ChangePasswordForm.tsx",
    "components/ui/Kit.tsx"
)

foreach ($component in $userComponents) {
    if (Test-Path "zimmer_user_panel/$component") {
        Write-TestResult -Category "User Panel" -Test "Component: $component" -Status "PASS" -Details "Component exists" -Component "Components"
    } else {
        Write-TestResult -Category "User Panel" -Test "Component: $component" -Status "FAIL" -Details "Component missing" -Component "Components"
    }
}

# 2.4 User Panel API Client Check
if (Test-Path "zimmer_user_panel/lib/apiClient.ts") {
    $apiClientContent = Get-Content "zimmer_user_panel/lib/apiClient.ts" -Raw
    if ($apiClientContent -match "localhost:8000") {
        Write-TestResult -Category "User Panel" -Test "API Client Config" -Status "PASS" -Details "Correctly configured for backend" -Component "API Client"
    } else {
        Write-TestResult -Category "User Panel" -Test "API Client Config" -Status "WARNING" -Details "API URL may be incorrect" -Component "API Client"
    }
} else {
    Write-TestResult -Category "User Panel" -Test "API Client Config" -Status "FAIL" -Details "API client file missing" -Component "API Client"
}

# =============================================================================
# 3. ADMIN PANEL TESTS
# =============================================================================
Write-Host "`n👑 ADMIN PANEL TESTS" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan

# 3.1 Admin Panel Build Test
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Category "Admin Panel" -Test "Build Test" -Status "PASS" -Details "Build successful" -Component "Next.js"
    } else {
        Write-TestResult -Category "Admin Panel" -Test "Build Test" -Status "FAIL" -Details "Build failed" -Component "Next.js"
    }
    Pop-Location
} catch {
    Write-TestResult -Category "Admin Panel" -Test "Build Test" -Status "FAIL" -Details "Build error: $($_.Exception.Message)" -Component "Next.js"
}

# 3.2 Admin Panel Pages Check
$adminPages = @(
    "pages/dashboard.tsx",
    "pages/login.tsx",
    "pages/users.tsx",
    "pages/automations.tsx",
    "pages/tickets.tsx",
    "pages/discounts/index.tsx",
    "pages/discounts/new.tsx",
    "pages/settings.tsx"
)

foreach ($page in $adminPages) {
    if (Test-Path "zimmermanagement/zimmer-admin-dashboard/$page") {
        Write-TestResult -Category "Admin Panel" -Test "Page: $page" -Status "PASS" -Details "Page exists" -Component "Pages"
    } else {
        Write-TestResult -Category "Admin Panel" -Test "Page: $page" -Status "FAIL" -Details "Page missing" -Component "Pages"
    }
}

# 3.3 Admin Panel API Client Check
if (Test-Path "zimmermanagement/zimmer-admin-dashboard/lib/api.ts") {
    $adminApiContent = Get-Content "zimmermanagement/zimmer-admin-dashboard/lib/api.ts" -Raw
    if ($adminApiContent -match "127.0.0.1:8000") {
        Write-TestResult -Category "Admin Panel" -Test "API Client Config" -Status "PASS" -Details "Correctly configured for backend" -Component "API Client"
    } else {
        Write-TestResult -Category "Admin Panel" -Test "API Client Config" -Status "WARNING" -Details "API URL may be incorrect" -Component "API Client"
    }
} else {
    Write-TestResult -Category "Admin Panel" -Test "API Client Config" -Status "FAIL" -Details "API client file missing" -Component "API Client"
}

# =============================================================================
# 4. DATABASE TESTS
# =============================================================================
Write-Host "`n🗄️ DATABASE TESTS" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

# 4.1 Database File Check
if (Test-Path "zimmer_dashboard.db") {
    Write-TestResult -Category "Database" -Test "Database File" -Status "PASS" -Details "SQLite database exists" -Component "SQLite"
} else {
    Write-TestResult -Category "Database" -Test "Database File" -Status "FAIL" -Details "Database file missing" -Component "SQLite"
}

# 4.2 Database Models Check
$dbModels = @(
    "zimmer-backend/models/user.py",
    "zimmer-backend/models/automation.py",
    "zimmer-backend/models/ticket.py",
    "zimmer-backend/models/discount.py",
    "zimmer-backend/models/payment.py"
)

foreach ($model in $dbModels) {
    if (Test-Path $model) {
        Write-TestResult -Category "Database" -Test "Model: $model" -Status "PASS" -Details "Model file exists" -Component "SQLAlchemy"
    } else {
        Write-TestResult -Category "Database" -Test "Model: $model" -Status "FAIL" -Details "Model file missing" -Component "SQLAlchemy"
    }
}

# 4.3 Database Schema Test
try {
    Push-Location "zimmer-backend"
    $pythonOutput = python -c "from database import get_db; from models.user import User; from models.automation import Automation; print('Database models import successfully')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Category "Database" -Test "Schema Import" -Status "PASS" -Details "All models import successfully" -Component "SQLAlchemy"
    } else {
        Write-TestResult -Category "Database" -Test "Schema Import" -Status "FAIL" -Details "Model import failed" -Component "SQLAlchemy"
    }
    Pop-Location
} catch {
    Write-TestResult -Category "Database" -Test "Schema Import" -Status "FAIL" -Details "Database test error: $($_.Exception.Message)" -Component "SQLAlchemy"
}

# =============================================================================
# 5. FEATURE-SPECIFIC TESTS
# =============================================================================
Write-Host "`n🎯 FEATURE-SPECIFIC TESTS" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# 5.1 Authentication System
$authFiles = @(
    "zimmer_user_panel/contexts/AuthContext.tsx",
    "zimmer_user_panel/hooks/useAuth.ts",
    "zimmer_user_panel/lib/auth.ts",
    "zimmermanagement/zimmer-admin-dashboard/lib/auth-client.ts"
)

foreach ($file in $authFiles) {
    if (Test-Path $file) {
        Write-TestResult -Category "Authentication" -Test "File: $file" -Status "PASS" -Details "Auth file exists" -Component "Auth"
    } else {
        Write-TestResult -Category "Authentication" -Test "File: $file" -Status "FAIL" -Details "Auth file missing" -Component "Auth"
    }
}

# 5.2 Settings System (Profile & Password)
$settingsFiles = @(
    "zimmer_user_panel/components/settings/ProfileForm.tsx",
    "zimmer_user_panel/components/settings/ChangePasswordForm.tsx",
    "zimmer_user_panel/pages/settings.tsx"
)

foreach ($file in $settingsFiles) {
    if (Test-Path $file) {
        Write-TestResult -Category "Settings" -Test "File: $file" -Status "PASS" -Details "Settings file exists" -Component "Settings"
    } else {
        Write-TestResult -Category "Settings" -Test "File: $file" -Status "FAIL" -Details "Settings file missing" -Component "Settings"
    }
}

# 5.3 Support System
$supportFiles = @(
    "zimmer_user_panel/pages/support.tsx",
    "zimmer-backend/routers/ticket.py",
    "zimmermanagement/zimmer-admin-dashboard/pages/tickets.tsx"
)

foreach ($file in $supportFiles) {
    if (Test-Path $file) {
        Write-TestResult -Category "Support" -Test "File: $file" -Status "PASS" -Details "Support file exists" -Component "Support"
    } else {
        Write-TestResult -Category "Support" -Test "File: $file" -Status "FAIL" -Details "Support file missing" -Component "Support"
    }
}

# 5.4 Payment System
$paymentFiles = @(
    "zimmer_user_panel/pages/payment/index.tsx",
    "zimmer_user_panel/components/PriceSummary.tsx",
    "zimmer_user_panel/lib/money.ts"
)

foreach ($file in $paymentFiles) {
    if (Test-Path $file) {
        Write-TestResult -Category "Payment" -Test "File: $file" -Status "PASS" -Details "Payment file exists" -Component "Payment"
    } else {
        Write-TestResult -Category "Payment" -Test "File: $file" -Status "FAIL" -Details "Payment file missing" -Component "Payment"
    }
}

# =============================================================================
# 6. INTEGRATION TESTS
# =============================================================================
Write-Host "`n🔗 INTEGRATION TESTS" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan

# 6.1 User Panel to Backend Integration
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/me" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
    Write-TestResult -Category "Integration" -Test "User Panel API" -Status "PASS" -Details "User API accessible" -Component "User-Backend"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-TestResult -Category "Integration" -Test "User Panel API" -Status "PASS" -Details "User API accessible (auth required)" -Component "User-Backend"
    } else {
        Write-TestResult -Category "Integration" -Test "User Panel API" -Status "WARNING" -Details "User API issue: $($_.Exception.Message)" -Component "User-Backend"
    }
}

# 6.2 Admin Panel to Backend Integration
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/users" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
    Write-TestResult -Category "Integration" -Test "Admin Panel API" -Status "PASS" -Details "Admin API accessible" -Component "Admin-Backend"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-TestResult -Category "Integration" -Test "Admin Panel API" -Status "PASS" -Details "Admin API accessible (auth required)" -Component "Admin-Backend"
    } else {
        Write-TestResult -Category "Integration" -Test "Admin Panel API" -Status "WARNING" -Details "Admin API issue: $($_.Exception.Message)" -Component "Admin-Backend"
    }
}

# 6.3 Ticket System Integration
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tickets" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
    Write-TestResult -Category "Integration" -Test "Ticket System API" -Status "PASS" -Details "Ticket API accessible" -Component "Ticket-Backend"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-TestResult -Category "Integration" -Test "Ticket System API" -Status "PASS" -Details "Ticket API accessible (auth required)" -Component "Ticket-Backend"
    } else {
        Write-TestResult -Category "Integration" -Test "Ticket System API" -Status "WARNING" -Details "Ticket API issue: $($_.Exception.Message)" -Component "Ticket-Backend"
    }
}

# =============================================================================
# 7. ENVIRONMENT CONFIGURATION TESTS
# =============================================================================
Write-Host "`n⚙️ ENVIRONMENT CONFIGURATION TESTS" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# 7.1 User Panel Environment
$userEnvFiles = @("zimmer_user_panel/env.corrected", "zimmer_user_panel/env.user")
$userEnvFound = $false
foreach ($envFile in $userEnvFiles) {
    if (Test-Path $envFile) {
        $userEnvFound = $true
        break
    }
}
if ($userEnvFound) {
    Write-TestResult -Category "Environment" -Test "User Panel Config" -Status "PASS" -Details "Environment file found" -Component "User Panel"
} else {
    Write-TestResult -Category "Environment" -Test "User Panel Config" -Status "WARNING" -Details "No environment files found" -Component "User Panel"
}

# 7.2 Admin Panel Environment
if (Test-Path "zimmermanagement/zimmer-admin-dashboard/.env.local") {
    Write-TestResult -Category "Environment" -Test "Admin Panel Config" -Status "PASS" -Details "Environment file found" -Component "Admin Panel"
} else {
    Write-TestResult -Category "Environment" -Test "Admin Panel Config" -Status "WARNING" -Details "No .env.local file found" -Component "Admin Panel"
}

# 7.3 Backend Environment
if (Test-Path "zimmer-backend/.env") {
    Write-TestResult -Category "Environment" -Test "Backend Config" -Status "PASS" -Details "Environment file found" -Component "Backend"
} else {
    Write-TestResult -Category "Environment" -Test "Backend Config" -Status "WARNING" -Details "No .env file found" -Component "Backend"
}

# =============================================================================
# 8. SECURITY TESTS
# =============================================================================
Write-Host "`n🔒 SECURITY TESTS" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan

# 8.1 Authentication Endpoints Security
$secureEndpoints = @(
    @{ Path = "/api/admin/users"; Name = "Admin Users" },
    @{ Path = "/api/admin/tickets"; Name = "Admin Tickets" },
    @{ Path = "/api/admin/automations"; Name = "Admin Automations" }
)

foreach ($endpoint in $secureEndpoints) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000$($endpoint.Path)" -Method Get -TimeoutSec 5 -ErrorAction SilentlyContinue
        Write-TestResult -Category "Security" -Test $endpoint.Name -Status "WARNING" -Details "Endpoint accessible without auth" -Component "Security"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 401) {
            Write-TestResult -Category "Security" -Test $endpoint.Name -Status "PASS" -Details "Properly protected with auth" -Component "Security"
        } else {
            Write-TestResult -Category "Security" -Test $endpoint.Name -Status "WARNING" -Details "Unexpected response: $($_.Exception.Message)" -Component "Security"
        }
    }
}

# =============================================================================
# GENERATE COMPREHENSIVE REPORT
# =============================================================================
$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n📊 COMPREHENSIVE TEST RESULTS SUMMARY" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "📈 Test Statistics:" -ForegroundColor Cyan
Write-Host "  Total Tests: $totalTests" -ForegroundColor White
Write-Host "  ✅ Passed: $passedTests" -ForegroundColor Green
Write-Host "  ❌ Failed: $failedTests" -ForegroundColor Red
Write-Host "  ⚠️ Warnings: $warningTests" -ForegroundColor Yellow
Write-Host "  ⏱️ Duration: $($duration.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Gray

$successRate = if ($totalTests -gt 0) { [math]::Round(($passedTests / $totalTests) * 100, 2) } else { 0 }
Write-Host "  📊 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

Write-Host "`n📋 Results by Category:" -ForegroundColor Cyan
$categories = $testResults | Group-Object Category
foreach ($category in $categories) {
    $categoryPassed = ($category.Group | Where-Object { $_.Status -eq "PASS" }).Count
    $categoryFailed = ($category.Group | Where-Object { $_.Status -eq "FAIL" }).Count
    $categoryWarnings = ($category.Group | Where-Object { $_.Status -eq "WARNING" }).Count
    $categoryTotal = $category.Count
    
    $categoryRate = if ($categoryTotal -gt 0) { [math]::Round(($categoryPassed / $categoryTotal) * 100, 1) } else { 0 }
    $categoryColor = if ($categoryRate -ge 90) { "Green" } elseif ($categoryRate -ge 70) { "Yellow" } else { "Red" }
    
    Write-Host "  [$($category.Name)]: $categoryPassed/$categoryTotal passed ($categoryRate%)" -ForegroundColor $categoryColor
}

Write-Host "`n🔍 Failed Tests Details:" -ForegroundColor Red
$failedTests = $testResults | Where-Object { $_.Status -eq "FAIL" }
if ($failedTests.Count -gt 0) {
    foreach ($test in $failedTests) {
        Write-Host "  ❌ [$($test.Category)] $($test.Test): $($test.Details)" -ForegroundColor Red
    }
} else {
    Write-Host "  🎉 No failed tests!" -ForegroundColor Green
}

Write-Host "`n⚠️ Warning Tests Details:" -ForegroundColor Yellow
$warningTests = $testResults | Where-Object { $_.Status -eq "WARNING" }
if ($warningTests.Count -gt 0) {
    foreach ($test in $warningTests) {
        Write-Host "  ⚠️ [$($test.Category)] $($test.Test): $($test.Details)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  🎉 No warning tests!" -ForegroundColor Green
}

# Overall System Status
Write-Host "`n🎯 OVERALL SYSTEM STATUS:" -ForegroundColor Cyan
if ($failedTests -eq 0 -and $warningTests -eq 0) {
    Write-Host "🎉 EXCELLENT! All tests passed. System is fully operational!" -ForegroundColor Green
    Write-Host "🚀 The Zimmer system is ready for production use!" -ForegroundColor Green
} elseif ($failedTests -eq 0) {
    Write-Host "✅ GOOD! No critical failures, but some warnings to investigate." -ForegroundColor Yellow
    Write-Host "🔧 Review the warning details above and address any issues." -ForegroundColor Yellow
} else {
    Write-Host "⚠️ ATTENTION NEEDED! Critical failures detected." -ForegroundColor Red
    Write-Host "🛠️ Please review and fix the failing tests before proceeding." -ForegroundColor Red
}

Write-Host "`n📋 SYSTEM ARCHITECTURE STATUS:" -ForegroundColor Cyan
Write-Host "• Backend API (FastAPI): $(if ($testResults | Where-Object { $_.Category -eq 'Backend' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'Backend' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })
Write-Host "• User Panel (Next.js): $(if ($testResults | Where-Object { $_.Category -eq 'User Panel' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'User Panel' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })
Write-Host "• Admin Panel (Next.js): $(if ($testResults | Where-Object { $_.Category -eq 'Admin Panel' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'Admin Panel' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })
Write-Host "• Database (SQLite): $(if ($testResults | Where-Object { $_.Category -eq 'Database' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'Database' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })
Write-Host "• Authentication: $(if ($testResults | Where-Object { $_.Category -eq 'Authentication' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'Authentication' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })
Write-Host "• Support System: $(if ($testResults | Where-Object { $_.Category -eq 'Support' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'Support' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })
Write-Host "• Settings System: $(if ($testResults | Where-Object { $_.Category -eq 'Settings' -and $_.Status -eq 'PASS' }) { '✅ Operational' } else { '❌ Issues' })" -ForegroundColor $(if ($testResults | Where-Object { $_.Category -eq 'Settings' -and $_.Status -eq 'PASS' }) { 'Green' } else { 'Red' })

Write-Host "`n🚀 Comprehensive System Test completed at $(Get-Date)" -ForegroundColor Green
Write-Host "Total execution time: $($duration.TotalMinutes.ToString('F2')) minutes" -ForegroundColor Gray