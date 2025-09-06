# Basic System Test for Zimmer Platform 2025
Write-Host "Zimmer Platform 2025 - System Health Check" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

$testResults = @()

function Test-Component {
    param([string]$Name, [string]$Test, [string]$Status, [string]$Details)
    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        default { "White" }
    }
    Write-Host "[$Name] $Test - " -NoNewline
    Write-Host $Status -ForegroundColor $color
    if ($Details) { Write-Host "  Details: $Details" -ForegroundColor Gray }
    $testResults += [PSCustomObject]@{Name=$Name; Test=$Test; Status=$Status; Details=$Details}
}

# 1. Backend Health Check
Write-Host "Testing Backend..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 5
    Test-Component "Backend" "Health Check" "PASS" "Backend is running"
} catch {
    Test-Component "Backend" "Health Check" "FAIL" "Backend not accessible"
}

# 2. User Panel Build Test
Write-Host "`nTesting User Panel..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    if (Test-Path "node_modules") {
        Test-Component "User Panel" "Dependencies" "PASS" "node_modules found"
    } else {
        Test-Component "User Panel" "Dependencies" "WARNING" "node_modules not found"
    }
    
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Test-Component "User Panel" "Build" "PASS" "Build successful"
    } else {
        Test-Component "User Panel" "Build" "FAIL" "Build failed"
    }
    Pop-Location
} catch {
    Test-Component "User Panel" "Build" "ERROR" "Build test error"
}

# 3. Admin Dashboard Build Test
Write-Host "`nTesting Admin Dashboard..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    if (Test-Path "node_modules") {
        Test-Component "Admin Dashboard" "Dependencies" "PASS" "node_modules found"
    } else {
        Test-Component "Admin Dashboard" "Dependencies" "WARNING" "node_modules not found"
    }
    
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Test-Component "Admin Dashboard" "Build" "PASS" "Build successful"
    } else {
        Test-Component "Admin Dashboard" "Build" "FAIL" "Build failed"
    }
    Pop-Location
} catch {
    Test-Component "Admin Dashboard" "Build" "ERROR" "Build test error"
}

# 4. New Features Test
Write-Host "`nTesting New Features..." -ForegroundColor Cyan

# Payment System
$paymentFiles = @(
    "zimmer_user_panel/pages/payment/index.tsx",
    "zimmer_user_panel/components/payments/ActiveAutomations.tsx",
    "zimmer_user_panel/components/payments/MonthlyExpenses.tsx",
    "zimmer_user_panel/components/payments/PaymentHistory.tsx"
)

$paymentCount = 0
foreach ($file in $paymentFiles) {
    if (Test-Path $file) { $paymentCount++ }
}
if ($paymentCount -eq $paymentFiles.Count) {
    Test-Component "Payment System" "Files" "PASS" "All payment components exist"
} else {
    Test-Component "Payment System" "Files" "FAIL" "Missing payment components"
}

# Automations System
$automationFiles = @(
    "zimmer_user_panel/pages/automations/index.tsx",
    "zimmer_user_panel/components/automations/MyAutomationsList.tsx",
    "zimmer_user_panel/components/automations/QuickActions.tsx"
)

$automationCount = 0
foreach ($file in $automationFiles) {
    if (Test-Path $file) { $automationCount++ }
}
if ($automationCount -eq $automationFiles.Count) {
    Test-Component "Automations System" "Files" "PASS" "All automation components exist"
} else {
    Test-Component "Automations System" "Files" "FAIL" "Missing automation components"
}

# Dashboard Components
$dashboardFiles = @(
    "zimmer_user_panel/components/dashboard/RecentPayments.tsx",
    "zimmer_user_panel/components/dashboard/MyAutomations.tsx",
    "zimmer_user_panel/components/dashboard/WeeklyActivityChart.tsx",
    "zimmer_user_panel/components/dashboard/DistributionPie.tsx",
    "zimmer_user_panel/components/dashboard/SixMonthTrend.tsx",
    "zimmer_user_panel/components/dashboard/SupportQuick.tsx"
)

$dashboardCount = 0
foreach ($file in $dashboardFiles) {
    if (Test-Path $file) { $dashboardCount++ }
}
if ($dashboardCount -eq $dashboardFiles.Count) {
    Test-Component "Dashboard" "Files" "PASS" "All dashboard components exist"
} else {
    Test-Component "Dashboard" "Files" "FAIL" "Missing dashboard components"
}

# 5. Dependencies Test
Write-Host "`nTesting Dependencies..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    $requiredDeps = @("react", "next", "typescript", "tailwindcss", "recharts", "framer-motion")
    $depCount = 0
    foreach ($dep in $requiredDeps) {
        if ($packageJson.dependencies.$dep) { $depCount++ }
    }
    if ($depCount -eq $requiredDeps.Count) {
        Test-Component "Dependencies" "Packages" "PASS" "All required dependencies found"
    } else {
        Test-Component "Dependencies" "Packages" "WARNING" "Some dependencies missing"
    }
    Pop-Location
} catch {
    Test-Component "Dependencies" "Packages" "ERROR" "Dependency check failed"
}

# Summary
Write-Host "`nTest Results Summary" -ForegroundColor Yellow
Write-Host "===================" -ForegroundColor Yellow

$passCount = ($testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$warningCount = ($testResults | Where-Object { $_.Status -eq "WARNING" }).Count
$errorCount = ($testResults | Where-Object { $_.Status -eq "ERROR" }).Count

Write-Host "PASS: $passCount" -ForegroundColor Green
Write-Host "FAIL: $failCount" -ForegroundColor Red
Write-Host "WARNING: $warningCount" -ForegroundColor Yellow
Write-Host "ERROR: $errorCount" -ForegroundColor Red

Write-Host "`nOverall Status:" -ForegroundColor Cyan
if ($failCount -eq 0 -and $errorCount -eq 0) {
    Write-Host "EXCELLENT! All critical tests passed!" -ForegroundColor Green
} elseif ($failCount -eq 0) {
    Write-Host "GOOD! No critical failures, some warnings to check." -ForegroundColor Yellow
} else {
    Write-Host "ATTENTION NEEDED! Critical failures detected." -ForegroundColor Red
}

Write-Host "`nSystem Test completed at $(Get-Date)" -ForegroundColor Green
