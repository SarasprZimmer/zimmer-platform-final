'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import { authClient } from '@/lib/auth-client'
import { authAPI } from '@/lib/api'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, refreshToken } = useAuth()
  const router = useRouter()
  const [authChecking, setAuthChecking] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // If we have an access token, try to validate it
        if (authClient.isAuthenticated()) {
          try {
            await authAPI.getCurrentUser()
            // Token is valid, we're authenticated
            setAuthChecking(false)
            return
          } catch (error) {
            // Token is invalid, try to refresh
            console.log('Token invalid, attempting refresh...')
          }
        }

        // Try to refresh token
        try {
          await refreshToken()
          setAuthChecking(false)
        } catch (error) {
          // Refresh failed, redirect to login
          console.log('Refresh failed, redirecting to login')
          router.push('/login')
        }
      } catch (error) {
        console.error('Auth check error:', error)
        router.push('/login')
      }
    }

    if (!isLoading) {
      checkAuth()
    }
  }, [isLoading, refreshToken, router])

  // Show loading skeleton while checking auth
  if (isLoading || authChecking) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">در حال بررسی احراز هویت...</p>
        </div>
      </div>
    )
  }

  // If not authenticated, show loading (will redirect)
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">در حال انتقال به صفحه ورود...</p>
        </div>
      </div>
    )
  }

  // User is authenticated, render children
  return <>{children}</>
} 