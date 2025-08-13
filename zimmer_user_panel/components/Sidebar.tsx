'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { 
  HomeIcon, 
  CogIcon, 
  CreditCardIcon, 
  QuestionMarkCircleIcon, 
  RocketLaunchIcon,
  ArrowRightOnRectangleIcon 
} from '@heroicons/react/24/outline'
import Cookies from 'js-cookie'

const navigationItems = [
  {
    name: 'داشبورد',
    href: '/dashboard',
    icon: HomeIcon
  },
  {
    name: 'اتوماسیون‌ها',
    href: '/automations',
    icon: RocketLaunchIcon
  },
  {
    name: 'پرداخت‌ها',
    href: '/payment',
    icon: CreditCardIcon
  },
  {
    name: 'پشتیبانی',
    href: '/support',
    icon: QuestionMarkCircleIcon
  },
  {
    name: 'تنظیمات',
    href: '/settings',
    icon: CogIcon
  }
]

export default function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()

  const handleLogout = () => {
    // Clear the auth token cookie
    Cookies.remove('auth-token')
    // Redirect to login page
    router.push('/login')
  }

  // Get the active state for navigation items
  const getActiveState = (href: string) => {
    return pathname === href ? 'active' : ''
  }

  return (
    <div className="w-64 bg-white shadow-lg h-screen fixed right-0 top-0 z-50">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">Z</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">Zimmer AI</h1>
            <p className="text-sm text-gray-500">اتوماسیون هوشمند</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-2">
        {navigationItems.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={`sidebar-item ${getActiveState(item.href)}`}
          >
            <item.icon className="w-5 h-5" />
            <span>{item.name}</span>
          </Link>
        ))}
      </nav>

      {/* Logout */}
      <div className="absolute bottom-4 right-4 left-4">
        <button 
          onClick={handleLogout}
          className="sidebar-item w-full text-red-600 hover:bg-red-50 hover:text-red-700"
        >
          <ArrowRightOnRectangleIcon className="w-5 h-5" />
          <span>خروج</span>
        </button>
      </div>
    </div>
  )
} 