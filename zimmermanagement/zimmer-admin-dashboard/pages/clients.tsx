import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import ProtectedRoute from '../components/ProtectedRoute';
import ClientCard from '../components/ClientCard';
import { adminAPI } from '../lib/api';
import { useAuth } from '../contexts/AuthContext';
import { CardSkeleton } from '../components/LoadingSkeletons';

interface User {
  id: number;
  name: string;
  email: string;
  phone_number: string;
  is_admin: boolean;
}

interface UserAutomation {
  id: number;
  user_id: number;
  user_name: string;
  automation_id: number;
  automation_name: string;
  tokens_remaining: number;
  demo_tokens: number;
  is_demo_active: boolean;
  demo_expired: boolean;
  status: string;
  created_at: string;
}

export default function Clients() {
  const [users, setUsers] = useState<User[]>([]);
  const [userAutomations, setUserAutomations] = useState<UserAutomation[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showDemoOnly, setShowDemoOnly] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    if (user) fetchUsers();
    // eslint-disable-next-line
  }, [user]);

  useEffect(() => {
    // Filter users based on search term and demo filter
    let filtered = users.filter(user =>
      user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    // Apply demo filter
    if (showDemoOnly) {
      filtered = filtered.filter(user => {
        const demoInfo = getDemoInfo(user.id);
        return demoInfo.hasActiveDemo;
      });
    }
    
    setFilteredUsers(filtered);
  }, [users, searchTerm, showDemoOnly]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      if (!user) return;
      
      const [usersData, automationsData] = await Promise.all([
        adminAPI.getUsers(),
        adminAPI.getUserAutomations()
      ]);
      
      setUsers(Array.isArray(usersData) ? usersData : []);
      setUserAutomations(Array.isArray(automationsData) ? automationsData : []);
    } catch (err) {
      console.error('Error fetching users:', err);
      setUsers([]); // Defensive: set to empty array on error
      setUserAutomations([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const getDemoInfo = (userId: number) => {
    const userAutos = userAutomations.filter(ua => ua.user_id === userId);
    const totalDemoTokens = userAutos.reduce((sum, ua) => sum + ua.demo_tokens, 0);
    const hasActiveDemo = userAutos.some(ua => ua.is_demo_active);
    const hasExpiredDemo = userAutos.some(ua => ua.demo_expired);
    return { totalDemoTokens, hasActiveDemo, hasExpiredDemo };
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <Layout title="Clients">
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Client Management</h2>
              <p className="text-gray-600 mt-2">Manage your clients and their automations</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Array.from({ length: 6 }).map((_, index) => (
                  <CardSkeleton key={index} />
                ))}
              </div>
            </div>
          </div>
        </Layout>
      </ProtectedRoute>
    );
  }



  return (
    <ProtectedRoute>
      <Layout title="Clients">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Client Management</h2>
          <p className="text-gray-600 mt-2">Manage your clients and their automations</p>
        </div>
        
        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                Search Clients
              </label>
              <div className="relative">
                <input
                  type="text"
                  id="search"
                  value={searchTerm}
                  onChange={handleSearch}
                  placeholder="Search by name or email..."
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            </div>
            
            <div className="flex items-end">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={showDemoOnly}
                  onChange={(e) => setShowDemoOnly(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                />
                <span className="ml-2 text-sm text-gray-700">Show only demo users</span>
              </label>
            </div>
          </div>
        </div>

        {/* Client List */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">
                Client List ({filteredUsers.length} {filteredUsers.length === 1 ? 'client' : 'clients'})
              </h3>
              <button
                onClick={fetchUsers}
                className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Refresh
              </button>
            </div>
          </div>
          
          <div className="p-6">
            {filteredUsers.length === 0 ? (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No clients found</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {searchTerm ? 'Try adjusting your search terms.' : 'Get started by adding your first client.'}
                </p>
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {filteredUsers.map((user) => (
                  <ClientCard 
                    key={user.id} 
                    user={user} 
                    demoInfo={getDemoInfo(user.id)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
    </ProtectedRoute>
  );
} 