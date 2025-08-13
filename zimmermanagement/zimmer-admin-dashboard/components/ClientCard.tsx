import React from 'react';
import Link from 'next/link';

interface User {
  id: number;
  name: string;
  email: string;
  phone_number: string;
  is_admin: boolean;
}

interface ClientCardProps {
  user: User;
  demoInfo?: {
    totalDemoTokens: number;
    hasActiveDemo: boolean;
    hasExpiredDemo: boolean;
  };
}

export default function ClientCard({ user, demoInfo }: ClientCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {user.name}
            </h3>
            <p className="text-sm text-gray-600 mb-2">{user.email}</p>
            <p className="text-sm text-gray-500">{user.phone_number}</p>
          </div>
          {user.is_admin && (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              Admin
            </span>
          )}
        </div>
        
        {/* Demo Token Info */}
        {demoInfo && (
          <div className="mt-3 pt-3 border-t border-gray-100">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Demo Tokens:</span>
              <span className={`font-medium ${
                demoInfo.hasActiveDemo ? 'text-green-600' : 
                demoInfo.hasExpiredDemo ? 'text-red-600' : 'text-gray-500'
              }`}>
                {demoInfo.totalDemoTokens}
              </span>
            </div>
            {demoInfo.hasActiveDemo && (
              <div className="mt-1 text-xs text-green-600">
                🎉 Active Demo
              </div>
            )}
            {demoInfo.hasExpiredDemo && (
              <div className="mt-1 text-xs text-red-600">
                ⚠️ Demo Expired
              </div>
            )}
          </div>
        )}
        
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="text-sm text-gray-500">
            ID: {user.id}
          </div>
          <Link 
            href={`/usage/${user.id}`}
            className="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors duration-200"
          >
            View Usage →
          </Link>
        </div>
      </div>
    </div>
  );
} 