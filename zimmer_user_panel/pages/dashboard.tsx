

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import DashboardLayout from '@/components/DashboardLayout'
import AvailableAutomationsCard from '@/components/dashboard/AvailableAutomationsCard'
import PurchasedAutomationsCard from '@/components/dashboard/PurchasedAutomationsCard'
import TokenUsageCard from '@/components/dashboard/TokenUsageCard'


// Mock data for dashboard components
const mockAvailableAutomations = [
  {
    id: 1,
    name: 'اتوماسیون مدیریت شبکه‌های اجتماعی',
    description: 'مدیریت خودکار پست‌ها، نظرات و تعاملات در شبکه‌های اجتماعی مختلف',
    price: 150000,
    popular: true,
    features: ['پست خودکار', 'مدیریت نظرات', 'تحلیل عملکرد', 'تقویم محتوا']
  },
  {
    id: 2,
    name: 'اتوماسیون تجزیه و تحلیل داده‌ها',
    description: 'جمع‌آوری و تحلیل خودکار داده‌ها از منابع مختلف',
    price: 200000,
    popular: false,
    features: ['جمع‌آوری داده', 'تحلیل پیشرفته', 'گزارش‌گیری', 'هشدارهای هوشمند']
  },
  {
    id: 3,
    name: 'اتوماسیون مدیریت ایمیل',
    description: 'مدیریت خودکار ایمیل‌ها، پاسخ‌های خودکار و فیلترینگ هوشمند',
    price: 120000,
    popular: true,
    features: ['پاسخ خودکار', 'فیلترینگ هوشمند', 'طبقه‌بندی', 'آمار ارسال']
  }
]

const mockPurchasedAutomations = [
  {
    id: 1,
    name: 'اتوماسیون مدیریت شبکه‌های اجتماعی',
    description: 'مدیریت خودکار پست‌ها و تعاملات',
    status: 'active' as const,
    purchaseDate: '2024-01-15',
    expiryDate: '2025-01-15',
    usage: 85,
    maxUsage: 100
  },
  {
    id: 2,
    name: 'اتوماسیون تجزیه و تحلیل داده‌ها',
    description: 'تحلیل خودکار داده‌ها و گزارش‌گیری',
    status: 'active' as const,
    purchaseDate: '2024-02-01',
    expiryDate: '2025-02-01',
    usage: 45,
    maxUsage: 200
  }
]

const mockTokenUsage = {
  used: 1250,
  remaining: 2750,
  total: 4000
}

export default function DashboardPage() {
  const { user, isAuthenticated, loading } = useAuth()
  const router = useRouter()


  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, loading, router])



  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600 mb-4">در حال بارگذاری...</p>
          <p className="text-sm text-gray-500 mb-6">اگر بیش از ۱۰ ثانیه طول کشید، احتمالاً مشکلی در اتصال به سرور وجود دارد</p>
          <button 
            onClick={() => router.push('/login')}
            className="btn-primary"
          >
            ورود به سیستم
          </button>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <DashboardLayout>
      <div className="p-8">
        <div className="max-w-7xl mx-auto">
          {/* Welcome Header with Refresh Button */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">داشبورد</h1>
                <p className="text-xl text-gray-600 mb-2">خوش آمدید، {user?.name || 'کاربر'}!</p>
                <p className="text-gray-500">ایمیل: {user?.email || 'ایمیل نامشخص'}</p>

              </div>

            </div>
          </div>

          {/* Dashboard Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Token Usage Card */}
            <div className="lg:col-span-2">
              <TokenUsageCard usage={mockTokenUsage} />
            </div>

            {/* Available Automations */}
            <div>
              <AvailableAutomationsCard automations={mockAvailableAutomations} />
            </div>

            {/* Purchased Automations */}
            <div>
              <PurchasedAutomationsCard automations={mockPurchasedAutomations} />
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
