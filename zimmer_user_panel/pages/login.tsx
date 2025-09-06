'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/router'
import { fetchCsrf } from '@/lib/csrf'
import TwoFADialog from '@/components/TwoFADialog'
import { Toast } from '@/components/Toast'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [mounted, setMounted] = useState(false)
  const [toast, setToast] = useState<string | null>(null)
  const [challenge, setChallenge] = useState<string | null>(null)
  const { isAuthenticated, login: authLogin } = useAuth()
  const router = useRouter()

  useEffect(() => {
    setMounted(true)
    if (isAuthenticated) {
      router.push('/dashboard')
    }
    fetchCsrf(process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000");
  }, [isAuthenticated, router])



  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await authLogin(email, password)
      setToast("خوش آمدید!")
      // The AuthContext will handle the redirect to dashboard
    } catch (err: any) {
      if (err?.status === 401 && err?.data?.error === "otp_required" && err?.data?.challenge_token) {
        setChallenge(err.data.challenge_token);
      } else {
        setError(err.message || 'خطا در اتصال به سرور')
      }
    } finally {
      setLoading(false)
    }
  }

  if (!mounted) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-green-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          {/* Expired Session Message */}


          {/* Logo */}
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-purple-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
              <span className="text-white font-bold text-3xl">Z</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Zimmer AI</h1>
            <p className="text-gray-600">ورود به پنل کاربری</p>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                ایمیل
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@email.com"
                className="w-full px-4 py-4 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 bg-gray-50 hover:bg-white"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                رمز عبور
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-4 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 bg-gray-50 hover:bg-white"
                required
              />
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
                <p className="text-sm text-red-800 text-center">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white py-4 px-6 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                  در حال ورود...
                </div>
              ) : (
                'ورود'
              )}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-8 text-center space-y-4">
            <p className="text-sm text-gray-500">
              حساب کاربری ندارید؟{' '}
              <Link href="/signup" className="text-purple-600 hover:text-purple-700 font-medium transition-colors">
                ثبت نام کنید
              </Link>
            </p>
            <p className="text-sm text-gray-500">
              <Link href="/forgot-password" className="text-purple-600 hover:text-purple-700 font-medium transition-colors">
                فراموشی رمز عبور
              </Link>
            </p>
          </div>
        </div>
      </div>
      {challenge && (
        <TwoFADialog
          challengeToken={challenge}
          onSuccess={() => { 
            setChallenge(null); 
            setToast("ورود موفق!"); 
            // The AuthContext will handle the redirect to dashboard
          }}
          onCancel={() => setChallenge(null)}
        />
      )}
      {toast && <Toast msg={toast} onDone={()=>setToast(null)} />}
    </div>
  )
}
