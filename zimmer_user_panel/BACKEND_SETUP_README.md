# Backend Setup Guide - Fix Loading Issue

## Problem
The user panel dashboard is stuck in a loading state because it cannot connect to the backend API at `http://localhost:8000`.

## Solution
You need to start the Zimmer Backend server before using the user panel.

## Quick Start

### Option 1: Using the Startup Scripts (Recommended)

#### Windows Users:
1. Open Command Prompt or PowerShell
2. Navigate to the backend directory:
   ```cmd
   cd zimmer-backend
   ```
3. Run the startup script:
   ```cmd
   start_backend.bat
   ```

#### Unix/Linux/Mac Users:
1. Open Terminal
2. Navigate to the backend directory:
   ```bash
   cd zimmer-backend
   ```
3. Make the script executable (first time only):
   ```bash
   chmod +x start_backend.sh
   ```
4. Run the startup script:
   ```bash
   ./start_backend.sh
   ```

### Option 2: Manual Setup

1. **Install Python Dependencies:**
   ```bash
   cd zimmer-backend
   pip install -r requirements.txt
   ```

2. **Start the Server:**
   ```bash
   python start_backend.py
   ```

## What Happens When You Start the Backend

1. **Server Starts:** FastAPI server runs on `http://localhost:8000`
2. **Health Check Available:** Visit `http://localhost:8000/health` to verify
3. **API Documentation:** Visit `http://localhost:8000/docs` for API docs
4. **User Panel Works:** The dashboard will now load properly

## Verification

After starting the backend:

1. **Check Backend Status:**
   - Visit: `http://localhost:8000/health`
   - Should show: `{"status": "healthy", "service": "zimmer-dashboard"}`

2. **Check User Panel:**
   - Visit: `http://localhost:3000/dashboard`
   - Should now load the full dashboard instead of being stuck loading

## Troubleshooting

### "Module not found" errors:
```bash
pip install -r requirements.txt
```

### Port 8000 already in use:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Unix/Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Backend starts but user panel still doesn't work:
1. Check browser console for errors
2. Verify backend is running on `http://localhost:8000`
3. Check if there are CORS issues in browser console

## Development Workflow

1. **Start Backend First:**
   ```bash
   cd zimmer-backend
   python start_backend.py
   ```

2. **Start User Panel:**
   ```bash
   cd zimmer_user_panel
   npm run dev
   ```

3. **Access:**
   - Backend API: `http://localhost:8000`
   - User Panel: `http://localhost:3000`
   - API Docs: `http://localhost:8000/docs`

## Environment Variables

The backend will use these default settings:
- **Host:** `127.0.0.1` (localhost)
- **Port:** `8000`
- **Database:** SQLite (default)

To customize, create a `.env` file in the backend directory:
```env
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./zimmer_dashboard.db
```

## Next Steps

Once the backend is running:
1. The user panel will automatically redirect to login if not authenticated
2. You can create a test account or use existing credentials
3. The full dashboard functionality will be available
4. All navigation links (Payment, Settings, Automations) will work properly

## Support

If you continue to have issues:
1. Check the backend console for error messages
2. Check the browser console for network errors
3. Verify both services are running on the correct ports
4. Ensure no firewall is blocking the connections
