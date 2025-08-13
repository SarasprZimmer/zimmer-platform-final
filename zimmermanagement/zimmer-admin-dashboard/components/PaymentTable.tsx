import React from 'react';

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

interface PaymentTableProps {
  records: PaymentRecord[];
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function formatCurrency(amount: number) {
  // Assuming IRR for now
  return amount.toLocaleString('fa-IR') + ' IRR';
}

function statusBadge(status: string) {
  let color = 'bg-gray-200 text-gray-700';
  if (status === 'completed') color = 'bg-green-100 text-green-800';
  else if (status === 'pending') color = 'bg-yellow-100 text-yellow-800';
  else if (status === 'failed') color = 'bg-red-100 text-red-800';
  return (
    <span className={`px-2 py-1 rounded text-xs font-semibold ${color}`}>{status.charAt(0).toUpperCase() + status.slice(1)}</span>
  );
}

const PaymentTable: React.FC<PaymentTableProps> = ({ records }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
            <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Tokens</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transaction ID</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {records.length === 0 ? (
            <tr>
              <td colSpan={7} className="px-4 py-4 text-center text-gray-400">No payments found.</td>
            </tr>
          ) : (
            records.map((record, idx) => (
              <tr key={record.id} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-4 py-2 whitespace-nowrap">{formatDate(record.date)}</td>
                <td className="px-4 py-2 whitespace-nowrap">{record.user_name}</td>
                <td className="px-4 py-2 whitespace-nowrap text-right">{formatCurrency(record.amount)}</td>
                <td className="px-4 py-2 whitespace-nowrap text-right">{record.tokens_purchased}</td>
                <td className="px-4 py-2 whitespace-nowrap">{record.method}</td>
                <td className="px-4 py-2 whitespace-nowrap">{statusBadge(record.status)}</td>
                <td className="px-4 py-2 whitespace-nowrap">{record.transaction_id}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default PaymentTable; 