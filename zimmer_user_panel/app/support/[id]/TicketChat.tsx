'use client';
import React from 'react';
import FormattedDate from '@/components/FormattedDate';
import Cookies from 'js-cookie';

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: string;
  isAdmin: boolean;
}

interface TicketChatProps {
  ticketId: number;
  userId: number;
  ticketMessage: string;
  onMessageSent: () => void;
}

export default function TicketChat({ ticketId, userId, ticketMessage, onMessageSent }: TicketChatProps) {
  const [newMessage, setNewMessage] = React.useState('');
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  // Parse ticket message to get replies
  const parseMessages = React.useMemo(() => {
    const fullMessage = ticketMessage;
    const replySeparator = '--- Reply from ';
    
    if (!fullMessage.includes(replySeparator)) {
      return [];
    }
    
    const parts = fullMessage.split(replySeparator);
    const messages: Message[] = [];
    
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
    
    return messages;
  }, [ticketMessage]);

  // Scroll to bottom when new messages arrive
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [parseMessages]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file size (2MB)
      if (file.size > 2 * 1024 * 1024) {
        setError('حجم فایل نباید بیشتر از 2 مگابایت باشد');
        return;
      }
      // Validate file type
      const allowedTypes = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.gif'];
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      if (!allowedTypes.includes(fileExtension)) {
        setError('نوع فایل مجاز نیست. فایل‌های مجاز: PDF, DOC, DOCX, TXT, JPG, PNG, GIF');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    setLoading(true);
    setError('');

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const token = Cookies.get('auth-token');
      
      const res = await fetch(apiUrl + `/api/tickets/${ticketId}`, {
        method: 'PUT',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: newMessage })
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'خطا در ارسال پیام');
      }

      setNewMessage('');
      setSelectedFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('message-file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      // Notify parent to refresh ticket data
      onMessageSent();
    } catch (err: any) {
      setError(err.message || 'خطای ناشناخته');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Messages */}
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {parseMessages.length === 0 ? (
          <div className="text-center py-8 text-gray-500">هنوز پیامی ارسال نشده است.</div>
        ) : (
          parseMessages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isAdmin ? 'justify-start' : 'justify-end'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.isAdmin
                    ? 'bg-gray-200 text-gray-900'
                    : 'bg-blue-500 text-white'
                }`}
              >
                <div className="text-sm mb-1">
                  <span className="font-medium">{message.sender}</span>
                  <span className="text-xs opacity-75 ml-2">
                    <FormattedDate date={message.timestamp} />
                  </span>
                </div>
                <div className="text-sm whitespace-pre-wrap">{message.content}</div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message input */}
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <textarea
            className="w-full border rounded-lg px-3 py-2"
            rows={3}
            placeholder="پیام خود را بنویسید..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            disabled={loading}
          />
        </div>
        
        <div className="flex items-center gap-3">
          <div className="flex-1">
            <input
              id="message-file-input"
              type="file"
              className="w-full text-sm"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-1">
              حداکثر حجم: 2 مگابایت
            </p>
            {selectedFile && (
              <p className="text-sm text-blue-600 mt-1">
                فایل انتخاب شده: {selectedFile.name}
              </p>
            )}
          </div>
          
          <button
            type="submit"
            className="btn-primary px-6"
            disabled={loading || !newMessage.trim()}
          >
            {loading ? 'در حال ارسال...' : 'ارسال'}
          </button>
        </div>
        
        {error && (
          <p className="text-red-600 text-sm">{error}</p>
        )}
      </form>
    </div>
  );
}