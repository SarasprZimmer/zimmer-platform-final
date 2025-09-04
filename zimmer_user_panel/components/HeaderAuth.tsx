"use client";
import { useEffect, useState } from "react";
import { me, logout } from "@/lib/apiClient";
import { setAccessToken } from "@/lib/authClient";

export default function HeaderAuth() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    (async () => {
      const u = await me();
      setUser(u);
    })();
  }, []);

  if (!user) return <div className="text-sm opacity-70">کاربر مهمان</div>;
  return (
    <div className="flex items-center gap-3">
      <div className="text-sm">{user.name}</div>
      <button onClick={async()=>{ await logout(); setAccessToken(null); location.href="/login"; }} className="text-sm underline">خروج</button>
    </div>
  );
}
