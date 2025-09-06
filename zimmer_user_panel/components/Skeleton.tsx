export function Skeleton({ className="" }: { className?: string }) {
  return <div className={`animate-pulse bg-gray-200/70 rounded-xl ${className}`} />;
}

export function Card({ children, className="" }: { children: React.ReactNode; className?: string }) {
  return <div className={`rounded-2xl border bg-white p-4 ${className}`}>{children}</div>;
}
