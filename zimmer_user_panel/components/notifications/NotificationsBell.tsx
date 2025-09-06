"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { apiFetch } from "@/lib/apiClient";
import { Notify, routeForNotification } from "@/lib/notifications";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";

export default function NotificationsBell(){
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Notify[] | null>(null);
  const [unread, setUnread] = useState<number>(0);
  const [busy, setBusy] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  async function load(initial=false){
    try{
      const r = await apiFetch("/api/notifications?limit=20&offset=0");
      if (!r.ok) throw new Error();
      const j = await r.json();
      const arr: Notify[] = Array.isArray(j) ? j : (j.items || []);
      setItems(arr);
      setUnread(arr.filter(x => !x.read).length);
      if (initial && arr.length === 0) {
        // try unread-count if available
        try {
          const c = await apiFetch("/api/notifications/unread-count");
          if (c.ok) {
            const cj = await c.json();
            if (typeof cj?.count === "number") setUnread(cj.count);
          }
        } catch {}
      }
    } catch {
      setItems([]);
    }
  }

  async function markAll(){
    setBusy(true);
    try{
      await apiFetch("/api/notifications/mark-all-read", { method:"POST" });
      await load();
    } finally { setBusy(false); }
  }

  async function markOne(id: number){
    setBusy(true);
    try{
      await apiFetch("/api/notifications/mark-read", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ ids:[id] })
      });
      await load();
    } finally { setBusy(false); }
  }

  // Live updates via SSE (if available), fallback to polling
  useEffect(()=>{
    let closed = false;
    load(true);

    // Try SSE
    const API = process.env.NEXT_PUBLIC_API_BASE_URL || "";
    let es: EventSource | null = null;
    if (typeof window !== "undefined" && API) {
      try{
        // We attach credentials via same-origin cookies; if CORS needed, adjust backend headers.
        es = new EventSource(`${API.replace(/\/+$/,"")}/api/notifications/stream`, { withCredentials: true } as any);
        es.onmessage = (ev) => {
          if (closed) return;
          try{
            const data = JSON.parse(ev.data);
            // Prepend new notification
            setItems(prev => {
              const next = [data as Notify, ...(prev || [])].slice(0, 20);
              return next;
            });
            setUnread(u => u + 1);
          } catch {}
        };
        es.onerror = () => { /* silently ignore, fallback polling handles */ };
      } catch {}
    }

    // Polling fallback (and also acts as backup refresher)
    const poll = setInterval(()=>{ load(false) }, 30000);

    // click outside to close
    const onDocClick = (e: MouseEvent) => {
      if (!dropdownRef.current) return;
      if (!dropdownRef.current.contains(e.target as any)) setOpen(false);
    };
    document.addEventListener("click", onDocClick);

    return () => {
      closed = true;
      clearInterval(poll);
      document.removeEventListener("click", onDocClick);
      try{ es?.close(); } catch {}
    };
  },[]);

  const unreadBadge = useMemo(()=> unread > 99 ? "99+" : String(unread || ""), [unread]);

  return (
    <div className="relative" ref={dropdownRef} dir="rtl">
      <button
        onClick={()=>setOpen(o=>!o)}
        className="relative rounded-full p-2 hover:bg-gray-100"
        aria-label="اعلان‌ها"
      >
        {/* bell icon */}
        <svg width="22" height="22" viewBox="0 0 24 24" className="fill-current"><path d="M12 2a6 6 0 00-6 6v2.586l-.707.707A1 1 0 006 14h12a1 1 0 00.707-1.707L18 10.586V8a6 6 0 00-6-6zm0 20a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
        {unread > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 rounded-full bg-red-600 text-white text-[10px] flex items-center justify-center">
            {unreadBadge}
          </span>
        )}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{ duration: 0.15 }}
            className="absolute left-0 mt-2 w-[360px] max-h-[70vh] overflow-auto rounded-2xl border bg-white shadow-lg z-50"
          >
            <div className="p-3 border-b flex items-center justify-between">
              <div className="font-medium">اعلان‌ها</div>
              <button className="text-sm underline disabled:opacity-50" onClick={markAll} disabled={busy || unread===0}>علامت‌گذاری همه</button>
            </div>
            <ul className="p-2 space-y-2">
              {items === null && (
                <>
                  <li className="h-12 animate-pulse bg-gray-100 rounded-xl" />
                  <li className="h-12 animate-pulse bg-gray-100 rounded-xl" />
                </>
              )}
              {items && items.length === 0 && (
                <li className="text-sm opacity-70 p-3">اعلانی وجود ندارد.</li>
              )}
              {items && items.map(n => (
                <li key={n.id} className={`rounded-xl border p-3 ${n.read ? "opacity-70" : ""}`}>
                  <div className="flex items-start gap-3">
                    <TypeBadge type={n.type} />
                    <div className="min-w-0 flex-1">
                      <div className="font-medium truncate">{n.title}</div>
                      {n.body && <div className="text-xs opacity-80 line-clamp-2">{n.body}</div>}
                      <div className="mt-2 flex items-center gap-2">
                        <Link href={routeForNotification(n)} className="text-xs underline">مشاهده</Link>
                        {!n.read && (
                          <button className="text-xs underline" onClick={()=>markOne(n.id)} disabled={busy}>خواندم</button>
                        )}
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
            <div className="p-2 border-t">
              <Link href="/notifications" className="block text-center text-sm underline">مشاهده همه اعلان‌ها</Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function TypeBadge({ type }: { type?: string }){
  const t = (type || "").toLowerCase();
  const label = t === "payment" ? "پرداخت" : t === "ticket" ? "تیکت" : t === "automation" ? "اتوماسیون" : "سیستمی";
  const color = t === "payment" ? "bg-emerald-100 text-emerald-800" :
                t === "ticket" ? "bg-blue-100 text-blue-800" :
                t === "automation" ? "bg-purple-100 text-purple-800" :
                "bg-gray-100 text-gray-800";
  return <span className={`text-[11px] px-2 py-0.5 rounded-full ${color}`}>{label}</span>;
}
