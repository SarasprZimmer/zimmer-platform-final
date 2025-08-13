import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import PaymentTable from '../components/PaymentTable';
import { authenticatedFetch } from '../lib/auth';
import { useAuth } from '../contexts/AuthContext';

interface PaymentRecord {
  id: number;
  user_name: string;
  amount: number;
  tokens_purchased: number;
  date: string;
  method: string;
  status: string;
  transaction_id: string;
}

export default function Payments() {
  const [payments, setPayments] = useState<PaymentRecord[]>([]);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [totalTokens, setTotalTokens] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    if (user) fetchPayments();
    // eslint-disable-next-line
  }, [user]);

  const fetchPayments = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!user) return;
      const response = await authenticatedFetch(`/api/admin/payments`);
      
      if (response.status === 404) {
        setError('Payment tracking is not yet implemented on the backend. Please contact your administrator.');
        setPayments([]);
        setTotalAmount(0);
        setTotalTokens(0);
        return;
      }
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      // Sort by newest first
      const sorted = Array.isArray(data.payments) ? data.payments.sort((a: PaymentRecord, b: PaymentRecord) => new Date(b.date).getTime() - new Date(a.date).getTime()) : [];
      setPayments(sorted);
      setTotalAmount(typeof data.total_amount === 'number' ? data.total_amount : 0);
      setTotalTokens(typeof data.total_tokens === 'number' ? data.total_tokens : 0);
    } catch (err) {
      setError('Failed to load payment data.');
      setPayments([]); // Defensive: set to empty array on error
      setTotalAmount(0);
      setTotalTokens(0);
    } finally {
      setLoading(false);
    }
  };

  function formatCurrency(amount: number) {
    return amount.toLocaleString('fa-IR') + ' IRR';
  }

  return (
    <Layout title="Payments">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Payment Management</h2>
          <p className="text-gray-600 mt-2">Track revenue and payment history</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">Payment History</h3>
            <div className="flex flex-col sm:flex-row sm:items-center gap-2">
              <span className="text-sm text-gray-500">Total Amount: <span className="font-semibold text-blue-600">{formatCurrency(totalAmount)}</span></span>
              <span className="text-sm text-gray-500">Total Tokens: <span className="font-semibold text-blue-600">{totalTokens}</span></span>
            </div>
            <button
              onClick={fetchPayments}
              className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Refresh
            </button>
          </div>
          <div className="p-6">
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="ml-3 text-gray-600">Loading payments...</span>
              </div>
            ) : error ? (
              <div className="text-center py-12">
                <div className="text-red-600 mb-4">
                  <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Payments</h3>
                <p className="text-gray-600 mb-4">{error}</p>
                <button
                  onClick={fetchPayments}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Try Again
                </button>
              </div>
            ) : (
              <PaymentTable records={payments} />
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
} 