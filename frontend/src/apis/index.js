import axios from 'axios';

export const BASE_URL = 'http://localhost:5000';

export const apiInstance = axios.create({
  baseURL: BASE_URL,
})