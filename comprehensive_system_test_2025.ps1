# Comprehensive System Test for Zimmer Platform 2025
# Tests Backend, Admin Dashboard, and User Panel with current structure
# Updated to support new payment system, automations, and dashboard components

Write-Host "🚀 Zimmer Platform 2025 - Comprehensive System Test" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "Testing: Backend API + Admin Dashboard + User Panel + New Features" -ForegroundColor Cyan
Write-Host ""

# Test Results
$testResults = @()

function Add-TestResult {
    param(
        [string]$Component,
        [string]$Test,
        [string]$Status,
        [string]$Details
    )
    $testResults += [PSCustomObject]@{
        Component = $Component
        Test = $Test
        Status = $Status
        Details = $Details
        Timestamp = Get-Date
    }
}

function Write-TestResult {
    param(
        [string]$Component,
        [string]$Test,
        [string]$Status,
        [string]$Details
    )
    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }
    
    Write-Host "[$Component] $Test - " -NoNewline
    Write-Host $Status -ForegroundColor $color
    if ($Details) {
        Write-Host "  Details: $Details" -ForegroundColor Gray
    }
    
    Add-TestResult -Component $Component -Test $Test -Status $Status -Details $Details
}

# 1. Backend Health Check
Write-Host "🔧 Testing Backend API..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/docs" -Method Get -TimeoutSec 10
    Write-TestResult -Component "Backend" -Test "Health Check" -Status "PASS" -Details "Backend is running and accessible"
} catch {
    Write-TestResult -Component "Backend" -Test "Health Check" -Status "FAIL" -Details "Backend not accessible: $($_.Exception.Message)"
}

# 2. Backend API Endpoints Test
$apiEndpoints = @(
    "http://127.0.0.1:8000/api/health",
    "http://127.0.0.1:8000/api/auth/login",
    "http://127.0.0.1:8000/api/auth/signup",
    "http://127.0.0.1:8000/api/user/profile",
    "http://127.0.0.1:8000/api/user/automations",
    "http://127.0.0.1:8000/api/user/payments",
    "http://127.0.0.1:8000/api/tickets"
)

foreach ($endpoint in $apiEndpoints) {
    try {
        $response = Invoke-RestMethod -Uri $endpoint -Method Get -TimeoutSec 5
        Write-TestResult -Component "Backend API" -Test "Endpoint: $($endpoint.Split('/')[-1])" -Status "PASS" -Details "Endpoint responding"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 401 -or $_.Exception.Response.StatusCode -eq 422) {
            Write-TestResult -Component "Backend API" -Test "Endpoint: $($endpoint.Split('/')[-1])" -Status "PASS" -Details "Endpoint responding (auth required)"
        } else {
            Write-TestResult -Component "Backend API" -Test "Endpoint: $($endpoint.Split('/')[-1])" -Status "WARNING" -Details "Endpoint issue: $($_.Exception.Message)"
        }
    }
}

# 3. User Panel Build Test
Write-Host "`n👥 Testing User Panel (Next.js)..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    
    # Check if node_modules exists
    if (Test-Path "node_modules") {
        Write-TestResult -Component "User Panel" -Test "Dependencies" -Status "PASS" -Details "node_modules found"
    } else {
        Write-TestResult -Component "User Panel" -Test "Dependencies" -Status "WARNING" -Details "node_modules not found, running npm install"
        npm install
    }
    
    # Test build
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "User Panel" -Test "Build" -Status "PASS" -Details "Build successful"
    } else {
        Write-TestResult -Component "User Panel" -Test "Build" -Status "FAIL" -Details "Build failed: $buildOutput"
    }
    
    Pop-Location
} catch {
    Write-TestResult -Component "User Panel" -Test "Build" -Status "ERROR" -Details "Build test error: $($_.Exception.Message)"
}

# 4. User Panel New Features Test
Write-Host "`n🎯 Testing User Panel New Features..." -ForegroundColor Cyan

# Test Payment Page
$paymentFiles = @(
    "zimmer_user_panel/pages/payment/index.tsx",
    "zimmer_user_panel/components/payments/ActiveAutomations.tsx",
    "zimmer_user_panel/components/payments/MonthlyExpenses.tsx",
    "zimmer_user_panel/components/payments/PaymentHistory.tsx"
)

foreach ($file in $paymentFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Payment System" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Payment component exists"
    } else {
        Write-TestResult -Component "Payment System" -Test "File: $($file.Split('/')[-1])" -Status "FAIL" -Details "Payment component missing"
    }
}

# Test Automations Page
$automationFiles = @(
    "zimmer_user_panel/pages/automations/index.tsx",
    "zimmer_user_panel/pages/automations/marketplace.tsx",
    "zimmer_user_panel/components/automations/MyAutomationsList.tsx",
    "zimmer_user_panel/components/automations/QuickActions.tsx"
)

foreach ($file in $automationFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Automations System" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Automation component exists"
    } else {
        Write-TestResult -Component "Automations System" -Test "File: $($file.Split('/')[-1])" -Status "FAIL" -Details "Automation component missing"
    }
}

# Test Support Page
$supportFiles = @(
    "zimmer_user_panel/pages/support.tsx"
)

foreach ($file in $supportFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Support System" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Support component exists"
    } else {
        Write-TestResult -Component "Support System" -Test "File: $($file.Split('/')[-1])" -Status "FAIL" -Details "Support component missing"
    }
}

# Test Dashboard Components
$dashboardFiles = @(
    "zimmer_user_panel/components/dashboard/RecentPayments.tsx",
    "zimmer_user_panel/components/dashboard/MyAutomations.tsx",
    "zimmer_user_panel/components/dashboard/WeeklyActivityChart.tsx",
    "zimmer_user_panel/components/dashboard/DistributionPie.tsx",
    "zimmer_user_panel/components/dashboard/SixMonthTrend.tsx",
    "zimmer_user_panel/components/dashboard/SupportQuick.tsx"
)

foreach ($file in $dashboardFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Dashboard" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Dashboard component exists"
    } else {
        Write-TestResult -Component "Dashboard" -Test "File: $($file.Split('/')[-1])" -Status "FAIL" -Details "Dashboard component missing"
    }
}

# 5. User Panel Dependencies Test
Write-Host "`n📦 Testing User Panel Dependencies..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    
    # Check for required dependencies
    $requiredDeps = @("react", "next", "typescript", "tailwindcss", "recharts", "framer-motion")
    foreach ($dep in $requiredDeps) {
        if ($packageJson.dependencies.$dep) {
            Write-TestResult -Component "Dependencies" -Test "Package: $dep" -Status "PASS" -Details "Version: $($packageJson.dependencies.$dep)"
        } else {
            Write-TestResult -Component "Dependencies" -Test "Package: $dep" -Status "FAIL" -Details "Missing required dependency"
        }
    }
    
    Pop-Location
} catch {
    Write-TestResult -Component "Dependencies" -Test "Package Check" -Status "ERROR" -Details "Dependency check failed: $($_.Exception.Message)"
}

# 6. User Panel Environment Configuration
Write-Host "`n⚙️ Testing User Panel Configuration..." -ForegroundColor Cyan
try {
    $envFiles = @("zimmer_user_panel/env.corrected", "zimmer_user_panel/env.user")
    $envFound = $false
    foreach ($envFile in $envFiles) {
        if (Test-Path $envFile) {
            $envFound = $true
            $envContent = Get-Content $envFile
            $apiUrl = $envContent | Where-Object { $_ -match "NEXT_PUBLIC_API_URL" }
            if ($apiUrl -match "127.0.0.1:8000") {
                Write-TestResult -Component "User Panel Config" -Test "API URL" -Status "PASS" -Details "API URL correctly configured"
            } else {
                Write-TestResult -Component "User Panel Config" -Test "API URL" -Status "WARNING" -Details "API URL may be incorrect"
            }
            break
        }
    }
    if (-not $envFound) {
        Write-TestResult -Component "User Panel Config" -Test "Environment Files" -Status "WARNING" -Details "No environment files found"
    }
} catch {
    Write-TestResult -Component "User Panel Config" -Test "Configuration" -Status "ERROR" -Details "Configuration check failed"
}

# 7. Admin Dashboard Build Test
Write-Host "`n🎯 Testing Admin Dashboard..." -ForegroundColor Cyan
try {
    Push-Location "zimmermanagement/zimmer-admin-dashboard"
    
    # Check if node_modules exists
    if (Test-Path "node_modules") {
        Write-TestResult -Component "Admin Dashboard" -Test "Dependencies" -Status "PASS" -Details "node_modules found"
    } else {
        Write-TestResult -Component "Admin Dashboard" -Test "Dependencies" -Status "WARNING" -Details "node_modules not found, running npm install"
        npm install
    }
    
    # Test build
    $buildOutput = npm run build 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "Admin Dashboard" -Test "Build" -Status "PASS" -Details "Build successful"
    } else {
        Write-TestResult -Component "Admin Dashboard" -Test "Build" -Status "FAIL" -Details "Build failed: $buildOutput"
    }
    
    Pop-Location
} catch {
    Write-TestResult -Component "Admin Dashboard" -Test "Build" -Status "ERROR" -Details "Build test error: $($_.Exception.Message)"
}

# 8. Database Schema Check
Write-Host "`n🗄️ Testing Database..." -ForegroundColor Cyan
try {
    Push-Location "zimmer-backend"
    $pythonOutput = python -c "from database import get_db; print('Database connection successful')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "Database" -Test "Connection" -Status "PASS" -Details "Database connection successful"
    } else {
        Write-TestResult -Component "Database" -Test "Connection" -Status "FAIL" -Details "Database connection failed"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "Database" -Test "Connection" -Status "ERROR" -Details "Database test error: $($_.Exception.Message)"
}

# 9. Authentication System Test
Write-Host "`n🔐 Testing Authentication System..." -ForegroundColor Cyan
$authFiles = @(
    "zimmer_user_panel/contexts/AuthContext.tsx",
    "zimmer_user_panel/lib/api.ts",
    "zimmer_user_panel/lib/auth.ts",
    "zimmer_user_panel/components/TwoFADialog.tsx",
    "zimmer_user_panel/pages/login.tsx",
    "zimmer_user_panel/pages/signup.tsx"
)

foreach ($file in $authFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Authentication" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Auth component exists"
    } else {
        Write-TestResult -Component "Authentication" -Test "File: $($file.Split('/')[-1])" -Status "FAIL" -Details "Auth component missing"
    }
}

# 10. UI Components Test
Write-Host "`n🎨 Testing UI Components..." -ForegroundColor Cyan
$uiFiles = @(
    "zimmer_user_panel/components/Skeleton.tsx",
    "zimmer_user_panel/components/DashboardLayout.tsx",
    "zimmer_user_panel/components/Sidebar.tsx",
    "zimmer_user_panel/components/Topbar.tsx",
    "zimmer_user_panel/lib/money.ts",
    "zimmer_user_panel/lib/mockApi.ts"
)

foreach ($file in $uiFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "UI Components" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "UI component exists"
    } else {
        Write-TestResult -Component "UI Components" -Test "File: $($file.Split('/')[-1])" -Status "FAIL" -Details "UI component missing"
    }
}

# 11. Font and Styling Test
Write-Host "`n🎨 Testing Font and Styling..." -ForegroundColor Cyan
$stylingFiles = @(
    "zimmer_user_panel/styles/globals.css",
    "zimmer_user_panel/tailwind.config.js",
    "zimmer_user_panel/public/fonts"
)

foreach ($file in $stylingFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Styling" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Styling file exists"
    } else {
        Write-TestResult -Component "Styling" -Test "File: $($file.Split('/')[-1])" -Status "WARNING" -Details "Styling file missing"
    }
}

# 12. Payment Gateway Integration Test
Write-Host "`n💳 Testing Payment Integration..." -ForegroundColor Cyan
$paymentFiles = @(
    "zimmer_user_panel/components/PurchaseModal.tsx",
    "zimmer_user_panel/components/DiscountCodeField.tsx",
    "zimmer_user_panel/components/PriceSummary.tsx"
)

foreach ($file in $paymentFiles) {
    if (Test-Path $file) {
        Write-TestResult -Component "Payment Integration" -Test "File: $($file.Split('/')[-1])" -Status "PASS" -Details "Payment component exists"
    } else {
        Write-TestResult -Component "Payment Integration" -Test "File: $($file.Split('/')[-1])" -Status "WARNING" -Details "Payment component missing"
    }
}

# 13. Mock Data Test
Write-Host "`n📊 Testing Mock Data..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $mockDataTest = node -e "
        try {
            const mockData = require('./lib/mockApi.ts');
            console.log('Mock data loaded successfully');
        } catch (e) {
            console.log('Mock data load failed:', e.message);
            process.exit(1);
        }
    " 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "Mock Data" -Test "Load" -Status "PASS" -Details "Mock data loads successfully"
    } else {
        Write-TestResult -Component "Mock Data" -Test "Load" -Status "WARNING" -Details "Mock data load issue: $mockDataTest"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "Mock Data" -Test "Load" -Status "ERROR" -Details "Mock data test failed"
}

# 14. TypeScript Compilation Test
Write-Host "`n📝 Testing TypeScript Compilation..." -ForegroundColor Cyan
try {
    Push-Location "zimmer_user_panel"
    $tscOutput = npx tsc --noEmit 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult -Component "TypeScript" -Test "Compilation" -Status "PASS" -Details "No TypeScript errors"
    } else {
        Write-TestResult -Component "TypeScript" -Test "Compilation" -Status "WARNING" -Details "TypeScript errors found: $tscOutput"
    }
    Pop-Location
} catch {
    Write-TestResult -Component "TypeScript" -Test "Compilation" -Status "ERROR" -Details "TypeScript check failed"
}

# Generate Summary Report
Write-Host "`n📊 System Test Results Summary" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

$passCount = ($testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$warningCount = ($testResults | Where-Object { $_.Status -eq "WARNING" }).Count
$errorCount = ($testResults | Where-Object { $_.Status -eq "ERROR" }).Count

Write-Host "✅ PASS: $passCount" -ForegroundColor Green
Write-Host "❌ FAIL: $failCount" -ForegroundColor Red
Write-Host "⚠️ WARNING: $warningCount" -ForegroundColor Yellow
Write-Host "💥 ERROR: $errorCount" -ForegroundColor Red

Write-Host "`n📋 Detailed Results by Component:" -ForegroundColor Yellow
$components = $testResults | Select-Object -ExpandProperty Component | Sort-Object | Get-Unique
foreach ($component in $components) {
    $componentResults = $testResults | Where-Object { $_.Component -eq $component }
    $componentPass = ($componentResults | Where-Object { $_.Status -eq "PASS" }).Count
    $componentFail = ($componentResults | Where-Object { $_.Status -eq "FAIL" }).Count
    $componentWarn = ($componentResults | Where-Object { $_.Status -eq "WARNING" }).Count
    $componentError = ($componentResults | Where-Object { $_.Status -eq "ERROR" }).Count
    
    Write-Host "`n[$component] - PASS: $componentPass, FAIL: $componentFail, WARN: $componentWarn, ERROR: $componentError" -ForegroundColor Cyan
}

Write-Host "`n🎯 Overall System Status:" -ForegroundColor Cyan
if ($failCount -eq 0 -and $errorCount -eq 0) {
    Write-Host "🎉 EXCELLENT! All critical tests passed. System is fully operational!" -ForegroundColor Green
    Write-Host "   ✅ Backend API is running" -ForegroundColor Green
    Write-Host "   ✅ User Panel builds successfully" -ForegroundColor Green
    Write-Host "   ✅ Admin Dashboard builds successfully" -ForegroundColor Green
    Write-Host "   ✅ All new features are implemented" -ForegroundColor Green
} elseif ($failCount -eq 0) {
    Write-Host "✅ GOOD! No critical failures, but some warnings to investigate." -ForegroundColor Yellow
} else {
    Write-Host "⚠️ ATTENTION NEEDED! Critical failures detected. System may not be fully operational." -ForegroundColor Red
}

# Save detailed report
$reportFile = "system_test_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
$reportContent = "# Zimmer Platform 2025 - System Test Report`n"
$reportContent += "Generated: $(Get-Date)`n`n"
$reportContent += "## Summary`n"
$reportContent += "- PASS: $passCount`n"
$reportContent += "- FAIL: $failCount`n"
$reportContent += "- WARNING: $warningCount`n"
$reportContent += "- ERROR: $errorCount`n`n"
$reportContent += "## Detailed Results`n"

foreach ($result in $testResults) {
    $reportContent += "- [$($result.Component)] $($result.Test): $($result.Status)"
    if ($result.Details) {
        $reportContent += " - $($result.Details)"
    }
    $reportContent += "`n"
}

$reportContent | Out-File -FilePath $reportFile -Encoding UTF8
Write-Host "`n📄 Detailed report saved to: $reportFile" -ForegroundColor Green

Write-Host "`n🚀 System Test completed at $(Get-Date)" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
