'use client';
import React from 'react';
import Cookies from 'js-cookie';

export default function LogoutButton() {
  const [loading, setLoading] = React.useState(false);
  async function handleLogout() {
    setLoading(true);
    // Clear the auth token cookie
    Cookies.remove('auth-token');
    // Redirect to login page
    window.location.href = '/login';
  }
  return (
    <button className="btn-secondary" onClick={handleLogout} disabled={loading}>
      خروج از حساب
    </button>
  );
} 