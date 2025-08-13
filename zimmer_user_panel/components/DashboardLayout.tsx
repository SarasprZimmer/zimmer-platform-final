'use client'

import { useState } from 'react'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import { User } from '@/lib/auth'

interface DashboardLayoutProps {
  children: React.ReactNode
  user?: User | null
}

export default function DashboardLayout({ children, user }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar />

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <div className="lg:mr-64">
        {/* Topbar */}
        <Topbar user={user} onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
        
        {/* Page content */}
        <main className="pt-16 min-h-screen">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
