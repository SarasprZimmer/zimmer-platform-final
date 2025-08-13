import { redirect } from 'next/navigation'
import { cookies } from 'next/headers'
import { verifyToken } from '@/lib/auth-server'

export default async function HomePage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;
  
  if (!token) {
    redirect('/login')
  }

  const tokenData = await verifyToken(token)
  
  if (!tokenData || tokenData.exp * 1000 < Date.now()) {
    redirect('/login')
  }

  redirect('/dashboard')
} 