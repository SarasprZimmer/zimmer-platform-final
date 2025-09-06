"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card, Skeleton } from "@/components/Skeleton";
import { motion } from "framer-motion";
import { mockData } from "@/lib/mockApi";

type UA = {
  id:number;
  name:string;
  description?:string;
  tokens_remaining?:number;
  demo_tokens?:number;
  integration_status?:string;
  status?: 'active' | 'inactive' | 'error';
  success_rate?: number;
  total_runs?: number;
  last_run?: string;
  next_run?: string;
  created_at?: string;
  usage_stats?: {
    tokens_used_today: number;
    tokens_used_this_month: number;
    average_daily_usage: number;
  };
};

export default function MyAutomationsList(){
  const [items,setItems]=useState<UA[]|null>(null);
  const [err,setErr]=useState<string|null>(null);
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set());

  const toggleExpanded = (id: number) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  useEffect(()=>{(async()=>{
    try{
      // Use mock data for now since API endpoints are not ready
      console.log('Using mock data for automations list');
      // Transform mock data to match the expected format
      const transformedData = mockData.automations.map((automation, index) => ({
        id: automation.id,
        name: automation.name,
        description: automation.description,
        tokens_remaining: automation.tokens_remaining,
        demo_tokens: automation.demo_tokens,
        integration_status: 'healthy',
        status: index % 3 === 0 ? 'active' : index % 3 === 1 ? 'inactive' : 'error',
        success_rate: 85 + Math.random() * 15, // Random between 85-100
        total_runs: Math.floor(Math.random() * 1000) + 100,
        last_run: index % 2 === 0 ? '۲ ساعت پیش' : '۱ روز پیش',
        next_run: index % 2 === 0 ? '۱ ساعت دیگر' : 'غیرفعال',
        created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
        usage_stats: {
          tokens_used_today: Math.floor(Math.random() * 50) + 10,
          tokens_used_this_month: Math.floor(Math.random() * 500) + 100,
          average_daily_usage: Math.floor(Math.random() * 30) + 5
        }
      }));
      setItems(transformedData);
      return;
      
      // TODO: Uncomment when API is ready
      // const r=await apiFetch("/api/user/automations");
      // if(!r.ok) throw new Error();
      // const j = await r.json();
      // setItems(Array.isArray(j) ? j : (j?.items || []));
    }catch{ setErr("عدم دریافت فهرست اتوماسیون‌ها"); }
  })()},[]);

  return (
    <Card>
      <div className="flex items-center justify-between mb-3">
        <div className="font-semibold">محصولات</div>
        <a href="/automations/marketplace" className="text-sm underline">مشاهده فروشگاه</a>
      </div>

      {!items && !err && (
        <div className="space-y-3">
          <Skeleton className="h-16" />
          <Skeleton className="h-16" />
          <Skeleton className="h-16" />
        </div>
      )}
      {err && <div className="text-sm text-red-600">{err}</div>}

      {items && items.length>0 && (
        <ul className="space-y-3">
          {items.map((a,idx)=>(
            <motion.li
              key={a.id}
              initial={{opacity:0, y:6}}
              animate={{opacity:1, y:0}}
              transition={{delay: idx*0.03}}
              className="rounded-xl border bg-white overflow-hidden"
            >
              <div className="flex items-center justify-between p-3">
                <div className="min-w-0 pr-2">
                  <div className="font-medium truncate">{a.name}</div>
                  <div className="text-xs opacity-70 truncate">{a.description || "—"}</div>
                  <div className="text-[11px] opacity-60 mt-1">
                    اعتبار باقی‌مانده: {a.tokens_remaining ?? 0}
                    {a.integration_status ? ` • وضعیت: ${faStatus(a.integration_status)}` : ""}
                  </div>
                </div>
                <button 
                  onClick={() => toggleExpanded(a.id)}
                  className="shrink-0 px-3 py-2 rounded-xl border hover:bg-gray-50 transition-colors"
                >
                  {expandedItems.has(a.id) ? 'بستن جزئیات' : 'مشاهده جزئیات'}
                </button>
              </div>
              
              {expandedItems.has(a.id) && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  className="border-t bg-gray-50 p-4"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {/* Status Section */}
                    <div className="space-y-2">
                      <h4 className="font-semibold text-sm text-gray-700">وضعیت</h4>
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span>وضعیت کلی:</span>
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            a.status === 'active' ? 'bg-green-100 text-green-800' :
                            a.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {a.status === 'active' ? 'فعال' : a.status === 'inactive' ? 'غیرفعال' : 'خطا'}
                          </span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>نرخ موفقیت:</span>
                          <span className="font-medium">{a.success_rate?.toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>کل اجراها:</span>
                          <span className="font-medium">{a.total_runs?.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>

                    {/* Usage Section */}
                    <div className="space-y-2">
                      <h4 className="font-semibold text-sm text-gray-700">استفاده</h4>
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span>امروز:</span>
                          <span className="font-medium">{a.usage_stats?.tokens_used_today} توکن</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>این ماه:</span>
                          <span className="font-medium">{a.usage_stats?.tokens_used_this_month} توکن</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>میانگین روزانه:</span>
                          <span className="font-medium">{a.usage_stats?.average_daily_usage} توکن</span>
                        </div>
                      </div>
                    </div>

                    {/* Schedule Section */}
                    <div className="space-y-2">
                      <h4 className="font-semibold text-sm text-gray-700">زمان‌بندی</h4>
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span>آخرین اجرا:</span>
                          <span className="font-medium">{a.last_run}</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>اجرای بعدی:</span>
                          <span className="font-medium">{a.next_run}</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>تاریخ ایجاد:</span>
                          <span className="font-medium">
                            {a.created_at ? new Date(a.created_at).toLocaleDateString('fa-IR') : '—'}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Token Usage Progress Bar */}
                  <div className="mt-4">
                    <div className="flex justify-between text-xs text-gray-600 mb-2">
                      <span>استفاده از توکن‌ها</span>
                      <span>{a.tokens_remaining} / {(a.tokens_remaining || 0) + (a.demo_tokens || 0)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: `${Math.min(100, Math.round(((a.tokens_remaining || 0) / ((a.tokens_remaining || 0) + (a.demo_tokens || 0) || 1)) * 100))}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.li>
          ))}
        </ul>
      )}

      {items && items.length===0 && (
        <div className="text-sm opacity-70">هنوز اتوماسیونی تهیه نکرده‌اید. <a className="underline" href="/automations/marketplace">مشاهده فروشگاه</a></div>
      )}
    </Card>
  );
}

function faStatus(s?: string){
  switch((s||"").toLowerCase()){
    case "healthy": return "سالم";
    case "degraded": return "کاهش کارایی";
    case "error": return "خطا";
    case "pending": return "در انتظار راه‌اندازی";
    default: return s || "-";
  }
}
