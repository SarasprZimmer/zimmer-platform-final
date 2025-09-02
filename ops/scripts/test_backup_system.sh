#!/usr/bin/env bash
set -euo pipefail

# Comprehensive backup system test
# Tests all components of the backup and restore system

echo "🧪 Testing Zimmer Backup System"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to run tests
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing: $test_name... "
    
    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Check if required directories exist
run_test "Backup directory structure" "[ -d 'ops/backup/archives' ]"

# Test 2: Check if all scripts exist and are executable
run_test "Backup script exists" "[ -f 'ops/scripts/backup_db.sh' ]"
run_test "Restore script exists" "[ -f 'ops/scripts/restore_db.sh' ]"
run_test "Test restore script exists" "[ -f 'ops/scripts/test_restore.sh' ]"
run_test "Latest backup script exists" "[ -f 'ops/scripts/latest_backup.sh' ]"
run_test "Backup status script exists" "[ -f 'ops/scripts/backup_status.sh' ]"

# Test 3: Check if restore compose file exists
run_test "Restore compose file exists" "[ -f 'ops/restore-compose.yml' ]"

# Test 4: Check if production compose file exists
run_test "Production compose file exists" "[ -f 'docker-compose.prod.yml' ]"

# Test 5: Check if Docker is available
run_test "Docker is available" "docker --version >/dev/null 2>&1"

# Test 6: Check if Docker Compose is available
run_test "Docker Compose is available" "docker compose version >/dev/null 2>&1"

# Test 7: Check if required tools are available
run_test "sha256sum is available" "sha256sum --version >/dev/null 2>&1"

# Test 8: Check if scripts are executable (on Unix-like systems)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    run_test "Backup script is executable" "[ -x 'ops/scripts/backup_db.sh' ]"
    run_test "Restore script is executable" "[ -x 'ops/scripts/restore_db.sh' ]"
    run_test "Test restore script is executable" "[ -x 'ops/scripts/test_restore.sh' ]"
    run_test "Latest backup script is executable" "[ -x 'ops/scripts/latest_backup.sh' ]"
    run_test "Backup status script is executable" "[ -x 'ops/scripts/backup_status.sh' ]"
else
    echo -e "${YELLOW}Skipping executable tests on Windows${NC}"
fi

# Test 9: Check if restore environment can be started
echo -n "Testing: Restore environment startup... "
if docker compose -f ops/restore-compose.yml up -d postgres-restore >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
    
    # Wait a moment for container to start
    sleep 5
    
    # Test 10: Check if restore environment is healthy
    echo -n "Testing: Restore environment health... "
    if docker inspect --format='{{json .State.Health.Status}}' zimmer_postgres_restore 2>/dev/null | grep -q healthy; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
    
    # Clean up
    docker compose -f ops/restore-compose.yml down >/dev/null 2>&1
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 11: Check if latest_backup script works with no backups
echo -n "Testing: Latest backup script (no backups)... "
if ! bash ops/scripts/latest_backup.sh 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Test 12: Check if backup status script works
echo -n "Testing: Backup status script... "
if bash ops/scripts/backup_status.sh >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "📊 Test Results"
echo "==============="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo "Total tests: $((TESTS_PASSED + TESTS_FAILED))"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! Backup system is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start your production stack: docker compose -f docker-compose.prod.yml up -d"
    echo "2. Create your first backup: bash ops/scripts/backup_db.sh"
    echo "3. Test restore: bash ops/scripts/test_restore.sh"
    echo "4. Monitor status: bash ops/scripts/backup_status.sh"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Please check the issues above.${NC}"
    exit 1
fi
