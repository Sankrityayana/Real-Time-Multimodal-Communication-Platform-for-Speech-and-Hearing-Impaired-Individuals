import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000
});

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
};

export const authApi = {
  register: (payload) => api.post('/auth/register/', payload),
  login: (payload) => api.post('/auth/login/', payload)
};

export const chatApi = {
  listMessages: (sessionId) => api.get(`/chat/sessions/${sessionId}/messages/`),
  createSession: (payload) => api.post('/chat/sessions/', payload)
};

export const aiApi = {
  transcribeAudio: (formData) => api.post('/ai/transcribe/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  synthesizeSpeech: (payload) => api.post('/ai/tts/', payload, {
    responseType: 'blob'
  }),
  detectSign: (payload) => api.post('/ai/sign/detect/', payload)
};
