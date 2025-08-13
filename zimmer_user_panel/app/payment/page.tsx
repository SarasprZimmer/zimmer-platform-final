import DashboardLayout from '@/components/DashboardLayout'
import { cookies } from 'next/headers'
import { verifyToken } from '@/lib/auth-server'
import { redirect } from 'next/navigation'
import { CreditCardIcon } from '@heroicons/react/24/outline'
import FormattedDate from '@/components/FormattedDate';

export default async function PaymentPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  const tokenData = token ? await verifyToken(token) : null;

  if (!tokenData) {
    redirect('/login');
  }

  // Fetch payment history
  const res = await fetch(process.env.NEXT_PUBLIC_API_URL + '/api/user/payments', {
    headers: { Authorization: `Bearer ${token}` },
    cache: 'no-store',
  });
  if (!res.ok) {
    redirect('/login');
  }
  const payments = await res.json();

  return (
    <DashboardLayout user={tokenData.user}>
      <div className="space-y-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">پرداخت‌ها</h1>
          <p className="text-gray-600">مشاهده تاریخچه پرداخت‌ها و مدیریت روش‌های پرداخت</p>
        </div>

        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-2">
              <CreditCardIcon className="w-6 h-6 text-primary-600" />
              <h3 className="font-semibold text-gray-900">تراکنش‌های اخیر</h3>
            </div>
            <button className="btn-primary">افزایش توکن</button>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm text-right">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-4 py-2">اتوماسیون</th>
                  <th className="px-4 py-2">مبلغ</th>
                  <th className="px-4 py-2">روش</th>
                  <th className="px-4 py-2">تاریخ</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(payments) && payments.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="text-center py-8 text-gray-500">
                      هیچ تراکنشی ثبت نشده است.
                    </td>
                  </tr>
                ) : (
                  (Array.isArray(payments) ? payments : []).map((p: any) => (
                    <tr key={p.id} className="border-b">
                      <td className="px-4 py-2">{p.automation_name}</td>
                      <td className="px-4 py-2">{p.amount.toLocaleString()} تومان</td>
                      <td className="px-4 py-2">{p.method}</td>
                      <td className="px-4 py-2"><FormattedDate date={p.timestamp} /></td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
} 