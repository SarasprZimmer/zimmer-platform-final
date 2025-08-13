import DashboardLayout from '@/components/DashboardLayout'
import { cookies } from 'next/headers'
import { verifyToken } from '@/lib/auth-server'
import { redirect } from 'next/navigation'
import { CogIcon } from '@heroicons/react/24/outline'
import React from 'react'
import ProfileForm from './ProfileForm';
import ChangePasswordForm from './ChangePasswordForm';

export default async function SettingsPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  const tokenData = token ? await verifyToken(token) : null;

  if (!tokenData) {
    redirect('/login');
  }

  // Fetch user profile
  const res = await fetch(process.env.NEXT_PUBLIC_API_URL + '/api/user/profile', {
    headers: { Authorization: `Bearer ${token}` },
    cache: 'no-store',
  });
  if (!res.ok) {
    redirect('/login');
  }
  const profile = await res.json();

  return (
    <DashboardLayout user={tokenData.user}>
      <div className="space-y-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">تنظیمات</h1>
          <p className="text-gray-600">مدیریت تنظیمات حساب کاربری و پروفایل</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-4xl mx-auto">
          <div>
            <ProfileForm profile={profile} />
          </div>
          <div>
            <ChangePasswordForm />
          </div>
        </div>
        {/* Logout button is available in the sidebar */}
      </div>
    </DashboardLayout>
  );
} 