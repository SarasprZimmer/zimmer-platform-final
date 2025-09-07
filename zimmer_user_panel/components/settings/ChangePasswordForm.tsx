"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card } from "@/components/ui/Kit";

export default function ChangePasswordForm(){
  const [p1,setP1]=useState(""); const [p2,setP2]=useState("");
  const [msg,setMsg]=useState<string|null>(null);
  const [busy,setBusy]=useState(false);

  async function submit(e:React.FormEvent){
    e.preventDefault();
    if(!p1 || !p2){ setMsg("رمز عبور را کامل وارد کنید."); return; }
    if(p1!==p2){ setMsg("رمزها یکسان نیستند."); return; }
    setBusy(true); setMsg(null);
    try{
      const r=await apiFetch("/api/user/password",{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ new_password: p1, confirm_password: p2 })
      });
      setMsg(r.ok ? "رمز عبور با موفقیت تغییر کرد." : "خطا در تغییر رمز.");
      if(r.ok){ setP1(""); setP2(""); }
    } finally { setBusy(false); }
  }

  return (
    <div className="max-w-2xl space-y-4" dir="rtl">
      <div className="text-lg font-semibold">تغییر رمز عبور</div>
      <form onSubmit={submit} className="grid md:grid-cols-2 gap-3">
        <input className="border rounded-xl p-3" placeholder="رمز جدید" type="password" value={p1} onChange={e=>setP1(e.target.value)} />
        <input className="border rounded-xl p-3" placeholder="تکرار رمز" type="password" value={p2} onChange={e=>setP2(e.target.value)} />
        {msg && <div className="md:col-span-2 text-sm">{msg}</div>}
        <div className="md:col-span-2 flex justify-end">
          <button type="submit" disabled={busy} className="px-4 py-2 rounded-xl border disabled:opacity-50">اعمال</button>
        </div>
      </form>
    </div>
  );
}