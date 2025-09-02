# Admin Notifications Page Test Guide

## Setup
1. Ensure the backend is running with notifications endpoints
2. Ensure you're logged in as an admin user
3. Navigate to `/notifications` in the admin dashboard

## Test Cases

### 1. Direct Notification to Specific Users
- **Mode**: "Send to Users"
- **User IDs**: Enter comma-separated user IDs (e.g., "1, 2, 3")
- **Type**: "system"
- **Title**: "Test Direct Notification"
- **Body**: "This is a test notification sent to specific users"
- **Expected**: Success message showing number of users notified

### 2. Broadcast to All Users
- **Mode**: "Broadcast"
- **Type**: "system"
- **Title**: "Test Broadcast"
- **Body**: "This is a test broadcast to all users"
- **Expected**: Success message showing number of users notified

### 3. Role-Based Broadcast
- **Mode**: "Broadcast"
- **Role**: "support_staff"
- **Type**: "system"
- **Title**: "Support Staff Notice"
- **Body**: "This is a test notification for support staff only"
- **Expected**: Success message showing number of support staff notified

### 4. Quick Templates
- Click each template button:
  - **Maintenance**: Should populate maintenance notification
  - **System Update**: Should populate system update notification
  - **Support Ticket**: Should populate support ticket notification
  - **Payment Success**: Should populate payment notification

### 5. JSON Data Validation
- **Mode**: "Broadcast"
- **Type**: "system"
- **Title**: "Test with Data"
- **Body**: "Testing JSON data"
- **Data**: `{"test": true, "deep_link": "/test"}`
- **Expected**: Success with JSON data included

### 6. Error Handling
- **Mode**: "Direct"
- **User IDs**: Leave empty
- **Expected**: Error message about user_ids being required

- **Mode**: "Direct"
- **User IDs**: "999, 1000" (non-existent users)
- **Expected**: Success message showing 0 users notified

## API Endpoints Tested
- `POST /api/admin/notifications` - Direct notifications
- `POST /api/admin/notifications/broadcast` - Broadcast notifications

## Features Verified
- ✅ Mode switching (Direct/Broadcast)
- ✅ User ID input validation
- ✅ Role-based filtering
- ✅ Quick templates
- ✅ JSON data handling
- ✅ Error handling
- ✅ Success feedback
- ✅ Form reset after submission
- ✅ Responsive design
- ✅ Admin-only access

## Notes
- All notifications require admin authentication
- The page uses the existing auth context and API client
- Templates are client-side only and don't persist
- JSON data is validated before sending to API
