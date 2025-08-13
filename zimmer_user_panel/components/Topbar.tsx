'use client'

import { User } from '@/lib/auth'
import { 
  BellIcon, 
  MagnifyingGlassIcon,
  Bars3Icon 
} from '@heroicons/react/24/outline'

interface TopbarProps {
  user: User
  onMenuToggle?: () => void
}

export default function Topbar({ user, onMenuToggle }: TopbarProps) {
  return (
    <div className="bg-white shadow-sm border-b border-gray-200 h-16 flex items-center justify-between px-6 fixed top-0 left-0 right-64 z-40">
      {/* Left side - Menu toggle for mobile */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 rounded-lg hover:bg-gray-100"
        >
          <Bars3Icon className="w-5 h-5" />
        </button>
        
        {/* Search */}
        <div className="hidden md:flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-2">
          <MagnifyingGlassIcon className="w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="جستجو..."
            className="bg-transparent outline-none text-sm w-64"
          />
        </div>
      </div>

      {/* Right side - User info and notifications */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="p-2 rounded-lg hover:bg-gray-100 relative">
          <BellIcon className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
        </button>

        {/* User */}
        {user && (
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">{user.name}</p>
              <p className="text-xs text-gray-500">{user.email}</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
              {user.avatar ? (
                <img
                  src={user.avatar}
                  alt={user.name}
                  className="w-10 h-10 rounded-full"
                />
              ) : (
                <span className="text-primary-600 font-bold text-lg">
                  {user.name.charAt(0)}
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 