import DashboardLayout from '@/components/DashboardLayout'
import TokenUsageCard from '@/components/dashboard/TokenUsageCard'
import PurchasedAutomationsCard from '@/components/dashboard/PurchasedAutomationsCard'
import AvailableAutomationsCard from '@/components/dashboard/AvailableAutomationsCard'
import { cookies } from 'next/headers'
import { verifyToken } from '@/lib/auth-server'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import { ArrowRightIcon } from '@heroicons/react/24/outline'

export default async function DashboardPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  const tokenData = token ? await verifyToken(token) : null;

  // Defensive: redirect if tokenData or tokenData.user is not valid
  if (!tokenData || !tokenData.user) {
    redirect('/login');
  }

  // Fetch data from FastAPI backend
  const [usageRes, purchasedRes, availableRes, dashboardRes] = await Promise.all([
    fetch(process.env.NEXT_PUBLIC_API_URL + '/api/user/usage', {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
    fetch(process.env.NEXT_PUBLIC_API_URL + '/api/user/automations', {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
    fetch(process.env.NEXT_PUBLIC_API_URL + '/api/automations/available', {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
    fetch(process.env.NEXT_PUBLIC_API_URL + '/api/user/dashboard', {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
  ]);

  if (!usageRes.ok || !purchasedRes.ok || !availableRes.ok || !dashboardRes.ok) {
    redirect('/login'); // fallback for auth errors
  }

  const usage = await usageRes.json() || { used: 0, total: 0, remaining: 0 };
  const purchasedAutomations = await purchasedRes.json() || [];
  const availableAutomations = await availableRes.json() || [];
  const dashboardData = await dashboardRes.json() || { 
    total_demo_tokens: 0, 
    has_active_demo: false, 
    has_expired_demo: false 
  };

  return (
    <DashboardLayout user={tokenData.user}>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            سلام {tokenData.user.name} 👋
          </h1>
          <p className="text-gray-600">
            به پنل کاربری Zimmer AI خوش آمدید. در اینجا می‌توانید اتوماسیون‌های خود را مدیریت کنید.
          </p>
        </div>

        {/* Token Usage */}
        <TokenUsageCard 
          usage={usage} 
          demoTokens={dashboardData.total_demo_tokens}
          isDemoActive={dashboardData.has_active_demo}
          demoExpired={dashboardData.has_expired_demo}
        />

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Purchased Automations */}
          <PurchasedAutomationsCard automations={purchasedAutomations} />
          {/* Available Automations */}
          <AvailableAutomationsCard automations={availableAutomations} />
        </div>

        {/* View All Automations Link */}
        <div className="text-center">
          <Link
            href="/automations"
            className="btn-primary inline-flex items-center gap-2"
          >
            مشاهده همه اتوماسیون‌ها
            <ArrowRightIcon className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </DashboardLayout>
  );
} 