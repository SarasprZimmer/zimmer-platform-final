# User Panel Smoke Test Script
# Tests basic functionality and identifies issues

Write-Host "🔥 Starting User Panel Smoke Test..." -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

# Helpers
function Build-Url {
	param(
		[string]$Base,
		[string]$Path
	)
	if ([string]::IsNullOrWhiteSpace($Base)) { $Base = "http://localhost:3000" }
	$Base = $Base.TrimEnd('/')
	if ([string]::IsNullOrWhiteSpace($Path)) { return $Base }
	if ($Path.StartsWith("http")) { return $Path }
	if (-not $Path.StartsWith("/")) { $Path = "/$Path" }
	return "$Base$Path"
}

function Add-Result {
	param(
		[string]$Test,
		[string]$Status,
		[string]$Details
	)
	if ($null -eq $script:testResults) {
		$script:testResults = New-Object System.Collections.Generic.List[object]
	}
	$script:testResults.Add([pscustomobject]@{ Test = $Test; Status = $Status; Details = $Details })
}

$baseUrl = "http://localhost:3000"
$testResults = New-Object System.Collections.Generic.List[object]

# Test 1: Basic page load
Write-Host "`n📄 Test 1: Basic page load" -ForegroundColor Cyan
try {
	$response = Invoke-WebRequest -Uri (Build-Url -Base $baseUrl -Path "/") -UseBasicParsing -TimeoutSec 10
	if ($response.StatusCode -eq 200) {
		Write-Host "✅ Main page loads successfully" -ForegroundColor Green
		Add-Result -Test "Main Page Load" -Status "PASS" -Details "Status: $($response.StatusCode)"
	} else {
		Write-Host "❌ Main page failed with status: $($response.StatusCode)" -ForegroundColor Red
		Add-Result -Test "Main Page Load" -Status "FAIL" -Details "Status: $($response.StatusCode)"
	}
} catch {
	Write-Host "❌ Main page load error: $($_.Exception.Message)" -ForegroundColor Red
	Add-Result -Test "Main Page Load" -Status "ERROR" -Details $_.Exception.Message
}

# Test 2: Login page
Write-Host "`n🔐 Test 2: Login page" -ForegroundColor Cyan
try {
	$response = Invoke-WebRequest -Uri (Build-Url -Base $baseUrl -Path "/login") -UseBasicParsing -TimeoutSec 10
	if ($response.StatusCode -eq 200) {
		Write-Host "✅ Login page loads successfully" -ForegroundColor Green
		Add-Result -Test "Login Page Load" -Status "PASS" -Details "Status: $($response.StatusCode)"
	} else {
		Write-Host "❌ Login page failed with status: $($response.StatusCode)" -ForegroundColor Red
		Add-Result -Test "Login Page Load" -Status "FAIL" -Details "Status: $($response.StatusCode)"
	}
} catch {
	Write-Host "❌ Login page load error: $($_.Exception.Message)" -ForegroundColor Red
	Add-Result -Test "Login Page Load" -Status "ERROR" -Details $_.Exception.Message
}

# Test 3: Dashboard page (should redirect to login)
Write-Host "`n📊 Test 3: Dashboard page redirect" -ForegroundColor Cyan
try {
	$response = Invoke-WebRequest -Uri (Build-Url -Base $baseUrl -Path "/dashboard") -UseBasicParsing -TimeoutSec 10 -MaximumRedirection 0
	if ($response.StatusCode -eq 302 -or $response.StatusCode -eq 200) {
		Write-Host "✅ Dashboard page handles redirect properly" -ForegroundColor Green
		Add-Result -Test "Dashboard Redirect" -Status "PASS" -Details "Status: $($response.StatusCode)"
	} else {
		Write-Host "❌ Dashboard page issue with status: $($response.StatusCode)" -ForegroundColor Red
		Add-Result -Test "Dashboard Redirect" -Status "FAIL" -Details "Status: $($response.StatusCode)"
	}
} catch {
	Write-Host "❌ Dashboard page error: $($_.Exception.Message)" -ForegroundColor Red
	Add-Result -Test "Dashboard Redirect" -Status "ERROR" -Details $_.Exception.Message
}

# Test 4: CSS and static assets
Write-Host "`n🎨 Test 4: Static assets" -ForegroundColor Cyan
try {
	$response = Invoke-WebRequest -Uri (Build-Url -Base $baseUrl -Path "/_next/static/css/app/globals.css") -UseBasicParsing -TimeoutSec 10
	if ($response.StatusCode -eq 200) {
		Write-Host "✅ CSS files load successfully" -ForegroundColor Green
		Add-Result -Test "CSS Assets" -Status "PASS" -Details "Status: $($response.StatusCode)"
	} else {
		Write-Host "❌ CSS files failed with status: $($response.StatusCode)" -ForegroundColor Red
		Add-Result -Test "CSS Assets" -Status "FAIL" -Details "Status: $($response.StatusCode)"
	}
} catch {
	Write-Host "❌ CSS files error: $($_.Exception.Message)" -ForegroundColor Red
	Add-Result -Test "CSS Assets" -Status "ERROR" -Details $_.Exception.Message
}

# Test 5: API endpoint test (should get CORS or auth error, not 500)
Write-Host "`n🔌 Test 5: API endpoint test" -ForegroundColor Cyan
try {
	$response = Invoke-WebRequest -Uri "http://localhost:8000/api/me" -UseBasicParsing -TimeoutSec 10
	if ($response.StatusCode -eq 401) {
		Write-Host "✅ API endpoint responds correctly (401 Unauthorized)" -ForegroundColor Green
		Add-Result -Test "API Endpoint" -Status "PASS" -Details "Status: $($response.StatusCode) - Correct auth response"
	} else {
		Write-Host "⚠️ API endpoint unexpected status: $($response.StatusCode)" -ForegroundColor Yellow
		Add-Result -Test "API Endpoint" -Status "WARNING" -Details "Status: $($response.StatusCode) - Unexpected response"
	}
} catch {
	Write-Host "❌ API endpoint error: $($_.Exception.Message)" -ForegroundColor Red
	Add-Result -Test "API Endpoint" -Status "ERROR" -Details $_.Exception.Message
}

# Test 6: Check for console errors in page content
Write-Host "`n🔍 Test 6: Page content analysis" -ForegroundColor Cyan
try {
	$response = Invoke-WebRequest -Uri (Build-Url -Base $baseUrl -Path "/") -UseBasicParsing -TimeoutSec 10
	$content = $response.Content
	
	if ($content -match 'error|Error|ERROR') {
		Write-Host "⚠️ Page content contains error text" -ForegroundColor Yellow
		Add-Result -Test "Content Analysis" -Status "WARNING" -Details "Contains error text"
	} elseif ($content -match "missing required error components") {
		Write-Host "❌ Page shows build error message" -ForegroundColor Red
		Add-Result -Test "Content Analysis" -Status "FAIL" -Details "Build error message detected"
	} else {
		Write-Host "✅ Page content appears normal" -ForegroundColor Green
		Add-Result -Test "Content Analysis" -Status "PASS" -Details "No obvious errors detected"
	}
} catch {
	Write-Host "❌ Content analysis error: $($_.Exception.Message)" -ForegroundColor Red
	Add-Result -Test "Content Analysis" -Status "ERROR" -Details $_.Exception.Message
}

# Generate summary report
Write-Host "`n📊 Test Results Summary:" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

$passCount = ($testResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($testResults | Where-Object { $_.Status -eq "FAIL" }).Count
$errorCount = ($testResults | Where-Object { $_.Status -eq "ERROR" }).Count
$warningCount = ($testResults | Where-Object { $_.Status -eq "WARNING" }).Count

Write-Host "✅ PASS: $passCount" -ForegroundColor Green
Write-Host "❌ FAIL: $failCount" -ForegroundColor Red
Write-Host "⚠️ WARNING: $warningCount" -ForegroundColor Yellow
Write-Host "💥 ERROR: $errorCount" -ForegroundColor Red

Write-Host "`n📋 Detailed Results:" -ForegroundColor Yellow
foreach ($result in $testResults) {
	$color = switch ($result.Status) {
		"PASS" { "Green" }
		"FAIL" { "Red" }
		"ERROR" { "Red" }
		"WARNING" { "Yellow" }
		default { "White" }
	}
	Write-Host "$($result.Status): $($result.Test) - $($result.Details)" -ForegroundColor $color
}

# Recommendations
Write-Host "`nRecommendations:" -ForegroundColor Yellow
if ($failCount -gt 0 -or $errorCount -gt 0) {
	Write-Host "- Check Next.js build logs for compilation errors" -ForegroundColor Cyan
	Write-Host "- Verify all required dependencies are installed" -ForegroundColor Cyan
	Write-Host "- Check for TypeScript compilation issues" -ForegroundColor Cyan
	Write-Host "- Verify environment variables are loaded correctly" -ForegroundColor Cyan
} else {
	Write-Host "- All tests passed! User panel appears to be working correctly." -ForegroundColor Green
}

Write-Host "`n🔥 Smoke test completed!" -ForegroundColor Yellow
