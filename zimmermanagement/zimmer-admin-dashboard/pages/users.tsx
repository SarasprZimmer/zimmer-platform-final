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
  is_admin: boolean;
  created_at: string;
}


export default function Users() {
  const { user } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const usersData = await adminAPI.getUsers();
      
      // Handle both array and object response formats
      if (Array.isArray(usersData)) {
        setUsers(usersData);
      } else if (usersData && usersData.users && Array.isArray(usersData.users)) {
        // Backend returns { total_count: number, users: User[] }
        setUsers(usersData.users);
      } else {
        console.warn('Unexpected users data format:', usersData);
        setUsers([]);
      }
    } catch (err: any) {
      console.error('API Error:', err);
      setUsers([]); // Set empty array as fallback
    } finally {
      setLoading(false);
    }
  };


  const getRoleLabel = (isAdmin: boolean) => {
    return isAdmin ? 'مدیر' : 'مشتری';
  };

  const getRoleColor = (isAdmin: boolean) => {
    return isAdmin ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800';
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
        <h1 className="text-2xl font-bold text-gray-900">مشتریان</h1>
        <div className="text-sm text-gray-500">
          مجموع: {users.length} کاربر
        </div>
      </div>


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
              key: 'is_admin',
              label: 'نقش',
              mobilePriority: true,
              render: (value: boolean) => (
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRoleColor(value)}`}>
                  {getRoleLabel(value)}
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
                  <span className="text-sm text-gray-500">
                    {row.is_admin ? 'مدیر سیستم' : 'مشتری'}
                  </span>
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
