import React, { useEffect, useState } from 'react';
import { getLeads, scrapeLeads } from './api';
import LeadTable from './components/LeadTable';
import SettingsModal from './components/SettingsModal';

function App() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);

  const fetchLeads = async () => {
    setLoading(true);
    const data = await getLeads();
    setLeads(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const handleScrape = async () => {
    setScraping(true);
    await scrapeLeads();
    await fetchLeads();
    setScraping(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">LeadGen Dashboard</h1>
        <button className="bg-gray-700 text-white px-4 py-2 rounded" onClick={() => setSettingsOpen(true)}>
          API Keys
        </button>
      </div>
      <button
        className="mb-6 bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
        onClick={handleScrape}
        disabled={scraping}
      >
        {scraping ? 'Scraping...' : 'Scrape New Leads'}
      </button>
      {loading ? (
        <div>Loading leads...</div>
      ) : (
        <LeadTable leads={leads} onStatusChange={fetchLeads} />
      )}
      <SettingsModal open={settingsOpen} onClose={() => setSettingsOpen(false)} onSave={fetchLeads} />
    </div>
  );
}

export default App;
