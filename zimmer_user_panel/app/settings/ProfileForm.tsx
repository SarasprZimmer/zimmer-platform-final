'use client';
import React from 'react';

export default function ProfileForm({ profile }: { profile: any }) {
  const [name, setName] = React.useState(profile.name || '');
  const [email, setEmail] = React.useState(profile.email || '');
  const [loading, setLoading] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const [error, setError] = React.useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    try {
      const res = await fetch('/api/user/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
      });
      if (!res.ok) throw new Error('خطا در بروزرسانی پروفایل');
      setSuccess(true);
    } catch (err: any) {
      setError(err.message || 'خطای ناشناخته');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block mb-1 text-sm font-medium">نام</label>
        <input
          className="w-full border rounded-lg px-3 py-2"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label className="block mb-1 text-sm font-medium">ایمیل</label>
        <input
          className="w-full border rounded-lg px-3 py-2"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
      </button>
      {success && <div className="text-green-600 text-sm mt-2">پروفایل با موفقیت بروزرسانی شد.</div>}
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
    </form>
  );
} 