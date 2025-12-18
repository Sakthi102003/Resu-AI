import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login/json', data),
  getMe: () => api.get('/auth/me'),
  updateMe: (data) => api.put('/auth/me', data),
};

// Resume APIs
export const resumeAPI = {
  create: (data) => api.post('/resume/', data),
  getAll: () => api.get('/resume/'),
  getById: (id) => api.get(`/resume/${id}`),
  update: (id, data) => api.put(`/resume/${id}`, data),
  delete: (id) => api.delete(`/resume/${id}`),
  exportPDF: (id, template = 'auto_cv') => api.post('/resume/export/pdf', null, {
    params: { resume_id: id, template },
    responseType: 'blob'
  }),
  exportDOCX: (id, template = 'auto_cv') => api.post('/resume/export/docx', null, {
    params: { resume_id: id, template },
    responseType: 'blob'
  }),
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
};

// Template APIs
export const templateAPI = {
  getAll: () => api.get('/templates/'),
  getById: (id) => api.get(`/templates/${id}`),
  preview: (id, resumeData, themeColor = '#3B82F6') => 
    api.post(`/templates/${id}/preview?theme_color=${encodeURIComponent(themeColor)}`, 
      resumeData,
      {
        responseType: 'blob'
      }
    ),
};

// Chat APIs
export const chatAPI = {
  respond: (data) => api.post('/chat/respond', data),
  enhance: (text, style = 'professional') => 
    api.post('/chat/enhance', null, { params: { text, style } }),
  getSuggestions: (resumeId) => 
    api.post('/chat/suggestions', null, { params: { resume_id: resumeId } }),
};

// AI Enhancement APIs
export const aiAPI = {
  enhance: (data) => api.post('/ai/enhance', data),
  atsScore: (resumeId) => api.post('/ai/ats-score', { resume_id: resumeId }),
  jobRecommend: (resumeId, preferences = {}) => 
    api.post('/ai/job-recommend', { resume_id: resumeId, preferences }),
  grammarCheck: (text) => 
    api.post('/ai/grammar-check', null, { params: { text } }),
  keywords: (jobTitle, industry = 'Technology') => 
    api.post('/ai/keywords', null, { params: { job_title: jobTitle, industry } }),
};

// Job APIs
export const jobAPI = {
  recommend: (resumeId, preferences = {}) => 
    api.post('/jobs/recommend', { resume_id: resumeId, preferences }),
  trending: (industry = 'Technology') => 
    api.get('/jobs/trending', { params: { industry } }),
};

export default api;
