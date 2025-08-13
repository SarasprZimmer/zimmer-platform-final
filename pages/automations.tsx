import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { authenticatedFetch } from '../lib/auth';
import { useAuth } from '../contexts/AuthContext';

interface Automation {
  id: number;
  name: string;
  description: string;
  pricing_type: 'token_per_session' | 'token_per_step' | 'flat_fee';
  price_per_token: number;
  status: boolean;
  api_base_url?: string;
  api_provision_url?: string;
  api_usage_url?: string;
  api_kb_status_url?: string;
  api_kb_reset_url?: string;
  created_at: string;
  updated_at: string;
}

interface AutomationFormData {
  name: string;
  description: string;
  pricing_type: 'token_per_session' | 'token_per_step' | 'flat_fee';
  price_per_token: number;
  status: boolean;
  api_base_url: string;
  api_provision_url: string;
  api_usage_url: string;
  api_kb_status_url: string;
  api_kb_reset_url: string;
}

interface IntegrationData {
  id: number;
  name: string;
  api_base_url?: string;
  api_provision_url?: string;
  api_usage_url?: string;
  api_kb_status_url?: string;
  api_kb_reset_url?: string;
  service_token_masked?: string;
  has_service_token: boolean;
}

interface TokenRotationResponse {
  automation_id: number;
  new_token: string;
  masked_token: string;
  rotated_at: string;
  message: string;
}

const pricingTypeLabels = {
  token_per_session: 'توکن به ازای هر جلسه',
  token_per_step: 'توکن به ازای هر مرحله',
  flat_fee: 'هزینه ثابت'
};

export default function Automations() {
  const [automations, setAutomations] = useState<Automation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showIntegrationPanel, setShowIntegrationPanel] = useState(false);
  const [showTokenDialog, setShowTokenDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [editingAutomation, setEditingAutomation] = useState<Automation | null>(null);
  const [selectedAutomation, setSelectedAutomation] = useState<Automation | null>(null);
  const [integrationData, setIntegrationData] = useState<IntegrationData | null>(null);
  const [newToken, setNewToken] = useState<string>('');
  const [deleteTarget, setDeleteTarget] = useState<Automation | null>(null);
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [rotatingToken, setRotatingToken] = useState(false);
  const { user } = useAuth();

  const [formData, setFormData] = useState<AutomationFormData>({
    name: '',
    description: '',
    pricing_type: 'token_per_session',
    price_per_token: 0,
    status: true,
    api_base_url: '',
    api_provision_url: '',
    api_usage_url: '',
    api_kb_status_url: '',
    api_kb_reset_url: ''
  });

  useEffect(() => {
    if (user) {
      fetchAutomations();
    }
  }, [user]);

  const fetchAutomations = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await authenticatedFetch('/api/admin/automations');
      
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`خطا در دریافت اتوماسیون‌ها: ${res.status} ${errorText}`);
      }
      
      const data = await res.json();
      setAutomations(data || []);
    } catch (err) {
      console.error('Error fetching automations:', err);
      setError('خطا در بارگذاری اتوماسیون‌ها.');
    } finally {
      setLoading(false);
    }
  };

  const fetchIntegrationData = async (automationId: number) => {
    try {
      const res = await authenticatedFetch(`/api/admin/automations/${automationId}/integration`);
      
      if (!res.ok) {
        throw new Error('خطا در دریافت اطلاعات اتصال');
      }
      
      const data = await res.json();
      setIntegrationData(data);
    } catch (err) {
      console.error('Error fetching integration data:', err);
      showToast('خطا در دریافت اطلاعات اتصال', 'error');
    }
  };

  const handleCreateAutomation = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      const res = await authenticatedFetch('/api/admin/automations', {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText);
      }
      
      setShowModal(false);
      resetForm();
      fetchAutomations();
      showToast('اتوماسیون با موفقیت ایجاد شد', 'success');
    } catch (err) {
      console.error('Error creating automation:', err);
      showToast('خطا در ایجاد اتوماسیون', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateAutomation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingAutomation) return;
    
    setSubmitting(true);
    
    try {
      const res = await authenticatedFetch(`/api/admin/automations/${editingAutomation.id}`, {
        method: 'PUT',
        body: JSON.stringify(formData),
      });
      
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText);
      }
      
      setShowModal(false);
      resetForm();
      fetchAutomations();
      showToast('اتوماسیون با موفقیت بروزرسانی شد', 'success');
    } catch (err) {
      console.error('Error updating automation:', err);
      showToast('خطا در بروزرسانی اتوماسیون', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRotateToken = async (automationId: number) => {
    setRotatingToken(true);
    
    try {
      const res = await authenticatedFetch(`/api/admin/automations/${automationId}/rotate-token`, {
        method: 'POST',
      });
      
      if (!res.ok) {
        throw new Error('خطا در چرخش توکن');
      }
      
      const data: TokenRotationResponse = await res.json();
      setNewToken(data.new_token);
      setShowTokenDialog(true);
      
      // Refresh integration data to show new masked token
      await fetchIntegrationData(automationId);
      
      showToast('توکن سرویس با موفقیت چرخانده شد', 'success');
    } catch (err) {
      console.error('Error rotating token:', err);
      showToast('خطا در چرخش توکن سرویس', 'error');
    } finally {
      setRotatingToken(false);
    }
  };

  const handleDeleteAutomation = async () => {
    if (!deleteTarget) return;
    
    try {
      const res = await authenticatedFetch(`/api/admin/automations/${deleteTarget.id}`, {
        method: 'DELETE',
      });
      
      if (!res.ok) {
        throw new Error('خطا در حذف اتوماسیون');
      }
      
      setShowDeleteDialog(false);
      setDeleteTarget(null);
      fetchAutomations();
      showToast('اتوماسیون با موفقیت حذف شد', 'success');
    } catch (err) {
      console.error('Error deleting automation:', err);
      showToast('خطا در حذف اتوماسیون', 'error');
    }
  };

  const openEditModal = (automation: Automation) => {
    setEditingAutomation(automation);
    setFormData({
      name: automation.name,
      description: automation.description,
      pricing_type: automation.pricing_type,
      price_per_token: automation.price_per_token,
      status: automation.status,
      api_base_url: automation.api_base_url || '',
      api_provision_url: automation.api_provision_url || '',
      api_usage_url: automation.api_usage_url || '',
      api_kb_status_url: automation.api_kb_status_url || '',
      api_kb_reset_url: automation.api_kb_reset_url || ''
    });
    setShowModal(true);
  };

  const openIntegrationPanel = async (automation: Automation) => {
    setSelectedAutomation(automation);
    await fetchIntegrationData(automation.id);
    setShowIntegrationPanel(true);
  };

  const openCreateModal = () => {
    setEditingAutomation(null);
    resetForm();
    setShowModal(true);
  };

  const openDeleteDialog = (automation: Automation) => {
    setDeleteTarget(automation);
    setShowDeleteDialog(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      pricing_type: 'token_per_session',
      price_per_token: 0,
      status: true,
      api_base_url: '',
      api_provision_url: '',
      api_usage_url: '',
      api_kb_status_url: '',
      api_kb_reset_url: ''
    });
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      showToast('توکن در کلیپ‌بورد کپی شد', 'success');
    } catch (err) {
      showToast('خطا در کپی کردن توکن', 'error');
    }
  };

  const showToast = (message: string, type: 'success' | 'error') => {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 left-4 z-50 px-4 py-2 rounded-md text-white ${
      type === 'success' ? 'bg-green-600' : 'bg-red-600'
    }`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 3000);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fa-IR');
  };

  const truncateUrl = (url: string, maxLength: number = 30) => {
    if (!url) return '-';
    return url.length > maxLength ? url.substring(0, maxLength) + '...' : url;
  };

  const filteredAutomations = automations.filter(automation => {
    const matchesStatus = statusFilter === 'all' || 
      (statusFilter === 'active' && automation.status) ||
      (statusFilter === 'inactive' && !automation.status);
    
    const matchesSearch = automation.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         automation.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesStatus && matchesSearch;
  });

  return (
    <Layout title="مدیریت اتوماسیون‌ها">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">مدیریت اتوماسیون‌ها</h2>
            <p className="text-gray-600 mt-2">مدیریت محصولات اتوماسیون زیمر</p>
          </div>
          <button
            onClick={openCreateModal}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            افزودن اتوماسیون جدید
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="جستجو بر اساس نام یا توضیحات..."
                className="w-full border-gray-300 rounded-md"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div>
              <select
                className="border-gray-300 rounded-md"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as 'all' | 'active' | 'inactive')}
              >
                <option value="all">همه وضعیت‌ها</option>
                <option value="active">فعال</option>
                <option value="inactive">غیرفعال</option>
              </select>
            </div>
          </div>
        </div>

        {/* Automations Table */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="mr-3 text-gray-600">در حال بارگذاری اتوماسیون‌ها...</span>
            </div>
          ) : error ? (
            <div className="text-center py-12 text-red-600">{error}</div>
          ) : filteredAutomations.length === 0 ? (
            <div className="text-center py-12 text-gray-500">اتوماسیونی یافت نشد.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نام</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">وضعیت</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">مدل قیمت‌گذاری</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Provision URL</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">KB Status URL</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">آخرین تغییر</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">عملیات</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredAutomations.map((automation, idx) => (
                    <tr key={automation.id} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{automation.name}</td>
                      <td className="px-4 py-2 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          automation.status 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {automation.status ? 'فعال' : 'غیرفعال'}
                        </span>
                      </td>
                      <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                        {pricingTypeLabels[automation.pricing_type]}
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900" title={automation.api_provision_url || ''}>
                        {truncateUrl(automation.api_provision_url || '')}
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900" title={automation.api_kb_status_url || ''}>
                        {truncateUrl(automation.api_kb_status_url || '')}
                      </td>
                      <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                        {formatDate(automation.updated_at)}
                      </td>
                      <td className="px-4 py-2 whitespace-nowrap text-sm font-medium space-x-2">
                        <button
                          onClick={() => openEditModal(automation)}
                          className="text-blue-600 hover:text-blue-900 ml-2"
                        >
                          ویرایش
                        </button>
                        <button
                          onClick={() => openIntegrationPanel(automation)}
                          className="text-green-600 hover:text-green-900 ml-2"
                        >
                          اتصال
                        </button>
                        <button
                          onClick={() => openDeleteDialog(automation)}
                          className="text-red-600 hover:text-red-900"
                        >
                          حذف
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Create/Edit Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {editingAutomation ? 'ویرایش اتوماسیون' : 'ایجاد اتوماسیون جدید'}
                  </h3>
                  <button
                    onClick={() => setShowModal(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                
                <form onSubmit={editingAutomation ? handleUpdateAutomation : handleCreateAutomation} className="space-y-4">
                  {/* اطلاعات عمومی */}
                  <div className="border-b border-gray-200 pb-4">
                    <h4 className="text-md font-medium text-gray-900 mb-3">اطلاعات عمومی</h4>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">نام اتوماسیون *</label>
                        <input
                          type="text"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.name}
                          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                          placeholder="نام اتوماسیون را وارد کنید"
                          required
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">وضعیت</label>
                        <select
                          className="w-full border-gray-300 rounded-md"
                          value={formData.status ? 'true' : 'false'}
                          onChange={(e) => setFormData({ ...formData, status: e.target.value === 'true' })}
                        >
                          <option value="true">فعال</option>
                          <option value="false">غیرفعال</option>
                        </select>
                      </div>
                    </div>
                    
                    <div className="mt-4">
                      <label className="block text-sm font-medium text-gray-700 mb-1">توضیحات</label>
                      <textarea
                        className="w-full border-gray-300 rounded-md min-h-[80px]"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="توضیحات اتوماسیون را وارد کنید"
                        required
                      />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">مدل قیمت‌گذاری *</label>
                        <select
                          className="w-full border-gray-300 rounded-md"
                          value={formData.pricing_type}
                          onChange={(e) => setFormData({ 
                            ...formData, 
                            pricing_type: e.target.value as 'token_per_session' | 'token_per_step' | 'flat_fee'
                          })}
                          required
                        >
                          <option value="token_per_session">توکن به ازای هر جلسه</option>
                          <option value="token_per_step">توکن به ازای هر مرحله</option>
                          <option value="flat_fee">هزینه ثابت</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">قیمت واحد</label>
                        <input
                          type="number"
                          step="0.01"
                          min="0"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.price_per_token}
                          onChange={(e) => setFormData({ ...formData, price_per_token: parseFloat(e.target.value) || 0 })}
                          placeholder="قیمت را وارد کنید"
                        />
                      </div>
                    </div>
                  </div>

                  {/* تنظیمات اتصال */}
                  <div>
                    <h4 className="text-md font-medium text-gray-900 mb-3">تنظیمات اتصال</h4>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">API Base URL (اختیاری)</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.api_base_url}
                          onChange={(e) => setFormData({ ...formData, api_base_url: e.target.value })}
                          placeholder="https://api.example.com"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Provision URL *</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.api_provision_url}
                          onChange={(e) => setFormData({ ...formData, api_provision_url: e.target.value })}
                          placeholder="https://api.example.com/provision"
                          required
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Usage URL (اختیاری)</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.api_usage_url}
                          onChange={(e) => setFormData({ ...formData, api_usage_url: e.target.value })}
                          placeholder="https://api.example.com/usage"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">KB Status URL *</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.api_kb_status_url}
                          onChange={(e) => setFormData({ ...formData, api_kb_status_url: e.target.value })}
                          placeholder="https://api.example.com/kb/status"
                          required
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">KB Reset URL (اختیاری)</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={formData.api_kb_reset_url}
                          onChange={(e) => setFormData({ ...formData, api_kb_reset_url: e.target.value })}
                          placeholder="https://api.example.com/kb/reset"
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex justify-end space-x-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowModal(false)}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                    >
                      لغو
                    </button>
                    <button
                      type="submit"
                      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                      disabled={submitting}
                    >
                      {submitting 
                        ? (editingAutomation ? 'در حال بروزرسانی...' : 'در حال ایجاد...') 
                        : (editingAutomation ? 'بروزرسانی' : 'ایجاد')
                      }
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}

        {/* Integration Panel */}
        {showIntegrationPanel && selectedAutomation && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    تنظیمات اتصال - {selectedAutomation.name}
                  </h3>
                  <button
                    onClick={() => setShowIntegrationPanel(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                
                {integrationData && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">API Base URL</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={integrationData.api_base_url || ''}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Provision URL</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={integrationData.api_provision_url || ''}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Usage URL</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={integrationData.api_usage_url || ''}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">KB Status URL</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={integrationData.api_kb_status_url || ''}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">KB Reset URL</label>
                        <input
                          type="url"
                          className="w-full border-gray-300 rounded-md"
                          value={integrationData.api_kb_reset_url || ''}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">وضعیت توکن سرویس</label>
                        <div className="flex items-center space-x-2">
                          <input
                            type="text"
                            className="w-full border-gray-300 rounded-md"
                            value={integrationData.service_token_masked || 'توکن تنظیم نشده'}
                            readOnly
                          />
                          <button
                            onClick={() => handleRotateToken(selectedAutomation.id)}
                            className="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700"
                            disabled={rotatingToken}
                          >
                            {rotatingToken ? 'در حال چرخش...' : 'چرخش توکن'}
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex justify-end pt-4">
                      <button
                        onClick={() => setShowIntegrationPanel(false)}
                        className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                      >
                        بستن
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Token Dialog */}
        {showTokenDialog && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-900">توکن سرویس جدید</h3>
                  <button
                    onClick={() => setShowTokenDialog(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                    <p className="text-yellow-800 text-sm">
                      ⚠️ این توکن فقط همین یک بار نمایش داده می‌شود. لطفاً آن را در سرویس اتوماسیون تنظیم کنید.
                    </p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">توکن جدید</label>
                    <div className="flex items-center space-x-2">
                      <input
                        type="text"
                        className="w-full border-gray-300 rounded-md font-mono text-sm"
                        value={newToken}
                        readOnly
                      />
                      <button
                        onClick={() => copyToClipboard(newToken)}
                        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                      >
                        کپی
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex justify-end pt-4">
                    <button
                      onClick={() => setShowTokenDialog(false)}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                    >
                      بستن
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Delete Confirmation Dialog */}
        {showDeleteDialog && deleteTarget && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-900">تایید حذف</h3>
                  <button
                    onClick={() => setShowDeleteDialog(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                
                <div className="space-y-4">
                  <p className="text-gray-700">
                    آیا از حذف اتوماسیون "{deleteTarget.name}" مطمئن هستید؟
                  </p>
                  <p className="text-sm text-red-600">
                    این عملیات قابل بازگشت نیست.
                  </p>
                  
                  <div className="flex justify-end space-x-3 pt-4">
                    <button
                      onClick={() => setShowDeleteDialog(false)}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                    >
                      لغو
                    </button>
                    <button
                      onClick={handleDeleteAutomation}
                      className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                    >
                      حذف
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}