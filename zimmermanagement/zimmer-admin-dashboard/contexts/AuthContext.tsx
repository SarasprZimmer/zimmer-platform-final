import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, login as authLogin, signup as authSignup, logout as authLogout, getToken, getUser, setToken, setUser, removeToken, removeUser } from '../lib/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUserState] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing authentication on app load
    const token = getToken();
    const savedUser = getUser();
    
    console.log('AuthContext: Checking authentication on load');
    console.log('Token present:', !!token);
    console.log('Saved user:', savedUser);
    
    if (token && savedUser) {
      setUserState(savedUser);
    }
    
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authLogin(email, password);
      const userData: User = {
        id: response.user_id,
        email: response.email,
        name: response.name,
      };
      
      setToken(response.access_token);
      setUser(userData);
      setUserState(userData);
    } catch (error) {
      throw error;
    }
  };

  const signup = async (email: string, password: string, name: string) => {
    try {
      await authSignup(email, password, name);
      // After successful signup, automatically log in
      await login(email, password);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    console.log('Logging out...');
    authLogout();
    setUserState(null);
    // Force redirect to login page
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    signup,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 