import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import DashboardLayout from '@/components/DashboardLayout'
import dynamic from "next/dynamic";
import ActiveAutomations from "@/components/payments/ActiveAutomations";
const MonthlyExpenses = dynamic(()=>import("@/components/payments/MonthlyExpenses"), { ssr:false });
const PaymentHistory = dynamic(()=>import("@/components/payments/PaymentHistory"), { ssr:false });

export default function PaymentPage(){
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
      <div className="p-6 space-y-6" dir="rtl">
        <div className="text-2xl font-bold text-gray-900 mb-2">مدیریت پرداخت‌ها</div>

        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 lg:col-span-6">
            <MonthlyExpenses />
          </div>
          <div className="col-span-12 lg:col-span-6">
            <ActiveAutomations />
          </div>
          <div className="col-span-12">
            <PaymentHistory />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
