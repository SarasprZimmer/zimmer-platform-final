# Admin Dashboard Authentication System

## Overview

The admin dashboard now uses a robust authentication system with automatic token refresh and proper session management.

## Architecture

### 1. Auth Client (`lib/auth-client.ts`)
- Manages access tokens in memory (not stored in localStorage/cookies)
- Provides utility functions for token management
- Handles redirects with reason parameters

### 2. API Client (`lib/api.ts`)
- Central axios instance with interceptors
- Automatic token refresh on 401 errors
- Proper error handling and redirects
- Includes comprehensive admin API methods

### 3. Auth Context (`contexts/AuthContext.tsx`)
- React context for authentication state
- Handles login, logout, and token refresh
- Manages expired session messages
- Integrates with keep-alive system

### 4. Protected Routes (`components/ProtectedRoute.tsx`)
- Guards routes requiring authentication
- Shows loading states during auth checks
- Automatic redirect to login on auth failure

### 5. Keep-Alive System (`lib/keep-alive.ts`)
- Monitors user activity
- Refreshes tokens every 10 minutes if user is active
- Respects idle timeout (5 minutes)

## Key Features

### ✅ Automatic Token Refresh
- On 401 error → attempts refresh → retries original request
- On refresh failure → clears token → redirects to `/login?reason=expired`

### ✅ Session Management
- Access tokens stored in memory only
- Refresh tokens handled by httpOnly cookies from backend
- Proper cleanup on logout

### ✅ Idle UX
- Keeps session alive when user is active
- Allows natural expiration when idle
- Monitors mouse, keyboard, and touch events

### ✅ Persian Messages
- Expired session banner: "نشست شما منقضی شده است. لطفاً دوباره وارد شوید."
- Loading states in Persian
- Error messages in Persian

### ✅ Logout Button
- POST `/api/auth/logout` with credentials
- Clears memory token
- Redirects to login page

## Usage

### Login Flow
```typescript
const { login } = useAuth()
await login(email, password)
// Automatic redirect to dashboard
```

### API Calls
```typescript
import { adminAPI } from '@/lib/api'

// All API calls automatically handle authentication
const users = await adminAPI.getUsers()
const tickets = await adminAPI.getTickets()
```

### Protected Routes
```typescript
import ProtectedRoute from '@/components/ProtectedRoute'

<ProtectedRoute>
  <YourComponent />
</ProtectedRoute>
```

### Logout
```typescript
const { logout } = useAuth()
await logout()
// Automatic redirect to login
```

## Migration from Old System

The old `lib/auth.ts` file is deprecated but maintained for backward compatibility. It now redirects to the new system with console warnings.

### Old → New
- `getToken()` → `authClient.getAccessToken()`
- `setToken()` → `authClient.setAccessToken()`
- `removeToken()` → `authClient.clearAccessToken()`
- `login()` → `authAPI.login()`
- `logout()` → `authAPI.logout()`
- `isAuthenticated()` → `authClient.isAuthenticated()`

## Security Features

- ✅ Access tokens never stored in localStorage/cookies
- ✅ Refresh tokens in httpOnly cookies (XSS protection)
- ✅ Automatic token rotation
- ✅ Idle timeout handling
- ✅ Proper cleanup on logout
- ✅ CSRF protection via httpOnly cookies

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Backend Requirements

The backend must support:
- `POST /api/auth/login` - Login endpoint
- `POST /api/auth/refresh` - Token refresh endpoint  
- `POST /api/auth/logout` - Logout endpoint
- `GET /api/me` - Current user endpoint
- httpOnly cookies for refresh tokens
- CORS with credentials support
