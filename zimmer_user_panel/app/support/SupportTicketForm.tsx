'use client';
import React from 'react';

export default function SupportTicketForm({ userId }: { userId: number }) {
  const [subject, setSubject] = React.useState('');
  const [message, setMessage] = React.useState('');
  const [importance, setImportance] = React.useState('medium');
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const [error, setError] = React.useState('');

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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    
    try {
      const formData = new FormData();
      formData.append('user_id', userId.toString());
      formData.append('subject', subject);
      formData.append('message', message);
      formData.append('importance', importance);
      if (selectedFile) {
        formData.append('file', selectedFile);
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(apiUrl + '/api/tickets', {
        method: 'POST',
        body: formData, // Don't set Content-Type header for FormData
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'خطا در ارسال تیکت');
      }
      
      setSuccess(true);
      setSubject('');
      setMessage('');
      setImportance('medium');
      setSelectedFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (err: any) {
      setError(err.message || 'خطای ناشناخته');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block mb-1 text-sm font-medium">موضوع</label>
        <input
          className="w-full border rounded-lg px-3 py-2"
          value={subject}
          onChange={e => setSubject(e.target.value)}
          required
        />
      </div>
      
      <div>
        <label className="block mb-1 text-sm font-medium">اهمیت</label>
        <select
          className="w-full border rounded-lg px-3 py-2"
          value={importance}
          onChange={e => setImportance(e.target.value)}
          required
        >
          <option value="low">کم</option>
          <option value="medium">متوسط</option>
          <option value="immediate">فوری</option>
        </select>
      </div>
      
      <div>
        <label className="block mb-1 text-sm font-medium">پیام</label>
        <textarea
          className="w-full border rounded-lg px-3 py-2"
          rows={4}
          value={message}
          onChange={e => setMessage(e.target.value)}
          required
        />
      </div>
      
      <div>
        <label className="block mb-1 text-sm font-medium">فایل پیوست (اختیاری)</label>
        <input
          id="file-input"
          type="file"
          className="w-full border rounded-lg px-3 py-2"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif"
        />
        <p className="text-xs text-gray-500 mt-1">
          حداکثر حجم: 2 مگابایت | فرمت‌های مجاز: PDF, DOC, DOCX, TXT, JPG, PNG, GIF
        </p>
        {selectedFile && (
          <p className="text-sm text-blue-600 mt-1">
            فایل انتخاب شده: {selectedFile.name}
          </p>
        )}
      </div>
      
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? 'در حال ارسال...' : 'ارسال تیکت'}
      </button>
      
      {success && <div className="text-green-600 text-sm mt-2">تیکت با موفقیت ارسال شد.</div>}
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
    </form>
  );
} 