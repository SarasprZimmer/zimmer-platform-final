import DashboardLayout from '@/components/DashboardLayout'
import { cookies } from 'next/headers'
import { verifyToken } from '@/lib/auth-server'
import { redirect } from 'next/navigation'
import { LifebuoyIcon } from '@heroicons/react/24/outline'
import FormattedDate from '@/components/FormattedDate';
import SupportTicketForm from './SupportTicketForm';

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

function getStatusText(status: string) {
  switch (status) {
    case 'open': return 'باز';
    case 'pending': return 'در انتظار';
    case 'resolved': return 'حل‌شده';
    default: return status;
  }
}

export default async function SupportPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  const tokenData = token ? await verifyToken(token) : null;

  if (!tokenData) {
    redirect('/login');
  }

  // Fetch tickets
  let tickets = [];
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(apiUrl + '/api/tickets', {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    });
    if (res.ok) {
      const data = await res.json();
      tickets = data.tickets || [];
    } else {
      console.error('Failed to fetch tickets:', res.status);
      // Don't redirect, just show empty state
    }
  } catch (error) {
    console.error('Error fetching tickets:', error);
    // Don't redirect, just show empty state
  }

  return (
    <DashboardLayout user={tokenData.user}>
      <div className="space-y-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">پشتیبانی</h1>
          <p className="text-gray-600">دریافت کمک و راهنمایی برای استفاده از خدمات Zimmer AI</p>
        </div>

        {/* Ticket submission form (client component) */}
        <div className="card mb-6">
          <SupportTicketForm userId={Number(tokenData.user.id)} />
        </div>

        {/* Ticket list */}
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <LifebuoyIcon className="w-5 h-5 text-primary-600" /> تیکت‌های من
          </h3>
          <div className="space-y-4">
            {tickets.length === 0 ? (
              <div className="text-center py-8 text-gray-500">تیکتی ثبت نشده است.</div>
            ) : (
              tickets.map((ticket: any) => (
                <a 
                  key={ticket.id} 
                  href={`/support/${ticket.id}`}
                  className="block border border-gray-200 rounded-lg p-4 hover:border-gray-300 hover:shadow-sm transition-all"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(ticket.status)}`}>
                      {getStatusText(ticket.status)}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full ${getImportanceColor(ticket.importance)}`}>
                      {getImportanceText(ticket.importance)}
                    </span>
                    <span className="text-xs text-gray-500"><FormattedDate date={ticket.created_at} /></span>
                  </div>
                  <div className="font-medium text-gray-900 mb-1">{ticket.subject}</div>
                  <div className="text-sm text-gray-700 mb-2">{ticket.message}</div>
                  
                  {/* Attachment */}
                  {ticket.attachment_path && (
                    <div className="mt-2">
                      <a 
                        href={`${process.env.NEXT_PUBLIC_API_URL}/api/tickets/${ticket.id}/attachment`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                        </svg>
                        دانلود فایل پیوست
                      </a>
                    </div>
                  )}
                  
                  {/* Message count indicator */}
                  <div className="mt-2 text-xs text-gray-500">
                    {ticket.messages ? `${ticket.messages.length} پیام` : '1 پیام'}
                  </div>
                </a>
              ))
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
} 