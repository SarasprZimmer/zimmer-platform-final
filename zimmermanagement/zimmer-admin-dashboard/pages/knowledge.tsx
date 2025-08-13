import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import KnowledgeForm from '../components/KnowledgeForm';
import KnowledgeTable from '../components/KnowledgeTable';
import { authenticatedFetch } from '../lib/auth';
import { useAuth } from '../contexts/AuthContext';

interface Client {
  id: number;
  name: string;
}

interface KnowledgeEntry {
  id: number;
  client_id: number;
  client_name: string;
  category: string;
  answer: string;
  created_at: string;
}

export default function Knowledge() {
  const [clients, setClients] = useState<Client[]>([]);
  const [entries, setEntries] = useState<KnowledgeEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterClient, setFilterClient] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      console.log('User authenticated, fetching data...');
      fetchClients();
      fetchEntries();
    } else {
      console.log('No user found, skipping data fetch');
    }
    // eslint-disable-next-line
  }, [user]);

  const fetchClients = async () => {
    try {
      console.log('Fetching clients...');
      const res = await authenticatedFetch('/api/admin/users');
      console.log('Clients response status:', res.status);
      
      if (res.status === 404) {
        console.log('Clients endpoint not implemented, using empty list');
        setClients([]);
        return;
      }
      
      if (!res.ok) {
        const errorText = await res.text();
        console.error('Clients API Error:', errorText);
        throw new Error(`Failed to fetch clients: ${res.status} ${errorText}`);
      }
      
      const data = await res.json();
      console.log('Clients data received:', data);
      setClients(Array.isArray(data.users) ? data.users : []);
    } catch (err) {
      console.error('Error fetching clients:', err);
      setClients([]); // Defensive: set to empty array on error
    }
  };

  const fetchEntries = async () => {
    setLoading(true);
    setError('');
    try {
      const params: any = {};
      if (filterClient) params.client_id = filterClient;
      if (filterCategory) params.category = filterCategory;
      // Build query string
      const query = new URLSearchParams(params).toString();
      const url = '/api/admin/knowledge' + (query ? `?${query}` : '');
      console.log('Fetching knowledge entries from:', url);
      
      const res = await authenticatedFetch(url);
      console.log('Response status:', res.status);
      
      if (!res.ok) {
        const errorText = await res.text();
        console.error('API Error:', errorText);
        throw new Error(`Failed to fetch knowledge entries: ${res.status} ${errorText}`);
      }
      
      const data = await res.json();
      console.log('Knowledge data received:', data);
      
      // Map client_id to client_name
      const clientMap: Record<number, string> = {};
      clients.forEach(c => { clientMap[c.id] = c.name; });
      
      const mapped = data.knowledge_entries.map((k: any) => ({
        ...k,
        client_name: k.client_name || clientMap[k.client_id] || `Client ${k.client_id}`,
      }));
      console.log('Mapped entries:', mapped);
      setEntries(mapped);
    } catch (err) {
      console.error('Error fetching knowledge entries:', err);
      setError('Failed to load knowledge entries.');
    } finally {
      setLoading(false);
    }
  };

  // Refresh entries after add
  const handleAdd = () => {
    fetchEntries();
  };

  // Filter handlers
  const handleClientFilter = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilterClient(e.target.value);
  };
  const handleCategoryFilter = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilterCategory(e.target.value);
  };
  useEffect(() => {
    fetchEntries();
    // eslint-disable-next-line
  }, [filterClient, filterCategory]);

  return (
    <Layout title="Knowledge Base">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Knowledge Base</h2>
          <p className="text-gray-600 mt-2">Manage client-specific knowledge entries</p>
        </div>
        <KnowledgeForm onAdd={handleAdd} />
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
            <div className="flex gap-2 items-center">
              <label className="text-sm text-gray-700">Filter by Client:</label>
              <select
                className="border-gray-300 rounded-md"
                value={filterClient}
                onChange={handleClientFilter}
              >
                <option value="">All</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>{client.name}</option>
                ))}
              </select>
            </div>
            <div className="flex gap-2 items-center">
              <label className="text-sm text-gray-700">Search Category:</label>
              <input
                type="text"
                className="border-gray-300 rounded-md"
                value={filterCategory}
                onChange={handleCategoryFilter}
                placeholder="e.g. visa, pricing"
              />
            </div>
          </div>
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-gray-600">Loading knowledge entries...</span>
            </div>
          ) : error ? (
            <div className="text-center py-12 text-red-600">{error}</div>
          ) : (
            <KnowledgeTable entries={entries} />
          )}
        </div>
      </div>
    </Layout>
  );
} 