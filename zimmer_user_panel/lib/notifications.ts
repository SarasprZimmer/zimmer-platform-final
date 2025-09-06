export type Notify = {
  id: number;
  type: "admin" | "ticket" | "payment" | "automation" | string;
  title: string;
  body?: string;
  data?: any;
  read: boolean;
  created_at: string;
};

export function routeForNotification(n: Notify): string {
  const d = n.data || {};
  switch ((n.type || "").toLowerCase()) {
    case "payment":
      if (d.payment_id) return `/payment/receipt?id=${encodeURIComponent(d.payment_id)}`;
      return "/payment";
    case "ticket":
      if (d.ticket_id) return `/support/tickets/${encodeURIComponent(d.ticket_id)}`;
      return "/support/tickets";
    case "automation":
      if (d.automation_id) return `/automations/${encodeURIComponent(d.automation_id)}`;
      return "/automations";
    case "admin":
    default:
      return "/notifications";
  }
}
