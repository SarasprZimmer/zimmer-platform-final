"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Notify, routeForNotification } from "@/lib/notifications";
import DashboardLayout from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/router";

export default function NotificationsPage(){
  const { user, isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [items, setItems] = useState<Notify[] | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  async function load(){
    try {
      const r = await apiFetch("/api/notifications?limit=100&offset=0");
      if (!r.ok) { 
        setItems([]); 
        return; 
      }
      const j = await r.json(); 
      setItems(Array.isArray(j) ? j : (j.items || []));
    } catch (error) {
      console.error('Failed to load notifications:', error);
      setItems([]);
    }
  }

  async function markAllRead() {
    setBusy(true);
    try {
      await apiFetch("/api/notifications/mark-all-read", { method: "POST" });
      await load();
    } catch (error) {
      console.error('Failed to mark all as read:', error);
    } finally {
      setBusy(false);
    }
  }

  async function markOneRead(id: number) {
    setBusy(true);
    try {
      await apiFetch("/api/notifications/mark-read", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ids: [id] })
      });
      await load();
    } catch (error) {
      console.error('Failed to mark as read:', error);
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => { 
    if (isAuthenticated) {
      load(); 
    }
  }, [isAuthenticated]);

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

  const unreadCount = items ? items.filter(n => !n.read).length : 0;

  return (
    <DashboardLayout>
      <div className="p-8">
        <div className="max-w-4xl mx-auto">
          {/* Page Header */}
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">اعلان‌ها</h1>
                <p className="text-gray-600">مدیریت و مشاهده تمام اعلان‌های سیستم</p>
              </div>
              {unreadCount > 0 && (
                <button 
                  onClick={markAllRead}
                  disabled={busy}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
                >
                  {busy ? "در حال پردازش..." : `علامت‌گذاری همه (${unreadCount})`}
                </button>
              )}
            </div>
          </div>

          {/* Notifications List */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            {!items && (
              <div className="space-y-4">
                <div className="h-16 rounded-xl bg-gray-100 animate-pulse" />
                <div className="h-16 rounded-xl bg-gray-100 animate-pulse" />
                <div className="h-16 rounded-xl bg-gray-100 animate-pulse" />
              </div>
            )}
            
            {items && items.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM4.828 7l2.586 2.586a2 2 0 002.828 0L12.828 7H4.828z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">اعلانی وجود ندارد</h3>
                <p className="text-gray-500">هنوز هیچ اعلانی دریافت نکرده‌اید.</p>
              </div>
            )}
            
            {items && items.length > 0 && (
              <div className="space-y-4">
                {items.map(n => (
                  <div 
                    key={n.id} 
                    className={`rounded-xl border p-6 transition-all duration-200 hover:shadow-md ${
                      n.read ? "opacity-70 bg-gray-50" : "bg-white border-purple-200"
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <TypeBadge type={n.type} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 mb-1">{n.title}</h3>
                            {n.body && (
                              <p className="text-gray-600 text-sm mb-3 line-clamp-2">{n.body}</p>
                            )}
                            <div className="flex items-center gap-4 text-xs text-gray-500">
                              <span>{new Date(n.created_at).toLocaleDateString('fa-IR')}</span>
                              <span>{new Date(n.created_at).toLocaleTimeString('fa-IR', { 
                                hour: '2-digit', 
                                minute: '2-digit' 
                              })}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2 ml-4">
                            <a 
                              href={routeForNotification(n)} 
                              className="px-3 py-1 bg-purple-100 text-purple-700 rounded-lg text-sm hover:bg-purple-200 transition-colors"
                            >
                              مشاهده
                            </a>
                            {!n.read && (
                              <button 
                                onClick={() => markOneRead(n.id)}
                                disabled={busy}
                                className="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200 disabled:opacity-50 transition-colors"
                              >
                                خواندم
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function TypeBadge({ type }: { type?: string }){
  const t = (type || "").toLowerCase();
  const label = t === "payment" ? "پرداخت" : 
                t === "ticket" ? "تیکت" : 
                t === "automation" ? "اتوماسیون" : 
                "سیستمی";
  const color = t === "payment" ? "bg-emerald-100 text-emerald-800" :
                t === "ticket" ? "bg-blue-100 text-blue-800" :
                t === "automation" ? "bg-purple-100 text-purple-800" :
                "bg-gray-100 text-gray-800";
  return (
    <span className={`text-xs px-3 py-1 rounded-full font-medium ${color}`}>
      {label}
    </span>
  );
}
