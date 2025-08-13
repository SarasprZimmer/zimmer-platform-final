import { TokenUsage } from '@/lib/mockData'
import { 
  ChartBarIcon,
  ExclamationTriangleIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'

interface TokenUsageCardProps {
  usage: TokenUsage
  demoTokens?: number
  isDemoActive?: boolean
  demoExpired?: boolean
}

export default function TokenUsageCard({ usage, demoTokens = 0, isDemoActive = false, demoExpired = false }: TokenUsageCardProps) {
  // Add null checks and default values
  const used = usage?.used || 0
  const total = usage?.total || 0
  const remaining = usage?.remaining || 0
  
  const percentage = total > 0 ? (used / total) * 100 : 0
  const isLow = percentage > 80

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <ChartBarIcon className="w-5 h-5 text-primary-600" />
          <h3 className="font-semibold text-gray-900">استفاده از توکن</h3>
        </div>
        {isLow && (
          <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />
        )}
      </div>

      <div className="space-y-4">
        {/* Progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              isLow ? 'bg-yellow-500' : 'bg-primary-600'
            }`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-primary-600">
              {used.toLocaleString()}
            </p>
            <p className="text-sm text-gray-500">استفاده شده</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">
              {remaining.toLocaleString()}
            </p>
            <p className="text-sm text-gray-500">باقی‌مانده</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-700">
              {total.toLocaleString()}
            </p>
            <p className="text-sm text-gray-500">کل</p>
          </div>
        </div>

        {/* Demo token badge */}
        {isDemoActive && demoTokens > 0 && (
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-3">
            <div className="flex items-center gap-2">
              <SparklesIcon className="w-5 h-5 text-purple-600" />
              <p className="text-sm font-medium text-purple-800">
                🎉 {demoTokens} جلسه آزمایشی باقی مانده
              </p>
            </div>
          </div>
        )}

        {/* Demo expired warning */}
        {demoExpired && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-sm text-red-800">
              دوره آزمایشی شما به پایان رسیده است. برای ادامه استفاده، لطفا بسته توکن خریداری کنید.
            </p>
          </div>
        )}

        {/* Warning message */}
        {isLow && !demoExpired && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
            <p className="text-sm text-yellow-800">
              توجه: استفاده از توکن شما نزدیک به حد مجاز است. برای ادامه استفاده، توکن بیشتری خریداری کنید.
            </p>
          </div>
        )}
      </div>
    </div>
  )
} 