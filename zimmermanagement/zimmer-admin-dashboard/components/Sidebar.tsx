import Link from 'next/link';
import { useRouter } from 'next/router';

const navigation = [
  { name: 'داشبورد', href: '/', icon: '📊' },
  { name: 'مشتریان', href: '/clients', icon: '👥' },
  { name: 'پایگاه دانش', href: '/knowledge', icon: '📚' },
  { name: 'قالب‌های پایگاه دانش', href: '/kb-templates', icon: '📑' },
  { name: 'مانیتورینگ پایگاه دانش', href: '/kb-monitoring', icon: '📊' },
  { name: 'پشتیبان‌گیری', href: '/backups', icon: '📦' },
  { name: 'تیکت‌های پشتیبانی', href: '/tickets', icon: '🎫' },
  { name: 'اتوماسیون‌ها', href: '/automations', icon: '🤖' },
  { name: 'استفاده از توکن', href: '/usage', icon: '🔢' },
  { name: 'پرداخت‌ها', href: '/payments', icon: '💳' },
  { name: 'لاگ‌های خطا', href: '/fallbacks', icon: '⚠️' },
];

const Sidebar = () => {
  const router = useRouter();

  return (
    <div className="w-64 bg-gray-50 border-l border-gray-200 min-h-screen">
      <div className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">پنل مدیریت</h2>
        
        <nav className="space-y-2">
          {navigation.map((item) => {
            const isActive = router.pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-100 text-blue-700 border-l-2 border-blue-600'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar; 