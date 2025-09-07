"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card, Badge } from "@/components/ui/Kit";
import Link from "next/link";

type TwoFAStatus = { enabled: boolean };
type Me = { email?: string; email_verified_at?: string | null };

export default function SecurityStatus(){
  const [me,setMe]=useState<Me|null>(null);
  const [twofa,setTwofa]=useState<TwoFAStatus|null>(null);
  const [note,setNote]=useState<string|null>(null);
  const [busy,setBusy]=useState(false);

  useEffect(()=>{(async()=>{
    const rMe=await apiFetch("/api/me");
    if(rMe.ok) setMe(await rMe.json());
    const r2=await apiFetch("/api/auth/2fa/status");
    if(r2.ok) setTwofa(await r2.json());
  })()},[]);

  const emailVerified = !!me?.email_verified_at;

  async function sendVerify(){
    if(!me?.email) return;
    setBusy(true); setNote(null);
    try{
      const r=await apiFetch("/api/auth/request-email-verify",{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ email: me.email })
      });
      setNote(r.ok ? "ایمیل تأیید برای شما ارسال شد." : "ارسال ایمیل تأیید با مشکل مواجه شد.");
    } finally { setBusy(false); }
  }

  return (
    <div className="max-w-2xl space-y-4" dir="rtl">
      <div className="text-lg font-semibold">امنیت حساب</div>
      <div className="grid md:grid-cols-2 gap-3 items-start">
        <div className="space-y-2">
          <div className="text-sm">تأیید ایمیل</div>
          <div className="flex items-center gap-2">
            {emailVerified
              ? <Badge className="bg-emerald-100 text-emerald-800">تأیید شده</Badge>
              : <Badge className="bg-yellow-100 text-yellow-800">تأیید نشده</Badge>}
          </div>
          {!emailVerified && (
            <button onClick={sendVerify} disabled={busy} className="px-3 py-2 rounded-xl border disabled:opacity-50">
              ارسال ایمیل تأیید
            </button>
          )}
        </div>

        <div className="space-y-2">
          <div className="text-sm">احراز هویت دومرحله‌ای (۲FA)</div>
          <div className="flex items-center gap-2">
            {twofa?.enabled
              ? <Badge className="bg-emerald-100 text-emerald-800">فعال</Badge>
              : <Badge className="bg-gray-100 text-gray-800">غیرفعال</Badge>}
          </div>
          <Link href="/settings/security" className="px-3 py-2 inline-block rounded-xl bg-black text-white">
            مدیریت ۲FA
          </Link>
        </div>
      </div>
      {note && <div className="text-sm">{note}</div>}
    </div>
  );
}
