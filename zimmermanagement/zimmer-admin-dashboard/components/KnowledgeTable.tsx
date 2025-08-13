import React, { useState } from 'react';

interface KnowledgeEntry {
  id: number;
  client_name: string;
  category: string;
  answer: string;
  created_at: string;
}

interface KnowledgeTableProps {
  entries: KnowledgeEntry[];
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

const MAX_ANSWER_LENGTH = 60;

const KnowledgeTable: React.FC<KnowledgeTableProps> = ({ entries }) => {
  const [expanded, setExpanded] = useState<{ [id: number]: boolean }>({});

  const toggleExpand = (id: number) => {
    setExpanded(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Client</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Answer</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created At</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {entries.length === 0 ? (
            <tr>
              <td colSpan={4} className="px-4 py-4 text-center text-gray-400">No knowledge entries found.</td>
            </tr>
          ) : (
            entries.map((entry, idx) => (
              <tr key={entry.id} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-4 py-2 whitespace-nowrap">{entry.client_name}</td>
                <td className="px-4 py-2 whitespace-nowrap">{entry.category}</td>
                <td className="px-4 py-2 whitespace-pre-line max-w-xs">
                  {entry.answer.length > MAX_ANSWER_LENGTH && !expanded[entry.id] ? (
                    <>
                      {entry.answer.slice(0, MAX_ANSWER_LENGTH)}...
                      <button className="ml-2 text-blue-600 text-xs underline" onClick={() => toggleExpand(entry.id)}>
                        Show more
                      </button>
                    </>
                  ) : entry.answer.length > MAX_ANSWER_LENGTH && expanded[entry.id] ? (
                    <>
                      {entry.answer}
                      <button className="ml-2 text-blue-600 text-xs underline" onClick={() => toggleExpand(entry.id)}>
                        Show less
                      </button>
                    </>
                  ) : (
                    entry.answer
                  )}
                </td>
                <td className="px-4 py-2 whitespace-nowrap">{formatDate(entry.created_at)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default KnowledgeTable; 