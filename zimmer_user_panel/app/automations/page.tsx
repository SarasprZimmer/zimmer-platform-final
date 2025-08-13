import DashboardLayout from '@/components/DashboardLayout'
import { cookies } from 'next/headers'
import { verifyToken } from '@/lib/auth-server'
import { redirect } from 'next/navigation'
import { 
  RocketLaunchIcon, 
  StarIcon, 
  SparklesIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  ArrowRightIcon,
  ShoppingCartIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

interface Automation {
  id: number
  name: string
  description: string
  price: number
  pricing_type: 'per_message' | 'per_minute' | 'per_session'
  status: boolean
  popular?: boolean
  features?: string[]
}

interface UserAutomation {
  id: number
  automation_id: number
  user_id: number
  status: 'active' | 'inactive' | 'expired'
  demo_tokens: number
  tokens_remaining: number
  demo_expired: boolean
  provisioned_at?: string
  integration_status?: string
  created_at: string
}

export default async function AutomationsPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  const tokenData = token ? await verifyToken(token) : null;

  if (!tokenData || !tokenData.user) {
    redirect('/login');
  }

  // Fetch available automations and user's purchased automations
  const [availableRes, purchasedRes] = await Promise.all([
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/automations/available`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/user/automations`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
  ]);

  const availableAutomations: Automation[] = availableRes.ok ? await availableRes.json() : [];
  const purchasedAutomations: UserAutomation[] = purchasedRes.ok ? await purchasedRes.json() : [];

  // Create a map of user's automations for quick lookup
  const userAutomationMap = new Map(
    purchasedAutomations.map(ua => [ua.automation_id, ua])
  );

  const formatPrice = (price: number | undefined, pricingType: string) => {
    if (!price || isNaN(price)) return 'قیمت نامشخص';
    const formattedPrice = price.toLocaleString('fa-IR');
    
    const pricingLabels = {
      per_message: 'به ازای پیام',
      per_minute: 'به ازای دقیقه', 
      per_session: 'به ازای جلسه'
    };
    
    return `${formattedPrice} تومان (${pricingLabels[pricingType as keyof typeof pricingLabels] || pricingType})`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircleIcon className="w-4 h-4 text-green-500" />
      case 'inactive':
        return <ClockIcon className="w-4 h-4 text-yellow-500" />
      case 'expired':
        return <XCircleIcon className="w-4 h-4 text-red-500" />
      default:
        return <ClockIcon className="w-4 h-4 text-gray-500" />
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active':
        return 'فعال'
      case 'inactive':
        return 'غیرفعال'
      case 'expired':
        return 'منقضی شده'
      default:
        return 'نامشخص'
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-50'
      case 'inactive':
        return 'text-yellow-600 bg-yellow-50'
      case 'expired':
        return 'text-red-600 bg-red-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  };

  return (
    <DashboardLayout user={tokenData.user}>
      <div className="space-y-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">اتوماسیون‌ها</h1>
          <p className="text-gray-600">
            اتوماسیون‌های موجود را مشاهده کنید و آن‌هایی که نیاز دارید را خریداری کنید
          </p>
        </div>

        {/* Purchased Automations Section */}
        {purchasedAutomations.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
              <RocketLaunchIcon className="w-5 h-5 text-primary-600" />
              اتوماسیون‌های خریداری شده
            </h2>
            <div className="grid gap-4">
              {purchasedAutomations.map((userAutomation) => {
                const automation = availableAutomations.find(a => a.id === userAutomation.automation_id);
                if (!automation) return null;

                return (
                  <div key={userAutomation.id} className="card border-2 border-primary-100">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {automation.name}
                          </h3>
                          <div className="flex items-center gap-2">
                            {getStatusIcon(userAutomation.status)}
                            <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(userAutomation.status)}`}>
                              {getStatusText(userAutomation.status)}
                            </span>
                          </div>
                        </div>
                        <p className="text-gray-600 mb-3">{automation.description}</p>
                        
                        {/* Usage Info */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div>
                            <span className="text-gray-500">توکن‌های آزمایشی:</span>
                            <span className="font-medium text-gray-900 mr-2">
                              {userAutomation.demo_tokens}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-500">توکن‌های باقی‌مانده:</span>
                            <span className="font-medium text-gray-900 mr-2">
                              {userAutomation.tokens_remaining || 0}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-500">وضعیت اتصال:</span>
                            <span className="font-medium text-gray-900 mr-2">
                              {userAutomation.integration_status === 'active' ? 'متصل' : 'غیرمتصل'}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-500">تاریخ خرید:</span>
                            <span className="font-medium text-gray-900 mr-2">
                              {new Date(userAutomation.created_at).toLocaleDateString('fa-IR')}
                            </span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex flex-col gap-2">
                        <Link
                          href={`/automation/${automation.id}`}
                          className="btn-primary text-sm flex items-center gap-2"
                        >
                          <RocketLaunchIcon className="w-4 h-4" />
                          داشبورد
                        </Link>
                        {userAutomation.integration_status !== 'active' && (
                          <button className="btn-secondary text-sm">
                            اتصال مجدد
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Available Automations Section */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
            <SparklesIcon className="w-5 h-5 text-primary-600" />
            اتوماسیون‌های موجود
          </h2>
          <div className="grid gap-4">
            {availableAutomations
              .filter(automation => !userAutomationMap.has(automation.id))
              .map((automation) => (
                <div key={automation.id} className="card hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {automation.name}
                        </h3>
                        {automation.popular && (
                          <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full flex items-center gap-1">
                            <StarIcon className="w-3 h-3" />
                            محبوب
                          </span>
                        )}
                      </div>
                      <p className="text-gray-600 mb-3">{automation.description}</p>
                      
                      {/* Features */}
                      {automation.features && automation.features.length > 0 && (
                        <div className="space-y-1 mb-4">
                          {automation.features.map((feature, index) => (
                            <div key={index} className="flex items-center gap-2 text-xs text-gray-600">
                              <div className="w-1 h-1 bg-primary-600 rounded-full"></div>
                              <span>{feature}</span>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      <div className="text-primary-600 font-semibold">
                        {formatPrice(automation.price, automation.pricing_type)}
                      </div>
                    </div>
                    
                    <div className="flex flex-col gap-2">
                      <Link
                        href={`/automation/purchase?automation_id=${automation.id}`}
                        className="btn-primary text-sm flex items-center gap-2"
                      >
                        <ShoppingCartIcon className="w-4 h-4" />
                        خرید
                      </Link>
                      <Link
                        href={`/automation/${automation.id}`}
                        className="btn-secondary text-sm flex items-center gap-2"
                      >
                        جزئیات
                        <ArrowRightIcon className="w-4 h-4" />
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Empty State */}
        {availableAutomations.length === 0 && (
          <div className="card text-center py-12">
            <SparklesIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              در حال حاضر اتوماسیونی موجود نیست
            </h3>
            <p className="text-gray-500">
              لطفاً بعداً دوباره بررسی کنید یا با پشتیبانی تماس بگیرید
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
