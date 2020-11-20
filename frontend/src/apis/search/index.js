import { apiInstance } from 'apis';

export const searchProducts = 
  async (keyword) => await apiInstance.get(`/search?q=${keyword}`)
