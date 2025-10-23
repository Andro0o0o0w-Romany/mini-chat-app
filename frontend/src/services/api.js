import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

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
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/token/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  logout: (refreshToken) => api.post('/auth/logout/', { refresh_token: refreshToken }),
  getCurrentUser: () => api.get('/auth/me/'),
  updateProfile: (data) => api.patch('/auth/me/', data),
  getUsers: () => api.get('/auth/users/'),
};

// Chat API
export const chatAPI = {
  // Conversations
  getConversations: () => api.get('/chat/conversations/'),
  getConversation: (id) => api.get(`/chat/conversations/${id}/`),
  createConversation: (data) => api.post('/chat/conversations/', data),
  getStats: () => api.get('/chat/conversations/stats/'),
  markConversationRead: (id) => api.post(`/chat/conversations/${id}/mark_read/`),
  
  // Messages
  getMessages: (conversationId) => api.get(`/chat/messages/?conversation=${conversationId}`),
  sendMessage: (data) => api.post('/chat/messages/', data),
};

// WebSocket API
export const getWebSocketURL = (conversationId, token) => {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsHost = process.env.REACT_APP_WS_URL || 'localhost:8000';
  return `${wsProtocol}//${wsHost}/ws/chat/${conversationId}/?token=${token}`;
};

export default api;

