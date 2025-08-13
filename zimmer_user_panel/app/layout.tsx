import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Zimmer AI - پنل کاربری',
  description: 'پنل کاربری اتوماسیون هوشمند Zimmer AI',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fa" dir="rtl">
      <body className="font-vazir bg-gray-50">
        {children}
      </body>
    </html>
  )
} 