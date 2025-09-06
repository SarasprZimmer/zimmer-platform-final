"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Card } from "@/components/ui/Kit";
import { useAuth } from "@/contexts/AuthContext";

export default function ProfileForm(){
  const { user } = useAuth();
  const [me,setMe]=useState<any|null>(null);
  const [name,setName]=useState(""); 
  const [phone,setPhone]=useState("");
  const [msg,setMsg]=useState<string|null>(null);
  const [busy,setBusy]=useState(false);
  const [loading,setLoading]=useState(true);

  useEffect(()=>{
    if (user) {
      // Use user data from AuthContext (limited fields available)
      setMe(user);
      setName(user.name || "");
      setPhone(""); // Phone not available in AuthContext, will be fetched from API
      setLoading(false);
      
      // Also fetch full profile data from API to get phone_number
      (async()=>{
        try {
          const r = await apiFetch("/api/me");
          if(r.ok){
            const j = await r.json();
            setMe(j); // Update with full profile data
            setName(j?.name || "");
            setPhone(j?.phone_number || ""); // Now we can get phone from API
          }
        } catch (error) {
          console.error("Error fetching full profile data:", error);
        }
      })();
    } else {
      // Fallback: try to fetch from API
      (async()=>{
        try {
          const r = await apiFetch("/api/me");
          if(r.ok){
            const j = await r.json();
            setMe(j);
            setName(j?.name || "");
            setPhone(j?.phone_number || ""); // Only set if phone_number exists
          } else {
            console.log("Failed to fetch user data:", r.status);
            // Set fallback data for testing
            setMe({ email: "user@example.com" });
            setName("");
            setPhone(""); // Keep phone empty
          }
        } catch (error) {
          console.error("Error fetching user data:", error);
          // Set fallback data for testing
          setMe({ email: "user@example.com" });
          setName("");
          setPhone(""); // Keep phone empty
        } finally {
          setLoading(false);
        }
      })();
    }
  },[user]);

  async function saveProfile(){
    setMsg(null); setBusy(true);
    try{
      const r = await apiFetch("/api/user/profile",{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ 
          name, 
          phone_number: phone
          // Note: email is not supported by backend API
        })
      });
      setMsg(r.ok ? "تغییرات ذخیره شد." : "خطا در ذخیره‌سازی");
    } finally { setBusy(false); }
  }

  if (loading) {
    return (
      <Card className="max-w-xl space-y-3" dir="rtl">
        <div className="text-lg font-semibold">پروفایل</div>
        <div className="text-sm text-gray-500">در حال بارگذاری...</div>
      </Card>
    );
  }

  return (
    <Card className="w-full space-y-6" dir="rtl">
      <div className="text-lg font-semibold">پروفایل</div>
      
      {/* Name Field - Full Width */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">نام و نام خانوادگی</label>
        <input 
          className="w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-purple-500 focus:border-transparent" 
          value={name} 
          onChange={e=>setName(e.target.value)}
          placeholder="نام و نام خانوادگی خود را وارد کنید"
        />
      </div>

      {/* Phone Field - Full Width */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">شماره تماس</label>
        <input 
          className="w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-purple-500 focus:border-transparent" 
          value={phone} 
          onChange={e=>setPhone(e.target.value)}
          placeholder="شماره تماس خود را وارد کنید"
          type="tel"
        />
      </div>

      {/* Email Field - Full Width, Read-only */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">ایمیل</label>
        <input 
          className="w-full border border-gray-300 rounded-xl p-3 bg-gray-50 text-gray-600" 
          value={me?.email || ""} 
          disabled 
          placeholder="ایمیل شما"
          type="email"
        />
        <p className="text-xs text-gray-500">ایمیل قابل تغییر نیست</p>
      </div>

      {/* Message Display */}
      {msg && (
        <div className={`text-sm p-3 rounded-lg ${msg.includes('خطا') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
          {msg}
        </div>
      )}

      {/* Save Button */}
      <div className="flex justify-end pt-4">
        <button 
          onClick={saveProfile} 
          disabled={busy} 
          className="px-6 py-3 rounded-xl bg-black text-white disabled:opacity-50 hover:bg-gray-800 transition-colors"
        >
          {busy ? "در حال ذخیره..." : "ذخیره تغییرات"}
        </button>
      </div>
    </Card>
  );
}
