import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5002/api';

export default function SettingsModal({ open, onClose, onSave }) {
  const [config, setConfig] = useState({
    TWILIO_ACCOUNT_SID: '',
    TWILIO_AUTH_TOKEN: '',
    TWILIO_PHONE_NUMBER: '',
    ELEVENLABS_API_KEY: '',
    ELEVENLABS_AGENT_ID: '',
    LLM_API_KEY: '',
  });
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (open) {
      axios.get(`${API_BASE}/config`).then(r => setConfig(r.data));
    }
  }, [open]);

  const handleChange = (e) => {
    setConfig({ ...config, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    setLoading(true);
    await axios.post(`${API_BASE}/config`, config);
    setLoading(false);
    setSaved(true);
    if (onSave) onSave();
    setTimeout(() => setSaved(false), 1500);
  };

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white p-6 rounded shadow max-w-lg w-full relative">
        <button className="absolute top-2 right-2 text-xl" onClick={onClose}>&times;</button>
        <h2 className="text-lg font-bold mb-4">API Key Settings</h2>
        <div className="space-y-2">
          <input name="TWILIO_ACCOUNT_SID" value={config.TWILIO_ACCOUNT_SID} onChange={handleChange} placeholder="Twilio Account SID" className="w-full border p-2 rounded" />
          <input name="TWILIO_AUTH_TOKEN" value={config.TWILIO_AUTH_TOKEN} onChange={handleChange} placeholder="Twilio Auth Token" className="w-full border p-2 rounded" />
          <input name="TWILIO_PHONE_NUMBER" value={config.TWILIO_PHONE_NUMBER} onChange={handleChange} placeholder="Twilio Phone Number" className="w-full border p-2 rounded" />
          <input name="ELEVENLABS_API_KEY" value={config.ELEVENLABS_API_KEY} onChange={handleChange} placeholder="ElevenLabs API Key" className="w-full border p-2 rounded" />
          <input name="ELEVENLABS_AGENT_ID" value={config.ELEVENLABS_AGENT_ID} onChange={handleChange} placeholder="ElevenLabs Agent ID" className="w-full border p-2 rounded" />
          <input name="LLM_API_KEY" value={config.LLM_API_KEY} onChange={handleChange} placeholder="LLM API Key" className="w-full border p-2 rounded" />
        </div>
        <button onClick={handleSave} className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700 disabled:opacity-50" disabled={loading}>
          {loading ? 'Saving...' : 'Save'}
        </button>
        {saved && <div className="text-green-600 mt-2">Saved!</div>}
      </div>
    </div>
  );
}
