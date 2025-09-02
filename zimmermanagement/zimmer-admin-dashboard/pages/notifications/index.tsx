import { useState } from "react";
import axios from "axios";
import Layout from "../../components/Layout";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL!;

export default function AdminNotificationsPage() {
  const [mode, setMode] = useState<"direct"|"broadcast">("direct");
  const [userIds, setUserIds] = useState<string>("");
  const [type, setType] = useState("system");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [role, setRole] = useState("");
  const [data, setData] = useState<string>("");

  const [submitting, setSubmitting] = useState(false);
  const [msg, setMsg] = useState<string>("");

  const loadTemplate = (template: string) => {
    switch (template) {
      case "maintenance":
        setType("system");
        setTitle("Scheduled Maintenance");
        setBody("System will be down for maintenance. We apologize for any inconvenience.");
        setData('{"maintenance_id":"maint_001","duration":"2 hours"}');
        break;
      case "update":
        setType("system");
        setTitle("System Update Available");
        setBody("New features have been deployed. Check out the latest improvements!");
        setData('{"version":"2.1.0","features":["notifications","improved-ui"]}');
        break;
      case "support":
        setType("ticket");
        setTitle("Support Ticket Updated");
        setBody("Your support ticket has received a new response.");
        setData('{"ticket_url":"/support/123"}');
        break;
      case "payment":
        setType("payment");
        setTitle("Payment Successful");
        setBody("Your payment has been processed successfully.");
        setData('{"payment_id":"pay_123","amount":100000}');
        break;
    }
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setSubmitting(true);
    setMsg("");
    try {
      if (mode === "direct") {
        const ids = userIds.split(",").map(s => s.trim()).filter(Boolean).map(Number);
        const payload: any = { user_ids: ids, type, title, body };
        if (data) payload.data = JSON.parse(data);
        const res = await axios.post(`${API_BASE}/api/admin/notifications`, payload, { withCredentials: true });
        setMsg(`Sent to ${res.data.created} user(s).`);
      } else {
        const payload: any = { type, title, body };
        if (role) payload.role = role;
        if (data) payload.data = JSON.parse(data);
        const res = await axios.post(`${API_BASE}/api/admin/notifications/broadcast`, payload, { withCredentials: true });
        setMsg(`Broadcast created for ${res.data.created} user(s).`);
      }
      setTitle(""); setBody(""); setUserIds(""); setData(""); setRole("");
    } catch (err: any) {
      setMsg(err?.response?.data?.detail || "Error sending notification");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Layout title="اعلان‌های داخلی">
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold">Internal Notifications</h1>

        <div className="bg-white rounded-2xl shadow-sm p-5 space-y-4">
        <div className="flex gap-3">
          <button className={`px-3 py-1 rounded-full ${mode==="direct"?"bg-purple-600 text-white":"bg-gray-100"}`} onClick={()=>setMode("direct")}>Send to Users</button>
          <button className={`px-3 py-1 rounded-full ${mode==="broadcast"?"bg-purple-600 text-white":"bg-gray-100"}`} onClick={()=>setMode("broadcast")}>Broadcast</button>
        </div>

        <div className="border-t pt-4">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Quick Templates</h3>
          <div className="flex flex-wrap gap-2">
            <button onClick={() => loadTemplate("maintenance")} className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200">Maintenance</button>
            <button onClick={() => loadTemplate("update")} className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full hover:bg-green-200">System Update</button>
            <button onClick={() => loadTemplate("support")} className="px-3 py-1 text-xs bg-orange-100 text-orange-700 rounded-full hover:bg-orange-200">Support Ticket</button>
            <button onClick={() => loadTemplate("payment")} className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200">Payment Success</button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4">
          {mode==="direct" && (
            <div>
              <label className="text-sm text-gray-700">User IDs (comma-separated)</label>
              <input className="mt-1 w-full border rounded-xl p-2" value={userIds} onChange={e=>setUserIds(e.target.value)} placeholder="e.g. 12, 45, 98" />
            </div>
          )}
          {mode==="broadcast" && (
            <div>
              <label className="text-sm text-gray-700">Role (optional)</label>
              <input className="mt-1 w-full border rounded-xl p-2" value={role} onChange={e=>setRole(e.target.value)} placeholder="manager | technical_team | support_staff" />
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-700">Type</label>
              <input className="mt-1 w-full border rounded-xl p-2" value={type} onChange={e=>setType(e.target.value)} placeholder="system | payment | ticket | automation" />
            </div>
            <div>
              <label className="text-sm text-gray-700">Title</label>
              <input className="mt-1 w-full border rounded-xl p-2" value={title} onChange={e=>setTitle(e.target.value)} required />
            </div>
          </div>

          <div>
            <label className="text-sm text-gray-700">Body</label>
            <textarea className="mt-1 w-full border rounded-xl p-2 h-28" value={body} onChange={e=>setBody(e.target.value)} />
          </div>

          <div>
            <label className="text-sm text-gray-700">Data (JSON, optional)</label>
            <textarea className="mt-1 w-full border rounded-xl p-2 h-24" placeholder='{"deep_link":"/support/123"}' value={data} onChange={e=>setData(e.target.value)} />
          </div>

          <div className="flex items-center gap-3">
            <button disabled={submitting} className="px-4 py-2 rounded-xl bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50">Send</button>
            {msg && <span className="text-sm text-gray-700">{msg}</span>}
          </div>
        </form>
        </div>
      </div>
    </Layout>
  );
}
