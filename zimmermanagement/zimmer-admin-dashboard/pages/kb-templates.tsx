import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../lib/api';

interface Automation {
  id: number;
  name: string;
  description: string;
}

interface KBTemplate {
  id: number;
  automation_id: number;
  automation_name: string;
  category: string | null;
  question: string;
  answer: string;
  created_at: string;
  updated_at: string;
}

interface KBTemplateForm {
  automation_id: number;
  category: string;
  question: string;
  answer: string;
}

const KBTemplatesPage = () => {
  const [templates, setTemplates] = useState<KBTemplate[]>([]);
  const [automations, setAutomations] = useState<Automation[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<KBTemplate | null>(null);
  const [formData, setFormData] = useState<KBTemplateForm>({
    automation_id: 0,
    category: '',
    question: '',
    answer: ''
  });
  const [selectedAutomation, setSelectedAutomation] = useState<number | ''>('');
  const [submitting, setSubmitting] = useState(false);
  const [notification, setNotification] = useState<{type: 'success' | 'error', message: string} | null>(null);

  // Load templates and automations
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [templatesRes, automationsRes] = await Promise.all([
        api.get('/admin/kb-templates'),
        api.get('/admin/automations')
      ]);
      
      setTemplates(templatesRes.data.templates);
      setAutomations(automationsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
      setNotification({type: 'error', message: 'خطا در بارگذاری اطلاعات'});
    } finally {
      setLoading(false);
    }
  };

  // Filter templates by selected automation
  const filteredTemplates = selectedAutomation 
    ? templates.filter(t => t.automation_id === selectedAutomation)
    : templates;

  const resetForm = () => {
    setFormData({
      automation_id: 0,
      category: '',
      question: '',
      answer: ''
    });
    setEditingTemplate(null);
  };

  const openModal = (template?: KBTemplate) => {
    if (template) {
      setEditingTemplate(template);
      setFormData({
        automation_id: template.automation_id,
        category: template.category || '',
        question: template.question,
        answer: template.answer
      });
    } else {
      resetForm();
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    resetForm();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.automation_id || !formData.question || !formData.answer) {
      setNotification({type: 'error', message: 'لطفاً تمام فیلدهای اجباری را پر کنید'});
      return;
    }

    try {
      setSubmitting(true);
      
      if (editingTemplate) {
        await api.put(`/admin/kb-templates/${editingTemplate.id}`, formData);
        setNotification({type: 'success', message: 'قالب با موفقیت ویرایش شد'});
      } else {
        await api.post('/admin/kb-templates', formData);
        setNotification({type: 'success', message: 'قالب جدید با موفقیت ایجاد شد'});
      }
      
      closeModal();
      loadData();
    } catch (error) {
      console.error('Error saving template:', error);
      setNotification({type: 'error', message: 'خطا در ذخیره قالب'});
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (templateId: number) => {
    if (!confirm('آیا از حذف این قالب اطمینان دارید؟')) {
      return;
    }

    try {
      await api.delete(`/admin/kb-templates/${templateId}`);
      setNotification({type: 'success', message: 'قالب با موفقیت حذف شد'});
      loadData();
    } catch (error) {
      console.error('Error deleting template:', error);
      setNotification({type: 'error', message: 'خطا در حذف قالب'});
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fa-IR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <Layout title="قالب‌های پایگاه دانش">
        <div className="flex justify-center items-center h-64">
          <div className="text-lg">در حال بارگذاری...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="قالب‌های پایگاه دانش">
      <div className="p-6">
        {/* Notification */}
        {notification && (
          <div className={`mb-4 p-4 rounded-lg ${
            notification.type === 'success' 
              ? 'bg-green-100 text-green-800 border border-green-200' 
              : 'bg-red-100 text-red-800 border border-red-200'
          }`}>
            <div className="flex justify-between items-center">
              <span>{notification.message}</span>
              <button
                onClick={() => setNotification(null)}
                className="text-lg font-bold hover:opacity-70"
              >
                ×
              </button>
            </div>
          </div>
        )}
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">مدیریت قالب‌های پایگاه دانش</h1>
          <button
            onClick={() => openModal()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            افزودن قالب جدید
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow-sm mb-6">
          <div className="flex items-center space-x-4 space-x-reverse">
            <label className="text-sm font-medium text-gray-700">فیلتر اتوماسیون:</label>
            <select
              value={selectedAutomation}
              onChange={(e) => setSelectedAutomation(e.target.value ? Number(e.target.value) : '')}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">همه اتوماسیون‌ها</option>
              {automations.map((automation) => (
                <option key={automation.id} value={automation.id}>
                  {automation.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    دسته‌بندی
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    پرسش
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    پاسخ
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    اتوماسیون
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    تاریخ ایجاد
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    عملیات
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredTemplates.map((template) => (
                  <tr key={template.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {template.category || '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                      {template.question}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                      {template.answer}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {template.automation_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(template.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2 space-x-reverse">
                        <button
                          onClick={() => openModal(template)}
                          className="text-blue-600 hover:text-blue-900"
                          title="ویرایش"
                        >
                          ✏️
                        </button>
                        <button
                          onClick={() => handleDelete(template.id)}
                          className="text-red-600 hover:text-red-900"
                          title="حذف"
                        >
                          ❌
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {filteredTemplates.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              هیچ قالبی یافت نشد
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl mx-4">
            <h2 className="text-xl font-bold mb-4">
              {editingTemplate ? 'ویرایش قالب' : 'افزودن قالب جدید'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  اتوماسیون *
                </label>
                <select
                  value={formData.automation_id}
                  onChange={(e) => setFormData({...formData, automation_id: Number(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value={0}>انتخاب اتوماسیون</option>
                  {automations.map((automation) => (
                    <option key={automation.id} value={automation.id}>
                      {automation.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  دسته‌بندی
                </label>
                <input
                  type="text"
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="دسته‌بندی (اختیاری)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  پرسش *
                </label>
                <input
                  type="text"
                  value={formData.question}
                  onChange={(e) => setFormData({...formData, question: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="پرسش را وارد کنید"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  پاسخ *
                </label>
                <textarea
                  value={formData.answer}
                  onChange={(e) => setFormData({...formData, answer: e.target.value})}
                  rows={4}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="پاسخ را وارد کنید"
                  required
                />
              </div>

              <div className="flex justify-end space-x-3 space-x-reverse pt-4">
                <button
                  type="button"
                  onClick={closeModal}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  انصراف
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {submitting ? 'در حال ذخیره...' : (editingTemplate ? 'ویرایش' : 'ایجاد')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </Layout>
  );
};

export default KBTemplatesPage; 