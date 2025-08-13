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
  ShoppingCartIcon,
  ChartBarIcon,
  ExclamationTriangleIcon
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

export default async function AutomationPage({ params }: any) {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  const tokenData = token ? await verifyToken(token) : null;

  if (!tokenData || !tokenData.user) {
    redirect('/login');
  }

  // Fetch automation details and user's access
  const [automationRes, userAutomationRes] = await Promise.all([
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/automations/${params.automation_id}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/user/automations/${params.automation_id}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    }),
  ]);

  const automation: Automation = automationRes.ok ? await automationRes.json() : null;
  const userAutomation: UserAutomation = userAutomationRes.ok ? await userAutomationRes.json() : null;

  if (!automation) {
    return (
      <DashboardLayout user={tokenData.user}>
        <div className="card text-center py-12 mt-12">
          <RocketLaunchIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">اتوماسیون یافت نشد</h3>
          <p className="text-gray-500 mb-4">اتوماسیون مورد نظر وجود ندارد یا در دسترس نیست</p>
          <Link href="/automations" className="btn-primary">
            بازگشت به لیست اتوماسیون‌ها
          </Link>
        </div>
      </DashboardLayout>
    );
  }

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

  // If user doesn't have access, show purchase option
  if (!userAutomation) {
    return (
      <DashboardLayout user={tokenData.user}>
        <div className="space-y-6">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{automation.name}</h1>
              {automation.popular && (
                <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full flex items-center gap-1">
                  <StarIcon className="w-3 h-3" />
                  محبوب
                </span>
              )}
            </div>
            <p className="text-gray-600">{automation.description}</p>
          </div>

          {/* Automation Details */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Left Column - Details */}
            <div className="space-y-6">
              <div className="card">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">جزئیات اتوماسیون</h2>
                <div className="space-y-3">
                  <div>
                    <span className="text-gray-500">قیمت:</span>
                    <span className="font-semibold text-primary-600 mr-2">
                      {formatPrice(automation.price, automation.pricing_type)}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">وضعیت:</span>
                    <span className={`font-medium mr-2 ${automation.status ? 'text-green-600' : 'text-red-600'}`}>
                      {automation.status ? 'فعال' : 'غیرفعال'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Features */}
              {automation.features && automation.features.length > 0 && (
                <div className="card">
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">ویژگی‌ها</h2>
                  <div className="space-y-2">
                    {automation.features.map((feature, index) => (
                      <div key={index} className="flex items-center gap-2 text-gray-700">
                        <CheckCircleIcon className="w-4 h-4 text-green-500" />
                        <span>{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Right Column - Purchase */}
            <div className="card">
              <div className="text-center">
                <SparklesIcon className="w-16 h-16 text-primary-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  این اتوماسیون را خریداری کنید
                </h3>
                <p className="text-gray-600 mb-6">
                  با خرید این اتوماسیون، دسترسی کامل به تمام ویژگی‌های آن را خواهید داشت
                </p>
                
                <div className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-semibold text-blue-900 mb-2">آنچه دریافت می‌کنید:</h4>
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li>• دسترسی کامل به اتوماسیون</li>
                      <li>• توکن‌های آزمایشی رایگان</li>
                      <li>• پشتیبانی فنی</li>
                      <li>• به‌روزرسانی‌های رایگان</li>
                    </ul>
                  </div>
                  
                  <Link
                    href={`/automation/purchase?automation_id=${automation.id}`}
                    className="btn-primary w-full flex items-center justify-center gap-2"
                  >
                    <ShoppingCartIcon className="w-5 h-5" />
                    خرید اتوماسیون
                  </Link>
                  
                  <Link
                    href="/automations"
                    className="btn-secondary w-full flex items-center justify-center gap-2"
                  >
                    <ArrowRightIcon className="w-5 h-5" />
                    مشاهده سایر اتوماسیون‌ها
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  // User has access - show dashboard
  return (
    <DashboardLayout user={tokenData.user}>
      <div className="space-y-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-gray-900">{automation.name}</h1>
            <div className="flex items-center gap-2">
              {getStatusIcon(userAutomation.status)}
              <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(userAutomation.status)}`}>
                {getStatusText(userAutomation.status)}
              </span>
            </div>
          </div>
          <p className="text-gray-600">{automation.description}</p>
        </div>

        {/* Usage Stats */}
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <ChartBarIcon className="w-5 h-5 text-primary-600" />
              <h3 className="font-semibold text-gray-900">استفاده از توکن</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">توکن‌های آزمایشی:</span>
                <span className="font-semibold text-gray-900">{userAutomation.demo_tokens}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">توکن‌های باقی‌مانده:</span>
                <span className="font-semibold text-gray-900">{userAutomation.tokens_remaining || 0}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ 
                    width: `${userAutomation.tokens_remaining && userAutomation.tokens_remaining > 0 
                      ? Math.min((userAutomation.tokens_remaining / (userAutomation.tokens_remaining + userAutomation.demo_tokens)) * 100, 100) 
                      : 0}%` 
                  }}
                />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <CheckCircleIcon className="w-5 h-5 text-green-600" />
              <h3 className="font-semibold text-gray-900">وضعیت اتصال</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">وضعیت:</span>
                <span className={`font-semibold ${userAutomation.integration_status === 'active' ? 'text-green-600' : 'text-red-600'}`}>
                  {userAutomation.integration_status === 'active' ? 'متصل' : 'غیرمتصل'}
                </span>
              </div>
              {userAutomation.provisioned_at && (
                <div className="flex justify-between">
                  <span className="text-gray-600">تاریخ اتصال:</span>
                  <span className="font-semibold text-gray-900">
                    {new Date(userAutomation.provisioned_at).toLocaleDateString('fa-IR')}
                  </span>
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <ClockIcon className="w-5 h-5 text-blue-600" />
              <h3 className="font-semibold text-gray-900">اطلاعات خرید</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">تاریخ خرید:</span>
                <span className="font-semibold text-gray-900">
                  {new Date(userAutomation.created_at).toLocaleDateString('fa-IR')}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">قیمت:</span>
                <span className="font-semibold text-primary-600">
                  {formatPrice(automation.price, automation.pricing_type)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">عملیات</h3>
          <div className="flex gap-4">
            <button className="btn-primary flex items-center gap-2">
              <RocketLaunchIcon className="w-4 h-4" />
              شروع اتوماسیون
            </button>
            {userAutomation.integration_status !== 'active' && (
              <button className="btn-secondary flex items-center gap-2">
                <CheckCircleIcon className="w-4 h-4" />
                اتصال مجدد
              </button>
            )}
            <Link href="/payment" className="btn-secondary flex items-center gap-2">
              <ShoppingCartIcon className="w-4 h-4" />
              خرید توکن بیشتر
            </Link>
          </div>
        </div>

        {/* Demo Expired Warning */}
        {userAutomation.demo_expired && (
          <div className="card border-2 border-red-200 bg-red-50">
            <div className="flex items-center gap-3">
              <ExclamationTriangleIcon className="w-5 h-5 text-red-600" />
              <div>
                <h4 className="font-semibold text-red-900">دوره آزمایشی به پایان رسیده</h4>
                <p className="text-red-700 text-sm">
                  دوره آزمایشی شما به پایان رسیده است. برای ادامه استفاده، لطفاً توکن بیشتری خریداری کنید.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
} 