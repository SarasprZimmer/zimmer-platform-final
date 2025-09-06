export function Card({ children, className="", ...props }: { children: React.ReactNode; className?: string } & React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`rounded-2xl border bg-white p-4 ${className}`} {...props}>{children}</div>;
}
