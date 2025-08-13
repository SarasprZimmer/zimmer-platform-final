#!/bin/bash

# Zimmer Environment Setup Script
# This script creates .env files from the example templates

echo "🚀 Setting up Zimmer environment files..."

# Function to create env file if it doesn't exist
create_env_file() {
    local example_file=$1
    local env_file=$2
    local description=$3
    
    if [ ! -f "$env_file" ]; then
        if [ -f "$example_file" ]; then
            cp "$example_file" "$env_file"
            echo "✅ Created $description"
        else
            echo "❌ Example file $example_file not found"
        fi
    else
        echo "⚠️  $description already exists, skipping..."
    fi
}

# Create environment files
create_env_file "zimmer-backend/env.example" "zimmer-backend/.env" "Backend environment file"
create_env_file "zimmer_user_panel/env.example" "zimmer_user_panel/.env.local" "User Panel environment file"
create_env_file "zimmermanagement/zimmer-admin-dashboard/env.example" "zimmermanagement/zimmer-admin-dashboard/.env.local" "Admin Dashboard environment file"

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit the .env files with your specific values"
echo "2. Make sure JWT_SECRET_KEY is the same across all applications"
echo "3. Update API URLs if needed"
echo ""
echo "🔧 To start the applications:"
echo "  Backend: cd zimmer-backend && python main.py"
echo "  User Panel: cd zimmer_user_panel && npm run dev"
echo "  Admin Dashboard: cd zimmermanagement/zimmer-admin-dashboard && npm run dev" 