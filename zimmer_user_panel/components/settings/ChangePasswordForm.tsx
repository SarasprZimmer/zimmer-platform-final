"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card } from "@/components/ui/Kit";

export default function ChangePasswordForm(){
  const [currentPassword,setCurrentPassword]=useState("");
  const [newPassword,setNewPassword]=useState(""); 
  const [confirmPassword,setConfirmPassword]=useState("");
  const [msg,setMsg]=useState<string|null>(null);
  const [busy,setBusy]=useState(false);

  async function changePass(){
    if(!currentPassword || !newPassword || !confirmPassword){ 
      setMsg("تمام فیلدها را کامل کنید."); 
      return; 
    }
    if(newPassword !== confirmPassword){
      setMsg("رمز عبور جدید و تکرار آن یکسان نیستند.");
      return;
    }
    if(newPassword.length < 6){
      setMsg("رمز عبور جدید باید حداقل ۶ کاراکتر باشد.");
      return;
    }
    setMsg(null); setBusy(true);
    try{
      const r = await apiFetch("/api/user/change-password", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ 
          current_password: currentPassword,
          new_password: newPassword
          // Note: confirm_password is not needed by backend, we validate it in frontend
        })
      });
      setMsg(r.ok ? "رمز عبور تغییر کرد." : "خطا در تغییر رمز عبور");
      if(r.ok){ 
        setCurrentPassword(""); 
        setNewPassword(""); 
        setConfirmPassword(""); 
      }
    } finally { setBusy(false); }
  }

  return (
    <Card className="w-full space-y-6" dir="rtl">
      <div className="text-lg font-semibold">تغییر رمز عبور</div>
      
      {/* Current Password Field */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">رمز عبور فعلی</label>
        <input 
          placeholder="رمز عبور فعلی خود را وارد کنید" 
          type="password" 
          className="w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-purple-500 focus:border-transparent" 
          value={currentPassword} 
          onChange={e=>setCurrentPassword(e.target.value)} 
        />
      </div>

      {/* New Password Fields */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">رمز عبور جدید</label>
          <input 
            placeholder="رمز عبور جدید را وارد کنید" 
            type="password" 
            className="w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-purple-500 focus:border-transparent" 
            value={newPassword} 
            onChange={e=>setNewPassword(e.target.value)} 
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">تکرار رمز عبور جدید</label>
          <input 
            placeholder="رمز عبور جدید را مجدداً وارد کنید" 
            type="password" 
            className="w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-purple-500 focus:border-transparent" 
            value={confirmPassword} 
            onChange={e=>setConfirmPassword(e.target.value)} 
          />
        </div>
      </div>

      {/* Message Display */}
      {msg && (
        <div className={`text-sm p-3 rounded-lg ${msg.includes('خطا') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
          {msg}
        </div>
      )}

      {/* Submit Button */}
      <div className="flex justify-end pt-4">
        <button 
          onClick={changePass} 
          disabled={busy} 
          className="px-6 py-3 rounded-xl border border-gray-300 hover:bg-gray-50 disabled:opacity-50 transition-colors"
        >
          {busy ? "در حال تغییر..." : "تغییر رمز عبور"}
        </button>
      </div>
    </Card>
  );
}
