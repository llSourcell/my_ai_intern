import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5002/api';

export const getLeads = () => axios.get(`${API_BASE}/leads`).then(r => r.data);
export const addLead = (lead) => axios.post(`${API_BASE}/leads`, lead);
export const updateLead = (id, data) => axios.patch(`${API_BASE}/leads/${id}`, data);
export const scrapeLeads = (limit = 30) => axios.post(`${API_BASE}/scrape`, { limit });
export const callLead = (lead_id, script) => axios.post(`${API_BASE}/call`, { lead_id, script });
export const getCallLogs = (lead_id) => axios.get(`${API_BASE}/call_logs/${lead_id}`).then(r => r.data);
export const addCallLog = (log) => axios.post(`${API_BASE}/call_logs`, log);
