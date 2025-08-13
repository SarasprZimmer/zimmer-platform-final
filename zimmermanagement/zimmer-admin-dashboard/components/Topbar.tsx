import React from 'react';
import { useAuth } from '../contexts/AuthContext';

interface TopbarProps {
  title: string;
}

const Topbar: React.FC<TopbarProps> = ({ title }) => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900">{title}</h1>
        
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">
            خوش آمدید، {user?.name || 'کاربر'}
          </span>
          <button
            onClick={logout}
            className="text-sm text-red-600 hover:text-red-800"
          >
            خروج
          </button>
        </div>
      </div>
    </header>
  );
};

export default Topbar; 