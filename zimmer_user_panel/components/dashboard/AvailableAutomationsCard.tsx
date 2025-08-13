'use client';

import { StarIcon, SparklesIcon, ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

interface Automation {
  id: number;
  name: string;
  description: string;
  price?: number;
  popular?: boolean;
  features?: string[];
}

interface AvailableAutomationsCardProps {
  automations: Automation[];
}

export default function AvailableAutomationsCard({ automations }: AvailableAutomationsCardProps) {
  const formatPrice = (price: number | undefined) => {
    if (!price || isNaN(price)) return 'قیمت نامشخص';
    return price.toLocaleString('fa-IR') + ' تومان';
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">اتوماسیون‌های موجود</h3>
          <p className="text-sm text-gray-600">اتوماسیون‌های جدید و محبوب</p>
        </div>
        <SparklesIcon className="w-6 h-6 text-primary-600" />
      </div>

      <div className="grid gap-4">
        {automations.map((automation) => (
          <div
            key={automation.id}
            className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-medium text-gray-900">
                    {automation.name}
                  </h4>
                  {automation.popular && (
                    <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full flex items-center gap-1">
                      <StarIcon className="w-3 h-3" />
                      محبوب
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  {automation.description}
                </p>
                
                {/* Features */}
                <div className="space-y-1 mb-4">
                  {(automation.features ?? []).map((feature, index) => (
                    <div key={index} className="flex items-center gap-2 text-xs text-gray-600">
                      <div className="w-1 h-1 bg-primary-600 rounded-full"></div>
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="text-left">
                <p className="text-lg font-bold text-primary-600 mb-2">
                  {formatPrice(automation.price)}
                </p>
                <Link 
                  href="/automation/purchase"
                  className="btn-primary text-sm inline-block"
                >
                  خرید
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

      {automations.length === 0 && (
        <div className="text-center py-8">
          <SparklesIcon className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">در حال حاضر اتوماسیون جدیدی موجود نیست</p>
        </div>
      )}

      {/* View All Link */}
      {automations.length > 0 && (
        <div className="text-center pt-4 border-t border-gray-200">
          <Link
            href="/automations"
            className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center justify-center gap-1"
          >
            مشاهده همه اتوماسیون‌ها
            <ArrowRightIcon className="w-3 h-3" />
          </Link>
        </div>
      )}
    </div>
  )
} 