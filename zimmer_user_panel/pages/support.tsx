'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/router';
import DashboardLayout from '@/components/DashboardLayout';
import { Card } from '@/components/Skeleton';

type Ticket = {
  id: number;
  subject: string;
  category: 'financial' | 'tech' | 'customer';
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  created_at: string;
  updated_at: string;
  messages: Array<{
    id: number;
    content: string;
    is_from_user: boolean;
    created_at: string;
  }>;
};

type FAQ = {
  id: number;
  question: string;
  answer: string;
  category: string;
};

export default function SupportPage() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'tickets' | 'faq' | 'new'>('tickets');
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [loadingTickets, setLoadingTickets] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const [newTicket, setNewTicket] = useState({
    subject: '',
    category: 'tech' as const,
    priority: 'medium' as const,
    description: ''
  });

  // Handle URL parameters for pre-selection
  useEffect(() => {
    const { category, tab } = router.query;
    
    if (tab === 'new') {
      setActiveTab('new');
    }
    
    if (category && ['financial', 'tech', 'customer'].includes(category as string)) {
      setNewTicket(prev => ({
        ...prev,
        category: category as 'financial' | 'tech' | 'customer'
      }));
    }
  }, [router.query]);

  // Mock data
  const mockTickets: Ticket[] = [
    {
      id: 1,
      subject: 'مشکل در ورود به سیستم',
      category: 'tech',
      status: 'open',
      priority: 'high',
      created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
      updated_at: new Date(Date.now() - 86400000 * 1).toISOString(),
      messages: [
        {
          id: 1,
          content: 'سلام، نمی‌تونم وارد حساب کاربری‌ام بشم. خطای 401 می‌گیرم.',
          is_from_user: true,
          created_at: new Date(Date.now() - 86400000 * 2).toISOString()
        },
        {
          id: 2,
          content: 'سلام، لطفاً مرورگر خود را پاک کنید و دوباره تلاش کنید. اگر مشکل ادامه داشت، رمز عبور خود را ریست کنید.',
          is_from_user: false,
          created_at: new Date(Date.now() - 86400000 * 1).toISOString()
        }
      ]
    },
    {
      id: 2,
      subject: 'سوال در مورد پرداخت',
      category: 'financial',
      status: 'resolved',
      priority: 'medium',
      created_at: new Date(Date.now() - 86400000 * 5).toISOString(),
      updated_at: new Date(Date.now() - 86400000 * 3).toISOString(),
      messages: [
        {
          id: 3,
          content: 'چطور می‌تونم پرداخت کنم؟',
          is_from_user: true,
          created_at: new Date(Date.now() - 86400000 * 5).toISOString()
        },
        {
          id: 4,
          content: 'شما می‌توانید از طریق کارت اعتباری، انتقال بانکی یا کیف پول دیجیتال پرداخت کنید.',
          is_from_user: false,
          created_at: new Date(Date.now() - 86400000 * 4).toISOString()
        }
      ]
    }
  ];

  const mockFAQs: FAQ[] = [
    {
      id: 1,
      question: 'چطور می‌تونم اتوماسیون جدید خریداری کنم؟',
      answer: 'برای خرید اتوماسیون جدید، به صفحه اتوماسیون‌ها بروید و روی "خرید" کلیک کنید. سپس مراحل پرداخت را تکمیل کنید.',
      category: 'خرید'
    },
    {
      id: 2,
      question: 'چطور می‌تونم رمز عبور خود را تغییر دهم؟',
      answer: 'به صفحه تنظیمات > امنیت بروید و روی "تغییر رمز عبور" کلیک کنید.',
      category: 'حساب کاربری'
    },
    {
      id: 3,
      question: 'چطور می‌تونم از اتوماسیون‌هایم استفاده کنم؟',
      answer: 'پس از خرید، اتوماسیون‌ها در داشبورد شما نمایش داده می‌شوند. روی هر کدام کلیک کنید تا شروع به استفاده کنید.',
      category: 'استفاده'
    },
    {
      id: 4,
      question: 'چطور می‌تونم پشتیبانی دریافت کنم؟',
      answer: 'می‌توانید از طریق این صفحه تیکت ایجاد کنید یا با ایمیل support@zimmer.ai تماس بگیرید.',
      category: 'پشتیبانی'
    }
  ];

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  useEffect(() => {
    // Load mock data
    setTickets(mockTickets);
    setFaqs(mockFAQs);
  }, []);

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingTickets(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const newTicketData: Ticket = {
      id: Date.now(),
      subject: newTicket.subject,
      category: newTicket.category,
      status: 'open',
      priority: newTicket.priority,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      messages: [{
        id: Date.now(),
        content: newTicket.description,
        is_from_user: true,
        created_at: new Date().toISOString()
      }]
    };
    
    setTickets(prev => [newTicketData, ...prev]);
    setNewTicket({ subject: '', category: 'tech', priority: 'medium', description: '' });
    setActiveTab('tickets');
    setLoadingTickets(false);
  };

  const handleSendMessage = async (ticketId: number) => {
    if (!newMessage.trim()) return;
    
    const ticket = tickets.find(t => t.id === ticketId);
    if (!ticket) return;
    
    const message = {
      id: Date.now(),
      content: newMessage,
      is_from_user: true,
      created_at: new Date().toISOString()
    };
    
    setTickets(prev => prev.map(t => 
      t.id === ticketId 
        ? { ...t, messages: [...t.messages, message], updated_at: new Date().toISOString() }
        : t
    ));
    
    setNewMessage('');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'text-red-600 bg-red-100';
      case 'in_progress': return 'text-yellow-600 bg-yellow-100';
      case 'resolved': return 'text-green-600 bg-green-100';
      case 'closed': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">در حال بارگذاری...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6" dir="rtl">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">پشتیبانی</h1>
          <p className="text-gray-600">در اینجا می‌توانید تیکت‌های پشتیبانی خود را مدیریت کنید و سوالات متداول را مشاهده کنید.</p>
          {router.query.category && (
            <div className="mt-4 p-3 bg-purple-50 border border-purple-200 rounded-xl">
              <p className="text-sm text-purple-700">
                <span className="font-medium">دسته‌بندی انتخاب شده:</span> {
                  router.query.category === 'financial' ? 'پشتیبانی مالی' :
                  router.query.category === 'tech' ? 'پشتیبانی فنی' :
                  router.query.category === 'customer' ? 'امور مشتریان' : ''
                }
              </p>
            </div>
          )}
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex space-x-4 mb-6">
            <button
              onClick={() => setActiveTab('tickets')}
              className={`px-6 py-3 rounded-xl font-medium transition-colors ${
                activeTab === 'tickets' 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              تیکت‌های من
            </button>
            <button
              onClick={() => setActiveTab('faq')}
              className={`px-6 py-3 rounded-xl font-medium transition-colors ${
                activeTab === 'faq' 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              سوالات متداول
            </button>
            <button
              onClick={() => setActiveTab('new')}
              className={`px-6 py-3 rounded-xl font-medium transition-colors ${
                activeTab === 'new' 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              تیکت جدید
            </button>
          </div>

          {/* Tickets Tab */}
          {activeTab === 'tickets' && (
            <div className="space-y-4">
              {tickets.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  هیچ تیکتی یافت نشد
                </div>
              ) : (
                tickets.map(ticket => (
                  <Card key={ticket.id} className="p-4 hover:shadow-lg transition-shadow cursor-pointer" onClick={() => setSelectedTicket(ticket)}>
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-2">{ticket.subject}</h3>
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>دسته‌بندی: {ticket.category === 'tech' ? 'فنی' : ticket.category === 'financial' ? 'مالی' : 'مشتریان'}</span>
                          <span>تاریخ: {new Date(ticket.created_at).toLocaleDateString('fa-IR')}</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(ticket.status)}`}>
                          {ticket.status === 'open' ? 'باز' : 
                           ticket.status === 'in_progress' ? 'در حال بررسی' :
                           ticket.status === 'resolved' ? 'حل شده' : 'بسته'}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getPriorityColor(ticket.priority)}`}>
                          {ticket.priority === 'urgent' ? 'فوری' :
                           ticket.priority === 'high' ? 'بالا' :
                           ticket.priority === 'medium' ? 'متوسط' : 'پایین'}
                        </span>
                      </div>
                    </div>
                  </Card>
                ))
              )}
            </div>
          )}

          {/* FAQ Tab */}
          {activeTab === 'faq' && (
            <div className="space-y-4">
              {faqs.map(faq => (
                <Card key={faq.id} className="p-4">
                  <div className="mb-2">
                    <span className="text-xs bg-purple-100 text-purple-600 px-2 py-1 rounded-full">
                      {faq.category}
                    </span>
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{faq.question}</h3>
                  <p className="text-gray-600">{faq.answer}</p>
                </Card>
              ))}
            </div>
          )}

          {/* New Ticket Tab */}
          {activeTab === 'new' && (
            <form onSubmit={handleCreateTicket} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">موضوع</label>
                <input
                  type="text"
                  value={newTicket.subject}
                  onChange={(e) => setNewTicket(prev => ({ ...prev, subject: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="موضوع تیکت را وارد کنید"
                  required
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">دسته‌بندی</label>
                  <select
                    value={newTicket.category}
                    onChange={(e) => setNewTicket(prev => ({ ...prev, category: e.target.value as any }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="tech">پشتیبانی فنی</option>
                    <option value="financial">پشتیبانی مالی</option>
                    <option value="customer">امور مشتریان</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">اولویت</label>
                  <select
                    value={newTicket.priority}
                    onChange={(e) => setNewTicket(prev => ({ ...prev, priority: e.target.value as any }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="low">پایین</option>
                    <option value="medium">متوسط</option>
                    <option value="high">بالا</option>
                    <option value="urgent">فوری</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">توضیحات</label>
                <textarea
                  value={newTicket.description}
                  onChange={(e) => setNewTicket(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  rows={4}
                  placeholder="توضیحات کامل مشکل یا سوال خود را بنویسید"
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={loadingTickets}
                className="w-full bg-purple-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loadingTickets ? 'در حال ایجاد...' : 'ایجاد تیکت'}
              </button>
            </form>
          )}
        </div>

        {/* Ticket Detail Modal */}
        {selectedTicket && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden">
              <div className="p-6 border-b">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold">{selectedTicket.subject}</h2>
                  <button
                    onClick={() => setSelectedTicket(null)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    ✕
                  </button>
                </div>
              </div>
              
              <div className="p-6 max-h-96 overflow-y-auto space-y-4">
                {selectedTicket.messages.map(message => (
                  <div key={message.id} className={`flex ${message.is_from_user ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-xs p-3 rounded-xl ${
                      message.is_from_user 
                        ? 'bg-purple-600 text-white' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      <p>{message.content}</p>
                      <p className={`text-xs mt-1 ${
                        message.is_from_user ? 'text-purple-100' : 'text-gray-500'
                      }`}>
                        {new Date(message.created_at).toLocaleString('fa-IR')}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="p-6 border-t">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="پیام خود را بنویسید..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    onClick={() => handleSendMessage(selectedTicket.id)}
                    disabled={!newMessage.trim()}
                    className="bg-purple-600 text-white px-6 py-2 rounded-xl hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    ارسال
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
