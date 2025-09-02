import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import DashboardLayout from '@/components/DashboardLayout'
import { PlayIcon, PauseIcon, TrashIcon, CogIcon, ChartBarIcon } from '@heroicons/react/24/outline'

interface Automation {
  id: number
  name: string
  description: string
  status: 'active' | 'inactive' | 'error'
  type: 'social_media' | 'data_analysis' | 'email' | 'workflow'
  lastRun: string
  nextRun: string
  successRate: number
  totalRuns: number
}

export default function AutomationsPage() {
  const { user, isAuthenticated, loading } = useAuth()
  const router = useRouter()
  const [automations, setAutomations] = useState<Automation[]>([
    {
      id: 1,
      name: 'اتوماسیون مدیریت شبکه‌های اجتماعی',
      description: 'مدیریت خودکار پست‌ها، نظرات و تعاملات در شبکه‌های اجتماعی مختلف',
      status: 'active',
      type: 'social_media',
      lastRun: '۲ ساعت پیش',
      nextRun: '۱ ساعت دیگر',
      successRate: 95,
      totalRuns: 1247
    },
    {
      id: 2,
      name: 'اتوماسیون تجزیه و تحلیل داده‌ها',
      description: 'جمع‌آوری و تحلیل خودکار داده‌ها از منابع مختلف',
      status: 'active',
      type: 'data_analysis',
      lastRun: '۶ ساعت پیش',
      nextRun: '۱۸ ساعت دیگر',
      successRate: 88,
      totalRuns: 892
    },
    {
      id: 3,
      name: 'اتوماسیون مدیریت ایمیل',
      description: 'مدیریت خودکار ایمیل‌ها، پاسخ‌های خودکار و فیلترینگ هوشمند',
      status: 'inactive',
      type: 'email',
      lastRun: '۲ روز پیش',
      nextRun: 'غیرفعال',
      successRate: 92,
      totalRuns: 567
    },
    {
      id: 4,
      name: 'اتوماسیون گردش کار',
      description: 'مدیریت خودکار فرآیندهای کاری و تاییدیه‌ها',
      status: 'error',
      type: 'workflow',
      lastRun: '۱ روز پیش',
      nextRun: 'متوقف شده',
      successRate: 78,
      totalRuns: 234
    }
  ])

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

  const toggleAutomation = (id: number) => {
    setAutomations(prev => prev.map(auto => 
      auto.id === id 
        ? { ...auto, status: auto.status === 'active' ? 'inactive' : 'active' }
        : auto
    ))
  }

  const deleteAutomation = (id: number) => {
    setAutomations(prev => prev.filter(auto => auto.id !== id))
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'social_media':
        return '📱'
      case 'data_analysis':
        return '📊'
      case 'email':
        return '📧'
      case 'workflow':
        return '⚙️'
      default:
        return '🔧'
    }
  }

  const getTypeName = (type: string) => {
    switch (type) {
      case 'social_media':
        return 'شبکه‌های اجتماعی'
      case 'data_analysis':
        return 'تجزیه و تحلیل داده'
      case 'email':
        return 'ایمیل'
      case 'workflow':
        return 'گردش کار'
      default:
        return 'سایر'
    }
  }

  return (
    <DashboardLayout>
      <div className="p-8">
        <div className="max-w-7xl mx-auto">
          {/* Page Header */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">اتوماسیون ها</h1>
                <p className="text-gray-600">مدیریت گردش‌های هوشمند و خودکار</p>
              </div>
              <button className="btn-primary">
                + ایجاد اتوماسیون جدید
              </button>
            </div>
          </div>

          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">کل اتوماسیون‌ها</p>
                  <p className="text-2xl font-bold text-gray-900">{automations.length}</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                  <ChartBarIcon className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">فعال</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {automations.filter(a => a.status === 'active').length}
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                  <PlayIcon className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">غیرفعال</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {automations.filter(a => a.status === 'inactive').length}
                  </p>
                </div>
                <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
                  <PauseIcon className="w-6 h-6 text-gray-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">خطا</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {automations.filter(a => a.status === 'error').length}
                  </p>
                </div>
                <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
                  <span className="text-red-600 font-bold">!</span>
                </div>
              </div>
            </div>
          </div>

          {/* Automations List */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">لیست اتوماسیون‌ها</h2>
            <div className="space-y-4">
              {automations.map((automation) => (
                <div key={automation.id} className="border border-gray-200 rounded-xl p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <span className="text-2xl">{getTypeIcon(automation.type)}</span>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">{automation.name}</h3>
                          <p className="text-sm text-gray-500">{getTypeName(automation.type)}</p>
                        </div>
                      </div>
                      
                      <p className="text-gray-600 mb-4">{automation.description}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <p className="text-gray-500">آخرین اجرا:</p>
                          <p className="font-medium text-gray-900">{automation.lastRun}</p>
                        </div>
                        <div>
                          <p className="text-gray-500">اجرای بعدی:</p>
                          <p className="font-medium text-gray-900">{automation.nextRun}</p>
                        </div>
                        <div>
                          <p className="text-gray-500">نرخ موفقیت:</p>
                          <p className="font-medium text-gray-900">{automation.successRate}%</p>
                        </div>
                        <div>
                          <p className="text-gray-500">کل اجراها:</p>
                          <p className="font-medium text-gray-900">{automation.totalRuns.toLocaleString()}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(automation.status)}`}>
                        {automation.status === 'active' ? 'فعال' : 
                         automation.status === 'inactive' ? 'غیرفعال' : 'خطا'}
                      </span>
                      
                      <button
                        onClick={() => toggleAutomation(automation.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          automation.status === 'active' 
                            ? 'text-orange-600 hover:bg-orange-50' 
                            : 'text-green-600 hover:bg-green-50'
                        }`}
                        title={automation.status === 'active' ? 'متوقف کردن' : 'فعال‌سازی'}
                      >
                        {automation.status === 'active' ? <PauseIcon className="w-5 h-5" /> : <PlayIcon className="w-5 h-5" />}
                      </button>
                      
                      <button
                        onClick={() => router.push(`/automations/${automation.id}/edit`)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="ویرایش"
                      >
                        <CogIcon className="w-5 h-5" />
                      </button>
                      
                      <button
                        onClick={() => deleteAutomation(automation.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="حذف"
                      >
                        <TrashIcon className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {automations.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CogIcon className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">اتوماسیونی یافت نشد</h3>
                <p className="text-gray-500 mb-6">اولین اتوماسیون خود را ایجاد کنید</p>
                <button className="btn-primary">ایجاد اتوماسیون جدید</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
