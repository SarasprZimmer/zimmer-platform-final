#!/bin/bash

# Zimmer Platform Startup Script
# Starts all three parts of the Zimmer platform:
# - Backend API (FastAPI)
# - Admin Dashboard (Next.js)
# - User Panel (Next.js)

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${2}${1}${NC}"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local service_name=$1
    local url=$2
    local timeout=${3:-30}
    
    print_color "⏳ Waiting for $service_name to be ready..." $YELLOW
    
    local start_time=$(date +%s)
    local end_time=$((start_time + timeout))
    
    while [ $(date +%s) -lt $end_time ]; do
        if curl -s -f "$url" >/dev/null 2>&1; then
            print_color "✅ $service_name is ready!" $GREEN
            return 0
        fi
        sleep 1
    done
    
    print_color "❌ $service_name failed to start within $timeout seconds" $RED
    return 1
}

# Function to start a service
start_service() {
    local service_name=$1
    local command=$2
    local working_dir=$3
    local success_url=$4
    
    print_color "🚀 Starting $service_name..." $BLUE
    
    if [ -n "$working_dir" ] && [ -d "$working_dir" ]; then
        cd "$working_dir"
    fi
    
    if [ -n "$success_url" ]; then
        # Start in background and wait for it to be ready
        eval "$command" &
        local pid=$!
        sleep 3
        
        if wait_for_service "$service_name" "$success_url"; then
            return 0
        else
            kill $pid 2>/dev/null || true
            return 1
        fi
    else
        # Start in background without waiting
        eval "$command" &
        sleep 2
        return 0
    fi
}

# Main script
print_color "🎯 Zimmer Platform Startup Script" $BLUE
print_color "=====================================" $BLUE
echo ""

# Check if we're in the right directory
if [ ! -d "zimmer-backend" ] || [ ! -d "zimmermanagement" ] || [ ! -d "zimmer_user_panel" ]; then
    print_color "❌ Error: Please run this script from the zimmer-full-structure root directory" $RED
    print_color "   Expected structure:" $YELLOW
    print_color "   ├── zimmer-backend/" $YELLOW
    print_color "   ├── zimmermanagement/" $YELLOW
    print_color "   └── zimmer_user_panel/" $YELLOW
    exit 1
fi

# Check if required ports are available
declare -A ports=(
    ["Backend API"]=8000
    ["Admin Dashboard"]=3000
    ["User Panel"]=3001
)

print_color "🔍 Checking port availability..." $BLUE
for service in "${!ports[@]}"; do
    port=${ports[$service]}
    if check_port $port; then
        print_color "⚠️  Port $port is already in use. $service might not start properly." $YELLOW
    else
        print_color "✅ Port $port is available for $service" $GREEN
    fi
done
echo ""

# Parse command line arguments
SKIP_BACKEND=false
SKIP_ADMIN=false
SKIP_USER_PANEL=false
RUN_MIGRATION=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-backend)
            SKIP_BACKEND=true
            shift
            ;;
        --skip-admin)
            SKIP_ADMIN=true
            shift
            ;;
        --skip-user-panel)
            SKIP_USER_PANEL=true
            shift
            ;;
        --migrate)
            RUN_MIGRATION=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-backend     Skip starting the backend API"
            echo "  --skip-admin       Skip starting the admin dashboard"
            echo "  --skip-user-panel  Skip starting the user panel"
            echo "  --migrate          Run database migration before starting"
            echo "  --help             Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Start all services"
            echo "  $0 --migrate          # Run migration and start all services"
            echo "  $0 --skip-backend     # Start only admin dashboard and user panel"
            exit 0
            ;;
        *)
            print_color "❌ Unknown option: $1" $RED
            print_color "Use --help for usage information" $YELLOW
            exit 1
            ;;
    esac
done

# Run database migration if requested
if [ "$RUN_MIGRATION" = true ]; then
    print_color "��️  Running database migration..." $BLUE
    cd zimmer-backend
    if python scripts/migrate_integration_columns.py; then
        print_color "✅ Database migration completed successfully" $GREEN
    else
        print_color "❌ Database migration failed" $RED
    fi
    cd ..
    echo ""
fi

# Start services
services_started=()

# Start Backend API
if [ "$SKIP_BACKEND" = false ]; then
    if start_service "Backend API" "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000" "zimmer-backend" "http://localhost:8000/health"; then
        services_started+=("Backend API")
    fi
fi

# Start Admin Dashboard
if [ "$SKIP_ADMIN" = false ]; then
    if start_service "Admin Dashboard" "npm run dev" "zimmermanagement/zimmer-admin-dashboard" "http://localhost:3000"; then
        services_started+=("Admin Dashboard")
    fi
fi

# Start User Panel
if [ "$SKIP_USER_PANEL" = false ]; then
    if start_service "User Panel" "npm run dev -- -p 3001" "zimmer_user_panel" "http://localhost:3001"; then
        services_started+=("User Panel")
    fi
fi

# Summary
echo ""
print_color "🎉 Zimmer Platform Startup Summary" $BLUE
print_color "===================================" $BLUE

if [ ${#services_started[@]} -gt 0 ]; then
    print_color "✅ Successfully started services:" $GREEN
    for service in "${services_started[@]}"; do
        print_color "   • $service" $GREEN
    done
    
    echo ""
    print_color "🌐 Access URLs:" $BLUE
    if [[ " ${services_started[@]} " =~ " Backend API " ]]; then
        print_color "   • Backend API: http://localhost:8000" $BLUE
        print_color "   • API Docs: http://localhost:8000/docs" $BLUE
    fi
    if [[ " ${services_started[@]} " =~ " Admin Dashboard " ]]; then
        print_color "   • Admin Dashboard: http://localhost:3000" $BLUE
    fi
    if [[ " ${services_started[@]} " =~ " User Panel " ]]; then
        print_color "   • User Panel: http://localhost:3001" $BLUE
    fi
    
    echo ""
    print_color "�� Tips:" $YELLOW
    print_color "   • Each service runs in its own process" $YELLOW
    print_color "   • Use Ctrl+C to stop all services" $YELLOW
    print_color "   • Check the console output for any errors" $YELLOW
    print_color "   • Services will automatically reload on file changes" $YELLOW
else
    print_color "❌ No services were started successfully" $RED
fi

echo ""
print_color "🎯 Happy coding with Zimmer! 🚀" $GREEN

# Keep script running to maintain background processes
if [ ${#services_started[@]} -gt 0 ]; then
    echo ""
    print_color "Press Ctrl+C to stop all services" $YELLOW
    wait
fi