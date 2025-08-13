import { Automation } from '@/lib/mockData'
import { 
  RocketLaunchIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon 
} from '@heroicons/react/24/outline'

interface PurchasedAutomationsCardProps {
  automations: Automation[]
}

export default function PurchasedAutomationsCard({ automations }: PurchasedAutomationsCardProps) {
  const getStatusIcon = (status: Automation['status']) => {
    switch (status) {
      case 'active':
        return <CheckCircleIcon className="w-4 h-4 text-green-500" />
      case 'inactive':
        return <ClockIcon className="w-4 h-4 text-yellow-500" />
      case 'expired':
        return <XCircleIcon className="w-4 h-4 text-red-500" />
    }
  }

  const getStatusText = (status: Automation['status']) => {
    switch (status) {
      case 'active':
        return 'فعال'
      case 'inactive':
        return 'غیرفعال'
      case 'expired':
        return 'منقضی شده'
    }
  }

  const getStatusColor = (status: Automation['status']) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-50'
      case 'inactive':
        return 'text-yellow-600 bg-yellow-50'
      case 'expired':
        return 'text-red-600 bg-red-50'
    }
  }

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-6">
        <RocketLaunchIcon className="w-5 h-5 text-primary-600" />
        <h3 className="font-semibold text-gray-900">اتوماسیون‌های خریداری شده</h3>
      </div>

      <div className="space-y-4">
        {automations.map((automation) => (
          <div
            key={automation.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h4 className="font-medium text-gray-900 mb-1">
                  {automation.name}
                </h4>
                <p className="text-sm text-gray-600 mb-2">
                  {automation.description}
                </p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>تاریخ خرید: {automation.purchaseDate}</span>
                  <span>تاریخ انقضا: {automation.expiryDate}</span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {getStatusIcon(automation.status)}
                <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(automation.status)}`}>
                  {getStatusText(automation.status)}
                </span>
              </div>
            </div>

            {/* Usage progress */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">استفاده</span>
                <span className="text-gray-900">
                  {(automation.usage || 0)} / {(automation.maxUsage || 0)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-primary-600 h-1.5 rounded-full transition-all duration-300"
                  style={{ width: `${(automation.maxUsage || 0) > 0 ? ((automation.usage || 0) / (automation.maxUsage || 0)) * 100 : 0}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {automations.length === 0 && (
        <div className="text-center py-8">
          <RocketLaunchIcon className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">هنوز هیچ اتوماسیونی خریداری نکرده‌اید</p>
        </div>
      )}
    </div>
  )
} 