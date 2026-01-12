import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL:  API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const contentService = {
  /**
   * Genera contenido basado en los parámetros
   */
  generateContent: async (data) => {
    const response = await api.post('/content/generate', data);
    return response.data;
  },

  /**
   * Obtiene la configuración disponible
   */
  getConfig: async () => {
    const response = await api. get('/content/config');
    return response. data;
  },

  /**
   * Health check
   */
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;