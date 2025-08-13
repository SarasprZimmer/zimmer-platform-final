// Test script for KB Monitoring page functionality
// Run this in browser console on the KB monitoring page

console.log('🧪 Testing KB Monitoring Page...');

// Test 1: Check if page loads correctly
function testPageLoad() {
  console.log('✅ Page loaded successfully');
  console.log('📊 Title:', document.title);
  console.log('🔍 Main heading:', document.querySelector('h1')?.textContent);
}

// Test 2: Check if automations are loaded
function testAutomationsLoad() {
  const automationCards = document.querySelectorAll('[class*="border rounded-lg cursor-pointer"]');
  console.log('🤖 Automation cards found:', automationCards.length);
  
  if (automationCards.length > 0) {
    console.log('✅ Automations loaded successfully');
    automationCards.forEach((card, index) => {
      const name = card.querySelector('h4')?.textContent;
      console.log(`  ${index + 1}. ${name}`);
    });
  } else {
    console.log('⚠️ No automation cards found');
  }
}

// Test 3: Check if KB status table appears when automation is selected
function testKBStatusTable() {
  const table = document.querySelector('table');
  if (table) {
    console.log('✅ KB Status table found');
    const rows = table.querySelectorAll('tbody tr');
    console.log('📋 Table rows:', rows.length);
  } else {
    console.log('⚠️ KB Status table not found (automation may not be selected)');
  }
}

// Test 4: Check for error modal functionality
function testErrorModal() {
  const modal = document.querySelector('[class*="fixed inset-0 bg-gray-600"]');
  if (modal) {
    console.log('✅ Error modal component found');
  } else {
    console.log('ℹ️ Error modal not visible (normal state)');
  }
}

// Test 5: Check for refresh button
function testRefreshButton() {
  const refreshBtn = document.querySelector('button[class*="bg-blue-600"]');
  if (refreshBtn) {
    console.log('✅ Refresh button found');
    console.log('🔄 Button text:', refreshBtn.textContent.trim());
  } else {
    console.log('⚠️ Refresh button not found');
  }
}

// Test 6: Check for stats cards
function testStatsCards() {
  const statsCards = document.querySelectorAll('[class*="bg-white overflow-hidden shadow rounded-lg"]');
  console.log('📊 Stats cards found:', statsCards.length);
  
  if (statsCards.length >= 4) {
    console.log('✅ All stats cards present');
    statsCards.forEach((card, index) => {
      const title = card.querySelector('dt')?.textContent;
      const value = card.querySelector('dd')?.textContent;
      console.log(`  ${index + 1}. ${title}: ${value}`);
    });
  } else {
    console.log('⚠️ Missing stats cards');
  }
}

// Test 7: Check RTL support
function testRTLSupport() {
  const body = document.body;
  const isRTL = body.dir === 'rtl' || body.style.direction === 'rtl';
  console.log('🌐 RTL Support:', isRTL ? '✅ Enabled' : '⚠️ Not detected');
  
  // Check for Persian text
  const persianText = document.querySelector('h1')?.textContent;
  if (persianText && /[\u0600-\u06FF]/.test(persianText)) {
    console.log('🇮🇷 Persian text detected:', persianText);
  }
}

// Run all tests
function runAllTests() {
  console.log('🚀 Starting KB Monitoring Page Tests...\n');
  
  testPageLoad();
  console.log('');
  
  testAutomationsLoad();
  console.log('');
  
  testKBStatusTable();
  console.log('');
  
  testErrorModal();
  console.log('');
  
  testRefreshButton();
  console.log('');
  
  testStatsCards();
  console.log('');
  
  testRTLSupport();
  console.log('');
  
  console.log('🏁 All tests completed!');
}

// Auto-run tests after page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', runAllTests);
} else {
  runAllTests();
}

// Export for manual testing
window.testKBMonitoring = runAllTests; 