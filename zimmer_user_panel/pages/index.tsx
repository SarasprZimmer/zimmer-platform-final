

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Cookies from 'js-cookie'

export default function HomePage() {
  const router = useRouter()
  const [isHydrated, setIsHydrated] = useState(false)

  // Mark as hydrated after first render
  useEffect(() => {
    setIsHydrated(true)
  }, [])

  useEffect(() => {
    if (!isHydrated) return; // Don't run until hydrated

    const token = Cookies.get('auth-token')
    
    if (!token) {
      router.push('/login')
    } else {
      router.push('/dashboard')
    }
  }, [router, isHydrated])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <p className="text-gray-600">در حال هدایت...</p>
      </div>
    </div>
  )
}
