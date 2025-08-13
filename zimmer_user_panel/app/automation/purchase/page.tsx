'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '@/components/DashboardLayout';
import { cookies } from 'next/headers';
import { verifyToken } from '@/lib/auth-server';
import { redirect } from 'next/navigation';
import { RocketLaunchIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface Automation {
  id: number;
  name: string;
  description: string;
  pricing_type: string;
  price_per_token: number;
}

interface PurchaseFormData {
  automation_id: number;
  telegram_bot_token: string;
  tokens_remaining: number;
}

export default function PurchaseAutomationPage() {
  const router = useRouter();
  const [automations, setAutomations] = useState<Automation[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [formData, setFormData] = useState<PurchaseFormData>({
    automation_id: 0,
    telegram_bot_token: '',
    tokens_remaining: 100
  });

  useEffect(() => {
    fetchAutomations();
  }, []);

  const fetchAutomations = async () => {
    try {
      const token = getAuthToken();
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/automations/available`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch automations');
      }

      const data = await response.json();
      setAutomations(data);
    } catch (err) {
      setError('خطا در بارگذاری اتوماسیون‌ها');
      console.error('Error fetching automations:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAuthToken = () => {
    if (typeof window !== 'undefined') {
      return document.cookie
        .split('; ')
        .find(row => row.startsWith('auth-token='))
        ?.split('=')[1];
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');

    try {
      const token = getAuthToken();
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/user/automations`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle specific bot token uniqueness error
        if (response.status === 400 && data.detail && data.detail.includes('این توکن ربات قبلاً ثبت شده است')) {
          setError('این ربات قبلاً به یک حساب دیگر متصل شده است.');
        } else {
          setError(data.detail || 'خطا در خرید اتوماسیون');
        }
        return;
      }

      setSuccess('اتوماسیون با موفقیت خریداری شد!');
      
      // Reset form
      setFormData({
        automation_id: 0,
        telegram_bot_token: '',
        tokens_remaining: 100
      });

      // Redirect to dashboard after a short delay
      setTimeout(() => {
        router.push('/dashboard');
      }, 2000);

    } catch (err) {
      setError('خطا در اتصال به سرور');
      console.error('Error purchasing automation:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatPrice = (price: number) => {
    return price.toLocaleString('fa-IR') + ' تومان';
  };

  if (loading) {
    return (
      <DashboardLayout user={null}>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span className="mr-3 text-gray-600">در حال بارگذاری...</span>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout user={null}>
      <div className="space-y-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">خرید اتوماسیون</h1>
          <p className="text-gray-600">اتوماسیون مورد نظر خود را انتخاب کرده و اطلاعات ربات تلگرام را وارد کنید</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <ExclamationTriangleIcon className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-red-800">خطا</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Success Message */}
        {success && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start gap-3">
            <RocketLaunchIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-green-800">موفقیت</h3>
              <p className="text-sm text-green-700 mt-1">{success}</p>
            </div>
          </div>
        )}

        {/* Purchase Form */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Automation Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                انتخاب اتوماسیون *
              </label>
              <select
                value={formData.automation_id}
                onChange={(e) => setFormData({ ...formData, automation_id: Number(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                required
              >
                <option value={0}>انتخاب اتوماسیون</option>
                {automations.map((automation) => (
                  <option key={automation.id} value={automation.id}>
                    {automation.name} - {formatPrice(automation.price_per_token)}
                  </option>
                ))}
              </select>
            </div>

            {/* Bot Token Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                توکن ربات تلگرام (اختیاری)
              </label>
              <input
                type="text"
                value={formData.telegram_bot_token}
                onChange={(e) => setFormData({ ...formData, telegram_bot_token: e.target.value })}
                placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">
                اگر توکن ربات تلگرام دارید، آن را وارد کنید. در غیر این صورت می‌توانید بعداً اضافه کنید.
              </p>
            </div>

            {/* Tokens Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                تعداد توکن (اختیاری)
              </label>
              <input
                type="number"
                value={formData.tokens_remaining}
                onChange={(e) => setFormData({ ...formData, tokens_remaining: Number(e.target.value) })}
                placeholder="100"
                min="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">
                تعداد توکن‌های اولیه. در صورت عدم وارد کردن، 5 توکن آزمایشی دریافت خواهید کرد.
              </p>
            </div>

            {/* Submit Button */}
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={submitting || formData.automation_id === 0}
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? 'در حال پردازش...' : 'خرید اتوماسیون'}
              </button>
            </div>
          </form>
        </div>

        {/* Available Automations List */}
        {automations.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">اتوماسیون‌های موجود</h2>
            <div className="grid gap-4">
              {automations.map((automation) => (
                <div
                  key={automation.id}
                  className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 mb-1">
                        {automation.name}
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">
                        {automation.description}
                      </p>
                      <div className="text-xs text-gray-500">
                        نوع قیمت‌گذاری: {automation.pricing_type === 'token_per_session' ? 'توکن به ازای هر جلسه' : 
                                       automation.pricing_type === 'token_per_step' ? 'توکن به ازای هر مرحله' : 'هزینه ثابت'}
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="text-lg font-bold text-primary-600">
                        {formatPrice(automation.price_per_token)}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
} 