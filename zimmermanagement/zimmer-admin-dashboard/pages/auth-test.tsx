import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { useAuth } from '../contexts/AuthContext';
import { getToken, getUser, isAuthenticated } from '../lib/auth';

export default function AuthTest() {
  const [authInfo, setAuthInfo] = useState<any>({});
  const { user } = useAuth();

  useEffect(() => {
    const token = getToken();
    const storedUser = getUser();
    const authenticated = isAuthenticated();
    
    setAuthInfo({
      token: token ? 'Present' : 'Missing',
      storedUser,
      authenticated,
      contextUser: user,
      localStorage: {
        auth_token: localStorage.getItem('auth_token'),
        user: localStorage.getItem('user')
      }
    });
  }, [user]);

  const clearAuth = () => {
    localStorage.clear();
    window.location.reload();
  };

  const testLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: 'admin@zimmer.com',
          password: 'admin123'
        })
      });
      
      const data = await response.json();
      console.log('Login response:', data);
      
      if (data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user', JSON.stringify({
          id: data.user_id,
          email: data.email,
          name: data.name
        }));
        window.location.reload();
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <Layout title="Auth Test">
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Authentication Test</h1>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Authentication Information</h2>
          
          <div className="space-y-4">
            <div>
              <h3 className="font-medium">Token Status:</h3>
              <p className="text-sm text-gray-600">{authInfo.token}</p>
            </div>
            
            <div>
              <h3 className="font-medium">Authenticated:</h3>
              <p className="text-sm text-gray-600">{authInfo.authenticated ? 'Yes' : 'No'}</p>
            </div>
            
            <div>
              <h3 className="font-medium">Context User:</h3>
              <pre className="bg-gray-100 p-2 rounded text-sm overflow-auto">
                {JSON.stringify(authInfo.contextUser, null, 2)}
              </pre>
            </div>
            
            <div>
              <h3 className="font-medium">Stored User:</h3>
              <pre className="bg-gray-100 p-2 rounded text-sm overflow-auto">
                {JSON.stringify(authInfo.storedUser, null, 2)}
              </pre>
            </div>
            
            <div>
              <h3 className="font-medium">LocalStorage:</h3>
              <pre className="bg-gray-100 p-2 rounded text-sm overflow-auto">
                {JSON.stringify(authInfo.localStorage, null, 2)}
              </pre>
            </div>
          </div>
          
          <div className="mt-6 space-x-4 space-x-reverse">
            <button
              onClick={testLogin}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Test Login
            </button>
            
            <button
              onClick={clearAuth}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Clear Auth
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
} 