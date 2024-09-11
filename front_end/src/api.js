import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/', // Substitua pela URL correta da API
  });
  

export default api;