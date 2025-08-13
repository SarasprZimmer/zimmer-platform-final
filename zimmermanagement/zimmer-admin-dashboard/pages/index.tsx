import React from 'react';
import Layout from '../components/Layout';

export default function Dashboard() {
  return (
    <Layout title="داشبورد">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">داشبورد مدیریت</h2>
          <p className="text-gray-600 mt-2">به پنل مدیریت زیمر خوش آمدید</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Stats Cards */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">👥</span>
                </div>
              </div>
              <div className="mr-4">
                <p className="text-sm font-medium text-gray-600">کل مشتریان</p>
                <p className="text-2xl font-semibold text-gray-900">۱۲۵</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">🎫</span>
                </div>
              </div>
              <div className="mr-4">
                <p className="text-sm font-medium text-gray-600">تیکت‌های باز</p>
                <p className="text-2xl font-semibold text-gray-900">۸</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">🔢</span>
                </div>
              </div>
              <div className="mr-4">
                <p className="text-sm font-medium text-gray-600">توکن‌های استفاده شده</p>
                <p className="text-2xl font-semibold text-gray-900">۲,۴۵۶</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">💳</span>
                </div>
              </div>
              <div className="mr-4">
                <p className="text-sm font-medium text-gray-600">درآمد ماهانه</p>
                <p className="text-2xl font-semibold text-gray-900">$۱۲,۵۰۰</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">عملیات سریع</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <span className="text-lg mr-2">🎫</span>
              <span className="text-sm font-medium">ایجاد تیکت جدید</span>
            </button>
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <span className="text-lg mr-2">📚</span>
              <span className="text-sm font-medium">افزودن به پایگاه دانش</span>
            </button>
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <span className="text-lg mr-2">👥</span>
              <span className="text-sm font-medium">مدیریت مشتریان</span>
            </button>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">فعالیت‌های اخیر</h3>
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm text-gray-900">تیکت جدید از کاربر احمد محمدی</p>
                <p className="text-xs text-gray-500">۲ ساعت پیش</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="w-2 h-2 bg-green-600 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm text-gray-900">پرداخت جدید ثبت شد</p>
                <p className="text-xs text-gray-500">۴ ساعت پیش</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="w-2 h-2 bg-yellow-600 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm text-gray-900">مشتری جدید ثبت نام کرد</p>
                <p className="text-xs text-gray-500">۶ ساعت پیش</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
} 