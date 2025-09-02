import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import DashboardLayout from '@/components/DashboardLayout'

export default function PaymentPage() {
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
          <p className="text-gray-600">در حال بارگذاری...</p>
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
          {/* Page Header */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">مدیریت پرداخت ها</h1>
            <p className="text-gray-600">مدیریت صورتحساب‌ها و اشتراک‌های شما</p>
          </div>

          {/* Current Subscription */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">اشتراک فعلی</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-purple-900 mb-2">طرح حرفه‌ای</h3>
                <p className="text-purple-700 text-sm mb-4">اشتراک ماهانه</p>
                <div className="text-3xl font-bold text-purple-900">۲۵۰,۰۰۰ تومان</div>
                <p className="text-purple-600 text-sm mt-2">در ماه</p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-green-900 mb-2">تاریخ انقضا</h3>
                <p className="text-green-700 text-sm mb-4">اشتراک تا</p>
                <div className="text-2xl font-bold text-green-900">۱۵ دی ۱۴۰۳</div>
                <p className="text-green-600 text-sm mt-2">۲۵ روز باقی مانده</p>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">وضعیت</h3>
                <p className="text-blue-700 text-sm mb-4">اشتراک</p>
                <div className="text-2xl font-bold text-blue-900">فعال</div>
                <p className="text-blue-600 text-sm mt-2">در حال استفاده</p>
              </div>
            </div>
          </div>

          {/* Billing History */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">تاریخچه صورتحساب</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-right py-4 px-6 text-sm font-semibold text-gray-900">تاریخ</th>
                    <th className="text-right py-4 px-6 text-sm font-semibold text-gray-900">توضیحات</th>
                    <th className="text-right py-4 px-6 text-sm font-semibold text-gray-900">مبلغ</th>
                    <th className="text-right py-4 px-6 text-sm font-semibold text-gray-900">وضعیت</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="py-4 px-6 text-sm text-gray-900">۱۵ آذر ۱۴۰۳</td>
                    <td className="py-4 px-6 text-sm text-gray-900">اشتراک ماهانه - طرح حرفه‌ای</td>
                    <td className="py-4 px-6 text-sm text-gray-900">۲۵۰,۰۰۰ تومان</td>
                    <td className="py-4 px-6">
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">پرداخت شده</span>
                    </td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-4 px-6 text-sm text-gray-900">۱۵ آبان ۱۴۰۳</td>
                    <td className="py-4 px-6 text-sm text-gray-900">اشتراک ماهانه - طرح حرفه‌ای</td>
                    <td className="py-4 px-6 text-sm text-gray-900">۲۵۰,۰۰۰ تومان</td>
                    <td className="py-4 px-6">
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">پرداخت شده</span>
                    </td>
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-4 px-6 text-sm text-gray-900">۱۵ مهر ۱۴۰۳</td>
                    <td className="py-4 px-6 text-sm text-gray-900">اشتراک ماهانه - طرح حرفه‌ای</td>
                    <td className="py-4 px-6 text-sm text-gray-900">۲۵۰,۰۰۰ تومان</td>
                    <td className="py-4 px-6">
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">پرداخت شده</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Payment Methods */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">روش‌های پرداخت</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-gray-200 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-blue-600 font-bold">V</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">کارت اعتباری</h3>
                      <p className="text-sm text-gray-500">**** **** **** 1234</p>
                    </div>
                  </div>
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">پیش‌فرض</span>
                </div>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">ویرایش</button>
              </div>
              
              <div className="border border-gray-200 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                      <span className="text-gray-600 font-bold">+</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">افزودن کارت جدید</h3>
                      <p className="text-sm text-gray-500">کارت اعتباری یا بانکی</p>
                    </div>
                  </div>
                </div>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">افزودن</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
