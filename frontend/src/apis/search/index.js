import { apiInstance } from 'apis';
import { stringify } from 'querystring';

export const searchProducts = 
  async (keyword) => await apiInstance.get(`/search?${stringify({
    q: keyword,
  })}`)

export const getSuggestions = 
  async (keyword) => await apiInstance.get(`/search/suggestions`)
