# Authentication Troubleshooting Guide

## Problem: User Panel Keeps Logging Me Out

If you're experiencing frequent logout issues where the user panel keeps logging you out unexpectedly, this guide will help you understand and fix the problem.

## Root Causes

### 1. **Token Expiration**
- **Access tokens expire every 15 minutes** for security
- **Keep-alive mechanism refreshes tokens every 8 minutes** (before expiration)
- If the refresh fails, you get logged out

### 2. **Session Idle Timeout**
- **Sessions expire after 120 minutes of inactivity**
- Moving your mouse, typing, or scrolling resets this timer
- If you're away from the computer, the session expires

### 3. **Backend Connectivity Issues**
- If the backend server is down or unreachable
- Network issues between frontend and backend
- Firewall or proxy blocking connections

### 4. **Browser Issues**
- Cookies disabled or blocked
- Browser extensions interfering with authentication
- Cache/cookie corruption

## Solutions

### **Immediate Fixes**

#### 1. **Manual Token Refresh**
- Look for the **🔄 تازه‌سازی توکن** button on the dashboard
- Click it to manually refresh your authentication token
- This should resolve immediate logout issues

#### 2. **Check Backend Status**
- Visit: `http://localhost:8000/health`
- Should show: `{"status": "healthy", "service": "zimmer-dashboard"}`
- If this fails, the backend is down

#### 3. **Restart Backend Server**
```bash
# Windows
cd zimmer-backend
start_backend.bat

# Unix/Linux/Mac
cd zimmer-backend
./start_backend.sh
```

### **Prevention Strategies**

#### 1. **Keep the Page Active**
- **Move your mouse** or **scroll** occasionally
- **Type** in any input field
- **Click** on page elements
- This keeps your session alive

#### 2. **Regular Activity**
- The system automatically refreshes tokens every 8 minutes
- As long as you're active, this happens seamlessly
- No manual intervention needed

#### 3. **Browser Settings**
- **Enable cookies** for localhost
- **Allow local storage**
- **Disable ad blockers** for localhost (if they interfere)

## Detailed Error Messages

### **"نشست منقضی شده" (Session Expired)**
- **Cause**: Your session timed out due to inactivity
- **Solution**: Simply log in again
- **Prevention**: Stay active on the page

### **"سرور در دسترس نیست" (Server Unavailable)**
- **Cause**: Backend server is down or unreachable
- **Solution**: Start the backend server
- **Prevention**: Ensure backend is running before using frontend

### **"توکن نامعتبر" (Invalid Token)**
- **Cause**: Authentication token is corrupted or expired
- **Solution**: Log in again
- **Prevention**: Use the manual refresh button if available

### **"تازه‌سازی توکن ناموفق" (Token Refresh Failed)**
- **Cause**: Automatic token refresh failed
- **Solution**: Try manual refresh or log in again
- **Prevention**: Check backend connectivity

## Technical Details

### **Token Lifecycle**
```
Login → Access Token (15 min) → Keep-alive Refresh (8 min) → New Token (15 min)
```

### **Session Management**
- **Refresh tokens**: Stored in secure HTTP-only cookies
- **Access tokens**: Stored in memory (cleared on logout)
- **Session data**: Stored in database with expiration tracking

### **Keep-alive Mechanism**
- **Frequency**: Every 8 minutes (before 15-minute token expiry)
- **Triggers**: User activity (mouse, keyboard, touch)
- **Fallback**: Manual refresh button available

## Debugging Steps

### **1. Check Browser Console**
- Press `F12` to open Developer Tools
- Look for authentication-related errors
- Check Network tab for failed requests

### **2. Verify Backend Status**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if port 8000 is in use
# Windows
netstat -ano | findstr :8000

# Unix/Linux/Mac
lsof -ti:8000
```

### **3. Test Authentication Endpoints**
```bash
# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Test refresh endpoint
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Cookie: refresh_token=your_token_here"
```

## Common Scenarios

### **Scenario 1: Frequent Logouts During Work**
- **Cause**: Keep-alive mechanism failing
- **Solution**: Check backend connectivity
- **Prevention**: Ensure stable network connection

### **Scenario 2: Logout After Computer Sleep**
- **Cause**: Session expired during inactivity
- **Solution**: Log in again
- **Prevention**: Wake computer before session expires (120 min)

### **Scenario 3: Logout on Page Refresh**
- **Cause**: Token not properly stored or corrupted
- **Solution**: Clear browser cache and cookies
- **Prevention**: Use manual refresh button if available

### **Scenario 4: Multiple Users Logged Out**
- **Cause**: Backend server restart or database issue
- **Solution**: Restart backend server
- **Prevention**: Regular backend maintenance

## Best Practices

### **For Users**
1. **Stay active** on the page while working
2. **Use manual refresh** if experiencing issues
3. **Check backend status** if problems persist
4. **Report issues** with specific error messages

### **For Developers**
1. **Monitor backend logs** for authentication errors
2. **Check database session tables** for expired sessions
3. **Verify network connectivity** between services
4. **Test authentication flow** regularly

## Support

If you continue to experience issues:

1. **Check the troubleshooting steps** above
2. **Verify backend is running** and accessible
3. **Clear browser cache and cookies**
4. **Try a different browser** to isolate the issue
5. **Check network connectivity** and firewall settings
6. **Review backend logs** for error messages

## Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Frequent logouts | Keep-alive failing | Manual refresh button |
| Logout after inactivity | Session timeout | Log in again |
| Can't access at all | Backend down | Start backend server |
| Logout on refresh | Token corruption | Clear browser cache |
| Multiple users affected | Backend issue | Restart backend |

Remember: **Most logout issues can be resolved by ensuring the backend is running and using the manual refresh button when needed.**
