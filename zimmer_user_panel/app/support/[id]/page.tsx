 'use client';
import DashboardLayout from '@/components/DashboardLayout'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import React from 'react'
import FormattedDate from '@/components/FormattedDate';
import TicketChat from './TicketChat';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { use } from 'react';
import Cookies from 'js-cookie';

function getStatusColor(status: string) {
  switch (status) {
    case 'open': return 'text-blue-600 bg-blue-50';
    case 'pending': return 'text-orange-600 bg-orange-50';
    case 'resolved': return 'text-green-600 bg-green-50';
    default: return 'text-gray-600 bg-gray-50';
  }
}

function getImportanceColor(importance: string) {
  switch (importance.toLowerCase()) {
    case 'low': return 'text-gray-600 bg-gray-50';
    case 'medium': return 'text-yellow-600 bg-yellow-50';
    case 'immediate': return 'text-red-600 bg-red-50';
    default: return 'text-gray-600 bg-gray-50';
  }
}

function getImportanceText(importance: string) {
  switch (importance.toLowerCase()) {
    case 'low': return 'کم';
    case 'medium': return 'متوسط';
    case 'immediate': return 'فوری';
    default: return importance;
  }
}

// Parse ticket message to separate original content from replies
function parseTicketMessages(ticket: any): { originalMessage: string; messages: any[] } {
  const fullMessage = ticket.message;
  const replySeparator = '--- Reply from ';
  
  if (!fullMessage.includes(replySeparator)) {
    // No replies, just original message
    return {
      originalMessage: fullMessage,
      messages: []
    };
  }
  
  const parts = fullMessage.split(replySeparator);
  const originalMessage = parts[0].trim();
  const messages: any[] = [];
  
  for (let i = 1; i < parts.length; i++) {
    const part = parts[i];
    const endIndex = part.indexOf(' ---');
    if (endIndex !== -1) {
      const sender = part.substring(0, endIndex);
      const content = part.substring(endIndex + 4).trim();
      messages.push({
        id: `reply-${i}`,
        sender,
        content,
        timestamp: new Date().toISOString(),
        isAdmin: sender.toLowerCase().includes('admin')
      });
    }
  }
  
  return { originalMessage, messages };
}

function getStatusText(status: string) {
  switch (status) {
    case 'open': return 'باز';
    case 'pending': return 'در انتظار';
    case 'resolved': return 'حل‌شده';
    default: return status;
  }
}

export default function TicketDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const [ticket, setTicket] = useState<any>(null);
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Unwrap params using React.use()
  const resolvedParams = use(params);
  const ticketId = resolvedParams.id;

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get token from cookies
        const token = Cookies.get('auth-token');
        console.log('Token found:', !!token);
        
        if (!token) {
          console.log('No token found, redirecting to login');
          router.push('/login');
          return;
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        console.log('API URL:', apiUrl);

        // First, get user profile
        console.log('Fetching user profile...');
        const userRes = await fetch(`${apiUrl}/api/user/profile`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        console.log('User profile response status:', userRes.status);
        
        if (!userRes.ok) {
          console.log('User profile failed, redirecting to login');
          router.push('/login');
          return;
        }
        
        const userData = await userRes.json();
        console.log('User data:', userData);
        setUser(userData);

        // Then fetch ticket details
        console.log('Fetching ticket details...');
        const ticketRes = await fetch(`${apiUrl}/api/tickets/${ticketId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        console.log('Ticket response status:', ticketRes.status);
        
        if (!ticketRes.ok) {
          const errorData = await ticketRes.json().catch(() => ({}));
          console.log('Ticket fetch failed:', errorData);
          setError('تیکت یافت نشد');
          return;
        }
        
        const ticketData = await ticketRes.json();
        console.log('Ticket data:', ticketData);

        // Check if user owns this ticket or is admin
        if (ticketData.user_id !== userData.id && !userData.is_admin) {
          console.log('User does not have access to this ticket');
          setError('شما دسترسی به این تیکت ندارید');
          return;
        }
        
        setTicket(ticketData);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('خطا در بارگذاری اطلاعات');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticketId, router]);

  const handleMessageSent = () => {
    // Refresh ticket data
    const fetchTicket = async () => {
      try {
        const token = Cookies.get('auth-token');
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${apiUrl}/api/tickets/${ticketId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        if (res.ok) {
          const ticketData = await res.json();
          setTicket(ticketData);
        }
      } catch (err) {
        console.error('Error refreshing ticket:', err);
      }
    };

    fetchTicket();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="mr-3 text-gray-600">در حال بارگذاری...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => router.push('/support')}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            بازگشت به تیکت‌ها
          </button>
        </div>
      </div>
    );
  }

  if (!ticket || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 mb-4">اطلاعات یافت نشد</p>
          <button 
            onClick={() => router.push('/support')}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            بازگشت به تیکت‌ها
          </button>
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => router.push('/support')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <ArrowLeftIcon className="w-5 h-5" />
            بازگشت به تیکت‌ها
          </button>
        </div>

        {/* Ticket Header */}
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <span className={`text-sm px-3 py-1 rounded-full ${getStatusColor(ticket.status)}`}>
              {getStatusText(ticket.status)}
            </span>
            <span className={`text-sm px-3 py-1 rounded-full ${getImportanceColor(ticket.importance)}`}>
              {getImportanceText(ticket.importance)}
            </span>
            <span className="text-sm text-gray-500">
              <FormattedDate date={ticket.created_at} />
            </span>
          </div>
          
          <h1 className="text-xl font-bold text-gray-900 mb-2">{ticket.subject}</h1>
          <p className="text-gray-700 mb-4">{parseTicketMessages(ticket).originalMessage}</p>
          
          {/* Original attachment */}
          {ticket.attachment_path && (
            <div className="mb-4">
              <a 
                href={`${process.env.NEXT_PUBLIC_API_URL}/api/tickets/${ticket.id}/attachment`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm text-blue-600 hover:text-blue-800"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
                دانلود فایل پیوست اصلی
              </a>
            </div>
          )}
        </div>

        {/* Chat Component */}
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">گفتگو</h3>
          <TicketChat 
            ticketId={ticket.id} 
            userId={user.id} 
            ticketMessage={ticket.message}
            onMessageSent={handleMessageSent}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}