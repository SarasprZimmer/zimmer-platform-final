import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { adminAPI } from '../lib/api';
import Layout from '../components/Layout';
import { TableSkeleton } from '../components/LoadingSkeletons';
import ResponsiveTable from '../components/ResponsiveTable';

interface User {
  id: number;
  name: string;
  email: string;
  phone_number: string | null;
  role: 'manager' | 'technical_team' | 'support_staff';
  is_active: boolean;
  created_at: string;
}

interface CreateUserData {
  name: string;
  email: string;
  phone_number: string;
  password: string;
  role: 'manager' | 'technical_team' | 'support_staff';
}

export default function Users() {
  const { user } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createForm, setCreateForm] = useState<CreateUserData>({
    name: '',
    email: '',
    phone_number: '',
    password: '',
    role: 'support_staff'
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const usersData = await adminAPI.getUsers();
      
      // Ensure we have an array
      if (Array.isArray(usersData)) {
        setUsers(usersData);
      } else {
        setUsers([]);
      }
    } catch (err: any) {
      console.error('API Error:', err);
      setUsers([]); // Set empty array as fallback
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await adminAPI.createUser(createForm);
      setShowCreateForm(false);
      setCreateForm({
        name: '',
        email: '',
        phone_number: '',
        password: '',
        role: 'support_staff'
      });
      fetchUsers();
    } catch (err: any) {
      // Error is handled by API client
    }
  };

  const handleUpdateRole = async (userId: number, role: string, isActive: boolean) => {
    try {
      await adminAPI.updateUser(userId, { role, is_active: isActive });
      fetchUsers();
    } catch (err: any) {
      // Error is handled by API client
    }
  };

  const handleDeactivateUser = async (userId: number) => {
    if (!confirm('آیا مطمئن هستید که می‌خواهید این کاربر را غیرفعال کنید؟')) {
      return;
    }
    try {
      await adminAPI.deleteUser(userId);
      fetchUsers();
    } catch (err: any) {
      // Error is handled by API client
    }
  };

  const handleActivateUser = async (userId: number) => {
    try {
      await adminAPI.updateUser(userId, { is_active: true });
      fetchUsers();
    } catch (err: any) {
      // Error is handled by API client
    }
  };

  const getRoleLabel = (role: string) => {
    switch (role) {
      case 'manager': return 'مدیر';
      case 'technical_team': return 'تیم فنی';
      case 'support_staff': return 'پشتیبانی';
      default: return role;
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'manager': return 'bg-red-100 text-red-800';
      case 'technical_team': return 'bg-blue-100 text-blue-800';
      case 'support_staff': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <Layout title="مدیریت کاربران">
        <div className="rtl">
          <TableSkeleton rows={5} columns={5} />
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="مدیریت کاربران">
      <div className="rtl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">مدیریت کاربران</h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          ایجاد کاربر جدید
        </button>
      </div>

      {/* Create User Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">ایجاد کاربر جدید</h2>
            <form onSubmit={handleCreateUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  نام
                </label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={createForm.name}
                  onChange={(e) => setCreateForm({...createForm, name: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  ایمیل
                </label>
                <input
                  type="email"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={createForm.email}
                  onChange={(e) => setCreateForm({...createForm, email: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  شماره تلفن
                </label>
                <input
                  type="tel"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={createForm.phone_number}
                  onChange={(e) => setCreateForm({...createForm, phone_number: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  رمز عبور
                </label>
                <input
                  type="password"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={createForm.password}
                  onChange={(e) => setCreateForm({...createForm, password: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  نقش
                </label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={createForm.role}
                  onChange={(e) => setCreateForm({...createForm, role: e.target.value as any})}
                >
                  <option value="support_staff">پشتیبانی</option>
                  <option value="technical_team">تیم فنی</option>
                  <option value="manager">مدیر</option>
                </select>
              </div>
              <div className="flex space-x-3 space-x-reverse">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
                >
                  ایجاد کاربر
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
                >
                  انصراف
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Users Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <ResponsiveTable
          columns={[
            {
              key: 'user_info',
              label: 'کاربر',
              mobilePriority: true,
              render: (value: any, row: User) => (
                <div>
                  <div className="text-sm font-medium text-gray-900">{row.name}</div>
                  <div className="text-sm text-gray-500">{row.email}</div>
                  {row.phone_number && (
                    <div className="text-sm text-gray-500">{row.phone_number}</div>
                  )}
                </div>
              ),
              className: 'whitespace-nowrap'
            },
            {
              key: 'role',
              label: 'نقش',
              mobilePriority: true,
              render: (value: string) => (
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRoleColor(value)}`}>
                  {getRoleLabel(value)}
                </span>
              ),
              className: 'whitespace-nowrap'
            },
            {
              key: 'is_active',
              label: 'وضعیت',
              mobilePriority: true,
              render: (value: boolean) => (
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  value ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {value ? 'فعال' : 'غیرفعال'}
                </span>
              ),
              className: 'whitespace-nowrap'
            },
            {
              key: 'created_at',
              label: 'تاریخ ایجاد',
              mobilePriority: false,
              render: (value: string) => new Date(value).toLocaleDateString('fa-IR'),
              className: 'whitespace-nowrap text-sm text-gray-500'
            },
            {
              key: 'actions',
              label: 'عملیات',
              mobilePriority: true,
              render: (value: any, row: User) => (
                <div className="space-x-2 space-x-reverse">
                  {row.id !== user?.id && (
                    <>
                      {row.is_active ? (
                        <button
                          onClick={() => handleDeactivateUser(row.id)}
                          className="text-red-600 hover:text-red-900 text-sm font-medium"
                        >
                          غیرفعال کردن
                        </button>
                      ) : (
                        <button
                          onClick={() => handleActivateUser(row.id)}
                          className="text-green-600 hover:text-green-900 text-sm font-medium"
                        >
                          فعال کردن
                        </button>
                      )}
                    </>
                  )}
                </div>
              ),
              className: 'whitespace-nowrap text-sm font-medium'
            }
          ]}
          data={users}
          emptyMessage="هیچ کاربری یافت نشد"
        />
      </div>
      </div>
    </Layout>
  );
}
