import React, { useState } from 'react';
import { callLead, updateLead, getCallLogs } from '../api';

const STATUS_COLORS = {
  'Not Called': 'bg-gray-200 text-gray-700',
  'Calling': 'bg-blue-200 text-blue-700',
  'Completed': 'bg-green-200 text-green-700',
  'Interested': 'bg-yellow-200 text-yellow-700',
  'Declined': 'bg-red-200 text-red-700',
};

export default function LeadTable({ leads, onStatusChange }) {
  const [loadingId, setLoadingId] = useState(null);
  const [transcript, setTranscript] = useState(null);

  const handleCall = async (lead) => {
    setLoadingId(lead.id);
    await callLead(lead.id);
    onStatusChange();
    setLoadingId(null);
  };

  const handleClose = async (lead) => {
    setLoadingId(lead.id);
    await updateLead(lead.id, { status: 'Completed' });
    onStatusChange();
    setLoadingId(null);
  };

  const handleTranscript = async (lead) => {
    const logs = await getCallLogs(lead.id);
    if (logs.length > 0) setTranscript(logs[0].transcript);
    else setTranscript('No transcript found.');
  };

  return (
    <div>
      <table className="min-w-full bg-white rounded shadow overflow-hidden">
        <thead>
          <tr>
            <th className="px-4 py-2">Business Name</th>
            <th className="px-4 py-2">Phone</th>
            <th className="px-4 py-2">Status</th>
            <th className="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id} className="border-t">
              <td className="px-4 py-2">{lead.name}</td>
              <td className="px-4 py-2">{lead.phone}</td>
              <td className="px-4 py-2">
                <span className={`px-2 py-1 rounded text-xs font-semibold ${STATUS_COLORS[lead.status] || ''}`}>{lead.status}</span>
              </td>
              <td className="px-4 py-2 space-x-2">
                <button
                  className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 disabled:opacity-50"
                  disabled={loadingId === lead.id || lead.status === 'Calling'}
                  onClick={() => handleCall(lead)}
                >
                  Call Now
                </button>
                <button
                  className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600 disabled:opacity-50"
                  disabled={loadingId === lead.id || lead.status === 'Completed'}
                  onClick={() => handleClose(lead)}
                >
                  Mark as Closed
                </button>
                <button
                  className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                  onClick={() => handleTranscript(lead)}
                >
                  View Transcript
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {transcript && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white p-6 rounded shadow max-w-lg w-full relative">
            <button className="absolute top-2 right-2 text-xl" onClick={() => setTranscript(null)}>&times;</button>
            <h2 className="text-lg font-bold mb-2">Call Transcript</h2>
            <pre className="whitespace-pre-wrap text-sm">{transcript}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
