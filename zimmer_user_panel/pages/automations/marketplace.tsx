import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import DashboardLayout from '@/components/DashboardLayout'
import { Card } from "@/components/Skeleton";

export default function Marketplace(){
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">در حال بارگذاری...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <DashboardLayout>
      <div className="p-6 space-y-4" dir="rtl">
        <div className="text-xl font-semibold">فروشگاه اتوماسیون‌ها</div>
        <Card>
          <div className="opacity-70 text-sm">این بخش به‌زودی تکمیل می‌شود. فعلاً می‌توانید از طریق پشتیبانی سفارش دهید.</div>
        </Card>
      </div>
    </DashboardLayout>
  );
}
